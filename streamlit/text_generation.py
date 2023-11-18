from openai import OpenAI
from prompt_store import get_prompt_1


def generate_recipe(age, gender, mood):
    print('insde recipe generation func')
    # Your OpenAI API key
    client = OpenAI(api_key='')

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


def generate_recipe_dyn(prompt_text):
    print('insde dyn recipe generation func')
    # Your OpenAI API key
    client = OpenAI(api_key='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')

    response = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"{prompt_text}"}
  ]
)

    return response.choices[0].message.content
