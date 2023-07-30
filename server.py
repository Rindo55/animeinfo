from pyrogram import Client, idle, filters
import asyncio
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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
    
        air = [aire['from'] and aire['to'] for aire in anime['aired']]
        aired = air.replace("T00:00:00+00:00", "")
        anime_info += f"Aired: {', '.join(aire)}\n\n"
        
        
        anime_info += f"- Premiered: {anime['season']} {anime['year']} \n\n"
        
        producers = [producer['name'] for producer in anime['producers']]
        anime_info += f"- Producers: {', '.join(producers)}\n\n"
        licensors = [licensor['name'] for licensor in anime['licensors']]
        anime_info += f"Licensors: {', '.join(licensors)}\n\n"
        studios = [studio['name'] for studio in anime['studios']]
        anime_info += f"Studio: {', '.join(studios)}\n\n"        
        anime_info += f"- Source: {anime['source']}\n\n"
        themes = [theme['name'] for theme in anime['themes']]
        anime_info += f"Themes: {', '.join(themes)}\n"
        anime_info += f"- Duration: {anime['duration']}\n\n"
        anime_info += f"- Rating: {anime['rating']}\n\n"



        return anime_info
    else:
        return "Anime not found."

@app.on_message(filters.command("anime"))
def handle_message(client, message):
    anime_title = " ".join(message.command[1:])
    anime_info = get_anime_info(anime_title)
    client.send_message(message.chat.id, anime_info)

ANIME_QUERY = """
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
    studios{
      name
    }
    }
    startDate {
        year
        month
        day
    }
    endDate {
        year
        month
        day
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
ANIME_DB = {}

async def return_json_senpai(query: str, vars_: dict):
    url = "https://graphql.anilist.co"
    anime = vars_["search"]
    db = ANIME_DB.get(anime)

    if db:
      return db
    data = requests.post(url, json={"query": query, "variables": vars_}).json()
    ANIME_DB[anime] = data

    return data

temp = []

async def get_anime(vars_,less):
    if 1 == 1:
        result = await return_json_senpai(ANIME_QUERY, vars_)

        error = result.get("errors")
        if error:
            error_sts = error[0].get("message")
            print([f"[{error_sts}]"])
            print(vars_)
            data = temp[0]
            temp.pop(0)
        else:
          data = result["data"]["Media"]   
          temp.append(data)
        idm = data.get("id")
        title = data.get("title")
        tit = title.get("english")
        if tit == None:
            tit = title.get("romaji")

        title_img = f"https://img.anili.st/media/{idm}"
        
        if less == True:
          return idm, title_img, tit

        return data

async def get_anime_img(query):
    vars_ = {"search": query}
    idm, title_img, title = await get_anime(vars_,less=True)

    #title = format_text(title)
    return idm, title_img, title
    
def get_anime_name(title):
    x = title.split(" - ")[-1]
    title = title.replace(x,"").strip()
    title = title[:-2].strip()

    x = title.split(" ")[-1].strip()
    if str(x[-1]) in digits and str(x[0]) == "S" and str(x[1]) in digits:
      if "S" in x:
        y = x.replace("S","S")
        title = title.replace(x,y)
    return title

atext = """
📺 **{}**
      **({})**
**━━━━━━━━━━━━━━━━━━━━━━**
**• Type: {}
• Source: {}
• Score: 🌟{}
• Genre: #{}
• Studio: {}
• Status: {}
• Episodes: {}
• Duration: {} mins/Ep**
"""

async def get_anilist_data(name):
    vars_ = {"search": name}
    data = await get_anime(vars_,less=False)
    id_ = data.get("id")
    title = data.get("title")
    form = data.get("format")
    source = data.get("source")
    status = data.get("status")
    episodes = data.get("episodes")
    duration = data.get("duration")
    trailer = data.get("trailer")
    genres = data.get("genres")
    studio = data.get("studios")
    averageScore = data.get("averageScore")
    img = f"https://img.anili.st/media/{id_}"

    # title
    title1 = title.get("english")
    title2 = title.get("romaji")

    if title2 == None:
      title2 = title.get("native")

    if title1 == None:
      title1 = title2   

    # genre

    genre = ""

    for i in genres:
      genre += i + ", #"

    genre = genre[:-3]
    genre = genre.replace("#Slice of Life", "#Slice_of_Life")
    genre = genre.replace("#Mahou Shoujo", "#Mahou_Shoujo")    
    genre = genre.replace("#Sci-Fi", "#SciFi")
    
    studiox = data['studios']['name']
   
    tags = []
    for i in data['tags']:
        tags.append(i["name"])
    tagsx = "#" + f"{', #'.join(tags)}"
    tagsx = tagsx.replace("#Age Gap", "#Age_Gap")
    tagsx = tagsx.replace("#Anti-hero", "#Antihero")
    tagsx = tagsx.replace("#Artificial Intelligence", "#Artificial_Intelligence")
    tagsx = tagsx.replace("#Augmented Reality", "#Augmented_Reality")
    tagsx = tagsx.replace("#Battle Royale", "#Battle_Royale")
    tagsx = tagsx.replace("#Body Horror", "#Body_Horror")
    tagsx = tagsx.replace("#Boys' Love", "#Boys_Love")
    tagsx = tagsx.replace("#Card Battle", "#Card_Battle")
    tagsx = tagsx.replace("#Coming of Age", "#Coming_of_Age")
    tagsx = tagsx.replace("#Cosmic Horror", "#Cosmic_Horror")
    tagsx = tagsx.replace("#Cute Boys Doing Cute Things", "#Cute_Boys_Doing_Cute_Things")
    tagsx = tagsx.replace("#Cute Girls Doing Cute Things", "#Cute_Girls_Doing_Cute_Things")
    tagsx = tagsx.replace("#Ensemble Cast", "#Ensemble_Cast")
    tagsx = tagsx.replace("#Fairy Tale", "#Fairy_Tale")
    tagsx = tagsx.replace("#Family Life", "#Family_Life")
    tagsx = tagsx.replace("#Female Harem", "#Female_Harem")
    tagsx = tagsx.replace("#Female Protagonist", "#Female_Protagonist")
    tagsx = tagsx.replace("#Full CGI", "#Full_CGI")
    tagsx = tagsx.replace("#Full Color", "#Full_Color")
    tagsx = tagsx.replace("#Found Family", "#Found_Family")
    tagsx = tagsx.replace("#Gender Bending", "#Gender_Bending")
    tagsx = tagsx.replace("#Ice Skating", "#Ice_Skating")
    tagsx = tagsx.replace("#Language Barrier", "#Language_Barrier")
    tagsx = tagsx.replace("#Lost Civilization", "#LostCivilization")
    tagsx = tagsx.replace("#Love Triangle", "#Love_Triangle")
    tagsx = tagsx.replace("#Male Protagonist", "#Male_Protagonist")
    tagsx = tagsx.replace("#Martial Arts", "#Martial_Arts")
    tagsx = tagsx.replace("#Memory Manipulation", "#Memory_Manipulation")
    tagsx = tagsx.replace("#Monster Boy", "#Monster_Boy")
    tagsx = tagsx.replace("#Monster Girl", "#Monster_Girl")
    tagsx = tagsx.replace("#Non-fiction", "#Nonfiction")
    tagsx = tagsx.replace("#Office Lady", "#Office_Lady")
    tagsx = tagsx.replace("#Ojou-sama", "#Ojousama")
    tagsx = tagsx.replace("#Otaku Culture", "#Otaku_Culture")
    tagsx = tagsx.replace("#Post-Apocalyptic", "#Post_Apocalyptic")
    tagsx = tagsx.replace("#Primarily Adult Cast", "#Primarily_Adult_Cast")
    tagsx = tagsx.replace("#Primarily Child Cast", "#Primarily_Child_Cast")
    tagsx = tagsx.replace("#Primarily Female Cast", "#Primarily_Female_Cast")
    tagsx = tagsx.replace("#Primarily Male Cast", "#Primarily_Male_Cast")
    tagsx = tagsx.replace("#Primarily Teen Cast", "#Primarily_Teen_Cast")
    tagsx = tagsx.replace("#School Club", "#School_Club")
    tagsx = tagsx.replace("#Real Robot", "#Real_Robot")
    tagsx = tagsx.replace("#Ero Guro", "#Ero_Guro")
    tagsx = tagsx.replace("#Software Development", "#Software_Development")
    tagsx = tagsx.replace("#Time Manipulation", "#Time_Manipulation")
    tagsx = tagsx.replace("#Surreal Comedy", "#Surreal_Comedy")
    tagsx = tagsx.replace("#Teens' Love", "#Teens_Love")
    tagsx = tagsx.replace("#Urban Fantasy", "#Urban_Fantasy")
    tagsx = tagsx.replace("#Super Power", "#Super_Power")
    tagsx = tagsx.replace("#Super Robot", "#Super_Robot")
    tagsx = tagsx.replace("#Video Games", "#Video Games")
    tagsx = tagsx.replace("#Virtual World", "#Virtual_World")
    tagsx = tagsx.replace("#Shrine Maiden", "#Shrine_Maiden")
    tagsx = tagsx.replace("#Lost Civilization", "#Lost_Civilization")
    tagsx = tagsx.replace("#Dissociative Identities", "#Dissociative_Identities")
    tagsx = tagsx.replace("#Achronological Order", "#Achronological Order")
    tagsx = tagsx.replace("#Time Skip", "#Time_Skip")
    tagsx = tagsx.replace("#Age Regression", "#Age_Regression")
    tagsx = tagsx.replace("#Human Pet", "#Human_Pet")
    tagsx = tagsx.replace("#Achronoligical Order", "#Achronoligical_Order")
    tagsx = tagsx.replace("#Family Life", "#Family_Life")
    tagsx = tagsx.replace("#Body Swapping", "#Body_Swapping")
    tagsx = tagsx.replace("#Large Breasts", "Large_Breasts")
    tagsx = tagsx.replace("#Classic Literature", "#Classic_Literature")
    tagsx = tagsx.replace("#Tanned Skin", "#Tanned_Skin")
    tagsx = tagsx.replace("#Video Games", "#Video_Games")
    caption = atext.format(
      title1,
      title2,
      form,
      source,
      averageScore,
      genre,
      studiox,
      status,
      episodes,
      duration
    )

    if trailer != None:
      ytid = trailer.get("id")
      site = trailer.get("site")
    else:
      site = None

    if site == "youtube":
      caption += f"**• [Trailer](https://www.youtube.com/watch?v={ytid})  |  [More Info](https://anilist.co/anime/{id_})\n ━━━━━━━━━━━━━━━━━━━━━━\n@Latest_ongoing_airing_anime**"
    else:
      caption += f"**• [More Info](https://anilist.co/anime/{id_})\n━━━━━━━━━━━━━━━━━━━━━━\n@Latest_ongoing_airing_anime**"

    return img, caption

@app.on_message(filters.command("anilist"))
async def handle_message(client, message):
    name = " ".join(message.command[1:])
    result = await get_anilist_data(name)
    img, caption = result
    return await client.send_photo(message.chat.id,photo=img,caption=caption)


async def get_anime_info(anime_name):
    query = '''
    query ($anime_name: String) {
        Media (search: $anime_name, type: ANIME) {
            title {
                romaji
                english
            }
            type
            averageScore
            source
            duration
            episodes
            genres
            tags {
                name
            }
            status
            studios {
                nodes {
                    name
                }
            }
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            licensors {
                nodes {
                    name
                }
            }
            season
            producers {
                nodes {
                    name
                }
            }
        }
    }
    '''

    variables = {
        "anime_name": anime_name
    }
    ANILIST_API = "https://graphql.anilist.co"
    response = requests.post(ANILIST_API, json={"query": query, "variables": variables})
    data = response.json()

    return data["data"]["Media"]


# Handler for /anime command
@app.on_message(filters.command("ani"))
async def anime_command_handler(client, message):
    # Get the anime name from the command arguments
    anime_name = " ".join(message.command[1:])

    # Get anime info from AniList
    anime_info = await get_anime_info(anime_name)

    # Format the anime info into a string
    info_string = f"Title: {anime_info['title']['romaji']}\n"
    info_string += f"English Title: {anime_info['title']['english']}\n"
    info_string += f"Type: {anime_info['type']}\n"
    info_string += f"Score: {anime_info['averageScore']}\n"
    info_string += f"Source: {anime_info['source']}\n"
    info_string += f"Duration: {anime_info['duration']}\n"
    info_string += f"Episodes: {anime_info['episodes']}\n"
    info_string += f"Genres: {', '.join(anime_info['genres'])}\n"
    info_string += f"Tags: {', '.join(tag['name'] for tag in anime_info['tags'])}\n"
    info_string += f"Status: {anime_info['status']}\n"
    info_string += f"Studio: {anime_info['studios']['nodes'][0]['name']}\n"
    info_string += f"Start Date: {anime_info['startDate']['year']}-{anime_info['startDate']['month']}-{anime_info['startDate']['day']}\n"
    info_string += f"End Date: {anime_info['endDate']['year']}-{anime_info['endDate']['month']}-{anime_info['endDate']['day']}\n"
    info_string += f"Licensors: {', '.join(licensor['name'] for licensor in anime_info['licensors']['nodes'])}\n"
    info_string += f"Season: {anime_info['season']}\n"
    info_string += f"Producers: {', '.join(producer['name'] for producer in anime_info['producers']['nodes'])}\n"

    # Send the anime info as a reply
    await message.reply_text(info_string)
app.start()
print("Powered by @animxt")
idle()

   
