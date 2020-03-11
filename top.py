import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import asyncio
import token

PREFIX = '!'

bad_words = [ 'уёбок', 'маму ебал', 'еблан', 'сервер говно', ' админ еблан' ]

client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

@client.event
async def on_ready():
    print( 'Аннабелль покдлючилась' )

    await client.change_presence( status = discord.Status.online, activity = discord.Game( 'Разъёб серверов' ) )

@client.event
async def on_command_error(ctx, error):
	pass


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},Данной команды не существует.**', color=0x0c0c0c))

@client.event
async def on_message(message):

    await client.process_commands(message)

    if 'discord.gg' in message.content.lower():
        await message.delete()
        await message.channel.send(embed = discord.Embed(description = f'{message.author}, реклама запрещена.',color=0x0c0c0c)) 
        return
#тут один пробел вместо таба

# Clear message
@client.command()
@commands.has_permissions( administrator = True)
async def очистка(ctx,amount : int):
    
    channel_log = client.get_channel(686476558701166603) #Айди канала логов

    await ctx.channel.purge( limit = amount )
    await ctx.send(embed = discord.Embed(description = f'**:heavy_check_mark: Удалено {amount} сообщений.**', color=0x0c0c0c))
    await channel_log.send(embed = discord.Embed(description = f'**:wastebasket:  Удалено {amount} сообщений.**', color=0x0c0c0c))

# Kick
@client.command()
@commands.has_permissions( administrator = True) 
async def кик(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        channel_log = client.get_channel(686476558701166603) #Айди канала логов

# Mute
@client.command()
@commands.has_permissions( administrator = True )
async def мут(ctx,amount : int,member: discord.Member = None, reason = None):
    mute_role = discord.utils.get(member.guild.roles, id = 685177184809123865) #Айди роли
    channel_log = client.get_channel(686476558701166603) #Айди канала логов

    await member.add_roles( mute_role )
    await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
    await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c))
    await asyncio.sleep(amount)
    await member.remove_roles( Участник )

# Unmute
@client.command()
@commands.has_permissions( administrator = True) 
async def размут(ctx,member: discord.Member = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 685177184809123865) #Айди роли
        channel_log = client.get_channel(686476558701166603) #Айди канала логов

        await member.remove_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был размучен.**', color=0x0c0c0c)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был размучен.**', color=0x0c0c0c))    

# Ban
@client.command()
@commands.has_permissions( administrator = True) 
async def бан(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:
        
        channel_log = client.get_channel(686476558701166603) #Айди канала логов

        await member.ban( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c)) 

# say
@client.command()
@commands.has_permissions( administrator = True)
async def say(ctx, *, arg):

    await ctx.message.delete()
    await ctx.send(embed = discord.Embed(description = f'{arg}', color=0x0c0c0c))

# Help
@client.command( pass_context = True )

async def хелп( ctx ):
    emb = discord.Embed( title = 'Помощь по Командам' )

    emb.add_field( name = '{}join'.format( PREFIX ), value = 'Вызвать бота в голосовой-чат' )
    emb.add_field( name = '{}play'.format( PREFIX ), value = 'Включить музыку' )
    emb.add_field( name = '{}myinfo'.format( PREFIX ), value = 'Информация о Себе' )
    emb.add_field( name = '{}sinfo'.format( PREFIX ), value = 'Информция о Сервере' )

    await ctx.send( embed = emb )

# AutoRole
@client.event

async def on_member_join( member ):
    channel = client.get_channel( 678617715145179143 )

    role = discord.utils.get( member.guild.roles, id = 678619450588790851 )

    await member.add_roles( role )
    await channel.send( embed = discord.Embed( description = f'Пользователь ``{ member.name }``, вступил в нашу банду!', color = 0x0c0c0c ) )

# PROFIL
@client.command()
async def sinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name}", description=f"Сервер создали {guild.created_at.strftime('%b %#d, %Y')}\n\n"
                                                             f"Регион {guild.region}\n\nГлава сервера {guild.owner}\n\n"
                                                             f"Людей на сервере {guild.member_count}\n\n",  color=0xff0000,timestamp=ctx.message.created_at)

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {guild.id}")

    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)

# userinfo
@client.command()
async def myinfo(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.'.format(Member.name), description=f"Участник зашёл на сервер: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
                                                                                      f"Никнейм: {Member.nick}\n\n"
                                                                                      f"Статус: {Member.status}\n\n"
                                                                                      f"ID: {Member.id}\n\n"
                                                                                      f"Роль: {Member.top_role}\n\n"
                                                                                      f"Аккаунт создан: {Member.created_at.strftime('%b %#d, %Y')}", 
                                                                                      color=0xff0000, timestamp=ctx.message.created_at)

    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)




# ОШИБКИ
@очистка.error 
async def clear_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.name},обязательно укажите количевство сообщений.**', color=0x0c0c0c))     
   

@мут.error 
async def tempmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@размут.error 
async def unmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@кик.error 
async def kick_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@бан.error 
async def ban_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))


# Music
@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот присоединился к Каналу: {channel}')

@client.command()
async def leave(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот отключился от канала: {channel}')

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удален')
    except PermissionError:
        print('[log] Не удалось удалить файл')

    await ctx.send('Пожалуйста ожидайте')

    voice = get(client.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загружаю музыку...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'[log] Переименовываю файл: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила свое проигрывание'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас проигрывает музыка: {song_name[0]}')
    
    # Token
token = "Njg1MjAwOTk2NTgyMDMxNDc3.XmT6HQ.URa-AAZg9TnElqrXmIEshCi8X1A"

client.run(token)
