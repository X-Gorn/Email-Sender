import smtplib, ssl, os, pyromod.listen
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Environment Variables
SENDER = os.environ['EMAIL'] # Sender Email/Your Email
PASSWORD = os.environ['PASSWORD'] # Your Email's Password
API_HASH = os.environ['API_HASH'] # Your API HASH
APP_ID = int(os.environ['APP_ID']) # Your APP ID
BOT_TOKEN = os.environ['BOT_TOKEN'] # Your BOT TOKEN
OWNER_ID = int(os.environ['OWNER_ID']) # Your Telegram ID

# Buttons
START_BUTTONS=[
    [
        InlineKeyboardButton("Source", url="https://github.com/X-Gorn/Email-Sender"),
        InlineKeyboardButton("Project Channel", url="https://t.me/xTeamBots"),
    ],
    [InlineKeyboardButton("Author", url="https://t.me/xgorn")],
]

# Running bot
xbot = Client('Email-Sender', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start message
@xbot.on_message(filters.command('start') & filters.chat(OWNER_ID) & filters.private)
async def start(bot, update):
    await update.reply_text(f'I\'m Email-Sender\nYou can sent an Email using this bot!\n\nExample: `/send receiver-email@gmail.com`', True, reply_markup=InlineKeyboardMarkup(START_BUTTONS))


@xbot.on_message(filters.command('send') & filters.chat(OWNER_ID) & filters.private)
async def email_sender(bot, update):
    if update.text == '/send':
        await update.reply('Example: `/send receiver-email@gmail.com`')
        return
    receiver = update.text.split(' ', 1)[1]
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    subject = await bot.ask(update.chat.id, 'Send Your Subject', filters='text', timeout=300)
    message = await bot.ask(update.chat.id, 'Send Your Message', filters='text', timeout=300)
    text = f'Subject: {subject.text}\n\n{message.text}'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, receiver, text)
    await update.reply('Successfully Sended to Receiver/Target.')


xbot.run()