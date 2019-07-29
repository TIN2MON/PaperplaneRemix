# TG-UserBot - A modular Telegram UserBot script for Python.
# Copyright (C) 2019  Kandarp <https://github.com/kandnub>
#
# TG-UserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TG-UserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TG-UserBot.  If not, see <https://www.gnu.org/licenses/>.


from asyncio import sleep, create_task
from pyrogram import Filters
from pyrogram.api.functions.messages import ToggleDialogPin

from userbot import client
from userbot.events import on_message, outgoing
from userbot.helper_funcs.time import string_to_secs


async def reminderTask(delay, string):
    await sleep(delay)
    peer = await client.resolve_peer('self')
    await client.send(
        ToggleDialogPin(peer=peer, pinned=True)
    )
    await client.send_message('self', string)


@outgoing(pattern=r"remindme (\w+) ([\s\S]*)")
async def remindme(c, event):
    time = event.matches[0].group(1)
    text = event.matches[0].group(2)
    seconds = await string_to_secs(time)

    if seconds != 0:
        create_task(
            reminderTask(seconds, text)
        )
        text = f"`Reminder will be sent in Saved Messages after {time}.`"
        if seconds >= 86400:
            text += "`\nThis may not work as expected, not fully certain though.`"
        await event.edit(text)
    else:
        await event.edit("`No kan do. ma'am.`")


@on_message(Filters.me & Filters.incoming & Filters.regex("(?i)^dismiss$"))
async def dismiss(c, event):
    reply = event.reply_to_message
    if reply:
        await reply.delete()
    await event.delete()

    peer = await client.resolve_peer('self')
    await client.send(
        ToggleDialogPin(peer=peer, pinned=None)
    )