import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from message_handler import MesssageHandler

# Load environment variables from .env file
load_dotenv()

# Get the Discord token from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent


bot = commands.Bot(command_prefix='/', intents=intents)

message_handler = MesssageHandler()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    is_lang_supported = await message_handler.is_message_language_supported(message)
    if is_lang_supported:
        async with message.channel.typing():
            response = await message_handler.handle_message(message)
            await message.reply(response)


@bot.command(name='hello', description='Sends a greeting message')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}!')


@bot.command()
async def wave(ctx, to: discord.User = commands.Author):
    await ctx.send(f'Hello {to.mention} :wave:')



if __name__ == "__main__":
    if not DISCORD_TOKEN:
         raise ValueError("DISCORD_TOKEN is not set in the environment variables.")
    bot.run(DISCORD_TOKEN)