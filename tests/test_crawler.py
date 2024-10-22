# tests/test_crawler.py
import unittest
from RufusClient.crawler import Crawler

class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler(base_url="https://www.example.com", user_prompt="Test Crawl", max_depth=1)
    
    def test_is_valid(self):
        self.assertTrue(self.crawler.is_valid("https://www.example.com"))
        self.assertFalse(self.crawler.is_valid("ftp://www.example.com"))
        self.assertFalse(self.crawler.is_valid("www.example.com"))
    
    def test_same_domain(self):
        self.assertTrue(self.crawler.same_domain("https://www.example.com/page"))
        self.assertFalse(self.crawler.same_domain("https://www.otherdomain.com"))
    
    def test_fetch(self):
        content = self.crawler.fetch("https://www.example.com")
        self.assertIsNotNone(content)
        self.assertIn("<title>Example Domain</title>", content)
    
    def test_crawl(self):
        crawled_urls = self.crawler.crawl()
        self.assertIn("https://www.example.com", crawled_urls)
        # Example.com has minimal links
        self.assertEqual(len(crawled_urls), 1)

if __name__ == "__main__":
    unittest.main()