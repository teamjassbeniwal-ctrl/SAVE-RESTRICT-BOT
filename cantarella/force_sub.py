from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_CHANNELS


async def force_subscribe(client, message):

    buttons = []

    for channel_id in FORCE_CHANNELS:
        try:
            await client.get_chat_member(channel_id, message.from_user.id)

        except UserNotParticipant:

            chat = await client.get_chat(channel_id)
            invite_link = chat.invite_link

            if invite_link is None:
                invite = await client.create_chat_invite_link(channel_id)
                invite_link = invite.invite_link

            buttons.append(
                [InlineKeyboardButton(chat.title, url=invite_link)]
            )

    if buttons:
        buttons.append([
            InlineKeyboardButton("✅ Try Again", callback_data="check_sub")
        ])

        await message.reply_text(
            "⚠️ Please join all required channels first",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return True

    return False
