import os
from dotenv import load_dotenv
import aiocron
import discord
from discord.ext import commands
import asana
from Classes.GSpreadsheet import GSpreadsheet
from Classes.AsanaHelper import AsanaHelper

if __name__ == '__main__':
    intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
    bot = commands.Bot(command_prefix='!tifa ', intents=intents)
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    gSheet = GSpreadsheet()
    message_channel = bot.get_channel(int(os.environ['CHANNEL_ID']))
    client = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')
    asanaHelper = AsanaHelper()

    # <editor-fold desc="Events">
    @bot.event
    async def on_ready():
        print("Ready for action!")


    @bot.event
    async def on_member_join(member):
        message_channel = bot.get_channel(int(os.environ['CHANNEL_ID']))
        await message_channel.send(f"Hoşgeldin {member}! Sefalar getirdin!")
    # </editor-fold>

    # <editor-fold desc="Commands">
    @bot.command()
    async def helpme(ctx):
        await ctx.send(
            "Daily girmek için ""!tifa daily"" komutundan sonra mesajı girmen yeterli. Örneğin !tifa daily dün çok sevdiğim şirketimde eğitim testleri gerçekleştirdim!")


    @bot.command() #clear all
    async def clear(ctx):
        message_channel = bot.get_channel(int(os.environ['CHANNEL_ID']))
        if ctx.author.id == int(os.environ['CREATOR_ID']):
            try:
                purge_count = ctx.message.content[12:]
                purge_count = int(purge_count)
                await ctx.channel.purge(limit=purge_count)
                await message_channel.send(f"Son {purge_count} mesaj silindi!")
            except Exception as e:
                await message_channel.send(f"Bir hata oluştu! Lütfen bir sayı girdiğinden emin olarak tekrar gir!!")
        else:
            await message_channel.send(f"Bu komutu sadece beni ilk geliştiren Fethi Tekyaygil ve onun "
                                       f"yetkilendirdikleri kullanabilir! Yine de iyi denemeydi :)")


    @bot.command()
    async def daily(ctx):
        message_channel = bot.get_channel(int(os.environ['CHANNEL_ID']))
        gSheet.AddUserDailyInSheet(ctx)
        await message_channel.send(f"Harika iş {ctx.message.author.display_name.split()[0]}! Böyle devam et :)")


    @bot.command()
    async def sheetlink(ctx):
        message_channel = bot.get_channel(int(os.environ['CHANNEL_ID']))
        await message_channel.send(f"Excel linki: {os.environ['SHEET_LINK']}")
    # </editor-fold>


    @bot.command()
    async def getworkspaces(ctx):
        message_channel = bot.get_channel(int(os.environ['CHANNEL_ID']))
        await message_channel.send(asanaHelper.GetWorkspaces())

    @bot.command()
    async def changeworkspace(ctx):
        message_channel = bot.get_channel(int(os.environ['CHANNEL_ID']))
        await message_channel.send(asanaHelper.ChangeWorkspace(ctx))

    # <editor-fold desc="Commands">
    @aiocron.crontab('00 12 * * 1-7')
    async def cronjob1():
        message_channel = bot.get_channel(int(os.environ['CHANNEL_ID']))
        await message_channel.send("Bugün Global AI Hub için ne yaptın ;) @everyone")


    cronjob1.start()
    # </editor-fold>

    bot.run(os.environ['DISCORD_TOKEN'])
