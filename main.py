import discord
from discord.ext import commands

import bridge
from bridge import *

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print("Бот запущен!")


@client.command()
async def h(ctx, arg=None):
    author = ctx.message.author
    await ctx.send(f'{author.mention}\n'
                   'Информация об игроке: !p <<ALLY>>\n'
                   'Сравнить игроков: !ga <<ALLY>> <<ALLY>>')


@client.command()
async def p(ctx, ally):
    author = ctx.message.author
    if len(ally) > 0 and ally.isdigit():
        date = bridge.player_info(ally)
        await ctx.send(f'{author.mention}\n'
                       f'{date}')
    else:
        await ctx.send(f'{author.mention}\n'
                       'Информация об игроке: !p <<ALLY>>\n')


@client.command()
async def ga(ctx, ally, ally2):
    author = ctx.message.author
    if len(ally) > 0 and ally.isdigit() and len(ally2) > 0 and ally2.isdigit():
        allys = [ally, ally2]
        date = bridge.players_vs(allys)
        await ctx.send(f'{author.mention}\n'
                       f'{date}')
    else:
        await ctx.send(f'{author.mention}\n'
                       'Сравнить игроков: !ga <<ALLY>> <<ALLY>>\n')

TOKEN = open('token.txt', 'r').readline()
client.run(TOKEN)
