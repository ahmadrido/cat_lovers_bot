import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from processor import get_answer

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8401369464:AAEbjoBYd8G3SokWlbaOim3EdRX03zxBlQE"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    welcome_message = """
Halo! 👋 Selamat datang di **CatLovers Bot** 🐱

Saya adalah chatbot yang siap membantu Anda dengan berbagai informasi tentang kucing, seperti:
🍽️ Makanan & Nutrisi
💉 Kesehatan & Vaksinasi
🎾 Perilaku & Pelatihan
🧼 Panduan Perawatan
🐈 Jenis-jenis Kucing
🏥 Penyakit & Gejala

Tanya apa saja tentang kucing, dan saya akan bantu jawab dengan ramah! 🐾

Contoh pertanyaan:
• "Makanan apa yang berbahaya untuk kucing?"
• "Kapan kucing harus divaksin?"
• "Kenapa kucingku suka mencakar sofa?"
• "Bagaimana cara merawat bulu kucing?"

Silakan tanya sekarang! 😊
"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

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
    # Handler untuk /start command
    # app.add_handler(MessageHandler(filters.COMMAND & filters.Regex(r'^/start$'), start_command))
    app.add_handler(CommandHandler("start", start_command))
    # Handler untuk teks
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    # Handler untuk foto (Identifikasi Jenis)
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("🚀 Bot CatLovers sedang running...")
    app.run_polling()