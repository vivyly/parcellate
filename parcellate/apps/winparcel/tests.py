import unittest
from .lib import (ReadRSS,
                  ReadPage,
                  #ReadSocial
                 )
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver


class FirefoxBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = FirefoxDriver()

    def tearDown(self):
        self.driver.quit()


class BasicTest(unittest.TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class AddReadTest(unittest.TestCase):
    def read_rss(self):
        pajiba = ReadRSS(url="http://feeds.feedburner.com/pajiba")
        entries = pajiba.parse_entries()
        seriouseats = ReadRSS(url="http://feeds.feedburner.com/seriouseats")
        entries = seriouseats.parse_entries()
        eatersf = ReadRSS(url="http://feeds.feedburner.com/eatersf")
        entries = eatersf.parse_entries()

    def test_read_page(self):
        pajiba_page = ReadPage(url="http://www.pajiba.com/trailers/let-benedict-cumberbatchs-narration-in-the-new-hobbit-trailer-desolate-you.php")
        print pajiba_page.find_content()
        se_page = ReadPage(url="http://sweets.seriouseats.com/2013/10/ways-to-use-apple-cider.html")
        print se_page.find_content()



