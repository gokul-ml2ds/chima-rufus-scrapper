# RufusClient/parser.py
from bs4 import BeautifulSoup
import openai
import logging

class Parser:
    def __init__(self, content, user_prompt, api_key):
        self.content = content
        self.user_prompt = user_prompt
        self.api_key = api_key
        self.soup = BeautifulSoup(content, 'html.parser')
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        openai.api_key = self.api_key

    def extract_relevant_sections(self):
        """
        Uses OpenAI GPT to identify relevant sections of the content based on the user prompt.
        """
        try:
            # Prepare the messages for the chat model
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Given the following HTML content, identify and extract the sections that are relevant to the user's prompt.\n\nUser Prompt: \"{self.user_prompt}\"\n\nHTML Content:\n{self.content}"}
            ]

            # Call OpenAI's API
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  
                messages=messages,
                max_tokens=500, #
                temperature=0.3,
                n=1
            )

            extracted_text = response.choices[0].message['content'].strip()  # Adjusted for the new response format
            return extracted_text

        except openai.error.OpenAIError as e:
            self.logger.error(f"OpenAI API error: {e}")
            return ""
        except Exception as e:
            self.logger.error(f"Unexpected error during extraction: {e}")
            return ""

    def parse(self):
        """
        Parses the HTML content and extracts relevant data based on the user prompt.
        Returns structured data in JSON format.
        """
        extracted_text = self.extract_relevant_sections()

        if not extracted_text:
            self.logger.warning("No relevant sections extracted.")
            return {}

        # Optionally, further process the extracted text to structure it
        # For simplicity, we'll return it as a single field
        structured_data = {
            "extracted_content": extracted_text
        }

        return structured_data
