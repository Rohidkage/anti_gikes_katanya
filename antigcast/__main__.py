import asyncio
from antigcast import Bot, app
from antigcast.config import LOGGER, LOG_CHANNEL_ID
from pyrogram import idle
from antigcast.helpers.tools import checkExpired


loop = asyncio.get_event_loop_policy().get_event_loop()

async def main():
    try:
        await app.start()
        app.me = await app.get_me()
        username = app.me.username
        namebot = app.me.first_name
        log = await app.send_message(LOG_CHANNEL_ID, "BOT AKTIF!")
        LOGGER("INFO").info(f"{namebot} | [ @{username} ] | 🔥 BERHASIL DIAKTIFKAN! 🔥")
        await log.delete()
    except Exception as a:
        print(a)
    LOGGER("INFO").info(f"[🔥 BOT AKTIF! 🔥]")
    await checkExpired()
    await idle()

@app.on_message(filters.command(["duar"], PREFIX) & ~filters.private & filters.user(OWNER_ID))
async def banFunc(_, m):
    ijin = await member_permissions(m.chat.id, m.from_user.id)
    xx = "can_restrict_members"
    if xx not in ijin:
        return
    user_id = await extract_user(m)
    if not user_id:
        return
    if user_id == app.me.id:
        return
    if user_id in OWNER_ID:
        return
    if user_id in (await list_admins(m.chat.id)):
        return
    dicekah = await is_bisu_user(user_id)
    if dicekah:
        return await m.reply_text("Binatang Liar Ini Sudah Terblacklist.")
    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            m.reply_to_m.sender_chat.title
            if m.reply_to_message
            else "Anon"
        )
    await add_bisu_user(user_id)
    return await m.reply(f"User : {mention} Binatang Liar Ini Sudah Terblacklist.")

@app.on_message(filters.command(["lepas"], PREFIX) & ~filters.private & filters.user(OWNER_ID))
async def banFunc(_, m):
    ijin = await member_permissions(m.chat.id, m.from_user.id)
    xx = "can_restrict_members"
    if xx not in ijin:
        return
    user_id = await extract_user(m)
    if not user_id:
        return
    dicekah = await is_bisu_user(user_id)
    if not dicekah:
        return await m.reply_text("Binatang Liar Terlepas Dari Blacklist.")
    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            m.reply_to_m.sender_chat.title
            if m.reply_to_message
            else "Anon"
        )
    await remove_bisu_user(user_id)
    return await m.reply(f"User : {mention} added to whitelist.")

LOGGER("INFO").info("Starting Bot...")
loop.run_until_complete(main())
