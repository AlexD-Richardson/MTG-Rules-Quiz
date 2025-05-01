import unittest
from unittest.mock import patch
import json
from mtg_rules_quiz_with_chatgpt import generate_question

class TestGenerateQuestion(unittest.TestCase):
    @patch("mtg_rules_quiz_with_chatgpt.client.chat.completions.create")
    def test_generate_question_success(self, mock_openai):
        """Test generate_question with a valid response."""
        # Mock a valid OpenAI API response
        mock_openai.return_value = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps({
                            "question": "What is the starting life total in a Commander game?",
                            "options": ["20", "30", "40", "50"],
                            "answer": "40"
                        })
                    }
                }
            ]
        }

        result = generate_question()
        self.assertIsNotNone(result)
        self.assertIn("question", result)
        self.assertIn("options", result)
        self.assertIn("answer", result)
        self.assertEqual(len(result["options"]), 4)

    @patch("mtg_rules_quiz_with_chatgpt.client.chat.completions.create")
    def test_generate_question_invalid_response_format(self, mock_openai):
        """Test generate_question with an invalid response format."""
        # Mock an invalid OpenAI API response
        mock_openai.return_value = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps({
                            "question": "What is the starting life total in a Commander game?",
                            "options": ["20", "30", "40"]
                            # Missing 'answer' key
                        })
                    }
                }
            ]
        }

        result = generate_question()
        self.assertIsNone(result)

    @patch("mtg_rules_quiz_with_chatgpt.client.chat.completions.create")
    def test_generate_question_json_decode_error(self, mock_openai):
        """Test generate_question with a JSON decoding error."""
        # Mock a response with invalid JSON
        mock_openai.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "This is not valid JSON"  # Invalid JSON string
                    }
                }
            ]
        }

        result = generate_question()
        self.assertIsNone(result)

    @patch("mtg_rules_quiz_with_chatgpt.client.chat.completions.create")
    def test_generate_question_api_error(self, mock_openai):
        """Test generate_question when the OpenAI API raises an exception."""
        # Mock an exception from the OpenAI API
        mock_openai.side_effect = Exception("API error")

        result = generate_question()
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()