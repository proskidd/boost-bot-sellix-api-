from optparse import Option
import discord
import json
import requests
import os
import httpx
import base64
import time
import os.path
import string
import random
from discord.ext import commands
from datetime import datetime
from colorama import Fore
import art 
from art import *
settings = json.load(open("config.json", encoding="utf-8"))

products = json.load(open("products.json", encoding="utf-8"))

prefix = settings["prefix"]
bot = commands.Bot(intents=discord.Intents.all(), command_prefix=f"{prefix}")

owner = settings["owner"]
log = int(settings["logchannel"])

Paypal = settings["Paypal_Gmail"]
BTC = settings["BTC_Addy"]
LTC = settings["LTC_Addy"]
ETH = settings["Eth_Addy"]
SOL = settings["SOL_Addy"]
MON = settings["MON_Addy"]
BHC = settings["BHC_Addy"]


Paypal_Emoji = settings["Paypal_Emoji"]
BTC_Emoji = settings["BTC_Emoji"]
LTC_Emoji = settings["LTC_Emoji"]
ETH_Emoji = settings["Eth_Emoji"]
SOL_Emoji = settings["SOL_Emoji"]
MON_Emoji = settings["MON_Emoji"]
BHC_Emoji = settings["BHC_Emoji"]

acti = settings["activity"]

sellixchannel = settings["sellixchannel"]

invitefield = "invite:"

bio = 'Quality boosts and tool in discord.gg/yacoii'
nick = '.gg/yacoii'

def licensed(user):
    try:
        open(f"data/stocks/1month/{user.id}.txt", "r")
        return True
    except FileNotFoundError:
        return False


def IsOwner(ctx):
    return str(ctx.author.id) in settings["owner"]


def getRandomString(length):
    pool = string.ascii_uppercase + string.digits
    return "".join(random.choice(pool) for i in range(length))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{acti}"))
    tprint(" yacoii ")
    print(Fore.GREEN, "[+] Online ")



@bot.event
async def on_message(message):  # sellix API.
    names = []
    values = []

    invite = ""

    if str(message.channel.id) == str(sellixchannel):

        for emb in message.embeds:
            for field in emb.fields:
                names.append(field.name)
                values.append(field.value)

                if field.name == invitefield:
                    invite = field.value

            for i in range(len(names)):
                name = names[i]

                if name.lower() == "product" and invite:

                    INVITE = invite.replace("//", "")

                    if "/invite/" in INVITE:
                        INVITE = INVITE.split("/invite/")[1]

                    elif "/" in INVITE:
                        INVITE = INVITE.split("/")[1]

                    if products[values[i]]:

                        jsondict = products[values[i]]

                        boosts = int(jsondict["boosts"])
                        months = int(jsondict["months"])

                        embed = discord.Embed(
                            title="**Sellix Order**", description=f"Sellix order received; boosting https://discord.gg/{INVITE} {boosts} times", timestamp=datetime.now(), color=0x8000ff)

                        msg = await message.channel.send(embed=embed)

                        boosts3(owner, INVITE, boosts)

                        embed2 = discord.Embed(
                            title="**Finished**", description=f"Finished Boosting https://discord.gg/{INVITE} x{boosts} times", timestamp=datetime.now(), color=discord.Colour.blurple())
                            
                        await msg.reply(embed=embed2)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Try slash commands 💀", mention_author=False)
        
        
        
        


@bot.slash_command(name="redeem", description="redeems key for license")
async def redeem(ctx, key):
    with open("data/keys.txt", "r") as f:
        lines = f.readlines()
        with open("data/keys.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != f"{key}":
                    f.write(line)
                open(f"data/stocks/1month/{ctx.author.id}.txt", "w")
                open(f"data/stocks/3month/{ctx.author.id}.txt", "w")
            else:
                await ctx.respond("Invalid Key")


@bot.slash_command(name="payments", description="Shows all the payment methods")
async def payments(ctx: discord.ApplicationContext):
    embed = discord.Embed(title='Payment Methods', description="**All Payment Methods Shown Below**",
                          timestamp=datetime.now(), color=0x8000ff)
    embed.add_field(name=f"{Paypal_Emoji} **Paypal**",
                    value=f"``{Paypal}``", inline=False)
    embed.add_field(name=f"{LTC_Emoji} **Litecoin**",
                    value=f"``{LTC}``", inline=False)
    embed.add_field(name=f"{BTC_Emoji} **Bitcoin**",
                    value=f"``{BTC}``", inline=False)
    embed.add_field(name=f"{ETH_Emoji} **Ethereum**",
                    value=f"``{ETH}``", inline=False)
    embed.add_field(name=f"{SOL_Emoji} **Solana**",
                    value=f"``{SOL}``", inline=False)
    embed.add_field(name=f"{MON_Emoji} **Monero**",
                    value=f"``{MON}``", inline=False)
    embed.add_field(name=f"{BHC_Emoji} **Bitcoin Cash**",
                    value=f"``{BHC}``", inline=False)
    embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
    return await ctx.respond(embed=embed)








@bot.slash_command(name="clear", description="Clears your whole stock")
async def clear(ctx, months: discord.Option(int, "Which stock", required=True)):
    if not licensed(ctx.author):
        embed = discord.Embed(title="**🚫 | Access Denied**", description="You do not haver permission to use this command ",
                              timestamp=datetime.now(), color=discord.Colour.red())
        await ctx.respond(embed=embed)
    if months != 1 and months != 3:
        return await ctx.respond("Only 1 or 3 months")
    if months == 1:
        f = open(f'data/stocks/1month/{ctx.author.id}.txt', 'r+')
        f.truncate(0)
        embed = discord.Embed(title="Success", description=f"Cleared your whole {months} stock", timestamp=datetime.now(
        ), color=discord.Colour.blurple())
        await ctx.respond(embed=embed)
    if months == 3:
        f = open(f"data/stocks/3month/{ctx.author.id}.txt", "r+")
        f.truncate(0)
        embed = discord.Embed(title="Success", description=f"Cleared your whole {months} stock", timestamp=datetime.now(
        ), color=discord.Colour.blurple())
        await ctx.respond(embed=embed)


@bot.slash_command(name="activity", description="changes bot activity name")
async def activity(ctx, activity: discord.Option(str, "Activity", required=True)):
    if IsOwner(ctx):
        embed = discord.Embed(description=f"Activity changed to ``{activity}``", timestamp=datetime.now(
        ), color=discord.Color.blurple()).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{activity}"))
        await ctx.respond(embed=embed)
        logs = bot.get_channel(log)
        embed = discord.Embed(title=f"PrimeBoostsLogs", description=f"*Command:* ``Activity``\n*Action:* ``Activity changed to {activity}``\n*Author:* {ctx.author.mention}\n*Location:* {ctx.channel.mention}", timestamp=datetime.now(
        ), color=discord.Color.blurple()).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        await logs.send(embed=embed)
    else:
        embed = discord.Embed(title="**🚫 | Access Denied**", description="You do not haver permission to use this command ",
                              timestamp=datetime.now(), color=discord.Colour.red())
        await ctx.respond(embed=embed)


@bot.command(name="licensed", description="Shows list of licensed people")
async def licenseds(ctx):
    if not IsOwner(ctx):
        await ctx.reply("You dont need to know who is licensed")
    else:
        await ctx.reply("Heres the list of licensed people", file=discord.File(f"data/stocks/licensed.txt"))


@bot.slash_command(name="licensed", description="Shows list of licensed people")
async def licenseds(ctx):
    if not IsOwner(ctx):
        await ctx.respond("You dont need to know who is licensed")
    else:
        await ctx.respond("Heres the list of licensed people", file=discord.File(f"data/stocks/licensed.txt"))


@bot.slash_command(name="license", description="Adds a license to a specified user")
async def add_license_(ctx, user: discord.User):
    if not IsOwner(ctx):
        embed = discord.Embed(title="**🚫 | Access Denied**", description="You do not have permission to use this command",
                              timestamp=datetime.now(), color=discord.Colour.red())
        await ctx.respond(embed=embed)
    if IsOwner(ctx):
        if not licensed(user):
            with open("data/stocks/licensed.txt", "a") as f:
                f.write(f"{user} - {user.id}\n")
                f.close
            open(f"data/stocks/1month/{user.id}.txt", "w")
            open(f"data/stocks/3month/{user.id}.txt", "w")
            logs = bot.get_channel(log)
            embed = discord.Embed(title=f"{ctx.author} just ran a command", description=f"License given to {user.mention}\n\nAuthor: {ctx.author.mention}\nLocation: {ctx.channel.mention}",
                                  timestamp=datetime.now(), color=discord.Colour.green()).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
            await logs.send(embed=embed)
            await ctx.respond(f"Licensed {user.mention}")
        else:
            with open("data/stocks/licensed.txt", "r") as f:
                lines = f.readlines()
            with open("data/stocks/licensed.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != f"{user} - {user.id}":
                        f.write(line)
            os.remove(f"data/stocks/1month/{user.id}.txt")
            os.remove(f"data/stocks/3month/{user.id}.txt")
            logs = bot.get_channel(log)
            embed = discord.Embed(title=f"{ctx.author} just ran a command", description=f"License removed from {user.mention}\n\nAuthor: {ctx.author.mention}\nLocation: {ctx.channel.mention}",
                                  timestamp=datetime.now(), color=discord.Colour.red()).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
            await logs.send(embed=embed)
            await ctx.respond(f"Unlicensed {user.mention}")


@bot.command(name="license", description="Adds a license to a specified user")
async def add_license_(ctx, user: discord.User = None):
    if not IsOwner(ctx):
        embed = discord.Embed(title="**🚫 | Access Denied**", description="You do not have permission to use this command",
                              timestamp=datetime.now(), color=discord.Colour.red())
        await ctx.reply(embed=embed, mention_author=False)
    if IsOwner(ctx):
        if user == None:
            await ctx.reply("Provide an user ID", mention_author=False)
        if not licensed(user):
            with open("data/stocks/licensed.txt", "a") as f:
                f.write(f"{user} - {user.id}\n")
                f.close
            open(f"data/stocks/1month/{user.id}.txt", "w")
            open(f"data/stocks/3month/{user.id}.txt", "w")
            logs = bot.get_channel(log)
            embed = discord.Embed(title=f"PrimeBoosts Logs", description=f"*Command:* ``license``\n*Action:* ``Removed License From`` {user.mention}\n*Author:* {ctx.author.mention}\n*Location:* {ctx.channel.mention}", timestamp=datetime.now(
            ), color=discord.Colour.green()).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
            await logs.send(embed=embed)
            await ctx.reply(f"Licensed {user.mention}", mention_author=False)
        else:
            with open("data/stocks/licensed.txt", "r") as f:
                lines = f.readlines()
            with open("data/stocks/licensed.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != f"{user} - {user.id}":
                        f.write(line)
            os.remove(f"data/stocks/1month/{user.id}.txt")
            os.remove(f"data/stocks/3month/{user.id}.txt")
            logs = bot.get_channel(log)
            embed = discord.Embed(title=f"PrimeBoosts Logs", description=f"*Command:* ``license``\n*Action:* ``Removed License From`` {user.mention}\n*Author:* {ctx.author.mention}\n*Location:* {ctx.channel.mention}", timestamp=datetime.now(
            ), color=discord.Colour.red()).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
            await logs.send(embed=embed)
            await ctx.reply(f"Unlicensed {user.mention}", mention_author=False)


@bot.slash_command(name="stock", description="Shows owner stock if isnt whitelisted else own")
async def stock(ctx: discord.ApplicationContext):
    if not licensed(ctx.author):
        embed = discord.Embed(title=f"Bluestorm Stock Currently Has", timestamp=datetime.now(
        ), color=0x8000ff).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        embed.add_field(name="1 Month Stock",
                        value=f"*Nitro Tokens:* ``{len(open(f'data/stocks/1month/{owner}.txt', encoding='utf-8').read().splitlines())}``\n*Boosts Stock:* ``{len(open(f'data/stocks/1month/{owner}.txt', encoding='utf-8').read().splitlines()) * 2}``", inline=True)
        embed.add_field(name="3 Month Stock",
                        value=f"*Nitro Tokens:* ``{len(open(f'data/stocks/3month/{owner}.txt', encoding='utf-8').read().splitlines())}``\n*Boosts Stock:* ``{len(open(f'data/stocks/3month/{owner}.txt', encoding='utf-8').read().splitlines()) * 2}``", inline=True)
        await ctx.respond(embed=embed)
    embed = discord.Embed(title=f"Shop Stock Currently Has", timestamp=datetime.now(
    ), color=0x8000ff).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
    embed.add_field(name="1 Month Stock",
                    value=f"*Nitro Tokens:* ``{len(open(f'data/stocks/1month/{ctx.author.id}.txt', encoding='utf-8').read().splitlines())}``\n*Boosts Stock:* ``{len(open(f'data/stocks/1month/{ctx.author.id}.txt', encoding='utf-8').read().splitlines()) * 2}``", inline=True)
    embed.add_field(name="3 Month Stock",
                    value=f"*Nitro Tokens:* ``{len(open(f'data/stocks/3month/{ctx.author.id}.txt', encoding='utf-8').read().splitlines())}``\n*Boosts Stock:* ``{len(open(f'data/stocks/3month/{ctx.author.id}.txt', encoding='utf-8').read().splitlines()) * 2}``", inline=True)
    return await ctx.respond(embed=embed)


@bot.command(name="stock", description="Shows owner stock if isnt whitelisted else own")
async def stock(ctx):
    if not licensed(ctx.author):
        embed = discord.Embed(title=f"Bluestorm Stock Currently Has", timestamp=datetime.now(
        ), color=0x8000ff).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        embed.add_field(name="1 Month Stock",
                        value=f"*Nitro Tokens:* ``{len(open(f'data/stocks/1month/{owner}.txt', encoding='utf-8').read().splitlines())}``\n*Boosts Stock:* ``{len(open(f'data/stocks/1month/{owner}.txt', encoding='utf-8').read().splitlines()) * 2}``", inline=True)
        embed.add_field(name="3 Month Stock",
                        value=f"*Nitro Tokens:* ``{len(open(f'data/stocks/3month/{owner}.txt', encoding='utf-8').read().splitlines())}``\n*Boosts Stock:* ``{len(open(f'data/stocks/3month/{owner}.txt', encoding='utf-8').read().splitlines()) * 2}``", inline=True)
        await ctx.reply(embed=embed)
    embed = discord.Embed(title=f"Shop Stock Currently Has", timestamp=datetime.now(
    ), color=0x8000ff).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
    embed.add_field(name="1 Month Stock",
                    value=f"*Nitro Tokens:* ``{len(open(f'data/stocks/1month/{ctx.author.id}.txt', encoding='utf-8').read().splitlines())}``\n*Boosts Stock:* ``{len(open(f'data/stocks/1month/{ctx.author.id}.txt', encoding='utf-8').read().splitlines()) * 2}``", inline=True)
    embed.add_field(name="3 Month Stock",
                    value=f"*Nitro Tokens:* ``{len(open(f'data/stocks/3month/{ctx.author.id}.txt', encoding='utf-8').read().splitlines())}``\n*Boosts Stock:* ``{len(open(f'data/stocks/3month/{ctx.author.id}.txt', encoding='utf-8').read().splitlines()) * 2}``", inline=True)
    return await ctx.reply(embed=embed)


@bot.slash_command(name="restock", description="Restocks with pastebin (RAW ONLY)")
async def restock(ctx, pastebin: discord.Option(str, "Raw Pastebin", required=True), months: discord.Option(int, "1 or 3 month", required=True)):
    if not licensed(ctx.author):
        cum = discord.Embed(title="**🚫 | Access Denied**", description="You do not have permission to use this command",
                            timestamp=datetime.now(), color=discord.Colour.red())
        return await ctx.respond(embed=cum)
    if months != 1 and months != 3:
        return await ctx.respond("Only 1 or 3 months")

    tokens = httpx.get(pastebin).text.splitlines()
    if months == 1:
        with open(f"data/stocks/1month/{ctx.author.id}.txt", "a", encoding="utf-8") as file:
            for token in tokens:
                file.write(f"{token}\n")
        logs = bot.get_channel(log)
        embed = discord.Embed(title=f"{ctx.author} just ran a command", description=f"{ctx.author.mention} Restocked {months} Month nitro tokens\nAmount: {str(len(tokens))} Nitro Tokens ({str(len(tokens)*2)}) boosts\n\nAuthor: {ctx.author.mention}\nLocation: {ctx.channel.mention}",
                              timestamp=datetime.now(), color=discord.Colour.dark_green()).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        await logs.send(embed=embed)
        embed = discord.Embed(
            title="Success", description=f"Successfully Restocked {str(len(tokens))} of {months} Month nitro tokens ({str(len(tokens)*2)}) boosts", timestamp=datetime.now(), color=discord.Colour.blurple())
        return await ctx.send(embed=embed)
    if months == 3:
        with open(f"data/stocks/3month/{ctx.author.id}.txt", "a", encoding="utf-8") as file:
            for token in tokens:
                file.write(f"{token}\n")
        logs = bot.get_channel(log)
        embed = discord.Embed(title=f"PrimeBoosts Logs", description=f"*Command:* ``restock``\n*Amount:* ``{str(len(tokens))} Nitro Tokens ({str(len(tokens)*2)})`` boosts\n\nAuthor: {ctx.author.mention}\nLocation: {ctx.channel.mention}", timestamp=datetime.now(
        ), color=discord.Colour.dark_green()).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        await logs.send(embed=embed)
        embed = discord.Embed(
            title="Success", description=f"Successfully Restocked {str(len(tokens))} of {months} Month nitro tokens ({str(len(tokens)*2)}) boosts", timestamp=datetime.now(), color=discord.Colour.blurple())
        return await ctx.send(embed=embed)


@bot.slash_command(name="send", description="Sends them the tokens in dms")
async def send(ctx, user: discord.User, amount: discord.Option(int, "Amount of tokens.", required=True), months: discord.Option(int, "1 or 3 month", required=True)):
    if not licensed(ctx.author):
        cum = discord.Embed(title="**🚫 | Access Denied**", description="You do not have permission to use this command",
                            timestamp=datetime.now(), color=discord.Colour.red())
        return await ctx.respond(embed=cum)
    else:
        if months != 1 and months != 3:
            return await ctx.respond("Only 1 or 3 months")
        if months == 1:

            temp_tokens = open(
                f"data/stocks/1month/{ctx.author.id}.txt", encoding="UTF-8").read().splitlines()
            if len(temp_tokens) < amount:
                return await ctx.respond(f"You dont have enough {amount} month nitro tokens in stock")

            tokens_to_give = temp_tokens[0:amount]
            temp_tokens = temp_tokens[amount:]

            f = open(f"data/stocks/tokens.txt", "w", encoding="UTF-8")
            for tk in tokens_to_give:
                f.write(tk + "\n")
            f.close()

            f = open(
                f"data/stocks/1month/{ctx.author.id}.txt", "w", encoding="UTF-8")
            for tk in temp_tokens:
                f.write(tk + "\n")
            f.close()

            await user.send(f"Here are your {months} month old nitro tokens {user.mention}\n*Amount:* ``{amount}``\nSent by {ctx.author.mention}", file=discord.File(f"data/stocks/tokens.txt"))
            await ctx.respond(f"Successfully sent {user.mention} {months} month old nitro tokens\n*Amount:*``{amount}``")
            logs = bot.get_channel(log)
            embed = discord.Embed(title=f"{ctx.author} just ran a command", description=f"{ctx.author.mention} Sent {months} Month old nitro tokens to {user.mention}\nAmount: {amount}\n\nAuthor: {ctx.author.mention}\nLocation: {ctx.channel.mention}",
                                  timestamp=datetime.now(), color=0x8000ff).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
            await logs.send(embed=embed)
            os.remove(f"data/stocks/tokens.txt")
        if months == 3:

            temp_tokens = open(
                f"data/stocks/3month/{ctx.author.id}.txt", encoding="UTF-8").read().splitlines()
            if len(temp_tokens) < amount:
                return await ctx.respond(f"You dont have enough {amount} month nitro tokens in stock")

            tokens_to_give = temp_tokens[0:amount]
            temp_tokens = temp_tokens[amount:]

            f = open(f"data/stocks/tokens.txt", "w", encoding="UTF-8")
            for tk in tokens_to_give:
                f.write(tk + "\n")
            f.close()

            f = open(
                f"data/stocks/3month/{ctx.author.id}.txt", "w", encoding="UTF-8")
            for tk in temp_tokens:
                f.write(tk + "\n")
            f.close()

            await user.send(f"Here are your {months} month old nitro tokens ({len(open(f'data/stocks/tokens.txt', encoding='utf-8').read().splitlines())}) {user.mention}\nSent by {ctx.author.mention}", file=discord.File(f"data/stocks/tokens.txt"))
            await ctx.respond(f"Successfully sent {user.mention} {months} month old nitro tokens ({len(open(f'data/stocks/tokens.txt', encoding='utf-8').read().splitlines())})")
            logs = bot.get_channel(log)
            embed = discord.Embed(title=f"PrimeBoosts", description=f"*Command:* ``Send``\n{ctx.author.mention} Sent {months} Month old nitro tokens to {user.mention}\nAmount: {amount}\n\nAuthor: {ctx.author.mention}\nLocation: {ctx.channel.mention}", timestamp=datetime.now(
            ), color=0x8000ff).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
            await logs.send(embed=embed)
            os.remove(f"data/stocks/tokens.txt")


def removeToken3(user, token: str):
    with open(f'data/stocks/3month/{user}.txt', "r") as f:
        Tokens = f.read().split("\n")
        for t in Tokens:
            if len(t) < 5 or t == token:
                Tokens.remove(t)
                print("removed token")
        open(f'data/stocks/3month/{user}.txt', "w").write("\n".join(Tokens))


def removeToken1(user, token: str):
    with open(f'data/stocks/1month/{user}.txt', "r") as f:
        Tokens = f.read().split("\n")
        for t in Tokens:
            print(t)
            if len(t) < 5 or t == token:
                Tokens.remove(t)
                print("removed token")
        open(f'data/stocks/1month/{user}.txt', "w").write("\n".join(Tokens))


def boosts3(user, invite: str, amount: int):
    print("[!] Starting up")
    if amount % 2 != 0:
        amount += 1

    tokens = get_all_tokens(f'data/stocks/3month/{user}.txt')
    all_data = []
    tokens_checked = 0
    actually_valid = 0
    boosts_done = 0
    for token in tokens:
        s, headers = get_headers(token)
        profile = validate_token(s, headers)
        tokens_checked += 1

        if profile != False:
            actually_valid += 1
            data_piece = [s, token, headers, profile]
            all_data.append(data_piece)
        else:
            pass
    for data in all_data:
        if boosts_done >= amount:
            return
        s, token, headers, profile = get_items(data)
        boost_data = s.get(
            f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=headers)
        if boost_data.status_code == 200:
            if len(boost_data.json()) != 0:
                join_outcome, server_id = do_join_server(
                    s, token, headers, profile, invite)
                if join_outcome:
                    for boost in boost_data.json():

                        if boosts_done >= amount:
                            removeToken3(user, token)
                            return
                        boost_id = boost["id"]
                        bosted = do_boost(s, token, headers,
                                          profile, server_id, boost_id)
                        if bosted:
                            print(
                                f"{Fore.GREEN}[!]Boosted - {token[20:]}******")
                            boosts_done += 1
                        else:
                            print(
                                f"{Fore.RED}[!] Already Boosting another server - {token[20:]}******")
                    removeToken3(user, token)
                else:
                    print(
                        f"{Fore.RED}{token}[!] Error joining - {token[20:]}******")

            else:
                removeToken3(user, token)
                print(
                    f"{Fore.RED}[!] No Nitro Found On Token - {token[20:]}******")


def boosts1(user, invite: str, amount: int):
    print("[!] Starting up")
    if amount % 2 != 0:
        amount += 1

    tokens = get_all_tokens(f'data/stocks/1month/{user}.txt')
    all_data = []
    tokens_checked = 0
    actually_valid = 0
    boosts_done = 0
    for token in tokens:
        s, headers = get_headers(token)
        profile = validate_token(s, headers)
        tokens_checked += 1

        if profile != False:
            actually_valid += 1
            data_piece = [s, token, headers, profile]
            all_data.append(data_piece)
        else:
            pass
    for data in all_data:
        if boosts_done >= amount:
            return
        s, token, headers, profile = get_items(data)
        boost_data = s.get(
            f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=headers)
        if boost_data.status_code == 200:
            if len(boost_data.json()) != 0:
                join_outcome, server_id = do_join_server(
                    s, token, headers, profile, invite)
                if join_outcome:
                    for boost in boost_data.json():

                        if boosts_done >= amount:
                            removeToken1(user, token)
                            return
                        boost_id = boost["id"]
                        bosted = do_boost(s, token, headers,
                                          profile, server_id, boost_id)
                        if bosted:
                            print(f"[!] Boosted - {token[20:]}************")
                            boosts_done += 1
                        else:
                            print(
                                f"[!] Already Boosting another server - {token[20:]}************")
                    removeToken1(user, token)
                else:
                    print(f"[!] Error joining - {token[20:]}************")

            else:
                removeToken1(user, token)
                print(
                    f"[!] No Nitro Found On Token - {token[20:]}************")




@bot.slash_command(name="boost", description="boost server")
async def boost(ctx: discord.ApplicationContext, inv: discord.Option(str, "Invitelink/code", required=True),
                amount: discord.Option(int, "amount", required=True), months: discord.Option(int, "How many months", required=True)):
    INVITE = inv.replace("//", "")
    if "/invite/" in INVITE:
        INVITE = INVITE.split("/invite/")[1]

    elif "/" in INVITE:
        INVITE = INVITE.split("/")[1]
    if not licensed(ctx.author):
        embed = discord.Embed(title="**🚫 | Access Denied**", description="You do not haver permission to use this command !",
                              timestamp=datetime.now(), color=discord.Colour.red())
        await ctx.respond(embed=embed, mention_author=False)
    embed = discord.Embed(
        title="**Started**", description=f"Started Boosting https://discord.gg/{INVITE} x{amount} times", timestamp=datetime.now(), color=discord.Colour.blurple())
    await ctx.respond(embed=embed)

    dataabotinvite = httpx.get(
        f"https://discord.com/api/v9/invites/{INVITE}").text
    if '{"message": "Unknown Invite", "code": 10006}' in dataabotinvite:
        return await ctx.edit("*Invite link is invalid*")
    if months == 1:
        boosts1(ctx.author.id, INVITE, amount)

    if months == 3:
        boosts3(ctx.author.id, INVITE, amount)
    logs = bot.get_channel(log)
    embed = discord.Embed(title=f"PrimeBoosts Logs", description=f"*Command:* ``boost``\n*Server:* ``https://discord.gg/{INVITE}``\n*Amount:* ``x{amount}``\n*Author:* {ctx.author.mention}\n*Location:* {ctx.channel.mention}", timestamp=datetime.now(
    ), color=discord.Colour.blurple()).set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
    await logs.send(embed=embed)
    embed = discord.Embed(
        title="**Finished**", description=f"Finished Boosting https://discord.gg/{INVITE} x{amount} times", timestamp=datetime.now(), color=discord.Colour.blurple())
    return await ctx.respond(embed=embed)


def get_super_properties():
    properties = '''{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-GB","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","browser_version":"95.0.4638.54","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":102113,"client_event_source":null}'''
    properties = base64.b64encode(properties.encode()).decode()
    return properties


def get_fingerprint(s):
    try:
        fingerprint = s.get(
            f"https://discord.com/api/v9/experiments", timeout=5).json()["fingerprint"]
        return fingerprint
    except Exception as e:
        # print(e)
        return "Error"


def get_cookies(s, url):
    try:
        cookieinfo = s.get(url, timeout=5).cookies
        dcf = str(cookieinfo).split('__dcfduid=')[1].split(' ')[0]
        sdc = str(cookieinfo).split('__sdcfduid=')[1].split(' ')[0]
        return dcf, sdc
    except:
        return "", ""


def get_proxy():
    return None  # can change if problems occur


def get_headers(token):
    while True:
        s = httpx.Client(proxies=get_proxy())
        dcf, sdc = get_cookies(s, "https://discord.com/")
        fingerprint = get_fingerprint(s)
        if fingerprint != "Error":  # Making sure i get both headers
            break

    super_properties = get_super_properties()
    headers = {
        'authority': 'discord.com',
        'method': 'POST',
        'path': '/api/v9/users/@me/channels',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US',
        'authorization': token,
        'cookie': f'__dcfduid={dcf}; __sdcfduid={sdc}',
        'origin': 'https://discord.com',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',

        'x-debug-options': 'bugReporterEnabled',
        'x-fingerprint': fingerprint,
        'x-super-properties': super_properties,
    }

    return s, headers


def find_token(token):
    if ':' in token:
        token_chosen = None
        tokensplit = token.split(":")
        for thing in tokensplit:
            if '@' not in thing and '.' in thing and len(
                    thing) > 30:  # trying to detect where the token is if a user pastes email:pass:token (and we dont know the order)
                token_chosen = thing
                break
        if token_chosen == None:
            print(f"Error finding token", Fore.RED)
            return None
        else:
            return token_chosen

    else:
        return token


def get_all_tokens(filename):
    all_tokens = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            token = line.strip()
            token = find_token(token)
            if token != None:
                all_tokens.append(token)

    return all_tokens


def validate_token(s, headers):
    check = s.get(f"https://discord.com/api/v9/users/@me", headers=headers)

    if check.status_code == 200:
        profile_name = check.json()["username"]
        profile_discrim = check.json()["discriminator"]
        profile_of_user = f"{profile_name}#{profile_discrim}"
        return profile_of_user
    else:
        return False


def do_member_gate(s, token, headers, profile, invite, server_id):
    outcome = False
    try:
        member_gate = s.get(
            f"https://discord.com/api/v9/guilds/{server_id}/member-verification?with_guild=false&invite_code={invite}",
            headers=headers)
        if member_gate.status_code != 200:
            return outcome
        accept_rules_data = member_gate.json()
        accept_rules_data["response"] = "true"

        # del headers["content-length"] #= str(len(str(accept_rules_data))) #Had too many problems
        # del headers["content-type"] # = 'application/json'  ^^^^

        accept_member_gate = s.put(f"https://discord.com/api/v9/guilds/{server_id}/requests/@me", headers=headers,
                                   json=accept_rules_data)
        if accept_member_gate.status_code == 201:
            outcome = True

    except:
        pass

    return outcome


def do_join_server(s, token, headers, profile, invite):
    join_outcome = False
    server_id = None
    try:
        # headers["content-length"] = str(len(str(server_join_data)))
        headers["content-type"] = 'application/json'

        for i in range(15):
            try:
                createTask = httpx.post("https://api.capmonster.cloud/createTask", json={
                    "clientKey": settings["capmonsterKey"],
                    "task": {
                        "type": "HCaptchaTaskProxyless",
                        "websiteURL": "https://discord.com/channels/@me",
                        "websiteKey": "76edd89a-a91d-4140-9591-ff311e104059"
                    }
                }).json()["taskId"]

                print(f"[-] Captcha Detected, Solving")

                getResults = {}
                getResults["status"] = "processing"
                while getResults["status"] == "processing":
                    getResults = httpx.post("https://api.capmonster.cloud/getTaskResult", json={
                        "clientKey": settings["capmonsterKey"],
                        "taskId": createTask
                    }).json()

                    time.sleep(1)

                solution = getResults["solution"]["gRecaptchaResponse"]

                print(f"[!] Captcha Solved")

                join_server = s.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={
                    "captcha_key": solution
                })

                break
            except:
                pass

        server_invite = invite
        if join_server.status_code == 200:
            join_outcome = True
            server_name = join_server.json()["guild"]["name"]
            server_id = join_server.json()["guild"]["id"]
            print(f"[!] Joined Server - {token[20:]}************")
        else:
            print(join_server.text)
    except:
        pass

    return join_outcome, server_id


def do_boost(s, token, headers, profile, server_id, boost_id):
    boost_data = {"user_premium_guild_subscription_slot_ids": [f"{boost_id}"]}
    headers["content-length"] = str(len(str(boost_data)))
    headers["content-type"] = 'application/json'

    boosted = s.put(f"https://discord.com/api/v9/guilds/{server_id}/premium/subscriptions", json=boost_data,
                    headers=headers)
    if boosted.status_code == 201:
        return True
    else:
        return False


def get_invite():
    while True:
        print(f"{Fore.CYAN}Server invite?", end="")
        invite = input(" > ").replace("//", "")

        if "/invite/" in invite:
            invite = invite.split("/invite/")[1]

        elif "/" in invite:
            invite = invite.split("/")[1]

        dataabotinvite = httpx.get(
            f"https://discord.com/api/v9/invites/{invite}").text

        if '{"message": "Unknown Invite", "code": 10006}' in dataabotinvite:
            print(f"{Fore.RED}discord.gg/{invite} is invalid")
        else:
            print(f"{Fore.GREEN}discord.gg/{invite} appears to be a valid server")
            break

    return invite


def get_items(item):
    s = item[0]
    token = item[1]
    headers = item[2]
    profile = item[3]
    return s, token, headers, profile




def get_super_properties():
    properties = '''{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-GB","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","browser_version":"95.0.4638.54","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":102113,"client_event_source":null}'''
    properties = base64.b64encode(properties.encode()).decode()
    return properties




bot.run(settings["bot_token"])
