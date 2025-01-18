import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Token Telegram Bot
TOKEN = "7561651517:AAGzQ_xaWcoEHZXy27G5OyHP9UFJn0e01Ms"

# Folder untuk menyimpan file sementara
DOWNLOAD_FOLDER = "./downloads/"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Fungsi untuk memulai bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Kirim tautan YouTube, TikTok, atau Instagram untuk mengunduh audionya saja."
    )

# Fungsi untuk mengunduh audio saja
async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    # Validasi URL
    if not any(domain in url for domain in ["youtube.com", "youtu.be", "tiktok.com", "instagram.com"]):
        await update.message.reply_text("Kirim link dari YouTube, TikTok, atau Instagram yang valid.")
        return

    await update.message.reply_text("Sedang memproses audio, harap tunggu...")
    try:
        ydl_opts = {
            "format": "bestaudio/best",  # Unduh audio terbaik
            "postprocessors": [{
                "key": "FFmpegExtractAudio",  # Ekstrak audio dari video
                "preferredcodec": "mp3",     # Format audio MP3
                "preferredquality": "192",   # Kualitas audio 192 kbps
            }],
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),  # Penamaan file
        }

        # Unduh audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                raise Exception("Tidak dapat mengambil informasi dari URL.")
            
            file_name = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.mp4', '.mp3')

        # Kirim audio ke pengguna
        if os.path.exists(file_name):
            await update.message.reply_text("Audio selesai diunduh, sedang mengirim...")
            await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(file_name, "rb"))

            # Hapus file setelah dikirim
            os.remove(file_name)
        else:
            raise Exception("File audio tidak ditemukan setelah diunduh.")

    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan: {e}")

# Fungsi utama untuk menjalankan bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Daftarkan handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))

    # Jalankan bot
    application.run_polling()

if __name__ == "__main__":
    main()
