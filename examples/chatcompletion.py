import os

from crias import llms

api_key = os.environ.get("OPENAI_API_KEY")
assert api_key, "Please set OPENAI_API_KEY environment variable"


def simple_generation():
    messages = llms.create_messages(user="Write a hello world program in python.")

    llm = llms.get("gpt-3.5-turbo", api_key)

    completion = llm.create(messages=messages, max_tokens=100)
    print(completion.choices[0].message.content)


if __name__ == "__main__":
    simple_generation()
