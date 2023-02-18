import logging
import telegram.ext
import asyncio
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler
from telegram.ext.filters import Text
from queue import Queue

# Definir as constantes do bot
TOKEN = "TELEGRAM_TOKEN"

# Definir os estados da conversa
FIRST, SECOND, THIRD, FOURTH = range(4)

# Definir as mensagens do bot
start_message = "Bem-vindo ao bot de atendimento do provedor de internet! Como posso ajudar?"
menu_message = "Escolha uma opção:\n1. Registrar novo atendimento\n2. Ver atendimentos registrados\n3. Sair"
register_message = "Digite o nome do cliente:"
confirm_message = "Atendimento registrado! Deseja registrar outro atendimento? (sim/não)"
cancel_message = "Atendimento cancelado."

# Definir as funções para cada comando do bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)
    return FIRST

def menu(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=menu_message)
    return SECOND

def register(update, context):
    context.user_data['name'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=confirm_message)
    return THIRD

def confirm(update, context):
    if update.message.text.lower() == 'sim':
        context.bot.send_message(chat_id=update.effective_chat.id, text=register_message)
        return THIRD
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Até mais!")
        return ConversationHandler.END

def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=cancel_message)
    return ConversationHandler.END

# Definir a função main para iniciar o bot
# Definir a função main para iniciar o bot
def main():
    # Configurar o logger
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Criar o objeto Queue para armazenar as atualizações
    update_queue = Queue()

    # Criar o objeto Updater e passar o token do bot e o objeto Queue
    updater = Updater(TOKEN, update_queue, use_context=True)

    # Criar o objeto Dispatcher e registrar os handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [MessageHandler(Filters.text & ~Filters.command, menu)],
            SECOND: [MessageHandler(Filters.regex('^1$'), register),
                     MessageHandler(Filters.regex('^2$'), show),
                     MessageHandler(Filters.regex('^3$'), cancel)],
            THIRD: [MessageHandler(Filters.text & ~Filters.command, confirm)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # Iniciar o bot
    updater.start_polling()

    # Manter o bot em execução
    updater.idle()

