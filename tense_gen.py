import os
from mistralai import Mistral
#aSvs02V12nE7yoEt0Scw8diGdYcriRz
api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

def generate_sentence():
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": "Napiš 1 větu v češtině. Nepiš nic jiného než větu. Větu nepřekládej. Nepiš o počasí.",
            },
        ],# i want it creative, so high temperature
        temperature=0.6,
    )
    return chat_response.choices[0].message.content

if __name__ == "__main__":
    print(generate_sentence())