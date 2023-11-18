import openai
from prompt_store import get_prompt_1

def generate_recipe(age, gender, mood):
    # Your OpenAI API key
    openai.api_key = ''

    # Constructing the prompt
    prompt_text = get_prompt_1(age, gender, mood)

    response = openai.ChatCompletion.create(
      engine="gpt-4-1106-preview", # Or the latest available model
      message=prompt_text,
    )

    return response.choices[0].message['content']


# Example usage
age = "write your age"
gender = "your gender"
mood = "what do you feel"

recipe = generate_recipe(age, gender, mood)
print(recipe)