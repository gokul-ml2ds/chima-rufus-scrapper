# RufusClient/crawler.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm 
import logging
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Import WebDriver Manager
import os
from tqdm import tqdm  # Add this import

class Crawler:
    def __init__(self, base_url, user_prompt, max_depth=3):
        self.base_url = base_url
        self.user_prompt = user_prompt
        self.max_depth = max_depth
        self.visited = set()
        self.to_visit = [(base_url, 0)]
        self.logger = self.setup_logger()
        
        # Initialize Selenium only if needed
        self.use_selenium = False  # Toggle to use Selenium when needed
        self.driver = None
        if self.use_selenium:
            self.initialize_selenium()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def initialize_selenium(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            self.logger.info("Selenium WebDriver initialized successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize Selenium WebDriver: {e}")
            self.driver = None

    def is_valid(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_links(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(self.base_url, href)
            if self.is_valid(full_url) and self.same_domain(full_url):
                links.add(full_url)
        return links

    def same_domain(self, url):
        base_domain = urlparse(self.base_url).netloc
        target_domain = urlparse(url).netloc
        return base_domain == target_domain

    def fetch(self, url):
        if self.use_selenium and self.driver:
            try:
                self.driver.get(url)
                time.sleep(3)
                content = self.driver.page_source
                return content
            except Exception as e:
                self.logger.error(f"Error fetching {url} with Selenium: {e}")
                return None
        else:
            try:
                headers = {'User-Agent': 'RufusBot/1.0'}
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.HTTPError as http_err:
                self.logger.error(f"HTTP error occurred while fetching {url}: {http_err}")
            except requests.ConnectionError as conn_err:
                self.logger.error(f"Connection error occurred while fetching {url}: {conn_err}")
            except requests.Timeout as timeout_err:
                self.logger.error(f"Timeout error occurred while fetching {url}: {timeout_err}")
            except requests.RequestException as req_err:
                self.logger.error(f"General error occurred while fetching {url}: {req_err}")
            return None

    def crawl(self):
        with tqdm(total=len(self.to_visit), desc="Crawling URLs", unit="url") as pbar:
            while self.to_visit:
                current_url, depth = self.to_visit.pop(0)
                if current_url in self.visited or depth > self.max_depth:
                    pbar.update(1)  # Update progress bar for skipped URLs
                    continue
                self.logger.info(f"Crawling: {current_url} at depth {depth}")
                content = self.fetch(current_url)
                if content:
                    self.visited.add(current_url)
                    links = self.get_links(content)
                    for link in links:
                        if link not in self.visited:
                            self.to_visit.append((link, depth + 1))
                pbar.update(1)  # Update progress bar after processing a URL

        # Close the Selenium driver if used
        if self.driver:
            self.driver.quit()
        
        return self.visited