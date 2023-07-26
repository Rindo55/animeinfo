from pyrogram import Client, idle, filters
from jikanpy import Jikan
import signal
import sys
import aiohttp
import requests
api_id = 3845818
api_hash = "95937bcf6bc0938f263fc7ad96959c6d"
bot_token = "5210009358:AAESvuzGgAhRITt0BZxgrMjnRqlq2yDf18Q"
app = Client("anime_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
def get_anime_info(anime_title):
    url = f"https://api.jikan.moe/v4/anime?q={anime_title}"
    response = requests.get(url)
    data = response.json()

    if data and "data" in data and len(data["data"]) > 0:
        anime = data["data"][0]
        anime_info = f"**Title: {anime['title']}**\n"
        anime_info += f"- Type: {anime['type']}\n\n"
        anime_info += f"- Score: {anime['score']}\n\n"
        anime_info += f"- Episodes: {anime['episodes']}\n\n"
        anime_info += f"- Status: {anime['status']}\n\n"
        anime_info += f"- Aired: {anime['aired']}\n\n"
        anime_info += f"Premiered: {anime['season']}\n\n"
        anime_info += f"Producers: {anime['producers']}\n\n"
        anime_info += f"Licensors: {anime['licensors']}\n\n"
        anime_info += f"Studio: {anime['studios']}\n\n"
        anime_info += f"Source: {anime['source']}\n\n"
        anime_info += f"Theme: {anime['theme']}\n\n"
        anime_info += f"Duration: {anime['duration']}\n\n"
        anime_info += f"Rating: {anime['rating']}\n\n"



        return anime_info
    else:
        return "Anime not found."

@app.on_message(filters.command("anime"))
def handle_message(client, message):
    anime_title = " ".join(message.command[1:])
    anime_info = get_anime_info(anime_title)
    client.send_message(message.chat.id, anime_info)
def get_ani_info(ani_title):
    url = f"https://graphql.anilist.co"
query = """
query ($id: Int, $idMal:Int, $search: String) {
  Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
    }
    genres
    tags {
      name
    }
    averageScore
    relations {
      edges {
        node {
          title {
            romaji
            english
          }
          id
        }
        relationType
      }
    }
    nextAiringEpisode {
      timeUntilAiring
      episode
    }
    isAdult
    isFavourite
    mediaListEntry {
      status
      score
      id
    }
    siteUrl
  }
}
"""
variables = {
    "search": ani_title
}
response = requests.post(url, json={"query": query, "variables": variables})
data = response.json()

if "data" in data and data["data"]["Media"]:
    anime = data["data"]["Media"]
    anime_info = f"Title (Romaji): {anime['title']['romaji']}\n"
    if anime['title']['english']:
        anime_info += f"Title (English): {anime['title']['english']}\n"
    if anime['title']['native']:
        anime_info += f"Title (Native): {anime['title']['native']}\n"
    anime_info += f"Format: {anime['format']}\n"
    anime_info += f"Episodes: {anime['episodes']}\n"
    if anime['averageScore']:
        anime_info += f"Average Score: {anime['averageScore']}\n"
    anime_info += f"Description: {anime['description']}\n"
    anime_info += f"Duration: {anime['duration']}\n"
    anime_info += f"Genre: {anime['genre']}\n"

return anime_info


@app.on_message(filters.command("anilist"))
def handle_message(client, message):
    ani_title = " ".join(message.command[1:])
    anime_info = get_ani_info(ani_title)
    client.send_message(message.chat.id, anime_info)
app.start()
print("Powered by @animxt")
idle()

   
