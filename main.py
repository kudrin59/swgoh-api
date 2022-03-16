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


@client.event
async def on_ready():
    print("Бот запущен!")


@client.command()
async def help(ctx):
    emb = discord.Embed(title="Список команд", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
    emb.add_field(name='Сохранить ALLYCODE', value=f'{prefix}reg <<ALLY>>', inline=False)
    emb.add_field(name='Режим отображения', value=f'{prefix}mode <<pc/phone>>', inline=False)
    emb.add_field(name='Информация об игроке', value=f'{prefix}p <<ALLY>>', inline=False)
    emb.add_field(name='Сравнить игроков', value=f'{prefix}ga <<ALLY>> <<ALLY>>', inline=False)
    emb.add_field(name='Информация об гильдии', value=f'{prefix}g <<ALLY>>', inline=False)
    await ctx.send(embed=emb)


@client.command()
async def reg(ctx, ally=None):
    author = ctx.message.author
    author_id = ctx.message.author.id
    if not ally:
        emb = discord.Embed(colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value="Вы не указали <<ALLY>>, либо он некорректный!")
        await ctx.send(embed=emb)
        return False
    if func_bot.set_user_ally(author_id, ally):
        rez = "Ваш код изменён!"
    else:
        rez = "Ваш код сохранён!\nБыл установлен режим отображения: 'phone'"
    emb = discord.Embed(colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
    emb.add_field(name=author, value=rez)
    await ctx.send(embed=emb)


@client.command()
async def mode(ctx, platform=None):
    author = ctx.message.author
    author_id = ctx.message.author.id
    if not platform or platform != "pc" and platform != "phone":
        emb = discord.Embed(colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value="Вы не указали режим, либо он некорректный!")
        await ctx.send(embed=emb)
        return False
    if func_bot.set_user_mode(author_id, platform):
        emb = discord.Embed(colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value=f"Изменил свой режим на '{platform}'!")
    else:
        emb = discord.Embed(colour=discord.Colour.orange(), timestamp=datetime.datetime.utcnow())
        emb.add_field(name=author, value="Для этой функции необходимо зарегистрироваться ( !reg )!")
    await ctx.send(embed=emb)


@client.command()
async def p(ctx, ally=None):
    author = ctx.message.author
    author_id = ctx.message.author.id
    emb = discord.Embed(colour=discord.Colour.dark_gray(), timestamp=datetime.datetime.utcnow())
    emb.add_field(name=author, value="Выполнение команды...")
    msg = await ctx.send(embed=emb)
    emb.clear_fields()
    emb.colour = discord.Colour.red()
    if not ally:
        ally = func_bot.get_user_ally(author_id)
    if not ally:
        await msg.delete()
        emb.add_field(name=author, value="Вы не указали <<ALLY>>, либо он некорректный!")
        await ctx.send(embed=emb)
        return False
    try:
        mode = func_bot.get_user_mode(author_id)
        player_name, data = bridge.player_info(ally)
    except:
        emb.add_field(name=author, value="Возникла ошибка!")
    else:
        emb.colour = discord.Colour.green()
        emb.title = f'Информация об игроке: {player_name}'
        s = []
        for el in data:
            s.append(el[0])
            for pole in el[1]:
                if mode == 'pc':
                    add = ' ' * (30 - len(pole[0]))
                    s.append(f'{pole[0]} {add} {pole[1]}')
                else:
                    s.append(f'{pole[0]}: {pole[1]}')
        d = '```' + '\n'.join(s) + '```'
        emb.description = d
    finally:
        await msg.delete()
        await ctx.send(embed=emb)


@client.command()
async def ga(ctx, ally=None, ally2=None):
    author = ctx.message.author
    author_id = ctx.message.author.id
    emb = discord.Embed(colour=discord.Colour.dark_gray(), timestamp=datetime.datetime.utcnow())
    emb.add_field(name=author, value="Выполнение команды...")
    msg = await ctx.send(embed=emb)
    emb.clear_fields()
    emb.colour = discord.Colour.red()
    if not ally or not ally2:
        if not ally:
            ally = func_bot.get_user_ally(author_id)
        else:
            ally2 = func_bot.get_user_ally(author_id)
    if not ally or not ally2:
        await msg.delete()
        emb.add_field(name=author, value="Вы не указали <<ALLY>> <<ALLY>>, либо он некорректный!")
        await ctx.send(embed=emb)
        return False
    try:
        allys = [ally, ally2]
        mode = func_bot.get_user_mode(author_id)
        player_name, data = bridge.players_compare(allys)
    except:
        emb.add_field(name=author, value="Возникла ошибка!")
    else:
        emb.colour = discord.Colour.green()
        emb.title = f"Сравнение игроков: {player_name[0]} vs {player_name[1]}"
        s = []
        for el in data:
            s.append(el[0])
            for pole in el[1]:
                if mode == 'pc':
                    add = ' ' * (30 - len(pole[0]))
                    s.append(f'{pole[0]} {add} {pole[1]} VS {pole[2]}')
                else:
                    s.append(f'{pole[0]}: {pole[1]} VS {pole[2]}')
        d = '```' + '\n'.join(s) + '```'
        emb.description = d
    finally:
        await msg.delete()
        await ctx.send(embed=emb)


@client.command()
async def g(ctx, ally=None):
    author = ctx.message.author
    author_id = ctx.message.author.id
    emb = discord.Embed(colour=discord.Colour.dark_gray(), timestamp=datetime.datetime.utcnow())
    emb.add_field(name=author, value="Выполнение команды...")
    msg = await ctx.send(embed=emb)
    emb.clear_fields()
    emb.colour = discord.Colour.red()
    if not ally:
        ally = func_bot.get_user_ally(author_id)
    if not ally:
        await msg.delete()
        emb.add_field(name=author, value="Вы не указали <<ALLY>>, либо он некорректный!")
        await ctx.send(embed=emb)
        return False
    try:
        mode = func_bot.get_user_mode(author_id)
        guild_name, data = bridge.guild_info(ally)
    except:
        emb.add_field(name=author, value="Возникла ошибка!")
    else:
        emb.colour = discord.Colour.green()
        emb.title = f'Информация о гильдии: {guild_name}'
        s = []
        for el in data:
            s.append(el[0])
            for pole in el[1]:
                if mode == 'pc':
                    add = ' ' * (30 - len(pole[0]))
                    s.append(f'{pole[0]} {add} {pole[1]}')
                else:
                    s.append(f'{pole[0]}: {pole[1]}')
        d = '```' + '\n'.join(s) + '```'
        emb.description = d
    finally:
        await msg.delete()
        await ctx.send(embed=emb)


TOKEN = open('token.txt', 'r').readline()
client.run(TOKEN)
