# tests/test_synthesizer.py
import unittest
from RufusClient.synthesizer import Synthesizer
from unittest.mock import patch

class TestSynthesizer(unittest.TestCase):
    def setUp(self):
        self.extracted_data = {
            "faqs": [
                {"question": "What is Rufus?", "answer": "Rufus is an intelligent web data extraction tool."}
            ],
            "pricing": [
                {"feature": "Basic", "price": "$10/month"},
                {"feature": "Pro", "price": "$30/month"}
            ]
        }
        self.user_prompt = "Find FAQs and pricing."
        self.api_key = "test_api_key"

    @patch('openai.Completion.create')
    def test_synthesize_success(self, mock_create):
        mock_create.return_value = type('obj', (object,), {
            'choices': [type('obj', (object,), {'text': '{"faqs": [{"question": "What is Rufus?", "answer": "Rufus is an intelligent web data extraction tool."}], "pricing": [{"feature": "Basic", "price": "$10/month"}, {"feature": "Pro", "price": "$30/month"}]}')})
        })
        synthesizer = Synthesizer(self.extracted_data, self.user_prompt, self.api_key)
        result = synthesizer.synthesize()
        self.assertIn('faqs', result)
        self.assertIn('pricing', result)
        self.assertEqual(len(result['faqs']), 1)
        self.assertEqual(len(result['pricing']), 2)
    
    @patch('openai.Completion.create')
    def test_synthesize_failure(self, mock_create):
        mock_create.side_effect = Exception("OpenAI API Error")
        synthesizer = Synthesizer(self.extracted_data, self.user_prompt, self.api_key)
        result = synthesizer.synthesize()
        self.assertEqual(result, {})

if __name__ == "__main__":
    unittest.main()