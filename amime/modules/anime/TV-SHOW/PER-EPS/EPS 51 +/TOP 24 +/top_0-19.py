import httpx
from anilist.types import Anime
from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyromod.helpers import ikb
from pyromod.nav import Pagination

from amime.amime import Amime


@Amime.on_callback_query(filters.regex(r"^tvshow_51plus_top anime (?P<page>\d+)"))
async def anime_suggestions(bot: Amime, callback: CallbackQuery):
    page = int(callback.matches[0]["page"])

    message = callback.message
    lang = callback._lang

    keyboard = []
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.post(
            url="https://graphql.anilist.co",
            json=dict(
                query="""
                query($per_page: Int) {
                    Page(page: 1, perPage: $per_page) {
                        media(type: ANIME, format: TV, sort: SCORE_DESC, status: FINISHED, episodes_greater: 51, episodes_lesser: 75) {
                            id
                            title {
                                romaji
                                english
                                native
                            }
                            siteUrl
                        }
                    }
                }
                """,
                variables=dict(
                    perPage=100,
                ),
            ),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        data = response.json()
        await client.aclose()
        if data["data"]:
            items = data["data"]["Page"]["media"]
            suggestions = [
                Anime(id=item["id"], title=item["title"], url=item["siteUrl"])
                for item in items
            ]

            layout = Pagination(
                suggestions,
                item_data=lambda i, pg: f"menu {i.id}",
                item_title=lambda i, pg: i.title.romaji,
                page_data=lambda pg: f"tvshow_51plus_top anime {pg}",
            )

            lines = layout.create(page, lines=8)

            if len(lines) > 0:
                keyboard += lines
    keyboard.append([(lang.Next, "tvshow_51plus_top1 anime 1")])
    keyboard.append([(lang.back_button, "ktgr-51plus")])

    await message.edit_text(
        lang.suggestions_text,
        reply_markup=ikb(keyboard),
    )
