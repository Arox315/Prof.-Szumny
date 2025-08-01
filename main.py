import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

from message_handler import MesssageHandler
from translator import Translator


load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

translator = Translator(locale_folder='localization', default_language='pl')
message_handler = MesssageHandler(translator=translator)

GUILD_ID = int(os.getenv('GUILD_ID'))


@bot.event
async def on_ready():
    guild_obj = discord.Object(id=GUILD_ID)

    # bot.tree.clear_commands(guild=None)               
    # bot.tree.clear_commands(guild=guild_obj)          

    # bot.tree.remove_command("lang", type=discord.AppCommandType.chat_input, guild=None)      
    # bot.tree.remove_command("lang", type=discord.AppCommandType.chat_input, guild=guild_obj) 

    # await bot.tree.sync(guild=None)                
    # await bot.tree.sync(guild=guild_obj) 
    
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} global command(s)")
    print(f'Logged in as: {bot.user.name} - ID: {bot.user.id}')
    print('------')


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Ignore bot commands
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return
    
    # Check if the message language is supported
    is_lang_supported = await message_handler.is_message_language_supported(message)

    if not is_lang_supported:
        unknown_response = await message_handler.handle_unknown_message(message)
        if unknown_response:
            await message.reply(unknown_response)
        return
    
    # Check if the bot can respond based on cooldown
    can_respond = await message_handler.can_respond()
    if not can_respond:
        return
    
    # Generate a response if the bot is ready to respond
    async with message.channel.typing():
        response = await message_handler.generate_response(message)
        if not response:
            return
        await message.reply(response)
    
    
@bot.command()
async def ping(ctx):
    """A simple command to check if the bot is online."""
    await ctx.send("Pong!")


# command for changing the language
@bot.tree.command(
    name='lang',
    description="Change the language in which the bot will respond.",
)

@app_commands.describe(language="Target language code")
async def change_language(interaction: discord.Interaction, language: str):
    try:
        await translator.set_language(language)
        await message_handler.change_language(language)

        embed = discord.Embed(
            title=translator.discord["success"],
            description=translator.translator['language_changed'].format(
                language=translator.languages[language]
            ),
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except ValueError as err:
        embed = discord.Embed(
            title=translator.discord["error"],
            description=str(err),
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

@change_language.autocomplete("language")
async def change_language_autocomplete(
    interaction: discord.Interaction, current: str
):
    options = [
        discord.app_commands.Choice(name=name, value=name) 
        for name in translator.translations.keys() 
        if current.lower() in name.lower() 
    ]
    return options



# class MyView(discord.ui.View):
#     async def on_timeout(self) -> None:
#         # Step 2
#         for item in self.children:
#             item.disabled = True

#         # Step 3
#         await self.message.edit(view=self)

#     @discord.ui.button(label='Example')
#     async def example_button(self, interaction: discord.Interaction, button: discord.ui.Button):
#         await interaction.response.send_message('Hello!', ephemeral=True)

# @bot.command()
# async def timeout_example(ctx):
#     """An example to showcase disabling buttons on timing out"""
#     view = MyView()
#     # Step 1
#     view.message = await ctx.send('Press me!', view=view)


if __name__ == "__main__":
    if not DISCORD_TOKEN:
         raise ValueError("DISCORD_TOKEN is not set in the environment variables.")
    bot.run(DISCORD_TOKEN)