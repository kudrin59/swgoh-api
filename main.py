import datetime

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
    emb = discord.Embed(title="Список комманд", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())

    emb.add_field(name='Сохранить ALLYCODE', value=f'{prefix}reg <<ALLY>>', inline=False)
    emb.add_field(name='Режим отображения', value=f'{prefix}mode <<pc/phone>>', inline=False)
    emb.add_field(name='Информация об игроке', value=f'{prefix}p <<ALLY>>', inline=False)
    emb.add_field(name='Сравнить игроков', value=f'{prefix}ga <<ALLY>> <<ALLY>>', inline=False)
    await ctx.send(embed=emb)


@client.command()
async def reg(ctx, ally=None):
    global users
    author = ctx.message.author
    author_id = ctx.message.author.id

    if not ally:
        emb = discord.Embed(colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value="Вы не указали <<ALLY>>, либо он некорректный!")
        await ctx.send(embed=emb)
        return False

    if func_bot.set_user_ally(users, author_id, ally):
        rez = "Ваш код перезаписан!"
    else:
        rez = "Ваш код сохранён!"

    emb = discord.Embed(colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
    emb.add_field(name=author, value=rez)
    await ctx.send(embed=emb)


@client.command()
async def mode(ctx, platform=None):
    global users
    author = ctx.message.author
    author_id = ctx.message.author.id

    if not platform or platform != "pc" and platform != "phone":
        emb = discord.Embed(colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value="Вы не указали режим, либо он некорректный!")
        await ctx.send(embed=emb)
        return False

    if func_bot.set_user_mode(users, author_id, platform):
        emb = discord.Embed(colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value=f"Изменил свой режим на '{platform}'!")
    else:
        emb = discord.Embed(colour=discord.Colour.orange(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value="Для этой функции необходимо зарегистрироваться ( !reg )!")

    await ctx.send(embed=emb)


@client.command()
async def p(ctx, ally=None):
    global users
    author = ctx.message.author
    author_id = ctx.message.author.id

    if not ally:
        ally = func_bot.get_user_ally(author_id, users)

    if not ally:
        emb = discord.Embed(colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value="Вы не указали <<ALLY>>, либо он некорректный!")
        await ctx.send(embed=emb)
        return False

    try:
        mode = func_bot.get_user_mode(author_id, users)
        player_name, data = bridge.player_info(ally, mode)
    except:
        emb = discord.Embed(colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value="Возникла ошибка!")
    else:
        emb = discord.Embed(title=f"Информация об игроке: {player_name}", colour=discord.Colour.green(),
                            timestamp=datetime.datetime.utcnow())
        for el in data:
            if mode == "pc":
                if len(el) > 2:
                    emb.add_field(name=el[0], value=el[1])
                    temp_str = "::\n" * el[2].count('\n')
                    emb.add_field(name="\u200b", value=temp_str, inline=True)
                    emb.add_field(name="\u200b", value=el[2], inline=True)
                else:
                    emb.add_field(name=el[0], value=el[1], inline=False)
            else:
                emb.add_field(name=el[0], value=el[1], inline=False)
    finally:
        await ctx.send(embed=emb)


@client.command()
async def ga(ctx, ally=None, ally2=None):
    global users
    author = ctx.message.author
    author_id = ctx.message.author.id

    if not ally or not ally2:
        if not ally:
            ally = func_bot.get_user_ally(author_id, users)
        else:
            ally2 = func_bot.get_user_ally(author_id, users)

    if not ally or not ally2:
        emb = discord.Embed(colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value="Вы не указали <<ALLY>> <<ALLY>>, либо они некорректны!")
        await ctx.send(embed=emb)
        return False

    allys = [ally, ally2]

    try:
        mode = func_bot.get_user_mode(author_id, users)
        player_name, data = bridge.players_compare(allys, mode)
    except:
        emb = discord.Embed(colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value="Возникла ошибка!")
    else:
        emb = discord.Embed(title=f"Сравнение игроков: {player_name[0]} vs {player_name[1]}", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())

        for el in data:
            if mode == "pc":
                emb.add_field(name=el[0], value=el[1])
                emb.add_field(name="\u200b", value=el[2], inline=True)
                emb.add_field(name="\u200b", value=el[3], inline=True)
            else:
                emb.add_field(name=el[0], value=el[1], inline=False)
    finally:
        await ctx.send(embed=emb)


TOKEN = open('token.txt', 'r').readline()
client.run(TOKEN)
