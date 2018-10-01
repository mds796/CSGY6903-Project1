import asyncio
from copy import deepcopy

from src.key import CandidateKey
from src.scorer import Scorer

ONE_MINUTE = 60
TWO_MINUTES = 2 * ONE_MINUTE


class GenericAttacker:
    def __init__(self, frequencies, candidates, dictionary):
        self.frequencies = frequencies
        self.candidates = candidates
        self.dictionary = dictionary

        self._smallest_word_size = None  # memoized

    def attack(self, cipher_text):
        """Attacks the given cipher text, to determine the encrypted plain text"""

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.composite_attack(cipher_text)).decrypt()

    async def composite_attack(self, cipher_text):
        tasks = {self.candidates_attack(cipher_text), self.dictionary_attack(cipher_text)}
        keys = []

        for attack in asyncio.as_completed(tasks):
            plain_text = await attack
            if plain_text is not None:
                keys.append(plain_text)

        return Scorer(self.dictionary, self.frequencies).best_key(keys)

    async def candidates_attack(self, cipher_text):
        """Attacks the cipher_tet using the candidate texts."""
        tasks = self.candidate_attack_tasks(cipher_text)

        for attack in asyncio.as_completed(tasks, timeout=ONE_MINUTE):
            plain_text = await attack
            if plain_text is not None:
                return plain_text

        return ""

    def candidate_attack_tasks(self, cipher_text):
        """The sub-tasks for a candidate-text based cipher-text attack."""
        tasks = set()

        for candidate in self.candidates:
            coroutine = self.candidate_attack(candidate, cipher_text)
            tasks.add(asyncio.ensure_future(coroutine))

        return tasks

    async def candidate_attack(self, candidate, cipher_text):
        """Attacks the given cipher text using the given candidate. Returns None if no valid key was found."""
        candidate_key = CandidateKey(cipher_text, {}, {}, self.frequencies)

        for word in candidate.words:
            success = candidate_key.add_assignment(word, self.smallest_word_size)
            if not success:
                return None

        if candidate_key.is_valid_key():
            return candidate_key
        else:
            return None

    async def dictionary_attack(self, cipher_text):
        """Schedules the sub-tasks to perform a dictionary attack on the given cipher-text."""
        tasks = set()

        for word in self.dictionary:
            candidate_key = CandidateKey(cipher_text, {}, {}, self.frequencies)
            coroutine = self.dictionary_attack_tasks(cipher_text, word, deepcopy(candidate_key))
            tasks.add(asyncio.ensure_future(coroutine))

        for attack in asyncio.as_completed(tasks, timeout=ONE_MINUTE):
                plain_text = await attack
                if plain_text is not None:
                    return plain_text

        return ""

    async def dictionary_attack_tasks(self, cipher_text, word, candidate_key):
        """The sub-tasks for a dictionary based cipher-text attack."""
        tasks = set()

        success = candidate_key.add_assignment(word, self.smallest_word_size)
        if not success:
            return None
        elif candidate_key.is_valid_key():
            return candidate_key

        for word in self.dictionary:
            coroutine = self.dictionary_attack_tasks(cipher_text, word, deepcopy(candidate_key))
            tasks.add(asyncio.ensure_future(coroutine))

        return tasks

    async def dictionary_word_attack(self, cipher_text):
        tasks = set()

        for candidate in self.candidates:
            coroutine = self.candidate_attack(candidate, cipher_text)
            tasks.add(asyncio.ensure_future(coroutine))

        return tasks

    @property
    def smallest_word_size(self):
        if self._smallest_word_size is not None:
            return self._smallest_word_size

        if len(self.dictionary.words) == 0:
            self._smallest_word_size = 0
        else:
            self._smallest_word_size = min([len(word) for word in self.dictionary])

        return self._smallest_word_size