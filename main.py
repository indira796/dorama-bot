import editdistance
from random import choice
from test import BOT_CONFIG, quotes
from ai import ask_gpt
import telebot
from mistralai import Mistral

def ask_gpt(content):
    client = Mistral(api_key = 'IblZhTcDMXZ0LqJEXK3iTbVlU2wm4Vdo')
    chat_response = client.chat.complete(
        model= 'mistral-large-latest',
        messages = [
            {
                "role": "user",
                "content": "What is the best French cheese?",
            },
        ]
    )
    return chat_response.choices[0].message.content


def clean(text):
    output_text = ''
    for s in text.lower():
        if s in 'qwertyuiopasdfghjklzxcvbnm йцукенгшщзхъфывапролджэячсмитьбю':
            output_text +=s
    return output_text

def get_intent(text):
    for intent in BOT_CONFIG['intents'].keys():
        for example in BOT_CONFIG['intents'][intent]['example']:
            text1 = clean(example)
            text2 = clean(text)
            if editdistance.evel(text1, text2) / max(len(text1), len(text2)) < 0.4:
                return intent
    return 'i cannot find intent'

def bot(text):
    intent = get_intent(text)
    if intent != '':
        return choice(BOT_CONFIG['intents'][intent]['responces'])
    else:
        return 'i not nderstand your'

client = telebot.TeleBot('8080210246:AAFKwVKGvOYC6v9rZVldwLpKBNwt4ceMrs0')
@client.message_handler(content_types= ['text'])

def lalala(message):
    if message.text[0:4] == '@gpt':
        a = message.text.replace('@gpt', '')
        client.send_message(message.chat.id, ask_gpt(message.text))
    elif message.text == 'get quote':
        client.send_message(message.chat.id, choice(quotes))
    else:
        client.send_message(message.chat.id,bot(message.text))

if __name__ == '__main__':
    client.infinity_polling()