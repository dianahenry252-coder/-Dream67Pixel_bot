import os
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler, 
    ContextTypes, 
    MessageHandler, 
    filters,
    ConversationHandler
)
from dotenv import load_dotenv
import requests
from io import BytesIO
from PIL import Image
import aiohttp

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment
TOKEN = os.getenv('BOT_TOKEN')

# Constants
WAITING_FOR_TEXT = 1

# Bot statistics
bot_stats = {
    'start_count': 0,
    'pixel_count': 0,
    'start_time': datetime.now(),
    'users': set()
}

# Store user data temporarily
user_data_store: Dict[int, Dict[str, Any]] = {}

# ============== COMMAND HANDLERS ==============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    user_id = user.id
    
    # Update stats
    bot_stats['start_count'] += 1
    bot_stats['users'].add(user_id)
    
    welcome_text = f"""
🌟 *Welcome to Dream67Pixel Bot!* 🌟

Hello {user.first_name}! I'm your pixel art assistant, ready to help you create amazing pixel art.

✨ *What I Can Do:*
• 🎨 Generate pixel art from text
• 🖼️ Convert images to pixel art (coming soon)
• 📊 Track your pixel creations
• 🎯 Help with your pixel projects

📌 *Quick Start:*
Use /pixel [your text] to create pixel art
Or click the buttons below to get started!

🤖 *Bot Status:* 🟢 Online
    """
    
    keyboard = [
        [InlineKeyboardButton("🎨 Create Pixel Art", callback_data='create_pixel')],
        [InlineKeyboardButton("📊 My Stats", callback_data='user_stats')],
        [InlineKeyboardButton("❓ Help", callback_data='help')],
        [InlineKeyboardButton("ℹ️ About", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message."""
    help_text = """
🤖 *Dream67Pixel Bot Commands*

*Available Commands:*
/start - Start the bot
/help - Show this help message
/pixel <text> - Generate pixel art
/mypixel - View your pixel creations
/stats - Show bot statistics
/about - About this bot
/feedback <message> - Send feedback

*How to Use Pixel Art:*
1. Type: `/pixel Hello World`
2. Or use the inline buttons
3. Share your creations with friends!

*Tips:*
• Keep text under 20 characters for best results
• Use emojis for fun pixel art
• Share your creations in the community!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def pixel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate pixel art from text."""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "❌ Please provide text for pixel art!\n\n"
            "Example: `/pixel Hello`\n"
            "Example: `/pixel 🎨 Art`",
            parse_mode='Markdown'
        )
        return
    
    # Get the text
    text = ' '.join(context.args)
    
    # Validate length
    if len(text) > 30:
        await update.message.reply_text(
            "⚠️ Please keep text under 30 characters for better pixel art!"
        )
        return
    
    # Generate pixel art
    pixel_art = generate_pixel_art(text)
    
    # Update stats
    bot_stats['pixel_count'] += 1
    
    # Store user's creation
    if user_id not in user_data_store:
        user_data_store[user_id] = {'creations': []}
    user_data_store[user_id]['creations'].append({
        'text': text,
        'timestamp': datetime.now().isoformat()
    })
    
    # Create response with the pixel art
    response = f"""
🎨 *Pixel Art Created!*

Text: `{text}`
