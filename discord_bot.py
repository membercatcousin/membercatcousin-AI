import discord
from bootstrap.responses_loader import load_all_data, load_settings
from bootstrap.on_start import get_prefix
from bootstrap.engine import process_input

# Load everything from files
vibe_data, legacy_data = load_all_data()
settings = load_settings()
bot_conf = settings.get('bot_settings', {})

# Extract values from YAML
TOKEN = bot_conf.get('bot_token')
PREFIX = bot_conf.get('prefix')
STATUS = bot_conf.get('status', "membercatcousin's AI")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=STATUS))
    print(f"Logged in as {client.user} | Prefix: {PREFIX}")

@client.event
async def on_message(message):
    if message.author == client.user: return

    if message.content.lower().startswith(PREFIX):
        query = message.content[len(PREFIX):].strip()
        response = process_input(query, vibe_data, legacy_data)
        await message.channel.send(f"{get_prefix()}{response}")

if __name__ == "__main__":
    if not TOKEN or TOKEN == 'BOT_TOKEN_HERE':
        print("ERROR: Missing bot_token in settings.yml")
    else:
        client.run(TOKEN)
