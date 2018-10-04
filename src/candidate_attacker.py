import asyncio
import random

from src.key import CandidateKey

CANDIDATE_TIMEOUT = 60


class CandidateAttacker:
    def __init__(self, frequencies, candidates):
        self.frequencies = frequencies
        self.candidates = candidates

    def attack(self, cipher_text):
        """Attacks the given cipher text, to determine the encrypted plain text"""

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.attack_with_timeout(cipher_text))

    async def attack_with_timeout(self, cipher_text):
        """Runs a candidate attack, followed by a dictionary attack, and falls back to selecting a random candidate."""
        try:
            candidate_key = await asyncio.wait_for(self.candidates_attack(cipher_text), timeout=CANDIDATE_TIMEOUT)
            if candidate_key is not None:
                return candidate_key.decrypt()
        except asyncio.TimeoutError:
            print("Out of time! Using fallback answer.")

        options = list(self.candidates)
        random.shuffle(options)
        return options.pop().text

    async def candidates_attack(self, cipher_text):
        """Attacks the cipher_tet using the candidate texts."""
        tasks = self.candidate_attack_tasks(cipher_text)

        for attack in asyncio.as_completed(tasks):
            key = await attack
            if key is not None:
                return key

        return None

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

        success = candidate_key.add_assignment(candidate.text)
        if not success:
            return None

        if candidate_key.is_valid_key():
            return candidate_key
        else:
            return None
