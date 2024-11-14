from openai import OpenAI


# Chave de API foi configurada via variavel de ambiente, utilize o comando recomendado pela tutorial da OPENAI
# export OPENAI_API_KEY="your_api_key_here"

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens=200,
    temperature=0.1,
    messages=[
        {"role": "system", "content": "Você é um experiente programdor. Retorne apenas códigos limpos e de qualidade."},
        {
            "role": "user",
            "content": "Escreve um código de Hello World em Python."
        }
    ]
)

print(completion.choices[0].message.content)