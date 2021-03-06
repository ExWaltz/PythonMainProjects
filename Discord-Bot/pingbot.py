import discord
import ytvids
import os
import asyncio
import json


client = discord.Client()

with open('config', 'r', encoding='UTF-8') as variables:
    jsn_variables = json.loads(variables.read())
    TOKEN = jsn_variables.get('token')
    YT_CHANNEL = jsn_variables.get('youtubeChannel')
    DS_CHANNEL = jsn_variables.get('discordChannel')

async def _write_to_file(list_vid, dict_vid, key_vid, val_vid):
    dict_vid[key_vid] = val_vid
    list_vid.seek(0)
    list_vid.write(json.dumps(dict_vid))
    list_vid.truncate()

async def _is_data_exist(vid_key, vid_data, file_name):
    with open(file_name, 'r+', encoding="utf-8") as vid_list_file:
        vid_dict = json.loads(vid_list_file.read())
        vid_type = vid_dict.get(vid_key)

        # Send a notification again, when the upcoming stream becomes live
        # Don't send notification if the stream becomes a normal video
        if vid_type is not None and vid_data[5] != vid_type[5] and vid_data != "DEFAULT":
            await _write_to_file(vid_list_file, vid_dict, vid_key, vid_data)
            return True

        # Check if the video is already in the listed videos
        if vid_dict.get(vid_key) is None:
            await _write_to_file(vid_list_file, vid_dict, vid_key, vid_data)
            return True

        return False

async def _get_vids():
    while True:
        if str(YT_CHANNEL).endswith("/"): YT_CHANNEL = YT_CHANNEL[:-1]
        real_path = os.path.dirname(os.path.realpath(__file__))
        if os.path.isdir(f'{real_path}/vid_list'): os.mkdir(f'{real_path}/vid_list')
        file_name = f"{real_path}/vids_list/{str(YT_CHANNEL).split('/')[-1]}.json"
        vids = ytvids.videos(YT_CHANNEL)
        if not os.path.isfile(file_name):
            with open(file_name, 'w', encoding="utf-8") as vid_list_file:
                vid_list_file.write(json.dumps(vids))
        upcoming = ytvids.upcoming(YT_CHANNEL)
        livestreams = ytvids.livestream(YT_CHANNEL)
        comp_vids = {}
        if vids: comp_vids.update(vids)
        if livestreams: comp_vids.update(livestreams)
        if upcoming: comp_vids.update(upcoming)
        discord_channel = client.get_channel(DS_CHANNEL)
        for key, val in comp_vids.items():
            check_data = await _is_data_exist(key, val, file_name)
            if check_data:
                await discord_channel.send(f"New Video: {val[0]}\nLink: {key}\nTime: {val[1]}\nViews: {val[2]}\nDuration: {val[3]}\nThumbnail: {val[4]}")
        await asyncio.sleep(1)

@client.event
async def on_ready():
    print('Bot is Ready')
    client.loop.create_task(_get_vids())

# client.run(TOKEN)

# Using .env technique
client.run(os.getenv("TOKEN"))
