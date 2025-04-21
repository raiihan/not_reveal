# NotRevealBot

A Telegram bot to upload files to private channels and share them via secure deep links.

## Features
- Upload any file type to private channels
- Get a deep link to download the file (no channel exposed)
- Fancy loading/providing messages
- Admin system (add/remove admins, batch upload, stats, etc.)
- Webhook ready for free Render.com deployment

## How to Deploy (Render)
1. Fork or upload this repo to your GitHub account
2. Create a new Web Service on [Render.com](https://render.com)
3. Connect your repo, set environment variables as in `.env.example`
4. Use `web: python3 bot.py` as start command
5. Deploy and enjoy!

Made for Sunny with ❤️