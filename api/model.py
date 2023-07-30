import os
import openai

def query_model(prompt, provider="openai"):

    if (provider=="openai"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("OPENAI_API_KEY environment variable not found.")
        
        openai.api_key = api_key
        completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt},
        ]
        )

        print(completion.choices[0].message)

    else:
        raise ValueError("Provider not supported")