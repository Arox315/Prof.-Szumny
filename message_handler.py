class MesssageHandler:
    message_cooldown = 5.0  # in seconds
    
    
    def __init__(self, client):
        self.client = client


    async def handle_message(self, message):
        if message.author == self.client.user:
            return
        
        if message.content.startswith('!hello'):
            await message.channel.send(f'Hello {message.author.name}!')
        elif message.content.startswith('!help'):
            await message.channel.send('Available commands: !hello, !help')
        else:
            await message.channel.send('Unknown command. Type !help for assistance.')
    

    