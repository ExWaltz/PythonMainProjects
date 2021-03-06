# Discord Ping Bot
This discord bot will send a message to a specified discord channel on any activity a channel has done.

# Configure the Bot
To configure this bot you can either edit the source code or change the variables on the `config` file.
On the `config` file, there are 3 variables; `token`, `youtubeChannel`, and `discordChannelID`.

## WARNING
DO NOT SHARE THE `config` FILE WITH ANYONE
The most dangerous part of this `config` file is the `token`.
If someone managed to get the token they would be able to take over the bot
and potentially cause damage to your server.
For other secure ways please go to [Tips and Tricks](#Tips-and-Tricks)

I WILL NOT BE RESPONSIBLE FOR YOUR CARELESSNESS

PLEASE REGENERATE THE TOKEN IF YOU SHARED THE CONFIG FILE
![Regenerate Token](https://i.imgur.com/esXmrEr.png)


## token 
The `token` variable will be the Token given when making a discord bot at [Discord Developer Portal](https://discord.com/developers/applications)
![A picture of copying the TOKEN from the discord bot](https://i.imgur.com/lsV4c9J.png)

## youtubeChannel
The `youtubeChannel` variable will be the Youtube channel link

### Examples of VALID links
- https://www.youtube.com/channel/XXXXXXXXXXXXX
- https://www.youtube.com/c/XXXXXXXXXXXXXX
- http://www.youtube.com/channel/XXXXXXXXXXXXX
- http://www.youtube.com/c/XXXXXXXXXXXXXX
- youtube.com/channel/XXXXXXXXXXXXXX
- youtube.com/c/XXXXXXXXXXXXXX

### Examples of NON valid links
- https://youtube.com/channel/XXXXXXXXXXX/XXXXXXXXX
- https://youtube.com/c/XXXXXXXXX/XXXXXXX
- http://youtube.com/channel/XXXXXXXXXXX/XXXXXXXXX
- http://youtube.com/c/XXXXXXXXX/XXXXXXX
- youtube.com/channel/XXXXXXXXXXX/XXXXXXXXX
- youtube.com/c/XXXXXXXXX/XXXXXXX
- youtube.com/channel/XXXXXXXXXXX?XX=XX
- youtube.com/c/XXXXXXXXXXX?XX=XX

## discordChannelID
The `discordChannelID` variable will be the discord channel ID.
You can take the discord channel ID by turning ON the developer settings on Discord
![Discord Settings > Appearance > Developer Mode](https://i.imgur.com/eFfNC47.png)
After this `Right Click` a channel and `Click` the `Copy ID`
![Hover over Discord Channel > Right Click > Click "Copy ID"](https://i.imgur.com/fOY8keT.png)

# Tips and Tricks
Depending on the hosting service; you can create a `.env` file to store your discord bot token.

On the `.env` file add the following line:
`TOKEN=<TOKEN>`
Insert the `token` variable on to the `<TOKEN>` part

The `.env` will not be visible to some hosting website, hiding your token from other people
If you follow this tip, then uncomment the last in the `pingbot.py` file and comment the `client.run(TOKEN)` line
![Change the last line and comment the 4th to the last line](https://i.imgur.com/VBsERF4.png)
