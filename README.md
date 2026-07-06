# 🎨 Dream67Pixel Bot

A powerful Telegram bot for creating pixel art from text, built with Python and deployed on Railway.

## ✨ Features

- 🎨 Generate pixel art from any text
- 📊 Track your creations
- 👥 User statistics
- 🚀 Fast and responsive
- 💾 Saves your pixel art history
- 🤝 Community features

## 🤖 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help menu |
| `/pixel [text]` | Generate pixel art |
| `/mypixel` | View your creations |
| `/stats` | Bot statistics |
| `/about` | About the bot |
| `/feedback [message]` | Send feedback |

## 🚀 Quick Deploy

### 1. Get Bot Token
- Open Telegram
- Message @BotFather
- Send `/newbot`
- Follow instructions
- Copy the token

### 2. Deploy on Railway
1. Fork this repository
2. Create account on [Railway](https://railway.app/)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose this repository
6. Add environment variable: `BOT_TOKEN`
7. Deploy!

### 3. Local Development
```bash
git clone https://github.com/yourusername/Dream67PixelBot.git
cd Dream67PixelBot
pip install -r requirements.txt
echo "BOT_TOKEN=your_token_here" > .env
python main.py
