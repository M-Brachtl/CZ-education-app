import os

from mistralai import Mistral
#aSvs02V12nE7yoEt0Scw8diGdYcriRz
api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-large-2407"

client = Mistral(api_key=api_key)

def generate_sentence(difficulty):
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": f"Napiš 1 větu v češtině. Nepiš nic jiného než větu. Větu nepřekládej. Nepiš o počasí. Udělej větu {difficulty}.",
            },
        ],
        temperature = 0.7,
    )
    return chat_response.choices[0].message.content

def double_check(the_sentence):
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": f"Následující větu opiš a oprav spelling či jiné chyby, napiš pouze čistě větu bez čehokoli jiného:\n{the_sentence}",
            },
        ],
        temperature = 0.1,
    )
    return chat_response.choices[0].message.content


if __name__ == "__main__":
    difficulty = "snadná"
    sentence = generate_sentence(difficulty)
    print(f"Generated sentence: {sentence}")
    corrected_sentence = double_check(sentence)
    print(f"Corrected sentence: {corrected_sentence}")