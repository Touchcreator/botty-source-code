import discord
from discord.ext import commands, tasks
import os
import requests
import json
from keep_repl_alive import keep_alive



client = commands.Bot(command_prefix = 'b!', case_insensitive = True)
client.remove_command('help')

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)
def get_definition(word):
  responsed = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/'+word)
  json_data = json.loads(responsed.text)
  embed = discord.Embed(title=word, description="Definitions:", colour=0x87CEEB)
  
  for i in range(0,len(json_data[0]['meanings'])):
    # print(json_data[0]['meanings'][i]["partOfSpeech"]+" "+json_data[0]['meanings'][i]["definitions"][0]["definition"])

    #print(json_data[0]['meanings'][i])
    embed.add_field(name=json_data[0]['meanings'][i]["partOfSpeech"], value=json_data[0]['meanings'][i]["definitions"][0]['definition'], inline=False)
    

  definition = embed
  return definition

def get_word():
  responsew = requests.get('https://random-word-api.herokuapp.com/word?number=1')
  json_data = json.loads(responsew.text)
  randoword = json_data[0]
  return(randoword)

def get_cat():
  catresponse = requests.get("http://aws.random.cat/meow")
  json_data = json.loads(catresponse.text)
  randocat = json_data[0]["file"]
  return(randocat)


@client.event
async def on_ready():
  print('touch made me log into {0.user}'.format(client))
  await client.change_presence(activity=discord.Game('b!help, by Touchcreator'))
  


@client.command()
async def help(ctx):
  await ctx.send('Go here: https://botty-commands.touchcreator.repl.co')

@client.command()
async def quote(ctx):
  await ctx.send(get_quote())

@client.command()
async def invite(ctx):
  await ctx.send("https://discord.com/api/oauth2/authorize?client_id=881296562586779668&permissions=8&scope=bot")

@client.command()
async def define(ctx):
  word = ctx.message.content.split(' ')[1]
  await ctx.send(embed=get_definition(word))

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
  await user.kick(reason=reason)
  await ctx.send(f"{user} have been kicked sucessfully")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
  await user.ban(reason=reason)
  await ctx.send(f"{user} have been banned sucessfully")

@client.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user
  
  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)
    await ctx.send(f"{user} have been unbanned sucessfully")
    return

@client.command()
async def word(ctx):
  await ctx.send(get_word())

@client.command()
async def catpic(ctx):
  #embed = discord.Embed(
    #title = 'Here is a cat picture :cat:'
  #)
  #embed.set_image(get_cat())
  #await ctx.send(embed=embed)
  await ctx.send("amogus *coding in cat pics is too hard :(*")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! :ping_pong:{round(client.latency)} ms")
    print(f"{client.latency} ms")


keep_alive()
client.run(os.getenv('TOKEN'))