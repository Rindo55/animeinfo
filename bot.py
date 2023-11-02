import requests
import json
import configparser as cfg

from pyrogram import Client, filters, idle
from pyrogram.types import Message
from datetime import datetime, timedelta
from pymongo import MongoClient

# MongoDB connection
api_id = 3845818
api_hash = "95937bcf6bc0938f263fc7ad96959c6d"
bot_token = "6358924089:AAF9ruOPppIC-F3z2LwAym-SGqOFsf-cxuM"
app = Client("anime_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

client = MongoClient('mongodb+srv://anidata:animehevc@cluster0.xa2h6hh.mongodb.net/?retryWrites=true&w=majority')
db = client['telegram_bot']
collection = db['query_limits']

# Pyrogram client

# Command handler for /querystatus
@app.on_message(filters.command(['querystatus']))
def query_status(_, message: Message):
    user_id = message.from_user.id
    query_limit = 10

    # Check if user entry exists in the collection
    user_entry = collection.find_one({'user_id': user_id})
    if user_entry:
        queries_left = user_entry['queries_left']
        message.reply(f"You have {queries_left} queries left for today.")
    else:
        message.reply(f"You have {query_limit} queries left for today.")

# Message handler
@app.on_message(filters.text)
def handle_message(_, message: Message):
    user_id = message.from_user.id
    query_limit = 10

    # Check if user entry exists in the collection
    user_entry = collection.find_one({'user_id': user_id})

    # If user entry exists, check if limit reached
    if user_entry:
        queries_left = user_entry['queries_left']
        last_query_time = user_entry['last_query_time']

        # Calculate time difference from last query
        time_diff = datetime.now() - last_query_time

        # If more than 24 hours passed, reset the limit
        if time_diff > timedelta(hours=24):
            queries_left = query_limit

        # If limit reached, send message and return
        if queries_left <= 0:
            message.reply("You have reached today's limit of 10 queries.")
            return

        # Update the query count and last query time
        collection.update_one(
            {'user_id': user_id},
            {'$set': {'queries_left': queries_left - 1, 'last_query_time': datetime.now()}}
        )
    else:
        # Create new user entry
        collection.insert_one(
            {'user_id': user_id, 'queries_left': query_limit - 1, 'last_query_time': datetime.now()}
        )
app.start()
print("Powered by @animxt")
idle()
