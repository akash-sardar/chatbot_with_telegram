from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
from openai import OpenAI

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini"
openai_client = OpenAI(api_key = OPENAI_API_KEY)

#configure logging
logging.basicConfig(level = logging.INFO)

# Initialize bot
bot = Bot(token = TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)

class Reference:
    def __init__(self)-> None:
        self.response = ""

reference = Reference()

def clear_past():
    reference.response = ""


@dispatcher.message_handler(commands = ['start'])
async def welcome(message: types.Message):
    '''
    This handler recieves messages with '/start' command
    Args: message(types.Message): _description_
    '''
    await message.reply("Hi ! \n I am an Intelligent ChatBot powered by Telegram app created by Akash!\nYou can start chatting anytime or alternatively type \'/help\' for help menu\n\nHow can I help you ?")


@dispatcher.message_handler(commands = ['help'])
async def helper(message: types.Message):
    '''
    This handler displayes help menu
    '''
    help_command = """
                Hi there, Please follow these commands to start:
                /start - to start the conversation
                /clear - to clear past conversation and context
                /help - to access this help menu
                """
    await message.reply(help_command)


@dispatcher.message_handler(commands = ['clear'])
async def clear(message: types.Message):
    '''
    This handler clears the context
    '''
    clear_past()
    await message.reply("Context Clear successful")


@dispatcher.message_handler()
async def main_bot(message: types.Message):
    '''
    This handler generates chat o/p using LLM
    '''
    print(f">>> USER: \n\t{message.text}")
    response = openai_client.chat.completions.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #user query
        ]
    )
    #print(response.choices[0].message.content)
    reference.response = response.choices[0].message.content
    print(f">>> Akash's chatbot: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates = True)