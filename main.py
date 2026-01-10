import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from processor import get_answer

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8401369464:AAEbjoBYd8G3SokWlbaOim3EdRX03zxBlQE"

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    """Handle incoming text messages from users."""
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text
    print(f"User bertanya: {user_text}")
    
    # Animasi 'typing...'
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # RAG
    try:
        bot_response = await get_answer(user_text)
        
        await update.message.reply_text(bot_response)
    except Exception as e:
        logging.error(f"Error saat get_answer: {e}")
        await update.message.reply_text("Duh belum sampe, coba tanya yang lain ya!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming photo messages from users."""
    # Untuk tahap awal, beri feedback kalau foto sudah diterima
    await update.message.reply_text("Fotonya cakep! Saya sedang menganalisis jenis kucing ini... (Fitur Vision menyusul)")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handler untuk teks
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    # Handler untuk foto (Identifikasi Jenis)
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("🚀 Bot CatLovers sedang running...")
    app.run_polling()