# Developed by: LastPerson07 × cantarella
# Telegram: @cantarellabots | @THEUPDATEDGUYS
import os
import asyncio
import random
import time
import shutil
import pyrogram
import requests
import hashlib 
import signal
import sys
from pyrogram import Client, filters, enums
from pyrogram.errors import (
    FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant, UserAlreadyParticipant,
    InviteHashExpired, UsernameNotOccupied, AuthKeyUnregistered, UserDeactivated, UserDeactivatedBan,
    MessageNotModified
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, InputMediaPhoto
from config import API_ID, API_HASH, ERROR_MESSAGE, FORCE_CHANNELS
from cantarella.force_sub import force_subscribe
from database.db import db
import math
from logger import LOGGER
logger = LOGGER(__name__)

SUBSCRIPTION = os.environ.get('SUBSCRIPTION', 'https://i.ibb.co/k2P1Zt9k/image.jpg')
FREE_LIMIT_SIZE = 2 * 1024 * 1024 * 1024  # 2GB for free users
PREMIUM_LIMIT_SIZE = 4 * 1024 * 1024 * 1024  # 4GB for premium users
FREE_LIMIT_DAILY = 10
UPI_ID = os.environ.get("UPI_ID", "https://razorpay.me/@jashanpreetsingh1927?amount=ZFm4ghdmeB6pF5PK8Ki64w%3D%3D")
QR_CODE = os.environ.get("QR_CODE", "https://i.ibb.co/k2P1Zt9k/image.jpg")

REACTIONS = [
    "👍", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬",
    "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱",
    "🥴", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌",
    "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", "😴",
    "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝",
    "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", "🆒",
    "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂️", "🤷‍♀️",
    "😡"
]

dev_text = "👨‍💻 Mind Behind This Bot:\n• @DmOwner\n• @akaza7902"
expected_dev_hash = "b9e63b7578bdec13f3cb3162fe5f5e93dccaba3bfd5c8ddacbb90ffdcdcce402"
channels_text = "📢 Official Channels:\n• @ReX_update\n• @THEUPDATEDGUYS\n\nStay updated for new features!"
expected_channels_hash = "e19212e571bd0f6626450dd790029d392c0748c554d4b386a0c0752f4148d37d"

if (
    hashlib.sha256(dev_text.encode('utf-8')).hexdigest() != expected_dev_hash or
    hashlib.sha256(channels_text.encode('utf-8')).hexdigest() != expected_channels_hash
):
    raise Exception("Tampered developer info detected! Bot will not start. Fuck the code - crashing now.")

class script(object):
    START_TXT = """<b>🎌 Welcome {},</b>

<b>🤖 I am <a href="https://t.me/{}">{}</a></b>
<i>Your Ultimate Restricted Content Saver Bot</i>

<blockquote>
<b>🚀 Status :</b> 🟢 Online & Ready  
<b>⚡ Speed :</b> Ultra Fast Processing  
<b>🔐 Security :</b> Safe & Encrypted  
<b>📊 Reliability :</b> 99.9% Uptime  
</blockquote>
<blockquote>
<b>🌟 What I Can Do:</b>
📱 Save restricted channel/group posts  
📂 Batch download multiple files  
🔓 Access private & public Telegram content  
💎 Premium support for large files (up to 4GB) & faster speed  
</blockquote>
<blockquote>
<b>📋 How To Use:</b>
• Send any public channel post link  
• For private channels use <code>/login</code>  
• Get full guide using <code>/help</code>  
• Stop running batch using <code>/cancel</code>  
</blockquote>
<b>🚀 Ready to explore? Let's get started!</b>

<i>💫 Powered by Team JB 💫</i>
"""
    HELP_TXT = """🖍️ HELP MENU

🔻 ғᴏʀ ᴘᴜʙʟɪᴄ ᴀɴᴅ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛs :-
► Jᴜsᴛ Sᴇɴᴅ Pᴏsᴛ Lɪɴᴋs
• Public Channels Example: https://t.me/channel/123
• Private Channels Example: https://t.me/c/12345/678
• Private content requires login: /login

🔻 ғᴏʀ ʙᴏᴛ ᴄʜᴀᴛs :-
► Send bot messages link like:
https://t.me/b/botusername/4321
- For bot message ID use Plus Messenger App

🔻 ғᴏʀ ᴍᴜʟᴛɪᴘʟᴇ ᴘᴏsᴛ ᴀᴛ ᴀ ᴛɪᴍᴇ :-
► Send public/private post links in "from-to" format to download multiple messages
• Example:
https://t.me/xxxx/1001-1010
https://t.me/c/xxxx/101-120
• Note: Free users: Max 5 files per batch & Max 2GB per file
• Premium users: Max 1000 files per batch & Max 4GB per file

📚 AVAILABLE COMMANDS :-
⏣ /start - ᴄʜᴇᴄᴋ ɪ'ᴍ ᴀʟɪᴠᴇ
⏣ /help - ʜᴇʟᴘ ᴍᴇɴᴜ
⏣ /batch - ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴜʟᴛɪᴘʟᴇ ᴘᴏsᴛs ᴀᴛ ᴀ ᴛɪᴍᴇ
⏣ /myplan - Check your plan
⏣ /premium - Check premium plans
⏣ /settings - ᴄᴜsᴛᴏᴍɪᴢᴇ sᴇᴛᴛɪɴɢs
⏣ /login - ʟᴏɢɪɴ ᴀᴄᴄᴏᴜɴᴛ
⏣ /logout - ʟᴏɢᴏᴜᴛ ᴀᴄᴄᴏᴜɴᴛ
⏣ /set_thumb - sᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ
⏣ /view_thumb - ᴠɪᴇᴡ ᴛʜᴜᴍʙɴᴀɪʟ
⏣ /del_thumb - ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ
⏣ /set_caption - sᴇᴛ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ
⏣ /see_caption - ᴠɪᴇᴡ ᴄᴀᴘᴛɪᴏɴ
⏣ /del_caption - ᴅᴇʟᴇᴛᴇ ᴄᴀᴘᴛɪᴏɴ
⏣ /setchat - sᴇᴛ ᴄʜᴀɴɴᴇʟ
⏣ /remchat - ᴅᴇʟᴇᴛᴇ ᴄʜᴀɴɴᴇʟ
⏣ /broadcast - ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ (ᴏᴡɴᴇʀ ᴏɴʟʏ)

⚠️ TIPS :-
• Make sure links are correct
• Private content needs login
• Use /cancel to stop batch download
"""
    HELP_TXT1 = """🖍️ HELP MENU

🔻 ғᴏʀ ᴘᴜʙʟɪᴄ ᴀɴᴅ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛs :-
► Jᴜsᴛ Sᴇɴᴅ Pᴏsᴛ Lɪɴᴋs
• Public Channels Example: https://t.me/channel/123
• Private Channels Example: https://t.me/c/12345/678
• Private content requires login: /login

🔻 ғᴏʀ ʙᴏᴛ ᴄʜᴀᴛs :-
► Send bot messages link like:
https://t.me/b/botusername/4321
- For bot message ID use Plus Messenger App

🔻 ғᴏʀ ᴍᴜʟᴛɪᴘʟᴇ ᴘᴏsᴛ ᴀᴛ ᴀ ᴛɪᴍᴇ :-
► Send public/private post links in "from-to" format to download multiple messages
• Example:
https://t.me/xxxx/1001-1010
https://t.me/c/xxxx/101-120
• Note: Free users: Max 5 files per batch & Max 2GB per file
• Premium users: Max 1000 files per batch & Max 4GB per file

⚠️ TIPS :-
• Make sure links are correct
• Private content needs login
• Use /cancel to stop batch download
"""
    ABOUT_TXT = """<b>ℹ️ About This Bot</b>
<blockquote><b>╭────[ 🧩 Team JB ]────⍟</b>
<b>├⍟ 🤖 Bot Name : <a href=http://t.me/Saverestrictedcontents01_bot>Save Content</a></b>
<b>├⍟ 👨‍💻 Developer : <a href=https://t.me/TeamJB_bot>Team JB</a></b>
<b>├⍟ 📚 Library : <a href='https://docs.pyrogram.org/'>Pyrogram Async</a></b>
<b>├⍟ 🐍 Language : <a href='https://www.python.org/'>Python 3.11+</a></b>
<b>├⍟ 🗄 Database : <a href='https://www.mongodb.com/'>MongoDB Atlas Cluster</a></b>
<b>├⍟ 📡 Hosting : Dedicated High-Speed VPS</b>
<b>╰───────────────⍟</b></blockquote>
"""
    PREMIUM_TEXT = """<b>💎 Team JB Premium Membership</b>

<i>Unlock Full Power & Unlimited Features</i>

<blockquote>
<b>✨ Premium Benefits:</b>
♾ Unlimited Daily Downloads  
📦 Download Files Up To 4GB (Free: 2GB Limit)  
⚡ Ultra Fast Processing Speed (10+ MB/s)  
🖼 Custom Thumbnail Support  
📝 Custom Caption Support  
📂 Advanced Batch Download Mode (Up to 1000 files)  
🛟 24/7 Priority Support  
🚫 No Ads / No Restrictions  
</blockquote>

<blockquote>
<b>💰 Subscription Plans:</b>
</blockquote>

🥉 <b>1 Month Plan</b>  
₹100 /   

🥈 <b>3 Months Plan</b>  
₹250/  

🥇 <b>Lifetime Plan</b>  
₹699 / <i>(One Time Payment)</i>  


<blockquote>
<b>💳 Payment Details:</b>
</blockquote>

💸 <b>UPI ID :</b>  
<code>{}</code>

📸 <b>Scan & Pay :</b>  
<a href="{}">Click Here To Open QR</a>

<b>✅ After Payment:</b>
Send payment screenshot to admin for instant premium activation.

<i>⚡ Upgrade Now & Enjoy Unlimited Saving Experience</i>

<i>💫 Powered by Team JB 💫</i>
"""
    PROGRESS_BAR = """\
<b>⚡ Processing Your File...</b>

<blockquote>
<b>📊 Progress :</b> {bar} <b>{percentage:.1f}%</b>

<b>🚀 Speed :</b> <code>{speed}/s</code>  
<b>💾 Downloaded :</b> <code>{current} / {total}</code>  
<b>⏱ Time Passed :</b> <code>{elapsed}</code>  
<b>⏳ Time Remaining :</b> <code>{eta}</code>
</blockquote>

<i>🔄 Please wait... Your file is being prepared.</i>
"""
    CAPTION = """<b><a href="https://t.me/teamjb1"></a></b>\n\n<b>⚜️ Powered By : <a href="https://t.me/TeamJB_bot">Team JB 😎</a></b>"""
    LIMIT_REACHED = """<b>🚫 Daily Limit Exceeded</b>
<b>Your 10 free saves for today have been used.</b>
<i>Quota resets automatically after 24 hours from first download.</i>
<blockquote><b>🔓 Upgrade to Premium for Unlimited Access!</b></blockquote>
Remove all restrictions and enjoy seamless downloading.
"""
    SIZE_LIMIT = """<b>⚠️ File Size Exceeded</b>
<b>Free tier limited to 2GB per file.</b>
<i>File size: {file_size}</i>
<blockquote><b>🔓 Upgrade to Premium</b></blockquote>
Download files up to 4GB with no limits!
"""
    PREMIUM_SIZE_LIMIT = """<b>⚠️ File Size Exceeded</b>
<b>Premium tier limited to 4GB per file.</b>
<i>File size: {file_size}</i>
<blockquote>Contact admin for larger files</blockquote>
"""
    BATCH_LIMIT = """<b>⚠️ Batch Limit Exceeded</b>
<b>Free users can download maximum 5 files per batch.</b>
<i>You requested: {requested} files</i>
<blockquote><b>🔓 Upgrade to Premium</b></blockquote>
Download up to 1000 files per batch with Premium!
"""

def humanbytes(size):
    if not size:
        return "0B"
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2] if tmp else "0s"

class DownloadCancelled(Exception):
    """Custom exception for cancelled downloads"""
    pass

class batch_temp(object):
    # Store active downloads with message IDs as keys
    ACTIVE_DOWNLOADS = {}
    # Store cancellation requests
    CANCELLATION_REQUESTS = {}
    # Store user sessions
    USER_SESSIONS = {}

def get_message_type(msg):
    if getattr(msg, 'document', None): return "Document"
    if getattr(msg, 'video', None): return "Video"
    if getattr(msg, 'photo', None): return "Photo"
    if getattr(msg, 'audio', None): return "Audio"
    if getattr(msg, 'text', None): return "Text"
    return None

async def downstatus(client, statusfile, message, chat):
    try:
        while not os.path.exists(statusfile):
            await asyncio.sleep(3)
        while os.path.exists(statusfile):
            try:
                with open(statusfile, "r", encoding='utf-8') as downread:
                    txt = downread.read()
                await client.edit_message_text(chat, message.id, f"{txt}")
                await asyncio.sleep(5)
            except MessageNotModified:
                await asyncio.sleep(5)
            except:
                await asyncio.sleep(5)
    except Exception as e:
        logger.error(f"Error in downstatus: {e}")

async def upstatus(client, statusfile, message, chat):
    try:
        while not os.path.exists(statusfile):
            await asyncio.sleep(3)
        while os.path.exists(statusfile):
            try:
                with open(statusfile, "r", encoding='utf-8') as upread:
                    txt = upread.read()
                await client.edit_message_text(chat, message.id, f"{txt}")
                await asyncio.sleep(5)
            except MessageNotModified:
                await asyncio.sleep(5)
            except:
                await asyncio.sleep(5)
    except Exception as e:
        logger.error(f"Error in upstatus: {e}")

def progress(current, total, message, type):
    try:
        user_id = message.from_user.id
        message_id = message.id
        
        # Check if this download has been cancelled
        download_key = f"{user_id}_{message_id}"
        if download_key in batch_temp.CANCELLATION_REQUESTS:
            raise DownloadCancelled("Download cancelled by user")
        
        if not hasattr(progress, "cache"):
            progress.cache = {}
       
        now = time.time()
        task_id = f"{message.id}{type}"
        last_time = progress.cache.get(task_id, 0)
       
        if not hasattr(progress, "start_time"):
            progress.start_time = {}
        if task_id not in progress.start_time:
            progress.start_time[task_id] = now
           
        if (now - last_time) > 5 or current == total:
            try:
                percentage = current * 100 / total
                speed = current / (now - progress.start_time[task_id]) if (now - progress.start_time[task_id]) > 0 else 0
                eta = (total - current) / speed if speed > 0 else 0
                elapsed = now - progress.start_time[task_id]
               
                filled_length = int(percentage / 5)
                bar = '█' * filled_length + ' ' * (20 - filled_length)
               
                status = script.PROGRESS_BAR.format(
                    bar=bar,
                    percentage=percentage,
                    current=humanbytes(current),
                    total=humanbytes(total),
                    speed=humanbytes(speed),
                    elapsed=TimeFormatter(elapsed * 1000),
                    eta=TimeFormatter(eta * 1000)
                )
               
                with open(f'{message.id}{type}status.txt', "w", encoding='utf-8') as fileup:
                    fileup.write(status)
                   
                progress.cache[task_id] = now
               
                if current == total:
                    progress.start_time.pop(task_id, None)
                    progress.cache.pop(task_id, None)
            except:
                pass
    except DownloadCancelled as e:
        raise e
    except Exception as e:
        logger.error(f"Error in progress function: {e}")

@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if await force_subscribe(client, message):
        return
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    try:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    except:
        pass
    apis = ["https://api.waifu.pics/sfw/waifu", "https://nekos.life/api/v2/img/waifu"]
    api_url = random.choice(apis)
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        photo_url = response.json()["url"]
    except Exception as e:
        logger.error(f"Failed to fetch image from API: {e}")
        photo_url = "https://i.ibb.co/k2P1Zt9k/image.jpg"
    buttons = [
        [
            InlineKeyboardButton("📢 Channel", url="https://t.me/teamjb1"),
            InlineKeyboardButton("💬 Group", url="https://t.me/botsupdatesgroup")
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/TeamJB_bot"),
            InlineKeyboardButton("ℹ️ About Bot", callback_data="about_btn")
        ],
        [
            InlineKeyboardButton('💎 Buy Premium', callback_data="buy_premium"),
            InlineKeyboardButton('🆘 Help & Guide', callback_data="help_btn1")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    bot = await client.get_me()
    await client.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=script.START_TXT.format(message.from_user.mention, bot.username, bot.first_name),
        reply_markup=reply_markup,
        reply_to_message_id=message.id,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    if await force_subscribe(client, message):
        return
    buttons = [[InlineKeyboardButton("❌ Close Menu", callback_data="close_btn")]]
    await client.send_message(
        chat_id=message.chat.id,
        text=script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["plan", "myplan", "premium"]))
async def send_plan(client: Client, message: Message):
    if await force_subscribe(client, message):
        return
    buttons = [
        [InlineKeyboardButton("📸 Send Payment Proof", url="https://t.me/TeamJB_bot")],
        [InlineKeyboardButton("❌ Close Menu", callback_data="close_btn")]
    ]
    await client.send_photo(
        chat_id=message.chat.id,
        photo=SUBSCRIPTION,
        caption=script.PREMIUM_TEXT.format(UPI_ID, QR_CODE),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    if await force_subscribe(client, message):
        return
    
    user_id = message.from_user.id
    
    # Mark ALL active downloads for this user as cancelled
    cancelled_count = 0
    for key in list(batch_temp.CANCELLATION_REQUESTS.keys()):
        if key.startswith(f"{user_id}_"):
            cancelled_count += 1
    
    # Also check active downloads dictionary
    for download_key in list(batch_temp.ACTIVE_DOWNLOADS.keys()):
        if download_key.startswith(f"{user_id}_"):
            batch_temp.CANCELLATION_REQUESTS[download_key] = time.time()
            cancelled_count += 1
    
    # Clean up user sessions
    if user_id in batch_temp.USER_SESSIONS:
        try:
            acc = batch_temp.USER_SESSIONS[user_id]
            await acc.disconnect()
            del batch_temp.USER_SESSIONS[user_id]
        except:
            pass
    
    # Clean up status files
    try:
        for filename in os.listdir('.'):
            if filename.endswith('status.txt'):
                try:
                    os.remove(filename)
                except:
                    pass
    except:
        pass
    
    if cancelled_count > 0:
        await message.reply_text(f"✅ **Cancellation request sent!**\n<i>{cancelled_count} active download(s) will be stopped shortly.</i>", parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply_text("✅ **No active downloads to cancel.**\n<i>You can start new downloads.</i>", parse_mode=enums.ParseMode.HTML)
    
    # Clean up old cancellation requests after 5 minutes
    async def cleanup_old_requests():
        await asyncio.sleep(300)  # 5 minutes
        current_time = time.time()
        for key in list(batch_temp.CANCELLATION_REQUESTS.keys()):
            if key.startswith(f"{user_id}_"):
                request_time = batch_temp.CANCELLATION_REQUESTS[key]
                if current_time - request_time > 300:
                    del batch_temp.CANCELLATION_REQUESTS[key]
    
    asyncio.create_task(cleanup_old_requests())

async def settings_panel(client, callback_query):
    """
    Renders the Settings Menu with professional layout.
    """
    user_id = callback_query.from_user.id
    is_premium = await db.check_premium(user_id)
    badge = "💎 Premium Member" if is_premium else "👤 Standard User"
   
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 Command List", callback_data="cmd_list_btn")],
        [InlineKeyboardButton("📊 Usage Stats", callback_data="user_stats_btn")],
        [InlineKeyboardButton("🗑 Dump Chat Settings", callback_data="dump_chat_btn")],
        [InlineKeyboardButton("🖼 Manage Thumbnail", callback_data="thumb_btn")],
        [InlineKeyboardButton("📝 Edit Caption", callback_data="caption_btn")],
        [InlineKeyboardButton("⬅️ Return to Home", callback_data="start_btn")]
    ])
   
    text = f"<b>⚙️ Settings Dashboard</b>\n\n<b>Account Status:</b> {badge}\n<b>User ID:</b> <code>{user_id}</code>\n\n<i>Customize and manage your bot preferences below for an optimized experience:</i>"
   
    try:
        await callback_query.edit_message_caption(
            caption=text,
            reply_markup=buttons,
            parse_mode=enums.ParseMode.HTML
        )
    except MessageNotModified:
        pass
    except Exception as e:
        logger.error(f"Error editing message: {e}")

@Client.on_callback_query(filters.regex("check_sub"))
async def check_sub(client, query):
    for channel_id in FORCE_CHANNELS:
        try:
            await client.get_chat_member(channel_id, query.from_user.id)
        except UserNotParticipant:
            return await query.answer("Join all channels first ❌", show_alert=True)

    await query.message.delete()
    await query.answer("Subscription Verified ✅")

async def safe_download_with_cancellation(acc, msg, file_name, progress_func, progress_args, user_id, message_id):
    """Safe download function that checks for cancellation"""
    download_key = f"{user_id}_{message_id}"
    
    # Register this download as active
    batch_temp.ACTIVE_DOWNLOADS[download_key] = {
        'start_time': time.time(),
        'status': 'downloading'
    }
    
    try:
        file = await acc.download_media(
            msg,
            file_name=file_name,
            progress=progress_func,
            progress_args=progress_args
        )
        
        # Remove from active downloads if successful
        batch_temp.ACTIVE_DOWNLOADS.pop(download_key, None)
        batch_temp.CANCELLATION_REQUESTS.pop(download_key, None)
        
        return file
    except DownloadCancelled:
        # Clean up on cancellation
        batch_temp.ACTIVE_DOWNLOADS.pop(download_key, None)
        batch_temp.CANCELLATION_REQUESTS.pop(download_key, None)
        raise
    except Exception as e:
        # Clean up on error
        batch_temp.ACTIVE_DOWNLOADS.pop(download_key, None)
        batch_temp.CANCELLATION_REQUESTS.pop(download_key, None)
        raise e

@Client.on_message(filters.text & filters.private & ~filters.regex("^/"))
async def save(client: Client, message: Message):
    if "https://t.me/" in message.text:
        user_id = message.from_user.id
        message_id = message.id
        download_key = f"{user_id}_{message_id}"
        
        # Remove any previous cancellation requests for this message
        batch_temp.CANCELLATION_REQUESTS.pop(download_key, None)
        
        # Check daily limit
        is_limit_reached = await db.check_limit(user_id)
        if is_limit_reached:
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("💎 Upgrade to Premium", callback_data="buy_premium")]])
            return await message.reply_photo(
                photo=SUBSCRIPTION,
                caption=script.LIMIT_REACHED,
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )
       
        # Parse message IDs from URL
        datas = message.text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID
        
        # Calculate batch size
        batch_size = (toID - fromID) + 1
        
        # Check batch limit based on user premium status
        is_premium = await db.check_premium(user_id)
        if not is_premium and batch_size > 5:
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("💎 Upgrade to Premium", callback_data="buy_premium")]])
            return await message.reply_photo(
                photo=SUBSCRIPTION,
                caption=script.BATCH_LIMIT.format(requested=batch_size),
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )
        elif is_premium and batch_size > 1000:
            return await message.reply_text("<b>⚠️ Batch Limit Exceeded</b>\n<i>Premium users can download maximum 1000 files per batch.</i>", parse_mode=enums.ParseMode.HTML)
        
        is_private_link = "https://t.me/c/" in message.text
        is_batch = "https://t.me/b/" in message.text
        is_public_link = not is_private_link and not is_batch
        
        # Initialize counter for successful downloads
        success_count = 0
        
        # Send batch start message
        start_msg = await message.reply_text(f"<b>🚀 Starting Download...</b>\n<i>Total files: {batch_size}</i>\n\n<i>Use /cancel to stop at any time.</i>", parse_mode=enums.ParseMode.HTML)
        
        for msgid in range(fromID, toID + 1):
            # Check if this specific download was cancelled
            if download_key in batch_temp.CANCELLATION_REQUESTS:
                try:
                    await start_msg.edit_text(f"<b>❌ Download Cancelled</b>\n<i>Successfully downloaded {success_count} files out of {batch_size}</i>", parse_mode=enums.ParseMode.HTML)
                except:
                    pass
                break
            
            # Check daily limit for each file (for free users)
            if not is_premium:
                is_limit_reached = await db.check_limit(user_id)
                if is_limit_reached:
                    try:
                        await start_msg.edit_text(f"<b>⚠️ Daily Limit Reached</b>\n<i>Successfully downloaded {success_count} files out of {batch_size}</i>", parse_mode=enums.ParseMode.HTML)
                    except:
                        pass
                    break
            
            if is_public_link:
                username = datas[3]
                try:
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=username,
                        message_id=msgid,
                        reply_to_message_id=message.id
                    )
                    await db.add_traffic(user_id)
                    success_count += 1
                    await asyncio.sleep(0.5)
                    continue
                except Exception as e:
                    logger.error(f"Error copying public message {msgid}: {e}")
            
            # For private/bot links, check user session
            user_data = await db.get_session(user_id)
            if user_data is None:
                await message.reply(
                    "<b>🔒 Authentication Required</b>\n\n"
                    "<i>Access to this content requires login.</i>\n"
                    "<i>Use /login to securely authorize your account.</i>",
                    parse_mode=enums.ParseMode.HTML
                )
                await start_msg.delete()
                return
            
            try:
                # Create or reuse session
                if user_id not in batch_temp.USER_SESSIONS:
                    if is_premium:
                        acc = Client(
                            f"saverestricted_{user_id}_{int(time.time())}",
                            session_string=user_data,
                            api_hash=API_HASH,
                            api_id=API_ID,
                            in_memory=True,
                            max_concurrent_transmissions=20,
                            sleep_threshold=0,
                            workers=4
                        )
                    else:
                        acc = Client(
                            f"saverestricted_{user_id}_{int(time.time())}",
                            session_string=user_data,
                            api_hash=API_HASH,
                            api_id=API_ID,
                            in_memory=True,
                            max_concurrent_transmissions=10,
                            sleep_threshold=10
                        )
                    await acc.connect()
                    batch_temp.USER_SESSIONS[user_id] = acc
                else:
                    acc = batch_temp.USER_SESSIONS[user_id]
            except Exception as e:
                await start_msg.delete()
                return await message.reply(f"<b>❌ Authentication Failed</b>\n\n<i>Your session may have expired. Please /logout and /login again.</i>\n<code>{e}</code>", parse_mode=enums.ParseMode.HTML)
            
            try:
                if is_private_link:
                    chatid = int("-100" + datas[4])
                    success = await handle_restricted_content(client, acc, message, chatid, msgid, success_count, user_id, message_id)
                    if success:
                        success_count += 1
                elif is_batch:
                    username = datas[4]
                    success = await handle_restricted_content(client, acc, message, username, msgid, success_count, user_id, message_id)
                    if success:
                        success_count += 1
                else:
                    username = datas[3]
                    success = await handle_restricted_content(client, acc, message, username, msgid, success_count, user_id, message_id)
                    if success:
                        success_count += 1
            except DownloadCancelled:
                try:
                    await start_msg.edit_text(f"<b>❌ Download Cancelled</b>\n<i>Successfully downloaded {success_count} files out of {batch_size}</i>", parse_mode=enums.ParseMode.HTML)
                except:
                    pass
                break
            except Exception as e:
                logger.error(f"Error processing message {msgid}: {e}")
            
            # Update progress message every 3 files or when complete
            if success_count % 3 == 0 or success_count == batch_size:
                try:
                    await start_msg.edit_text(f"<b>📥 Download Progress</b>\n<i>Files downloaded: {success_count}/{batch_size}</i>\n\n<i>Use /cancel to stop</i>", parse_mode=enums.ParseMode.HTML)
                except MessageNotModified:
                    pass
                except:
                    pass
            
            # Shorter delay for premium users
            delay = 0.3 if is_premium else 1
            await asyncio.sleep(delay)
        
        # Clean up session
        if user_id in batch_temp.USER_SESSIONS:
            try:
                acc = batch_temp.USER_SESSIONS[user_id]
                await acc.disconnect()
                del batch_temp.USER_SESSIONS[user_id]
            except:
                pass
        
        # Clean up cancellation flags
        batch_temp.CANCELLATION_REQUESTS.pop(download_key, None)
        
        # Send completion message
        if success_count > 0:
            try:
                await start_msg.edit_text(f"<b>✅ Download Complete</b>\n<i>Successfully downloaded {success_count} out of {batch_size} files</i>", parse_mode=enums.ParseMode.HTML)
            except:
                pass
        else:
            try:
                await start_msg.delete()
            except:
                pass

async def handle_restricted_content(client: Client, acc, message: Message, chat_target, msgid, success_count, user_id, parent_message_id):
    is_premium = await db.check_premium(user_id)
    download_key = f"{user_id}_{parent_message_id}"
    
    # Check if cancelled before processing
    if download_key in batch_temp.CANCELLATION_REQUESTS:
        raise DownloadCancelled()
    
    try:
        msg: Message = await acc.get_messages(chat_target, msgid)
    except Exception as e:
        logger.error(f"Error fetching message {msgid} from {chat_target}: {e}")
        return False
    if msg.empty:
        return False
    
    msg_type = get_message_type(msg)
    if not msg_type:
        return False
    
    file_size = 0
    if msg_type == "Document": file_size = msg.document.file_size
    elif msg_type == "Video": file_size = msg.video.file_size
    elif msg_type == "Audio": file_size = msg.audio.file_size
    
    # Check file size limit based on user status
    if not is_premium and file_size > FREE_LIMIT_SIZE:
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("💎 Upgrade to Premium", callback_data="buy_premium")]])
        await client.send_message(
            message.chat.id,
            script.SIZE_LIMIT.format(file_size=humanbytes(file_size)),
            reply_markup=btn,
            parse_mode=enums.ParseMode.HTML
        )
        return False
    elif is_premium and file_size > PREMIUM_LIMIT_SIZE:
        await client.send_message(
            message.chat.id,
            script.PREMIUM_SIZE_LIMIT.format(file_size=humanbytes(file_size)),
            parse_mode=enums.ParseMode.HTML
        )
        return False
    
    # Handle text messages
    if msg_type == "Text":
        try:
            await client.send_message(message.chat.id, msg.text, entities=msg.entities, parse_mode=enums.ParseMode.HTML)
            await db.add_traffic(user_id)
            return True
        except:
            return False
    
    # Check if cancelled before downloading
    if download_key in batch_temp.CANCELLATION_REQUESTS:
        raise DownloadCancelled()
    
    # Add traffic for media files
    await db.add_traffic(user_id)
    smsg = await client.send_message(message.chat.id, f'<b>⬇️ Downloading file {success_count + 1}...</b>\n<i>Type: {msg_type}</i>', reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
    
    temp_dir = f"downloads/{message.id}_{success_count}"
    if not os.path.exists(temp_dir): 
        os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Start download status task
        download_task = asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg, message.chat.id))
        
        # Download file with cancellation check
        file = await safe_download_with_cancellation(
            acc, msg, f"{temp_dir}/", 
            progress, [message, "down"],
            user_id, parent_message_id
        )
        
        # Cancel download task
        download_task.cancel()
        if os.path.exists(f'{message.id}downstatus.txt'): 
            try:
                os.remove(f'{message.id}downstatus.txt')
            except:
                pass
                
    except DownloadCancelled:
        if os.path.exists(temp_dir): 
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
        try:
            await smsg.edit("❌ **Download Cancelled**")
        except:
            pass
        raise DownloadCancelled()
    except Exception as e:
        if os.path.exists(temp_dir): 
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
        try:
            await smsg.delete()
        except:
            pass
        return False
    
    # Check if cancelled before uploading
    if download_key in batch_temp.CANCELLATION_REQUESTS:
        if os.path.exists(temp_dir): 
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
        try:
            await smsg.delete()
        except:
            pass
        raise DownloadCancelled()
    
    try:
        # Start upload status task
        upload_task = asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg, message.chat.id))
        
        ph_path = None
        thumb_id = await db.get_thumbnail(user_id)
        
        if thumb_id:
            try:
                ph_path = await client.download_media(thumb_id, file_name=f"{temp_dir}/custom_thumb.jpg")
            except Exception as e:
                logger.error(f"Failed to download custom thumb: {e}")
        if not ph_path:
            try:
                if msg_type == "Video" and msg.video.thumbs:
                    ph_path = await acc.download_media(msg.video.thumbs[0].file_id, file_name=f"{temp_dir}/thumb.jpg")
                elif msg_type == "Document" and msg.document.thumbs:
                    ph_path = await acc.download_media(msg.document.thumbs[0].file_id, file_name=f"{temp_dir}/thumb.jpg")
            except:
                pass
        
        # Get custom caption
        custom_caption = await db.get_caption(user_id)
        if custom_caption:
            final_caption = custom_caption
        else:
            final_caption = script.CAPTION
            if msg.caption:
                final_caption = f"{msg.caption}\n\n" + final_caption
        
        # Send file based on type
        if msg_type == "Document":
            await client.send_document(
                message.chat.id, 
                file, 
                thumb=ph_path, 
                caption=final_caption, 
                progress=progress, 
                progress_args=[message, "up"]
            )
        elif msg_type == "Video":
            await client.send_video(
                message.chat.id, 
                file, 
                duration=msg.video.duration, 
                width=msg.video.width, 
                height=msg.video.height, 
                thumb=ph_path, 
                caption=final_caption, 
                progress=progress, 
                progress_args=[message, "up"]
            )
        elif msg_type == "Audio":
            await client.send_audio(
                message.chat.id, 
                file, 
                thumb=ph_path, 
                caption=final_caption, 
                progress=progress, 
                progress_args=[message, "up"]
            )
        elif msg_type == "Photo":
            await client.send_photo(
                message.chat.id, 
                file, 
                caption=final_caption
            )
        
        # Cancel upload task
        upload_task.cancel()
        
    except Exception as e:
        try:
            await smsg.edit(f"Upload Failed: {str(e)[:100]}")
        except:
            pass
        return False
    finally:
        if os.path.exists(f'{message.id}upstatus.txt'): 
            try:
                os.remove(f'{message.id}upstatus.txt')
            except:
                pass
        if os.path.exists(temp_dir): 
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
        try:
            await client.delete_messages(message.chat.id, [smsg.id])
        except:
            pass
    
    return True

@Client.on_callback_query()
async def button_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    message = callback_query.message
    if not message: 
        await callback_query.answer()
        return
    
    try:
        # --- DEVELOPER INFO ---
        if data == "dev_info":
            await callback_query.answer(
                text=dev_text,
                show_alert=True
            )
        elif data == "channels_info":
            await callback_query.answer(
                text=channels_text,
                show_alert=True
            )
        elif data == "settings_btn":
            await settings_panel(client, callback_query)
        elif data == "buy_premium":
            buttons = [
                [InlineKeyboardButton("📸 Send Payment Proof", url="https://t.me/TeamJB_bot")],
                [InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]
            ]
            try:
                await client.edit_message_media(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    media=InputMediaPhoto(
                        media=SUBSCRIPTION,
                        caption=script.PREMIUM_TEXT.format(UPI_ID, QR_CODE)
                    ),
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            except MessageNotModified:
                await callback_query.answer("Already showing premium plans!", show_alert=False)
            except Exception as e:
                logger.error(f"Error editing premium message: {e}")
                await callback_query.answer("Error loading premium plans", show_alert=True)
        elif data == "help_btn1":
            buttons = [[InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]]
            try:
                await client.edit_message_caption(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    caption=script.HELP_TXT1,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    parse_mode=enums.ParseMode.HTML
                )
            except MessageNotModified:
                await callback_query.answer("Already showing help!", show_alert=False)
            except Exception as e:
                logger.error(f"Error editing help message: {e}")
        elif data == "about_btn":
            buttons = [[InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]]
            try:
                await client.edit_message_caption(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    caption=script.ABOUT_TXT,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    parse_mode=enums.ParseMode.HTML
                )
            except MessageNotModified:
                await callback_query.answer("Already showing about!", show_alert=False)
            except Exception as e:
                logger.error(f"Error editing about message: {e}")
        elif data == "start_btn":
            bot = await client.get_me()
            apis = ["https://api.waifu.pics/sfw/waifu", "https://nekos.life/api/v2/img/waifu"]
            api_url = random.choice(apis)
            try:
                response = requests.get(api_url)
                response.raise_for_status()
                photo_url = response.json()["url"]
            except Exception as e:
                logger.error(f"Failed to fetch image from API: {e}")
                photo_url = "https://i.ibb.co/k2P1Zt9k/image.jpg"
            buttons = [
                [
                    InlineKeyboardButton("📢 Channel", url="https://t.me/teamjb1"),
                    InlineKeyboardButton("💬 Group", url="https://t.me/botsupdatesgroup")
                ],
                [
                    InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/TeamJB_bot"),
                    InlineKeyboardButton("ℹ️ About Bot", callback_data="about_btn")
                ],
                [
                    InlineKeyboardButton('💎 Buy Premium', callback_data="buy_premium"),
                    InlineKeyboardButton('🆘 Help & Guide', callback_data="help_btn1")
                ]
            ]
            try:
                await client.edit_message_media(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    media=InputMediaPhoto(
                        media=photo_url,
                        caption=script.START_TXT.format(callback_query.from_user.mention, bot.username, bot.first_name)
                    ),
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            except MessageNotModified:
                await callback_query.answer("Already at home!", show_alert=False)
            except Exception as e:
                logger.error(f"Error editing start message: {e}")
        elif data == "close_btn":
            try:
                await message.delete()
            except:
                await callback_query.answer("Couldn't delete message", show_alert=True)
        elif data in ["cmd_list_btn", "user_stats_btn", "dump_chat_btn", "thumb_btn", "caption_btn"]:
            await callback_query.answer("This feature will be available soon!", show_alert=True)
    except Exception as e:
        logger.error(f"Error in callback handler: {e}")
    
    await callback_query.answer()
