const { Telegraf } = require('telegraf');
const ytdl = require('ytdl-core');
const TikTokScraper = require('tiktok-scraper');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Token Telegram Bot
const BOT_TOKEN = "7561651517:AAGzQ_xaWcoEHZXy27G5OyHP9UFJn0e01Ms";
const bot = new Telegraf(BOT_TOKEN);

// Folder untuk menyimpan file sementara
const DOWNLOAD_FOLDER = './downloads/';
if (!fs.existsSync(DOWNLOAD_FOLDER)) {
    fs.mkdirSync(DOWNLOAD_FOLDER);
}

// Fungsi untuk memulai bot
bot.start((ctx) => {
    ctx.reply("Halo! Kirim tautan YouTube, TikTok, atau Instagram untuk mengunduh audionya saja.");
});

// Fungsi untuk mengunduh audio
bot.on('text', async (ctx) => {
    const url = ctx.message.text.trim();

    // Validasi URL
    if (!url.includes('youtube.com') && !url.includes('youtu.be') && !url.includes('tiktok.com') && !url.includes('instagram.com')) {
        ctx.reply("Kirim link dari YouTube, TikTok, atau Instagram yang valid.");
        return;
    }

    ctx.reply("Sedang memproses audio, harap tunggu...");

    try {
        let filePath;

        if (url.includes('youtube.com') || url.includes('youtu.be')) {
            // Unduh audio dari YouTube
            const info = await ytdl.getInfo(url);
            const title = info.videoDetails.title.replace(/[\/\\?%*:|"<>]/g, '-');
            filePath = path.join(DOWNLOAD_FOLDER, `${title}.mp3`);
            const audioStream = ytdl(url, { filter: 'audioonly', quality: 'highestaudio' });

            // Simpan audio ke file
            const writeStream = fs.createWriteStream(filePath);
            audioStream.pipe(writeStream);
            await new Promise((resolve) => writeStream.on('finish', resolve));

        } else if (url.includes('tiktok.com')) {
            // Unduh audio dari TikTok
            const videoMeta = await TikTokScraper.getVideoMeta(url);
            const audioUrl = videoMeta.collector[0].musicUrl;
            const title = videoMeta.collector[0].text.replace(/[\/\\?%*:|"<>]/g, '-');
            filePath = path.join(DOWNLOAD_FOLDER, `${title}.mp3`);

            // Unduh dan simpan audio
            const response = await axios({
                url: audioUrl,
                method: 'GET',
                responseType: 'stream',
            });
            const writeStream = fs.createWriteStream(filePath);
            response.data.pipe(writeStream);
            await new Promise((resolve) => writeStream.on('finish', resolve));

        } else if (url.includes('instagram.com')) {
            ctx.reply("Instagram saat ini tidak mendukung pengunduhan audio saja.");
            return;
        }

        // Kirim file audio ke pengguna
        if (fs.existsSync(filePath)) {
            await ctx.replyWithAudio({ source: filePath });
            fs.unlinkSync(filePath); // Hapus file setelah dikirim
        } else {
            throw new Error("File audio tidak ditemukan setelah diunduh.");
        }
    } catch (err) {
        console.error(err);
        ctx.reply(`Terjadi kesalahan: ${err.message}`);
    }
});

// Jalankan bot
bot.launch().then(() => {
    console.log("Bot berjalan...");
});

// Graceful shutdown
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
