import re
import unittest

from ppgen.core import generate_complex_password, generate_passphrase, load_word_list


class WordLengthTests(unittest.TestCase):
    def test_word_list_uses_actual_word_length(self):
        word_dict = load_word_list()

        self.assertEqual(word_dict["挨个儿"]["char_count"], 3)
        self.assertTrue(
            all(len(word) == data["char_count"] for word, data in word_dict.items())
        )

    def test_complex_password_respects_character_count(self):
        word_dict = load_word_list()

        for _ in range(100):
            _, hints = generate_complex_password(
                word_dict, word_count=2, character_count=2, capitalize=True
            )
            words = re.findall(r"([\u4e00-\u9fff]+)\(", hints)

            self.assertEqual(len(words), 2)
            self.assertTrue(all(len(word) == 2 for word in words), hints)

    def test_complex_password_respects_single_word_count(self):
        word_dict = load_word_list()

        for _ in range(100):
            _, hints = generate_complex_password(
                word_dict, word_count=1, character_count=4, capitalize=True
            )
            words = re.findall(r"([\u4e00-\u9fff]+)\(", hints)

            self.assertEqual(len(words), 1)
            self.assertEqual(len(words[0]), 4, hints)

    def test_passphrase_respects_single_word_count(self):
        word_dict = load_word_list()

        for _ in range(100):
            _, hints = generate_passphrase(
                word_dict, word_count=1, character_count=4, capitalize=True
            )
            words = re.findall(r"([\u4e00-\u9fff]+)\(", hints)

            self.assertEqual(len(words), 1)
            self.assertEqual(len(words[0]), 4, hints)


if __name__ == "__main__":
    unittest.main()
