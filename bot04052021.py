import telebot
from telebot import types
from tratainputcode import trataInput
from geraReport import Visualization
import os
import requests
import json

bot = telebot.TeleBot('1631430287:AAFbmEC-7654WlacSDzCHReaip_nXt1yR1I') # bot bruno
#bot = telebot.TeleBot('1613492568:AAG-_TyHADfLf0Lqw7VpRFfOGMpNHk3yQKU') # bot jonathan

dic = {'materia':'','cor_prova':'','respostas':'','retorno':''}
# handle commands, /start
@bot.message_handler(commands=['start'])
def handle_command(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton(text="1")
    button2 = types.KeyboardButton(text="2")
    button3 = types.KeyboardButton(text="3")
    button4 = types.KeyboardButton(text="4")

    keyboard.add(button1, button2, button3,button4)
    bot.send_message(message.chat.id, f'''Olá bem vindo ao RecomendaAIBot. 
    Selecione a funcionalidade que deseja usar{os.linesep}
    1 - Recomendações Prova de Humanidades{os.linesep}
    2 - Recomendações Prova de Ciências da Natureza{os.linesep}
    3 - Recomendações Prova de Linguagens{os.linesep}
    4 - Recomendações Prova de Matemática''', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text.strip().upper() in['1','2','3','4'])
def trataInputsProva(message):
    materias = {'1':'CH','2':'CN','3':'LC','4':'MT'}
    dic['materia'] = materias[message.text.strip().upper()]
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton(text="AZUL")
    button2 = types.KeyboardButton(text="VERDE")
    button3 = types.KeyboardButton(text="AMARELA")

    keyboard.add(button1, button2, button3)
    bot.send_message(message.chat.id, 'Selecione a cor da Prova que fez:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text.strip().upper() in['AZUL','VERDE','AMARELA'])
def trataInputsProva(message):
    dic['cor_prova'] = message.text.strip().upper()
    bot.send_message(message.chat.id, 'Perfeito, agora pode digitar as suas respostas nesse formato : R - ABC...')
    
    print('Respostas',message.text)
    
@bot.message_handler(func=lambda message: message.text.strip().upper().startswith('R -'))
def trataInputsProva(message):

    bot.send_message(message.chat.id, 'Legal estamos processando sua requisição:')
    respostas = message.text.upper().replace('R -','').strip()
    dic['respostas'] = respostas
    print('Respostas',respostas)
    dic['retorno'] = trataInput(dic['cor_prova'],dic['materia'],dic['respostas'])
    #print(dic['retorno'])
    pload = dic.get("retorno")
    pload = json.loads(pload)

    r = requests.post('http://localhost:5000/modelo', json=pload)
    print(r.json())
    response = r.json()
    chat_id = message.chat.id
    materia = dic.get("materia")
    PATH = f'resultados/resultado_{chat_id}_{materia}.txt'
    user = message.from_user.first_name
    Visualization.executar(response)
    #executar(response)
    resp_file = open(os.path.join(os.getcwd(),'resultados','Enem_Report.pdf'),'rb')
    #f = open(PATH, "w")
    #f.write(str(response))
    #f.close()
    #resp_file = open(PATH, 'rb')

    #bot.reply_to(message, 'Legal, algo mais ? Caso tenha acabado, digite sair !')
    bot.send_message(chat_id, text=f"{user} baixe agora o resultado do seu simulado")
    bot.send_document(chat_id, resp_file)

    

# handle all messages, echo response back to users
@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    
    if message.text.strip().lower() == 'menu':
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton(text="1")
        button2 = types.KeyboardButton(text="2")
        button3 = types.KeyboardButton(text="3")
        button4 = types.KeyboardButton(text="4")

        keyboard.add(button1, button2, button3,button4)
        bot.send_message(message.chat.id, f'''Olá bem vindo ao RecomendaAIBot. 
        Selecione a funcionalidade que deseja usar{os.linesep}
        1 - Recomendações Prova de Humanidades{os.linesep}
        2 - Recomendações Prova de Ciências da Natureza{os.linesep}
        3 - Recomendações Prova de Linguagens{os.linesep}
        4 - Recomendações Prova de Matemática''', reply_markup=keyboard)
   
        
    elif message.text.strip().lower() == 'sair':
        bot.reply_to(message,'Tudo bem ! Muito obrigado por utilizar o RecomendaAIBot !!')
    else:
        print(message.text)
        bot.reply_to(message, 'Ops, não entendi. Se quiser saber as opções disponíveis, digite "menu" ou se quiser sair, digite "sair"')
        


bot.polling()