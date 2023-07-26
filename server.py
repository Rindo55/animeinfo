from pyrogram import Client, idle
from jikanpy import Jikan
import signal
import sys
api_id = 3845818
api_hash = "95937bcf6bc0938f263fc7ad96959c6d"
bot_token = "5210009358:AAESvuzGgAhRITt0BZxgrMjnRqlq2yDf18Q"
app = Client("anime_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

   
def get_anime_info(anime_title):
    url = f"https://api.jikan.moe/v4/anime?q={anime_title}"
    response = requests.get(url)
    data = response.json()

    if data:
        anime = data[0]
        anime_info = f"Title: {anime['title']['romaji']}\n"
        anime_info += f"Type: {anime['type']}\n"
        anime_info += f"Episodes: {anime['episodes']}\n"
        anime_info += f"Score: {anime['averageScore']}\n"
        anime_info += f"Synopsis: {anime['description']['en']}\n"

        return anime_info
    else:
        return "Anime not found."

@app.on_message(filters.command("anime"))
def handle_message(client, message):
    anime_title = " ".join(message.command[1:])
    anime_info = get_anime_info(anime_title)
    client.send_message(message.chat.id, anime_info)
app.start()
print("Powered by @animxt")
idle()

   
