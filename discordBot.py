import os
import random
import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  
intents.guilds = True
intents.members = True  
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Le bot est en ligne !"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot (command_prefix="!", intents=intents)

@bot.command()
async def bonjour(ctx):
  await ctx.send(f"Bonjour {ctx.author} !")


@bot.command()
async def ping(ctx):
  await ctx.send(f"Pong !")




@bot.command()
async def pileouface(ctx):
  await ctx.send(random.choice(["pile", "face" ]))




insultes = ["fdp", "FDP", "NTM" , "connard" , "pute" , "palmade" , "pele" , "connard" , "salope"]  


bot.taille_du_bot = 0
avertissements = {}

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.command()
async def cookie(ctx):
    bot.taille_du_bot += 1
    await ctx.send(f"{ctx.author.mention}, Soline a mangé un cookie ! Taille actuelle : {bot.taille_du_bot}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


    for insulte in insultes:
        if insulte in message.content.lower():
            user_id = str(message.author.id)
            avertissements[user_id] = avertissements.get(user_id, 0) + 1


            bot.taille_du_bot = max(0, bot.taille_du_bot - 1)

            await message.channel.send(f"{message.author.mention}, attention ! Avertissement #{avertissements[user_id]}.")
            await message.channel.send(f"Soline bot a maigri... Taille actuelle : {bot.taille_du_bot}.")


            if avertissements[user_id] >= 3:
                guild = message.guild
                member = guild.get_member(message.author.id)

                if member:
                    try:
                        await member.kick(reason="Trop d'insultes Soline a trop maigri.")
                        await message.channel.send(f"{message.author.mention} a été expulsé pour avoir accumulé trop d'avertissements.")
                    except discord.Forbidden:
                        await message.channel.send(f"Je n'ai pas la permission d'expulser {message.author.mention}.")
                    except Exception as e:
                        await message.channel.send(f"Erreur en expulsant {message.author.mention}: {e}")

            break

    await bot.process_commands(message)










token = os.environ['TOKEN_BOT']
keep_alive()
bot.run(token)