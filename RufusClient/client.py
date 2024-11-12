# RufusClient/client.py
import os
import json
from .crawler import Crawler
from .parser import Parser
from .synthesizer import Synthesizer
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from .env file
load_dotenv()

class RufusClient:
    def __init__(self, user_prompt, max_depth=2):
        self.user_prompt = user_prompt
        self.max_depth = max_depth
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found. Please set it in the .env file.")


    def scrape(self, url):
        crawler = Crawler(base_url=url, user_prompt=self.user_prompt, max_depth=self.max_depth)
        crawled_urls = crawler.crawl()

        aggregated_data = {"extracted_content": []}  # Initialize with a list to hold multiple contents
        
        # Use ThreadPoolExecutor to parse the fetched content in parallel
        with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(crawler.fetch, crawled_url): crawled_url for crawled_url in crawled_urls}
            
            for future in as_completed(future_to_url):
                crawled_url = future_to_url[future]
                try:
                    content = future.result()
                    if content:
                        parser = Parser(content, self.user_prompt, self.openai_api_key)
                        parsed_data = parser.parse()
                        # Merge parsed_data into aggregated_data
                        extracted_content = parsed_data.get("extracted_content", "")
                        if extracted_content:
                            aggregated_data["extracted_content"].append(extracted_content)
                except Exception as exc:
                    print(f"Error processing {crawled_url}: {exc}")
        
        synthesizer = Synthesizer(aggregated_data, self.user_prompt, self.openai_api_key)
        structured_documents = synthesizer.synthesize()
        
        return structured_documents