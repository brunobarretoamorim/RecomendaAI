from telegram.ext import Updater
import requests
import json
from pprint import pprint

updater = Updater(token='1613492568:AAG-_TyHADfLf0Lqw7VpRFfOGMpNHk3yQKU', use_context=True)
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="E ai estudante, beleza ? Abaixo está todas as nossas opções: \n" 
                                                                + "1. /Enviar - Para enviar sua prova\n"
                                                                + "2. /consultar - Para consultar sua nota anterior\n"
                                                                + "3. /Duvidas - Para duvidas frequentes"
                                                                )

def soma(update, context):
    print(context.chat_data)
    print(context.user_data)

    context.bot.send_message(chat_id=update.effective_chat.id, text="A soma dos valores é: ")

def modelo(update, context):
    pload = {"materia" : "mt", "data" : [1, 1, 1, 5, 5, 2, 2, 2, 4, 1, 1, 3, 3, 1, 3, 5, 4, 5, 5, 2, 4, 5, 4, 4, 2, 5, 4, 4 , 3, 5]}
    r = requests.post('http://localhost:5000/modelo', json= pload)
    response = r.json()
    chat_id = update.effective_chat.id
    materia = pload.get("materia")
    PATH = f'resultados/resultado_{chat_id}.txt'
    user = update.effective_user.first_name

    f = open(PATH, "w")
    f.write(str(response))
    f.close()


    resp_file = open(PATH, 'rb')
    print(update.effective_chat.id)

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{user} Baixe agora o resultado do seu simulado")

    context.bot.send_document(chat_id=update.effective_chat.id, document=resp_file, filename=f'Resuldado Simulado Materia {materia}')


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="E ai estudante, beleza ? Abaixo está todas as nossas opções: \n" 
                                                                + "1. /Enviar - Para enviar sua prova\n"
                                                                + "2. /consultar - Para consultar sua nota anterior\n"
                                                                + "3. /Duvidas - Para duvidas frequentes"
                                                                )

import re
from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.regex(re.compile(r'help', re.IGNORECASE)), echo)
dispatcher.add_handler(echo_handler)


from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
soma_handler = CommandHandler('soma', soma)
modelo_handler = CommandHandler('Resultado', modelo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(soma_handler)
dispatcher.add_handler(modelo_handler)


updater.start_polling()