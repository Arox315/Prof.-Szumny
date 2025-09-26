# About the bot
A simple discord bot that uses LLM to create random responses in a form of comprehensive description on a topic to the keyword in users' messages.
By default the bot supports Polish and English languages.
The bot responds to random eligible messages in an interval. Every setting can be changed in a config file or via bot's commands.

# Requirements
- Valid [OpenAI API](https://platform.openai.com/docs/overview) key 
- [Discord bot](https://discord.com/developers)
- Polish and English Hunspell dictionaries. Can be obtained from [LibreOffice dictionaries](https://github.com/LibreOffice/dictionaries)

# Setup
1. Copy the repository `git clone https://github.com/Arox315/Prof.-Szumny.git`
2. Download required modules from `requirements.txt` by running a command: `pip install -r requirements.txt`
3. Create a `.env` file containing two variables: `DISCORD_TOKEN` and `OPENAI_API_KEY`
4. Download required Hunspell dictionaries. Copy `.dic` and `.aff` files into folder `/path/to/enchant/data/mingw<bits>/enchant/share/hunspell`. For more help follow the [instructions](https://pyenchant.github.io/pyenchant/install.html)
5. Run `main.py` file
6. In discord setup bot to your liking with commands. In a text channel run `/help` to see what commands the bot has to offer

## Adding new language
To add new language download desired language's Hunspell dictionary then:
* In `localization` folder create new `.json` file named by a language code e.g. `de.json` for Geramn. Copy the contents of an existing localization file and translate it to desired language.
* Afterwards, in the same folder create `prompt_<language-code>.txt` (e.g. `prompt_de.txt`) file with a initial prompt for the LLM. You can copy the contents of an existing localization prompt and translate it to desired language.
* In discord run `/lang` command to set the new language.
