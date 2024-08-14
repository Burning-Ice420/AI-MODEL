from openai import OpenAI
 

client = OpenAI(
  api_key="__YOTU",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named helium skilled in general tasks like Alexa and Google Cloud, you can also answer questions like chat gpt"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)