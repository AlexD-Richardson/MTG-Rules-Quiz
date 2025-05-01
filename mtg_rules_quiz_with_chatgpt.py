from dotenv import load_dotenv
import openai
import os
import json

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")
openai.api_key = api_key


from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

def generate_question():
    """Generate a Magic: The Gathering rules question using ChatGPT."""
    prompt = (
        "Generate a multiple-choice question about Magic: The Gathering rules. Try to make the question between basic and intermediate level. "
        "The question should be clear and concise and shouldn't be the same as any previous questions that you have generated. "
        "Provide the question, four answer options that are not labeled in any way. Make sure the correct answer is one of the options and the other options are the wrong answers. "
        "Format the response as JSON with keys: 'question', 'options', and 'answer'."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        print(response)  # Debugging: Print the response
        # Access the content of the response
        content = response["choices"][0]["message"]["content"]

        # Safely parse the JSON response
        question_data = json.loads(content)

        # Validate the structure of the response
        if not all(key in question_data for key in ['question', 'options', 'answer']):
            raise ValueError("Invalid response format from OpenAI API.")
        if not isinstance(question_data['options'], list) or len(question_data['options']) != 4:
            raise ValueError("Options must be a list of four items.")

        return question_data
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from OpenAI response.")
    except ValueError as e:
        print(f"Error parsing question data: {e}")
    except Exception as e:
        print(f"Error generating question: {e}")
    return None

def run_quiz():
    print("Welcome to the Magic: The Gathering Rules Quiz!")
    print("Answer the following questions to test your knowledge.\n")
    
    score = 0
    num_questions = 5  # Number of questions to generate

    for i in range(num_questions):
        question_data = generate_question()
        if not question_data:
            print("Failed to generate a question. Skipping...\n")
            continue

        print(f"Question {i + 1}: {question_data['question']}")
        for idx, option in enumerate(question_data['options'], start=1):
            print(f"{idx}. {option}")
        
        # Get user input
        try:
            user_answer = int(input("Your answer (1-4): "))
            if 1 <= user_answer <= 4:
                if question_data['options'][user_answer - 1] == question_data['answer']:
                    print("Correct!\n")
                    score += 1
                else:
                    print(f"Wrong! The correct answer was: {question_data['answer']}\n")
            else:
                print("Invalid input. Please enter a number between 1 and 4.\n")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.\n")
    
    print(f"Quiz Complete! Your score: {score}/{num_questions}")
    if score == num_questions:
        print("Perfect score! You're a Magic: The Gathering rules master!")
    elif score > num_questions // 2:
        print("Great job! You know your Magic rules well.")
    else:
        print("Keep practicing! You'll master the rules in no time.")


if __name__ == "__main__":
    run_quiz()