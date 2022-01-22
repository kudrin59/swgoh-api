import discord
from discord.ext import commands

import bridge
import func_bot
from bridge import *
from func_bot import *

prefix = '!'
client = commands.Bot(command_prefix=prefix)
client.remove_command('help')

users = func_bot.load_users()


@client.event
async def on_ready():
    print("Бот запущен!")


@client.command()
async def help(ctx):
    emb = discord.Embed()

    emb.add_field(name='{}reg <<ALLY>>'.format(prefix), value='Сохранить ALLYCODE')
    emb.add_field(name='{}p <<ALLY>>'.format(prefix), value='Информация об игроке')
    emb.add_field(name='{}ga <<ALLY>> <<ALLY>>'.format(prefix), value='Сравнить игроков')
    await ctx.send(embed=emb)


@client.command()
async def reg(ctx, ally=None):
    global users
    info = "Сохранить ALLYCODE: !reg <<ALLY>>"
    author = ctx.message.author
    author_id = ctx.message.author.id

    if not ally:
        await ctx.send(f'{author.mention} {info}\n')
        return False

    rez = ""
    create = True

    for user in users:
        if user[0] == str(author_id):
            user[1] = ally
            rez = "Код перезаписан!"
            create = False
            break

    if create:
        user = [author_id, ally]
        users.append(user)
        rez = "Код сохранён!"

    func_bot.save_users(users)
    await ctx.send(f'{author.mention}\n'
                   f'{rez}\n')


@client.command()
async def p(ctx, ally=None):
    info = "Информация об игроке: !p <<ALLY>>"
    author = ctx.message.author
    author_id = ctx.message.author.id

    if not ally:
        ally = func_bot.get_user_ally(author_id, users)
    if not ally:
        await ctx.send(f'{author.mention} {info}\n')
        return False

    date = bridge.player_info(ally)
    await ctx.send(f'{author.mention}\n'
                   f'{date}')


@client.command()
async def ga(ctx, ally=None, ally2=None):
    info = "Сравнить игроков: !ga <<ALLY>> <<ALLY>>"
    author = ctx.message.author
    author_id = ctx.message.author.id

    if not ally or not ally2:
        if not ally:
            ally = func_bot.get_user_ally(author_id, users)
        else:
            ally2 = func_bot.get_user_ally(author_id, users)

    if not ally or not ally2:
        await ctx.send(f'{author.mention} {info}\n')
        return False

    allys = [ally, ally2]

    date = bridge.players_vs(allys)
    await ctx.send(f'{author.mention}\n'
                   f'{date}')


TOKEN = open('token.txt', 'r').readline()
client.run(TOKEN)
