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
    def test_read_rss(self):
        pajiba = ReadRSS(url="http://feeds.feedburner.com/pajiba")
        pajiba.save_entries()
        seriouseats = ReadRSS(url="http://feeds.feedburner.com/seriouseats")
        seriouseats.save_entries()
        eatersf = ReadRSS(url="http://feeds.feedburner.com/eatersf")
        eatersf.save_entries()

    def test_read_page(self):
        pajiba_page = ReadPage(url="http://www.pajiba.com/trailers/let-benedict-cumberbatchs-narration-in-the-new-hobbit-trailer-desolate-you.php")
        pajiba_page.save_page()
        se_page = ReadPage(url="http://sweets.seriouseats.com/2013/10/ways-to-use-apple-cider.html")
        se_page.save_page()



