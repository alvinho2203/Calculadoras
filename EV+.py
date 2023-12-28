import telegram
from telegram.ext import MessageHandler, CommandHandler, Filters, Updater


temp_data = {}

def calcular_juice(odd1, odd2):
    return (1/odd1) + (1/odd2) - 1

def calcular_fair_odd(odd1, juice):
    return 2 * odd1 / (2 - (juice * odd1))

def calcular_stake(fair_odd, odd3):
    stake = (((1 / fair_odd) * odd3 - 1) / (odd3 - 1)) * 0.2
    return round(stake / 0.0025) * 0.25

def receber_odd(update, context):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    try:
        odd = float(update.message.text)
    except ValueError:
        context.bot.send_message(chat_id, "Por favor, forneça um valor de odd válido.")
        return

    if user_id not in temp_data:
        temp_data[user_id] = []

    temp_data[user_id].append(odd)

    if len(temp_data[user_id]) == 3:
        odd1, odd2, odd3 = temp_data[user_id]
        juice = calcular_juice(odd1, odd2)
        fair_odd = calcular_fair_odd(odd1, juice)
        stake = calcular_stake(fair_odd, odd3)

        resultado = f"Juice: {juice:.4f}\nFair Odd: {fair_odd:.2f}\nStake: {stake:.2f}%"
        context.bot.send_message(chat_id, resultado)

        del temp_data[user_id]

def start(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id,
        "Bem-vindo à Calculadora de Apostas!\n"
        "Por favor, forneça as odds em três mensagens diferentes."
    )

def main():

    updater = Updater(token="6454137964:AAFXuwMBy3xRLPLOV9odPXo19eWgREXK71M", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, receber_odd))
    dp.add_handler(CommandHandler("start", start))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()