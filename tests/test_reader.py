"""
Unit tests for the RSS reader
Author: Jose Vicente Nunez (kodegeek.com@protonmail.com)
"""

import unittest
from pathlib import Path

from enablesysadminrssreader import parse_rss, get_rss

TEST_DIR = Path(__file__).parent


class RssReaderTestCase(unittest.TestCase):

    def setUp(self) -> None:
        rss_file = TEST_DIR.joinpath('rss.xml')
        with open(rss_file, 'r') as rss:
            self.rss = rss.read()

    def test_parse_rss(self):
        parsed_rss = parse_rss(self.rss)
        self.assertIsNotNone(parsed_rss)
        for article in parsed_rss:
            for key in ['title', 'link', 'description']:
                self.assertIn(key, article)
                self.assertIsNotNone(article[key])

    def test_get_rss(self):
        raw_xml = get_rss()
        self.assertIsNotNone(raw_xml)


if __name__ == '__main__':
    unittest.main()
