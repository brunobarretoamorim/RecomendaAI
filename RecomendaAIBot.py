import requests
import time
import json
import os


class TelegramBot:
    def __init__(self):
        token = '1631430287:AAFbmEC-7654WlacSDzCHReaip_nXt1yR1I'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    eh_primeira_mensagem = int(
                        dado["message"]["message_id"]) == 1
                    resposta = self.criar_resposta(
                        mensagem, eh_primeira_mensagem)
                    self.responder(resposta, chat_id)

    # Obter mensagens
    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    # Criar uma resposta
    def criar_resposta(self, mensagem, eh_primeira_mensagem):
        if eh_primeira_mensagem == True or mensagem in ('menu', 'Menu'):
            return f'''Olá bem vindo ao RecomendaAIBot. Digite a funcionalidade que deseja usar{os.linesep}1 - Recomendações Prova de Humanidades{os.linesep}2 - Recomendações Prova de Ciências da Natureza{os.linesep}3 - Recomendações Prova de Linguagens{os.linesep}4 - Recomendações Prova de Matemática'''
        if mensagem == '1':
            return f'''Deseja inserir a prova de Humanidades{os.linesep}Confirmar pedido?(s/n)
            '''
        elif mensagem == '2':
            return f'''Deseja inserir a prova de Ciências da Naturea{os.linesep}Confirmar pedido?(s/n)
            '''
        elif mensagem == '3':
            return f'''Deseja inserir a prova de Linguagens{os.linesep}Confirmar pedido?(s/n)'''
        
        elif mensagem == '4':
            return f'''Deseja inserir a prova de Matemática{os.linesep}Confirmar pedido?(s/n)'''

        elif mensagem.lower() in ('s', 'sim'):
            return ''' Pedido Confirmado! '''
        elif mensagem.lower() in ('n', 'não'):
            return ''' Desistiu da recomendação ? Gostaria de outra ajuda ? Se sim, digite "menu", caso queira sair, digite "sair". '''
        elif mensagem.lower() in ('sair', 'Sair'):
            return ''' Tudo bem. Muito obrigado por utilizar o Bot RecomendaAI !!!'''
        else:
            return 'Gostaria de acessar o menu? Digite "menu"'

    # Responder
    def responder(self, resposta, chat_id):
        link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)


bot = TelegramBot()
bot.Iniciar()