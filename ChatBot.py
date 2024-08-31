import random
from twitchio.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token='Your-TOKEN-HERE',   #get u tocken here  https://twitchapps.com/tmi/
            prefix='!', #Change it to the prefix you want to use or leave it without prefix
            initial_channels=['channel-name'] #Put the channel name where the bot will work
        )
        #Here you can add more commands and use them
        self.responses = {    
            'hi': 'Hello {user}, :D',
            'bye': 'Bye {user}, :D',
        }

    async def event_ready(self):
        print(f'Bot connected as {self.nick}')

    async def event_message(self, message):
        if message.author.name.lower() == self.nick.lower():
            return

        response_template = self.responses.get(message.content.lower())
        if response_template:
            if callable(response_template):
                response = response_template(message.author.name)
            else:
                response = response_template.format(user=message.author.name)
            await message.channel.send(response)

        await self.handle_commands(message)

    @commands.command(name='ban')  #ban, you can delete it if you want
    async def ban_command(self, ctx, user: str):
        if ctx.author.is_mod:
            await ctx.channel.ban(user)
            await ctx.send(f'Banned {user}')
        else:
            await ctx.send('You do not have permission to use this command.')

    @commands.command(name='timeout') #timeout, you can delete it if you want 
    async def timeout_command(self, ctx, user: str, duration: int):
        if ctx.author.is_mod:
            await ctx.channel.timeout(user, duration)
            await ctx.send(f'{user} has been timed out for {duration} seconds.')
        else:
            await ctx.send('You do not have permission to use this command.')

    def get_random_advice(self, user):
        advice = random.choice(self.advice_list)
        return f'{self.nick} says: {advice}'


bot = Bot()
bot.run()
