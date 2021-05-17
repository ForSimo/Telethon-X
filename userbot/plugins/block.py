import asyncio

from telethon import events, functions

from . import (
    ALIVE_NAME,
    PM_START,
    PMMENU,
    PMMESSAGE_CACHE,
    check,
    get_user_from_event,
    parse_pre,
    set_key,
)
from .sql_helper import pmpermit_sql as pmpermit_sql

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
CACHE = {}
PMPERMIT_PIC = Config.PMPERMIT_PIC
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Telethon-X"


if Config.PRIVATE_GROUP_ID != 0:

    @bot.on(admin_cmd(outgoing=True))
    async def you_dm_niqq(event):
        if event.fwd_from:
            return
        chat = await event.get_chat()
        if event.text.startswith((".block")):
            return
        if (
            event.is_private
            and not pmpermit_sql.is_approved(chat.id)
            and chat.id not in PM_WARNS
        ):
            pmpermit_sql.approve(chat.id, "outgoing")

    @bot.on(admin_cmd(pattern="block(?: |$)(.*)"))
    async def block_p_m(event):
        if event.is_private:
            user = await event.get_chat()
        else:
            user, reason = await get_user_from_event(event)
            if not user:
                return
        if user.id in PM_START:
            PM_START.remove(user.id)
        await event.edit(
            f"`You are blocked Now .You Can't Message Me from now..`[{user.first_name}](tg://user?id={user.id})"
        )
        await event.client(functions.contacts.BlockRequest(user.id))

    @bot.on(admin_cmd(pattern="unblock(?: |$)(.*)"))
    async def unblock_pm(event):
        if event.is_private:
            user = await event.get_chat()
        else:
            user, reason = await get_user_from_event(event)
            if not user:
                return
        await event.client(functions.contacts.UnblockRequest(user.id))
        await event.edit(
            f"`You are Unblocked Now .You Can Message Me From now..`[{user.first_name}](tg://user?id={user.id})"
        )

CMD_HELP.update(
    {
        "block": "**Plugin : **`block`\
        \n\n  •  **Syntax : **`.block`\
        \n  •  **Function : **__Blocks the person.__\
        \n\n  •  **Syntax : **`.unblock`\
        \n  •  **Function : **__Unblocks the person.__"
    }
)

#  - @ForSimo
