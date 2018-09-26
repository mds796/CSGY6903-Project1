from src.dictionary import Dictionary


class CodeBreaker:
    def break_with_candidates(self, candidates):
        dictionary = Dictionary([])

        for candidate in candidates:
            dictionary = dictionary.merge(candidate.dictionary())

        self.break_with_dictionary(dictionary)

    def break_with_dictionary(self, dictionary):
        pass
