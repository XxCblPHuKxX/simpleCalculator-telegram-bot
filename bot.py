from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re

TOKEN = "here is a bot token from the @BotFather in telegram"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я калькулятор! Отправь выражение, например: 5.2 + 3.7\n"
        "Поддерживаю: +, -, *, /"
    )

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    pattern = r'^(\d+\.?\d*)\s*([+\-/])\s(\d+\.?\d*)$'
    match = re.match(pattern, message.strip())

    if not match:
        await update.message.reply_text(
            "Неверный формат! Пример: 5.2 + 3.7"
        )
        return

    try:
        num1 = float(match.group(1))
        operator = match.group(2)
        num2 = float(match.group(3))

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                await update.message.reply_text("Ошибка: деление на ноль!")
                return
            result = num1 / num2
        else:
            await update.message.reply_text("Ошибка: неподдерживаемый оператор! Используйте +, -, *, /")
            return

        result = round(result, 2)
        await update.message.reply_text(f"Результат: {result}")

    except ValueError:
        await update.message.reply_text("Ошибка: введите корректные числа!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))
    app.run_polling()

if __name__ == "__main__":
    main()
