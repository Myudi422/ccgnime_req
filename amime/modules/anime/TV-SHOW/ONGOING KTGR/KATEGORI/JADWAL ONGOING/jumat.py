from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

import datetime
import re
import anilist
from pyromod.helpers import array_chunk, ikb

from amime.amime import Amime
from amime.config import CHATS
from amime.database import Requests
from amime.modules.anime.view import anime_view




@Amime.on_message(filters.cmd(r"jumat$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^jumat$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.anime_tujuh, f"menu 129201"),
        ],
        [
            (lang.anime_tiga, f"menu 141774"),
        ],
        


    ]

    if is_callback:
        keyboard.append([(lang.back_button, "jadwal")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.ongoing_text,
        reply_markup=ikb(keyboard),
    )

