import discord, asyncio, json, re, time, random, requests, typing, json, os, uuid, psutil, datetime, warnings, pytz, logging, string, aiohttp, http

warnings.filterwarnings('ignore', category = DeprecationWarning)

from discord import ui, app_commands, Interaction, SelectOption, SelectMenu, ButtonStyle, ActionRow, Button
from discord.app_commands import Choice
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
from discord.utils import get
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# ------------------------------------------
# CONFIGURATIONS ET INFORMATIONS GLOBALES
# ------------------------------------------

PERM_ADMIN_ID = 1251852225186234418
default_guild_id = 1251656625622618213
UPVOTE_CHANNEL_ID = 1260559146428792882

METRICS_API_URL = "https://metrics.paladium-bot.fr/"

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix = '/', intents = intents)
bot.remove_command('help')

class client(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            bio.start()
            print('bio ✔️')

            guild = self.get_guild(default_guild_id)
            global startTime
            startTime = time.time()

            france_tz = pytz.timezone('Europe/Paris')
            current_time = datetime.now(france_tz)
            formatted_time = current_time.strftime(f"%d %B %Y - %Hh%M")
            print(formatted_time)
            print(f'''
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    │  Logged in as {self.user.id} ==> ✔️     │
    │                                             │
    │  {self.user} is  Online ==> ✔️          │
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛''')

bot = client()
tree = app_commands.CommandTree(bot)

def convert(time):
    pos = ["s", "m", "h", "d"]
    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

def parse_duration(duration_str):
    try:
        amount, unit = int(duration_str[:-1]), duration_str[-1]

        if unit == 's':
            return amount
        elif unit == 'm':
            return amount * 60
        elif unit == 'h':
            return amount * 3600
        elif unit == 'd':
            return amount * 86400
        else:
            return None
    except ValueError:
        return None

# ------------------------------------------
# description / bio
# ------------------------------------------

@tasks.loop(seconds=4)
async def bio():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Game(name=f"Ynover"))
        await asyncio.sleep(4)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"les Ynoviens :)"))
        await asyncio.sleep(4)

# ------------------------------------------
# description / bio
# ------------------------------------------
# ------------------------------------------
# /HELP
# ------------------------------------------

@tree.command(name = 'help', description = 'Affiche la liste des commandes disponibles')
async def help(interaction:discord.Interaction):
    ping_ms = round(client.latency * 1000)

    embed = discord.Embed(title = 'Liste des commandes', 
                          description = f'''✧ **Ping :** `{ping_ms}ms`\n Voici la liste des commandes disponibles''', color = 0X22B1A4)

    embed.add_field(name = '＃ Administration \📌', value = f'''''', inline = False)
    embed.add_field(name = '＃ Création \🎨', value = f'''''', inline = False)
    embed.add_field(name = '＃ Jeux \🚀', value = f'''''', inline = False)
    embed.add_field(name = '＃ Divers \🔮', value = f'''''', inline = False)
    
    embed.set_footer(text = f"Ynover - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1280861064162054248/1280863792166604885/logo_ynov_campus_rvb.gif?ex=66d9a0dd&is=66d84f5d&hm=3869fa5c41a09f823afb0d31af877108083b60622e275f66850b6d386b643043&')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/1280861064162054248/1280863792506474556/logo_ynov_campus_rvb_blanc.jpg?ex=66d9a0dd&is=66d84f5d&hm=890a0b66fa1362304f067f04673c5f00c357bbda8bf94ff11e9888efeb0ce212&')

    await interaction.response.send_message(embed = embed)

# ------------------------------------------
# /HELP
# ------------------------------------------
# ------------------------------------------
# /PING
# ------------------------------------------

@tree.command(name = 'ping', description = 'Affiche le temps de latence du bot.')
async def ping(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    global startTime
    current_time = time.time()
    difference = int(round(current_time - startTime))
    uptime = str(timedelta(seconds=difference))
    total_members = 0
    for guild in bot.guilds:
        total_members += guild.member_count

    ping_ms = round(client.latency * 1000)
    headers = {'Authorization': 'Bearer ptla_VVQi0WpHAaahey0YEuMQPXRN3vWeQBP6zkl8fuT2dkk'}
    response = requests.get("https://panel.paladium-bot.fr//api/client/servers/fc0a8a1f/resources", headers = headers)

    if response.status_code == 200:
        data = response.json()['attributes']["resources"]
        ram_used = round(int(data["memory_bytes"]) / (1024 * 1024), 2)

        embed = discord.Embed(
            title = f'Temps de latence du Bot',
            description = f'''`＃ PING` : **{ping_ms}ms**.
`＃ Temps de Connexion` : **{str(timedelta(seconds=difference))}**.
`＃ RAM utilisée` : **{ram_used} Mo / {(psutil.virtual_memory().total // (1024 ** 2))} Mo**.
`＃ Latence API` : **{response.elapsed.total_seconds() * 1000:.2f} ms**.''', 
            color = 0x22B1A4
        )
    else:
        print("[ /HELP ] 〉Erreur lors de la récupération des statistiques du serveur")
        await interaction.response.send_message('Erreur lors de la récupération des statistiques du serveur', ephemeral = True)
        return

    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1280861064162054248/1280863792166604885/logo_ynov_campus_rvb.gif?ex=66d9a0dd&is=66d84f5d&hm=3869fa5c41a09f823afb0d31af877108083b60622e275f66850b6d386b643043&')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/1280861064162054248/1280863792506474556/logo_ynov_campus_rvb_blanc.jpg?ex=66d9a0dd&is=66d84f5d&hm=890a0b66fa1362304f067f04673c5f00c357bbda8bf94ff11e9888efeb0ce212&')
    await interaction.response.send_message(embed = embed)

# ------------------------------------------
# /LIENS
# ------------------------------------------

@tree.command(name = 'liens', description = 'Affiche les liens importants.')
async def liens(interaction: discord.Interaction):
    embed = discord.Embed(title = 'Liens importants', 
                          description = f'''## Liens qui vous aideront à naviguer et à en savoir plus sur le BDS d'Ynov Paris

> [` Site Officiel `](https://bds.ynov.com/) » **Publique**.
> [` Hébergement VPS `](https://panel.paladium-bot.fr/server/fc0a8a1f) » **Privé**.''',color = 0X650000)

    embed.set_footer(text = f"Ynover - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1280861064162054248/1280863792166604885/logo_ynov_campus_rvb.gif?ex=66d9a0dd&is=66d84f5d&hm=3869fa5c41a09f823afb0d31af877108083b60622e275f66850b6d386b643043&')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/1280861064162054248/1280863792506474556/logo_ynov_campus_rvb_blanc.jpg?ex=66d9a0dd&is=66d84f5d&hm=890a0b66fa1362304f067f04673c5f00c357bbda8bf94ff11e9888efeb0ce212&')

    await interaction.response.send_message(embed = embed)

# ------------------------------------------
# /LIENS
# ------------------------------------------

bot.run('TOKEN')