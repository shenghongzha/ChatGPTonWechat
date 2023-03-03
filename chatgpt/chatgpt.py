import openai


class ChatGPT:
    def __init__(self, api_key):
        openai.api_key = api_key

    def ask(self, prompt, engine="davinci", max_tokens=50, temperature=0.7):
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].text.strip()

