import openai
import json
import logging
import time  # Import time for sleep during retry

class Synthesizer:
    def __init__(self, extracted_data, user_prompt, api_key, model="gpt-3.5-turbo"):
        self.extracted_data = extracted_data
        self.user_prompt = user_prompt
        self.api_key = api_key
        self.model = model
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        openai.api_key = self.api_key
    
    def synthesize(self):
        if not self.extracted_data:
            self.logger.warning("No data extracted to synthesize.")
            return {}

        # Prepare messages for the chat model
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Organize the following data based on the prompt '{self.user_prompt}': {json.dumps(self.extracted_data)}"}
        ]

        # Initialize retry parameters
        retries = 3
        for attempt in range(retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=500,
                    temperature=0.3,
                    n=1
                )
                
                # Log the request and response
                self.logger.info(f"API Request: {messages}")
                self.logger.info(f"API Response: {response}")

                synthesized_text = response.choices[0].message['content'].strip()  # Adjusted for the new response format
                
                # Attempt to parse JSON
                try:
                    # Optional: Clean the synthesized text (e.g., remove newlines or excessive whitespace)
                    synthesized_text = synthesized_text.replace('\n', ' ').strip()

                    structured_data = json.loads(synthesized_text)
                    return structured_data
                except json.JSONDecodeError as e:
                    self.log_json_error(synthesized_text, e)
                    return {"raw_output": synthesized_text}  # Return the raw output for debugging


            except openai.error.RateLimitError as e:
                self.logger.warning(f"Rate limit reached. Attempt {attempt + 1} of {retries}.")
                time.sleep(2 ** attempt)  # Exponential backoff
            except openai.error.OpenAIError as e:
                self.logger.error(f"OpenAI API error: {e}")
                return {}

        self.logger.error("Max retries reached. Unable to synthesize.")
        return {}
    
    def log_json_error(self, synthesized_text, error):
        self.logger.error("Failed to parse synthesized text into JSON.")
        self.logger.error(f"JSONDecodeError: {error}")  # Log the specific error
        self.logger.error(f"Synthesized Text: {synthesized_text}")  # Log the raw text for inspection
        self.logger.error("Please check the format of the synthesized text for any issues.")
