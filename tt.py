import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

# Ganti dengan token bot Telegram Anda
BOT_TOKEN = "7846302722:AAF_UHsrR0KDKIX16l4XI5rStgDiXWyVA8c"

# Folder untuk menyimpan file sementara
DOWNLOAD_FOLDER = "./downloads/"

# Pastikan folder download ada
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Fungsi untuk menangani perintah '/start'
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Selamat datang! Kirim URL video dari TikTok, Instagram, atau YouTube untuk diunduh."
    )

# Fungsi untuk menangani pengunduhan video dari TikTok, Instagram, atau YouTube
async def download_video(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    if not any(domain in url for domain in ['tiktok.com', 'instagram.com', 'youtube.com']):
        await update.message.reply_text("Silakan kirim URL TikTok, Instagram, atau YouTube yang valid.")
        return

    try:
        # Set konfigurasi unduhan untuk video
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',  # Resolusi maksimal 1080p
            'merge_output_format': 'mp4',  # Menggabungkan video dan audio ke format MP4
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),  # Penamaan file
        }

        # Unduh video dari URL
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = os.path.join(DOWNLOAD_FOLDER, f"{info_dict['id']}.mp4")

            # Kirim file video ke pengguna
            await update.message.reply_video(video=open(video_path, 'rb'))

            # Hapus file setelah dikirim
            os.remove(video_path)
    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan: {e}")

# Fungsi utama untuk menjalankan bot
def main():
    # Buat aplikasi bot
    application = Application.builder().token(BOT_TOKEN).build()

    # Daftarkan handler untuk perintah dan pesan
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Jalankan bot
    application.run_polling()

if __name__ == '__main__':
    main()
