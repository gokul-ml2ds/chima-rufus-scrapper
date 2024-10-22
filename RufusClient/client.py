# RufusClient/client.py
import os
import json
from .crawler import Crawler
from .parser import Parser
from .synthesizer import Synthesizer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class RufusClient:
    def __init__(self, user_prompt, max_depth=1):
        self.user_prompt = user_prompt
        self.max_depth = max_depth
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found. Please set it in the .env file.")

    def scrape(self, url):
        crawler = Crawler(base_url=url, user_prompt=self.user_prompt, max_depth=self.max_depth)
        crawled_urls = crawler.crawl()
        
        aggregated_data = {"extracted_content": []}  # Initialize with a list to hold multiple contents
        for crawled_url in crawled_urls:
            content = crawler.fetch(crawled_url)
            if content:
                parser = Parser(content, self.user_prompt, self.openai_api_key)
                parsed_data = parser.parse()
                # Merge parsed_data into aggregated_data
                extracted_content = parsed_data.get("extracted_content", "")
                if extracted_content:
                    aggregated_data["extracted_content"].append(extracted_content)
        
        synthesizer = Synthesizer(aggregated_data, self.user_prompt, self.openai_api_key)
        structured_documents = synthesizer.synthesize()
        
        return structured_documents