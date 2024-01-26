from telethon import TelegramClient, utils, events
from telethon.tl.functions.messages import SendMediaRequest
from telethon.tl.types import InputMediaUploadedDocument

async def handle_message(event):
    # Replace 'message' with 'event.message'
    message = event.message
    topic_id = 1227  # Replace with your actual condition
    if topic_id == 1227:
        topic_id = 1227
        model_name = "gemini-pro-vision"
        sticker_id = random.choice(stickers)
        
        # Replace 'app' with 'client'
        sticker = await client(SendMediaRequest(
            peer=KAYO_ID,
            media=InputMediaUploadedDocument(
                file=sticker_id,
                mime_type='image/png',  # Adjust the mime type accordingly
            ),
            reply_to_msg_id=topic_id
        ))

        txt = await client.send_message(
            KAYO_ID,
            f"Loading {model_name} ...",
            reply_to=topic_id
        )
        
        model = genai.GenerativeModel(model_name)
        await txt.edit("Downloading Image....")

        # Replace 'message' with 'event.message'
        file_path = await event.message.download()
        caption = event.message.text
        img = PIL.Image.open(file_path)
        
        await txt.edit("Shhh! 🤫, **Gemini Pro Vision** is at Work.\n Please Wait..\n\n#BETA")
        response = (
            model.generate_content([caption, img])
            if caption
            else model.generate_content(img)
        )
        os.remove(file_path)
        await txt.edit('Formating the Result...')
        await sticker.delete()
        await txt.delete()
        
        if response.text:
            print("response: ", response.text)
            await client.send_message(
                KAYO_ID,
                response.text,
                reply_to=topic_id
            )
        elif response.parts:  # handle multiline resps
            for part in response.parts:
                print("part: ", part)
                await client.send_message(
                    KAYO_ID,
                    part,
                    reply_to=topic_id
                )
                time.sleep(2)
        else:
            await event.reply(
                "Couldn't figure out what's in the Image. Contact @pirate_user for help."
            )
