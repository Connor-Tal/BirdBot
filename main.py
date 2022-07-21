import datetime
import random
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ['TOKEN']

invites = {}
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

#commands    
@bot.event
async def on_ready():
    print(bot.user.name,"has connected to discord" )
    for guild in bot.guilds:
      invites[guild.id] = await guild.invites()
      print(guild)
def find_invite_by_code(invite_list, code):
    for inv in invite_list:     
        if inv.code == code:      
            return inv

@bot.event
async def on_member_join(member):
  invites_before_join = invites[member.guild.id]
  invites_after_join = await member.guild.invites()
  for invite in invites_before_join: 
    if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
      print(f"Member {member.name} Joined")
      print(f"Invite Code: {invite.code}")
      print(f"Inviter: {invite.inviter}")
      if invite.code == 'PEyhP4SsYu':
        newbie = discord.utils.get(member.guild.roles, id = 993562619854200995)
        await member.add_roles(newbie)
        await member.send("Welcome to birds server!") 
      if invite.code == 'xgEnhEJfbJ':
        newbie = discord.utils.get(member.guild.roles, id = 993562619854200995)
        await member.add_roles(newbie)
        await member.send("Welcome to birds server!") 
      if invite.code == 'kNnQWBrZnE':
        await channel.send("Hi")
      
      invites[member.guild.id] = invites_after_join
      return

@bot.event
async def on_member_remove(member):

    invites[member.guild.id] = await member.guild.invites()    

@bot.event
async def on_message(msg):
    if 'beep' in msg.content:
        print('Keyword found')
        await msg.reply("Bad word", delete_after=1)
        await msg.delete()
        duration = datetime.timedelta(float(0.5))  
        await msg.author.timeout_for(duration)
    else:
      return

    
@bot.command(name = 'roll', help = 'Simulates rolling dice. !roll <number of dice>, <number or sides> ')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
      dice = [
        str(random.choice(range(1, number_of_sides + 1)))
          for _ in range(number_of_dice)
        ]
      await ctx.send(', '.join(dice))

@bot.command(name = 'hello', help = 'Says hello. !hello')
async def hello(ctx):
    languages = [
        'Hola', 'Hello', 'Namaste', 'Konnichiwa', 'Guten tag', 'Hallo', 'Bonjour', 'Salam', 'Ciao', 'Shalom','Bonjou/Bonswa'
    ]
    hellovar = random.choice(languages)
    await ctx.send(hellovar)

@bot.command(name = 'ping', help = 'pong! !ping')
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name = 'yesno', help = 'yes or no !yesno')
async def yesno(ctx):
  yesno = random.randint(1,2)
  if yesno == 1:
    yesnoo = "Yes"
  if yesno == 2:
    yesnoo = "No"
  await ctx.send(yesnoo)

@commands.has_permissions(ban_members=True)
@bot.command(name = 'ban', help = 'ADMIN ONLY bans a person !ban <member name> <reason>')
async def ban(ctx, member:discord.User, *, reason=None):
    if reason == None:
        reason = f"No Reason Provided"
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"{member.mention} has been **banned** by {ctx.message.author}", delete_after=1)
    await ctx.message.delete()
    print(f"Sucsessfully banned {member.name}")

@commands.has_permissions(ban_members=True)
@bot.command(name = 'kick', help = 'ADMIN ONLY kicks a member !kick <member name> <reason>')
async def kick(ctx, member:discord.User, *, reason=None):
    if reason == None:
        reason = f"No Reason Provided"
    await ctx.guild.kick(member, reason=reason)
    await ctx.send(f"{member.mention} has been **kicked** by {ctx.message.author}", delete_after=1)
    await ctx.message.delete()
    print(f"Sucsessfully kicked {member.name}")

@commands.has_permissions(ban_members=True)
@bot.command(name = 'unban', help = 'ADMIN ONLY unbans a member !unban <member name> <reason>')
async def unban(ctx, member:discord.User, *, reason=None):
    if reason == None:
        reason = f"No Reason Provided"
    await ctx.guild.unban(member, reason=reason)
    await ctx.send(f"{member.mention} has been **unbanned** by {ctx.message.author}", delete_after=1)
    ctx.message.delete()
    print(f"Sucsessfully unbanned {member.name}")

@commands.has_permissions(ban_members = True)
@bot.command(name = 'timeout', help = 'Timesout a member !timeout <member> <minutes>')
async def timeout(ctx, member: discord.Member, minutes: float):
    duration = datetime.timedelta(minutes=minutes)
    await member.timeout_for(duration)
    await ctx.send(f"Member timed out for {minutes} minutes by {ctx.message.author}",delete_after=1)
    await ctx.message.delete()
    print(f"Sucssessfully muted {member.name}")

@commands.has_permissions(ban_members = True)
@bot.command(name = 'untimeout', help = 'Untimes out a member !untimeout <member>')
async def untimeout(ctx, member: discord.Member):  
    await member.remove_timeout(reason=None)
    await ctx.send(f"{discord.member} has been untimed out by {ctx.message.author}",delete_after=1)
    await ctx.message.delete()
    print(f"Sucsessfully unmuted {member.name}")
bot.run(token)