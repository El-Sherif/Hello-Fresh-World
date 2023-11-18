from openai import OpenAI
client = OpenAI()
from prompt_store import get_prompt_1

def generate_recipe(age, gender, mood):
    # Your OpenAI API key
    client = OpenAI(api_key='key')

    # Constructing the prompt
    prompt_text = get_prompt_1(age, gender, mood)

    response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"{prompt_text}"}
  ]
)

    return response.choices[0].message.content



# Example usage
age = "write your age"
gender = "your gender"
mood = "what do you feel"

recipe = generate_recipe(age, gender, mood)
print(recipe)