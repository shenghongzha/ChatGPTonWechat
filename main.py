import werobot
import openai

robot = werobot.WeRoBot(token='your_token')
openai.api_key="your_api_key"
def generate_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    message = response.choices[0].text
    return message.strip()

@robot.handler]
def hello (messages):
    print(messages.content)
    return generate_response(messages.content)

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()