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

#TODO: Add commands to set and remove allowed channels for the bot to respond in ✔️
#TODO: Add minimum message length, cooldown time, and allowed channels to info command
#TODO: Add those settings to the config file
#TODO: Add a command to reset the bot's settings to default values
#TODO: Add a help command that lists all commands and their descriptions


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Ignore bot commands
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return
    
    # Check if message is on allowed channel
    if not await message_handler.is_channel_allowed(message.channel.name):
        print(f"Ignored message from {message.author.name} in {message.channel.name}: {message.content} - Channel not allowed")
        return

    # Check if the bot can respond based on cooldown
    if not await message_handler.can_respond():
        return

    # Check the length of the message
    if not await message_handler.is_message_length_valid(message):
        print(f"Ignored message from {message.author.name} in {message.channel.name}: {message.content} - Too short")
        return

    # Check if the message language is supported
    if not await message_handler.is_message_language_supported(message):
        if unknown_response := await message_handler.handle_unknown_message(message):
            await message.reply(unknown_response)
        return
    
    # Generate a response if the bot is ready to respond
    async with message.channel.typing():
        if response := await message_handler.generate_response(message):
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


# command for changing the model
@bot.tree.command(
    name='model',
    description="Change the model used by the bot."
)

@app_commands.describe(model="Target model name")
async def change_model(interaction: discord.Interaction, model: str):
    try:
        await message_handler.change_model(model)

        embed = discord.Embed(
            title=translator.discord["success"],
            description=translator.translator['model_changed'].format(
                model=model
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

@change_model.autocomplete("model")
async def change_model_autocomplete(
    interaction: discord.Interaction, current: str
):
    options = [
        discord.app_commands.Choice(name=model, value=model) 
        for model in message_handler.message_bot.model.get_all_models() 
        if current.lower() in model.lower()
    ]
    return options


# command to get information about the bot
@bot.tree.command(
    name='info',
    description="Get information about the bot."
)
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title=translator.discord["bot_info"],
        color=discord.Color.blue()
    )
    embed.add_field(name=translator.discord["info_language_header"], value=translator.languages[message_handler.message_bot.language], inline=False)
    embed.add_field(name=translator.discord["info_model_header"], value=message_handler.message_bot.model.value, inline=False)
    embed.add_field(name=translator.discord["info_cooldown"], value=message_handler.message_cooldown, inline=False)
    embed.add_field(name=translator.discord["info_minimum_message_length"], value=message_handler.minimum_message_length, inline=False)
    #embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(
    name='min_mess_length',
    description="Set the minimum message length (in words) for the bot to respond."
)
async def set_min_message_length(interaction: discord.Interaction, length: int):
    try:
        await message_handler.set_minimum_message_length(length)
        embed = discord.Embed(
            title=translator.discord["success"],
            description=translator.translator['min_message_length_changed'].format(length=length),
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


@bot.tree.command(
    name='cooldown',
    description="Set the cooldown time (in seconds) between bot responses."
)
async def set_message_cooldown(interaction: discord.Interaction, cooldown: float):
    try:
        await message_handler.set_message_cooldown(cooldown)
        embed = discord.Embed(
            title=translator.discord["success"],
            description=translator.translator['cooldown_changed'].format(cooldown=cooldown),
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


@bot.tree.command(
    name='add_channel',
    description="Add channel to the list of allowed channels the bot can respond in."
)
async def add_allowed_channel(interaction: discord.Interaction, channel_name: str):
    try:
        await message_handler.add_allowed_channel(channel_name)
        embed = discord.Embed(
            title=translator.discord["success"],
            description=translator.translator['allowed_channel_added'].format(channel=channel_name),
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


@bot.tree.command(
    name='remove_channel',
    description="Remove channel from the list of allowed channels the bot can respond in."
)
async def remove_allowed_channel(interaction: discord.Interaction, channel_name:str):
    try:
        await message_handler.remove_allowed_channel(channel_name)
        embed = discord.Embed(
            title=translator.discord["success"],
            description=translator.translator['allowed_channel_removed'].format(channel=channel_name),
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


@bot.tree.command(
    name='clear_channels',
    description="Clear all channels from the list of allowed channels."
)
async def clear_allowed_channels(interaction: discord.Interaction):
    await message_handler.clear_allowed_channels()
    embed = discord.Embed(
        title=translator.discord["channels_clear_info"],
        description=translator.translator['allowed_channels_cleared'],
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
    

@bot.tree.command(
    name='list_channels',
    description="List all allowed channels."
)
async def list_allowed_channels(interaction: discord.Interaction):
    channels = await message_handler.get_allowed_channels()
    if channels:
        embed=discord.Embed(
            title=translator.discord['channels_list'],
            description="\n".join(channel for channel in channels),
            color=discord.Color.blue()
        )
    else:
        embed=discord.Embed(
            title=translator.discord['channels_list'],
            description=translator.translator['channels_list_empty'],
            color=discord.Color.blue()
        )
    await interaction.response.send_message(embed=embed, ephemeral=True)


# embed = discord.Embed(
#         title=translator.discord["bot_info"],
#         color=discord.Color.blue()
#     )
#     embed.add_field(name=translator.discord["info_language_header"], value=translator.languages[message_handler.message_bot.language], inline=True)
#     embed.add_field(name=translator.discord["info_model_header"], value=message_handler.message_bot.model.value, inline=True)

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