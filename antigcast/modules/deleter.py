import asyncio
from time import time
from antigcast import Bot
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import *
from pyrogram.errors import FloodWait, MessageDeleteForbidden, UserNotParticipant

from antigcast.config import *
from antigcast.helpers.tools import *
from antigcast.helpers.admins import *
from antigcast.helpers.message import *
from antigcast.helpers.database import *

admins_in_chat = {}

async def list_admins(chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 60:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in app.get_chat_members(
                chat_id, filter=ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]

@Bot.on_message(filters.command("addbl") & ~filters.private & Admin)
async def addblmessag(app : Bot, message : Message):
    trigger = get_arg(message)
    if message.reply_to_message:
        trigger = message.reply_to_message.text or message.reply_to_message.caption

    xxnx = await message.reply(f"`Menambahakan` {trigger} `ke dalam blacklist..`")
    try:
        await add_bl_word(trigger.lower())
    except BaseException as e:
        return await xxnx.edit(f"Error : `{e}`")

    try:
        await xxnx.edit(f"{trigger} `berhasil di tambahkan ke dalam blacklist..`")
    except:
        await app.send_message(message.chat.id, f"{trigger} `berhasil di tambahkan ke dalam blacklist..`")

    await asyncio.sleep(5)
    await xxnx.delete()
    await message.delete()

@Bot.on_message(filters.command("delbl") & ~filters.private & Admin)
async def deldblmessag(app : Bot, message : Message):
    trigger = get_arg(message)
    if message.reply_to_message:
        trigger = message.reply_to_message.text or message.reply_to_message.caption

    xxnx = await message.reply(f"`Menghapus` {trigger} `ke dalam blacklist..`")
    try:
        await remove_bl_word(trigger.lower())
    except BaseException as e:
        return await xxnx.edit(f"Error : `{e}`")

    try:
        await xxnx.edit(f"{trigger} `berhasil di hapus dari blacklist..`")
    except:
        await app.send_message(message.chat.id, f"{trigger} `berhasil di hapus dari blacklist..`")

    await asyncio.sleep(5)
    await xxnx.delete()
    await message.delete()


@Bot.on_message(filters.new_chat_members, group=-1)
async def new_chat_members(app: Bot, message: Message):
    text = f"Maaf, Grup ini tidak terdaftar di dalam list. Silahkan hubungi owner Untuk mendaftarkan Group Anda.\n\n**Bot akan meninggalkan group!**"
    chat = message.chat.id
    chats = await get_actived_chats()
    for member in message.new_chat_members:
        try:
            if member.id == Bot.id:
                if chat not in chats:
                    await message.reply(text=text)
                    await asyncio.sleep(5)
                    try:
                        await app.leave_chat(chat)
                    except UserNotParticipant as e:
                        print(e)
                        return
        except Exception as e:
            print(e)

@Bot.on_message(filters.text & filters.group & Gcast, group=-1)
async def gasapus(app: Bot, m: Message):
    user = m.from_user
    if not user:
        return
    if m.sender_chat:
        return
    if m.chat.id not in await get_actived_chats():
        return
    if user.id in await list_admins(m.chat.id):
        return
    try:
        await app.delete_messages(m.chat.id, m.id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await app.delete_messages(m.chat.id, m.id)
    except MessageDeleteForbidden:
        return