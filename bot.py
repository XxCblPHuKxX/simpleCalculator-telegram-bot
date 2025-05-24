from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я боткалькулятор. Отправь мне выражение например /calc 2 + 3")

def calculate_expression(expression: str) -> tuple:
    try:
        expression = re.sub(r'\s*([+\-/])\s', r' \1 ', expression.strip())
        if not re.match(r'^[\d\s+\-*/.()]+$', expression):
            return None, "Ошибка: используй только числа и операторы (+, -, *, /)"

        result = eval(expression, {"_builtins_": {}}, {})
        return result, None
    except ZeroDivisionError:
        return None, "Ошибка: деление на ноль. Попробуй другое выражение."
    except Exception as e:
        return None, f"Ошибка: неверное выражение ({str(e)}). Пример: /calc 2 + 3"

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        expression = ' '.join(context.args)
        if not expression:
            await update.message.reply_text("Отправь выражение после /calc, например, /calc 2 + 3")
            return

        result, error = calculate_expression(expression)
        if error:
            await update.message.reply_text(error)
        else:
            await update.message.reply_text(f"Результат: {result}")
            
    except Exception as e:
        print(f"Error processing calc: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуй снова, например, /calc 2 + 3")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, отправь выражение, например, /calc 2 + 3")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    if update.message:
        await update.message.reply_text("Произошла ошибка. Попробуй снова!")

app = ApplicationBuilder().token("here is your bot token from @BotFather").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("calc", calc))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_error_handler(error)

app.run_polling() 
