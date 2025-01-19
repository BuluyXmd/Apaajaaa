const { Telegraf } = require('telegraf');
const ytdl = require('ytdl-core');
const TikTokScraper = require('tiktok-scraper');
const fs = require('fs-extra');
const path = require('path');

// Token Telegram Bot
const BOT_TOKEN = "7846302722:AAF_UHsrR0KDKIX16l4XI5rStgDiXWyVA8c";
const bot = new Telegraf(BOT_TOKEN);

// Folder untuk menyimpan file sementara
const DOWNLOAD_FOLDER = './downloads/';
fs.ensureDirSync(DOWNLOAD_FOLDER);

// Fungsi untuk memulai bot
bot.start((ctx) => {
    ctx.reply("Selamat datang! Kirim URL video dari TikTok, Instagram, atau YouTube untuk diunduh.");
});

// Fungsi untuk menangani unduhan video
bot.on('text', async (ctx) => {
    const url = ctx.message.text.trim();

    // Validasi URL
    if (!url.includes('youtube.com') && !url.includes('youtu.be') && !url.includes('tiktok.com') && !url.includes('instagram.com')) {
        ctx.reply("Silakan kirim URL TikTok, Instagram, atau YouTube yang valid.");
        return;
    }

    ctx.reply("Sedang memproses, harap tunggu...");

    try {
        let filePath;

        if (url.includes('youtube.com') || url.includes('youtu.be')) {
            // Unduh video dari YouTube
            const info = await ytdl.getInfo(url);
            const title = info.videoDetails.title.replace(/[\/\\?%*:|"<>]/g, '-');
            filePath = path.join(DOWNLOAD_FOLDER, `${title}.mp4`);
            const videoStream = ytdl(url, { quality: 'highestvideo' });

            // Simpan video ke file
            const writeStream = fs.createWriteStream(filePath);
            videoStream.pipe(writeStream);
            await new Promise((resolve) => writeStream.on('finish', resolve));

        } else if (url.includes('tiktok.com')) {
            // Unduh video dari TikTok
            const videoMeta = await TikTokScraper.getVideoMeta(url);
            const videoUrl = videoMeta.collector[0].videoUrl;
            const title = videoMeta.collector[0].text.replace(/[\/\\?%*:|"<>]/g, '-');
            filePath = path.join(DOWNLOAD_FOLDER, `${title}.mp4`);

            // Unduh dan simpan video
            const response = await fetch(videoUrl);
            const writeStream = fs.createWriteStream(filePath);
            response.body.pipe(writeStream);
            await new Promise((resolve) => writeStream.on('finish', resolve));

        } else if (url.includes('instagram.com')) {
            ctx.reply("Instagram saat ini tidak mendukung pengunduhan video.");
            return;
        }

        // Kirim video ke pengguna
        if (fs.existsSync(filePath)) {
            await ctx.replyWithVideo({ source: filePath });
            fs.unlinkSync(filePath); // Hapus file setelah dikirim
        } else {
            throw new Error("File video tidak ditemukan setelah diunduh.");
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
