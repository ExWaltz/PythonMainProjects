import discord
import chnlvids
import os
import asyncio
import json


client = discord.Client()

with open('config', 'r', encoding='utf-8') as config_var:
    jsn_variables = json.loads(config_var.read())
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
            print('Video Type changed')
            await _write_to_file(vid_list_file, vid_dict, vid_key, vid_data)
            return True

        # Check if the video is already in the listed videos
        if vid_dict.get(vid_key) is None:
            print('New Video')
            await _write_to_file(vid_list_file, vid_dict, vid_key, vid_data)
            return True

        return False

async def _embed_message(vid_link, vid_title, upload_date, views, duration, thumbnail, status, chnl_name, chnl_avatar):
    embed_color = discord.Colour.red()
    view_text = "Viewers"
    view_val = f"{views} {duration}"
    default_description = f"{chnl_name} is now LIVE NOW! Go watch it on Youtube!"
    embed = discord.Embed(title = vid_title)

    if status == "UPCOMING": 
        embed_color = discord.Colour.purple()
        default_description = f"{chnl_name} is going live at {upload_date} on Youtube!"

    elif status == "DEFAULT":
        embed_color = discord.Colour.blue()
        view_text = "VIEWS"
        view_val = f"{views}"
        default_description = f"{chnl_name} uploaded a new video at {upload_date} on Youtube!"
        embed.add_field(name = "Duration", value = duration)

    embed.color = embed_color
    embed.description = default_description
    embed.url = vid_link
    embed.set_author(name = chnl_name, url = YT_CHANNEL, icon_url = chnl_avatar)
    embed.add_field(name = "Date", value = upload_date, inline = False)
    embed.add_field(name = view_text, value = view_val)
    embed.set_thumbnail(url = chnl_avatar)
    embed.set_image(url = thumbnail)
    return embed

async def _get_vids():
    while True:
        youtube_channel = YT_CHANNEL
        discord_channel = client.get_channel(DS_CHANNEL)

        # Get the channel ID
        if str(YT_CHANNEL).endswith("/"): youtube_channel = YT_CHANNEL[:-1]
        real_path = os.path.dirname(os.path.realpath(__file__))
        if os.path.isdir(f'{real_path}/vid_list'): os.mkdir(f'{real_path}/vid_list')
        file_name = f"{real_path}/vids_list/{str(youtube_channel).split('/')[-1]}.json"
        vids = chnlvids.videos(youtube_channel)

        # Writes down past videos to prevent old videos from being sent
        if not os.path.isfile(file_name):
            # Store all old videos in vids_list/file_name.json
            print('Making a new file for new channel')
            with open(file_name, 'w', encoding="utf-8") as vid_list_file:
                vid_list_file.write(json.dumps(vids))

        upcoming = chnlvids.upcoming(youtube_channel)     # Get Upcoming Videos
        livestreams = chnlvids.livestream(youtube_channel)    # Get livestreams
        comp_vids = {}
        # Combine all the results
        if vids: comp_vids.update(vids)
        if livestreams: comp_vids.update(livestreams)
        if upcoming: comp_vids.update(upcoming)
        for key, val in comp_vids.items():
            check_data = await _is_data_exist(key, val, file_name)
            if check_data:
                # check_data structure
                # { "VIDEO_LINK" : [ "VIDEO_TITLE", "VIDEO_TIME", "VIDEO_VIEWS", "VIDEO_DURATION", "VIDEO_THUMBNAIL", "VIDEO_STATUS", "CHANNEL_NAME, CHANNEL_PROFILE_IMG"]}
                # VIDEO_STATUS has 3 possible values; "UPCOMING", "LIVE", and "DEFAULT"
                # UPCOMING will eventually change into LIVE
                # LIVE will eventrually turn into DEFAULT

                print('Sending Youtube Update Message')
                embed_message = await _embed_message(key, val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7])
                await discord_channel.send(embed = embed_message)
                # await discord_channel.send(f"New Video: {val[0]}\nLink: {key}\nTime: {val[1]}\nViews: {val[2]}\nDuration: {val[3]}\nThumbnail: {val[4]}")
        # Frequency of updates in second
        await asyncio.sleep(0.5)

@client.event
async def on_ready():
    print('Bot is Ready')
    client.loop.create_task(_get_vids())

client.run(TOKEN)

# Using .env technique
# client.run(os.getenv("TOKEN"))
