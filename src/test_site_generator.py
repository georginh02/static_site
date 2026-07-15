import unittest
from site_generator import extract_title

class Testsitegenerator(unittest.TestCase):

    def test_no_heading(self):
        markdown = """Tolkien Club"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h1_heading(self):
        markdown = """
# Tolkien Club
"""
        self.assertEqual(extract_title(markdown), "Tolkien Club")

    def test_h2_heading(self):
        markdown = """
## Tolkien Club
"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h3_heading(self):
        markdown = """
### Tolkien Club
"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h4_heading(self):
        markdown = """
#### Tolkien Club
"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h5_heading(self):
        markdown = """
##### Tolkien Club
"""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h6_heading(self):
        markdown = """
###### Tolkien Club
"""
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
