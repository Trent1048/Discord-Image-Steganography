import discord
import json

# read the user info file:
with open("./user_info.json", "r") as user_info_json:
    user_info = json.load(user_info_json)

# create the discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# define the message sending function
@client.event
async def on_ready():
    user = await client.fetch_user(user_info["user_id"])
    await user.send("This is a test automated message (from Trent)")

# run the client
client.run(user_info["bot_id"])