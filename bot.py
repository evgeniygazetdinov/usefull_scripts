from key import KEY

from telegram.ext import Updater
from telegram.ext import CommandHandler



def start(bot,update):
    bot.sendMessage(chat_id = update.message.chat_id,text ="Залупи")




updater = Updater(token = KEY)
start_handler = CommandHandler('start',start)
updater.dispatcher.add_handler(start_handler)
updater.start_polling()
