import asyncio
from collections import deque
from copy import deepcopy

from src import cipher
from src.key import CandidateKey
from src.scorer import Scorer

ONE_MINUTE = 60
DICTIONARY_TIMEOUT = (2 * ONE_MINUTE) + 55


class DictionaryAttacker:
    def __init__(self, frequencies, dictionary):
        self.frequencies = frequencies
        self.dictionary = dictionary

    def attack(self, cipher_text):
        """Attacks the given cipher text, to determine the encrypted plain text"""

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.attack_with_timeout(cipher_text)).decrypt()

    async def attack_with_timeout(self, cipher_text):
        """Runs a dictionary attack, and falls back to a random key."""
        try:
            dictionary_key = await asyncio.wait_for(self.dictionary_attack(cipher_text), timeout=DICTIONARY_TIMEOUT)
            if dictionary_key is not None:
                return dictionary_key
        except asyncio.TimeoutError:
            pass

        return cipher.generate_homophonic(self.frequencies)

    async def dictionary_attack(self, cipher_text):
        """Schedules the sub-tasks to perform a dictionary attack on the given cipher-text."""
        keys = deque()
        candidate_key = CandidateKey(cipher_text, {}, {}, self.frequencies)
        tasks = self.dictionary_attack_tasks(candidate_key, keys)

        while len(tasks) > 0:
            new_tasks = set()

            for task in asyncio.as_completed(tasks):
                sub_tasks = await task
                new_tasks = new_tasks.union(sub_tasks)

            tasks = new_tasks

        return Scorer(self.dictionary, self.frequencies).best_key([candidate_key] + list(keys))

    def dictionary_attack_tasks(self, key, keys):
        """The sub-tasks for a dictionary based cipher-text attack."""
        tasks = set()

        for word in self.dictionary.shuffle():
            coroutine = self.word_attack(key, keys, word)
            tasks.add(asyncio.ensure_future(coroutine))

        return tasks

    async def word_attack(self, source_key, keys, word):
        """Attacks a cipher-text using a single dictionary word. Returns tasks to continue the attack"""
        key = deepcopy(source_key)

        success = key.add_assignment(word)
        if success and key.is_valid_key():
            keys.append(key)
        elif success:
            return self.dictionary_attack_tasks(key, keys)

        return set()
