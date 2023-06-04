import os
from telethon import events
from config import bot, FILES_CHANNEL, LOGS_CHANNEL, LINKS_CHANNEL, FILES_HIDER_BOT_USERNAME
import json
from gogoapi import Gogo
from mongodb import ConfigDB, AutoAnimeDB
import asyncio
import downloader
from FastTelethonhelper import fast_upload
import traceback

cdb = ConfigDB()
adb = AutoAnimeDB()

link_format = """
┃█████████████████████
[FILENAME]
┃█████████████████████
JUST CLICK AND PRESS START
"""

loop = asyncio.get_event_loop()

@bot.on(events.NewMessage(pattern="/start", func=lambda e: e.is_private))
async def start_fn(event):
    await bot.send_message(event.chat_id, "Hello!!!")
    
async def checker_loop():
    data = cdb.find({"_id":"GogoAnime"})
    api = Gogo(
        gogoanime_token=data["gogoanime"],
        auth_token=data["auth"],
        host=data["url"]
    )
    while True:
        try:
            gogo_anime_list = api.get_bookmarks()
            db_anime_list = adb.full()
            for i in gogo_anime_list:
                db_anime = None
                for j in db_anime_list:
                    if i["Anime"] == j["Anime"]:
                        db_anime = j
                        break
                if db_anime == None:
                    db_anime = {
                            "Anime": i["Anime"],
                            "Episode": 0,
                            "Link": i["Link"].split("-episode-")[0]
                        }
                    adb.add(db_anime)

                if db_anime["Episode"] < i["Episode"]:
                    for j in range(db_anime["Episode"]+1, i["Episode"]+1):
                        d = db_anime["Link"]
                        links = api.get_download_link(d, j)
                        thumb = downloader.DownLoadFile(links["thumb"], "thumb.png")
                        done = False
                        for count in range(5):
                            if done:
                                break
                            try:
                                await bot.send_message(LOGS_CHANNEL, f"Downloading: {i['Anime']} - {j} 360p")
                                file360 = downloader.DownLoadFile(links["360"], f"{i['Anime']} - {j} 360p.mkv")
                                await bot.send_message(LOGS_CHANNEL, f"Uploading: {i['Anime']} - {j} 360p")
                                res360 = await fast_upload(bot, file360)
                                link = await bot.send_message(
                                    FILES_CHANNEL,
                                    f"{i['Anime']} - {j} 360p",
                                    file=res360, 
                                    force_document=True,
                                    thumb=thumb,
                                    link_preview = False,
                                )
                                await bot.send_message(LINKS_CHANNEL, f"[{link_format.replace('[FILENAME]', link.file.name)}](t.me/{FILES_HIDER_BOT_USERNAME}?start=single_{FILES_CHANNEL}_{link.id})", link_preview = False)
                                os.remove(file360)
                                done = True

                            except:
                                err_str = traceback.format_exc()
                                await bot.send_message(LOGS_CHANNEL, f"Error while downloading \n`{i['Anime']} - {j} 360p`\n, Refer to the following Error Message\n\n\n{err_str}")    
                                asyncio.sleep(180)
                                links = api.get_download_link(d, j)
                                if count == 4:
                                    await bot.send_message(LOGS_CHANNEL, f"Error 5 times, skipping the episode and moving to next.")

                        done = False
                        for count in range(5):
                            if done:
                                break
                            try:
                                await bot.send_message(LOGS_CHANNEL, f"Downloading: {i['Anime']} - {j} 720p")
                                file720 = downloader.DownLoadFile(links["720"], f"{i['Anime']} - {j} 720p.mkv")
                                await bot.send_message(LOGS_CHANNEL, f"Uploading: {i['Anime']} - {j} 720p")
                                res720 = await fast_upload(bot, file720)
                                link = await bot.send_message(
                                    FILES_CHANNEL, 
                                    f"{i['Anime']} - {j} 720p", 
                                    file=res720, 
                                    force_document=True,
                                    thumb=thumb,
                                    link_preview = False,
                                )
                                await bot.send_message(LINKS_CHANNEL, f"[{link_format.replace('[FILENAME]', link.file.name)}](t.me/{FILES_HIDER_BOT_USERNAME}?start=single_{FILES_CHANNEL}_{link.id})", link_preview = False)
                                os.remove(file720)
                                done = True
                            except:
                                err_str = traceback.format_exc()
                                await bot.send_message(LOGS_CHANNEL, f"Error while downloading \n`{i['Anime']} - {j} 720`\n, Refer to the following Error Message\n\n\n{err_str}")
                                asyncio.sleep(180)
                                links = api.get_download_link(d, j)
                                if count == 4:
                                    await bot.send_message(LOGS_CHANNEL, f"Error 5 times, skipping the episode and moving to next.")

                        done = False
                        for count in range(5):
                            if done:
                                break                            
                            try:
                                await bot.send_message(LOGS_CHANNEL, f"Downloading: {i['Anime']} - {j} 1080p")
                                file1080 = downloader.DownLoadFile(links["1080"], f"{i['Anime']} - {j} 1080p.mkv")
                                await bot.send_message(LOGS_CHANNEL, f"Uploading: {i['Anime']} - {j} 1080p")
                                res1080 = await fast_upload(bot, file1080)
                                link = await bot.send_message(
                                    FILES_CHANNEL, 
                                    f"{i['Anime']} - {j} 1080p", 
                                    file=res1080,
                                    force_document=True,
                                    thumb=thumb,
                                    link_preview = False,
                                )
                                await bot.send_message(LINKS_CHANNEL, f"[{link_format.replace('[FILENAME]', link.file.name)}](t.me/{FILES_HIDER_BOT_USERNAME}?start=single_{FILES_CHANNEL}_{link.id})", link_preview = False)
                                os.remove(file1080)
                                done = True
                            except:
                                err_str = traceback.format_exc()
                                await bot.send_message(LOGS_CHANNEL, f"Error while downloading \n`{i['Anime']} - {j} 1080p`\n, Refer to the following Error Message\n\n\n{err_str}")
                                asyncio.sleep(180)
                                links = api.get_download_link(d, j)
                                if count == 4:
                                    await bot.send_message(LOGS_CHANNEL, f"Error 5 times, skipping the episode and moving to next.")


                        adb.modify(
                            {
                                "Anime": i["Anime"]
                            },
                            {
                                "Anime": i["Anime"],
                                "Episode": j,
                                "Link": i["Link"].split("-episode-")[0]
                            }
                        )

                    await bot.send_message(LOGS_CHANNEL, f"Uploaded: {i['Anime']} All New Episodes in all Resolutions")

        except:
            err_str = traceback.format_exc()
            await bot.send_message(LOGS_CHANNEL, f"Error!!! Most Likeley Token Expired, Please Refresh Them, if that does not work, Refer to the following Error Message\n\n\n{err_str}")    
            await bot.send_message(LOGS_CHANNEL, "Bot will Retry in 20 minutes, fix the error meanwhile....")

        await bot.send_message(LOGS_CHANNEL, f"Sleeping for 20 minutes then checking for updates again.")
        await asyncio.sleep(1200)

@bot.on(events.NewMessage(func=lambda e: e.is_private))
async def update_config(event):
    if event.file:
        if event.file.name.endswith(".json"):
            file = await event.download_media()
            with open(file) as f:
                data = json.load(f)
            os.remove(file)
            cdb.modify(
                {
                    "_id":"GogoAnime"
                },
                {
                    "_id":"GogoAnime",
                    "url": data[0]["domain"],
                    "gogoanime": data[0]["value"],
                    "auth": data[1]["value"]
                }
            )
            await event.reply("Config Parameters Updated Successfully")


loop.run_until_complete(checker_loop())

bot.start()

bot.run_until_disconnected()