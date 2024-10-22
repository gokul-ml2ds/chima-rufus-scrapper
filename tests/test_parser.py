# tests/test_parser.py
import unittest
from RufusClient.parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.sample_html = """
        <html>
            <body>
                <section class="faq">
                    <h2>What is Rufus?</h2>
                    <p>Rufus is an intelligent web data extraction tool.</p>
                </section>
                <section class="pricing">
                    <table>
                        <tr>
                            <td>Basic</td>
                            <td>$10/month</td>
                        </tr>
                        <tr>
                            <td>Pro</td>
                            <td>$30/month</td>
                        </tr>
                    </table>
                </section>
            </body>
        </html>
        """
        self.parser = Parser(content=self.sample_html, user_prompt="Find FAQs and pricing.")

    def test_extract_faqs(self):
        faqs = self.parser.extract_faqs()
        self.assertEqual(len(faqs), 1)
        self.assertEqual(faqs[0]['question'], "What is Rufus?")
        self.assertEqual(faqs[0]['answer'], "Rufus is an intelligent web data extraction tool.")
    
    def test_extract_pricing(self):
        pricing = self.parser.extract_pricing()
        self.assertEqual(len(pricing), 2)
        self.assertEqual(pricing[0]['feature'], "Basic")
        self.assertEqual(pricing[0]['price'], "$10/month")
        self.assertEqual(pricing[1]['feature'], "Pro")
        self.assertEqual(pricing[1]['price'], "$30/month")
    
    def test_parse(self):
        data = self.parser.parse()
        self.assertIn('faqs', data)
        self.assertIn('pricing', data)
        self.assertEqual(len(data['faqs']), 1)
        self.assertEqual(len(data['pricing']), 2)

if __name__ == "__main__":
    unittest.main()