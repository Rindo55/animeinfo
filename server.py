from pyrogram import Client
from jikanpy import Jikan
import signal
import sys
api_id = "3845818"
api_hash = "95937bcf6bc0938f263fc7ad96959c6d"
bot_token = "5210009358:AAESvuzGgAhRITt0BZxgrMjnRqlq2yDf18Q"
app = Client("my_anime_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
app.start()
   
@app.on_message()
def handle_message(client, message):
   anime_title = message.text  # Get the anime title from the message
   try:
      jikan = Jikan()
      anime = jikan.search("anime", anime_title)["results"][0]  # Search for the anime
      anime_info = f"Title: {anime['title']}\n"
      anime_info += f"Type: {anime['type']}\n"
      anime_info += f"Episodes: {anime['episodes']}\n"
      anime_info += f"Score: {anime['score']}\n"
      anime_info += f"Synopsis: {anime['synopsis']}\n"

      app.send_message(message.chat.id, anime_info)  # Send the anime information as a reply
   except IndexError:
      app.send_message(message.chat.id, "Anime not found.")  # Send a message if the anime is not found
from pyrogram import Client
from jikanpy import Jikan
import signal
import sys

api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"

app = Client("my_anime_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message()
def handle_message(client, message):
    anime_title = message.text

    try:
        jikan = Jikan()
        anime = jikan.search("anime", anime_title)["results"][0]
        anime_info = f"Title: {anime['title']}\n"
        anime_info += f"Type: {anime['type']}\n"
        anime_info += f"Episodes: {anime['episodes']}\n"
        anime_info += f"Score: {anime['score']}\n"
        anime_info += f"Synopsis: {anime['synopsis']}\n"

        client.send_message(message.chat.id, anime_info)
    except IndexError:
        client.send_message(message.chat.id, "Anime not found.")

def stop_client(signal, frame):
   app.stop()
   sys.exit(0)

signal.signal(signal.SIGINT, stop_client)

app.run()

   
