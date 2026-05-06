import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

products = {
    "1": {"name": "Free Fire Panel", "price": 100},
    "2": {"name": "Premium Account", "price": 200}
}

user_orders = {}

menu_keyboard = ReplyKeyboardMarkup(
    [["🛍 Shop", "📦 My Orders"], ["💰 Payment Info"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Flassy Shop Bot!", reply_markup=menu_keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == "🛍 Shop":
        msg = "Available Products:\n"
        for pid, p in products.items():
            msg += f"{pid}. {p['name']} - {p['price']}৳\n"
        msg += "\nSend product number to buy."
        await update.message.reply_text(msg)

    elif text in products:
        product = products[text]
        user_orders[user_id] = product
        await update.message.reply_text(
            f"You selected {product['name']}\nPrice: {product['price']}৳\n\nSend payment screenshot after payment."
        )

    elif text == "📦 My Orders":
        order = user_orders.get(user_id)
        if order:
            await update.message.reply_text(f"Your last order: {order['name']}")
        else:
            await update.message.reply_text("No orders found.")

    elif text == "💰 Payment Info":
        await update.message.reply_text(
            "Send money to:\n\nbKash: 01XXXXXXXXX\nNagad: 01XXXXXXXXX\nRocket: 01XXXXXXXXX\n\nThen send screenshot."
        )

    else:
        await update.message.reply_text("Invalid option.")

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New payment from {user.id}"
    )
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id
    )
    await update.message.reply_text("Payment received! Wait for approval.")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    await update.message.reply_text("Admin panel active.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
