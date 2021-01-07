
import unittest
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from utils.preprocessing import remove_html_tags, remove_special_characters, replace_contractions, remove_accented_chars

class Preprocessing(unittest.TestCase):

    def test_remove_html_tags(self):
        """
        Test that it can remove html tags.
        """
        html_content = '<html> \
            <h1> Article Heading </h1> \
            <p> First sentence of some important article. And another one. And then the last one </p></html >'
        content_without_hmtl_tags = '  Article Heading   First sentence of some important article. And another one. And then the last one '

        self.assertEqual(remove_html_tags(
            html_content), content_without_hmtl_tags, "Sould be " + content_without_hmtl_tags)

    def test_remove_accented_characters(self):
        text_with_accented_characters = "Sómě Áccěntěd těxt, ménagement"
        text_without_accented_characters = "Some Accented text, menagement"
        self.assertEqual(remove_accented_chars(text_with_accented_characters),
                         text_without_accented_characters, "Sould be " + text_without_accented_characters)

    def test_replace_contractions(self):
        """
        Test that it fix contractions
        """
        text_with_contractions = "I'll be there within 5 min. Shouldn't you be there too?"
        decontracted_text = "I will be there within 5 min. should not you be there too?"
        self.assertEqual(replace_contractions(text_with_contractions),
                         decontracted_text, "Sould be " + decontracted_text)

    def test_remove_special_characters(self):
        text_with_special_characters = "007 Not sure@ if this % was #fun! 558923 What do# you think** of it.? $500USD!"
        text_with_only_alpha_characters = " Not sure if this  was fun What do you think of it"
        self.assertEqual(remove_special_characters(
            text_with_only_alpha_characters), text_with_only_alpha_characters, "Should be " + text_with_only_alpha_characters)

if __name__ == '__main__':
    unittest.main()
