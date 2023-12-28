from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext

def calcular_aposta_dois_resultados(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    try:
        odd1 = float(context.user_data['odd1'])
        odd2 = float(context.user_data['odd2'])
        valor_apostado = float(context.user_data['valor_apostado'])
    except ValueError:
        context.bot.send_message(chat_id, "Por favor, forneça valores válidos.")
        return

    if odd1 <= 1 or odd2 <= 1 or valor_apostado <= 0:
        context.bot.send_message(chat_id, "Entrada inválida. As odds devem ser maiores que 1 e o valor apostado deve ser um número positivo.")
        return

    total_odds = 1 / odd1 + 1 / odd2
    investimento_justo = valor_apostado / total_odds
    investimento_time1 = investimento_justo / odd1
    investimento_time2 = investimento_justo / odd2
    lucro_time1 = investimento_time1 * (odd1 - 1)
    lucro_time2 = investimento_time2 * (odd2 - 1)
    total_time1 = investimento_time1 + lucro_time1
    total_time2 = investimento_time2 + lucro_time2
    lucro_total = total_time2 - valor_apostado
    porcentagem_retorno = (lucro_total / valor_apostado) * 100

    resultado = (
        "\nResultados:\nInvestimento e Retorno:\n"
        f"ODD 1: R$ {investimento_time1:.2f} - Retorna: R$ {total_time1:.2f}\n"
        f"ODD 2: R$ {investimento_time2:.2f} - Retorna: R$ {total_time2:.2f}\n"
        f"Lucro Total: R$ {lucro_total:.2f}\n"
        f"Porcentagem de Retorno: {porcentagem_retorno:.2f}%"
    )

    context.bot.send_message(chat_id, resultado)

def receber_odd(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    try:
        odd = float(update.message.text)
    except ValueError:
        context.bot.send_message(chat_id, "Por favor, forneça um valor de odd válido.")
        return

    if 'odd1' not in context.user_data:
        context.user_data['odd1'] = odd
        context.bot.send_message(chat_id, "Ótimo! Agora, forneça a ODD CONTRÁRIA que deseja comparar (ODD 2)")

    elif 'odd2' not in context.user_data:
        context.user_data['odd2'] = odd
        context.bot.send_message(chat_id, "Perfeito! Agora, forneça o valor a ser apostado:")

    elif 'valor_apostado' not in context.user_data:
        context.user_data['valor_apostado'] = odd
        calcular_aposta_dois_resultados(update, context)

def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id,
        "Bem-vindo à Calculadora de Apostas!\n"
        "Forneça a ODD que deseja comparar (ODD 1)"
    )

def main() -> None:
    # Configurar o bot do Telegram
    updater = Updater(token="6937216736:AAHDuE4jWyVo1xHvHiKp36rYGU-74uPUYb0", use_context=True)

    # Configurar os manipuladores de mensagem
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, receber_odd))
    dp.add_handler(CommandHandler("start", start))

    # Iniciar o bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()