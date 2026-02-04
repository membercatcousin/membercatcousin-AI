import discord
from bootstrap.responses_loader import load_all_data, load_settings
from bootstrap.on_start import get_prefix
from bootstrap.engine import process_input
# Import the new real exceptions so we can catch them
from bootstrap.exceptions import TopicBlockedException, ResponseNotAvailableException

# --- INITIALIZATION ---
# Load data and settings
vibe_data, legacy_data = load_all_data()
settings = load_settings()
bot_conf = settings.get('bot_settings', {})

# Extract values from YAML
TOKEN = bot_conf.get('bot_token')
PREFIX = bot_conf.get('prefix', '!ai')
STATUS = bot_conf.get('status', "membercatcousin's AI")

# Setup Discord Intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=STATUS))
    print(f"--- Discord Mode Active ---")
    print(f"Logged in as: {client.user}")
    print(f"Prefix: {PREFIX}")
    print(f"---------------------------")

@client.event
async def on_message(message):
    # Prevent bot from talking to itself
    if message.author == client.user:
        return

    # Check if the bot was mentioned OR the prefix was used
    is_mentioned = client.user.mentioned_in(message) and not message.mention_everyone
    starts_with_prefix = message.content.lower().startswith(PREFIX)

    if starts_with_prefix or is_mentioned:
        # 1. Clean the Input
        if starts_with_prefix:
            # Remove prefix
            query = message.content[len(PREFIX):].strip()
        else:
            # Remove mentions (both <@ID> and <@!ID> formats)
            query = message.content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip()

        # Handle empty messages (e.g. just a ping)
        if not query:
            await message.channel.send(f"{get_prefix()}System online. Waiting for input...")
            return

        # 2. Process Input with Error Handling
        try:
            # The Engine might raise an exception now!
            response = process_input(query, vibe_data, legacy_data, settings)

            # If successful, send the response
            await message.channel.send(f"{get_prefix()}{response}")

        except TopicBlockedException as e:
            # Catch the Security Error (Layer 0)
            # Sends the error in a code block ` ` for the "System Error" look
            await message.channel.send(f"{get_prefix()}⛔ **SECURITY ALERT**\n`{e}`")

        except ResponseNotAvailableException as e:
            # Catch the Not Found Error (Fallback)
            await message.channel.send(f"{get_prefix()}⚠️ **SYSTEM EXCEPTION**\n`{e}`")

        except Exception as e:
            # Catch any actual bugs in the code
            print(f"CRITICAL ERROR: {e}")
            await message.channel.send(f"{get_prefix()}🔥 **CRITICAL FAILURE**\n`UnexpectedError: {e}`")

if __name__ == "__main__":
    if not TOKEN or TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("ERROR: Missing bot_token in settings.yml")
    else:
        client.run(TOKEN)
