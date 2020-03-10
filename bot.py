"""bot.py
"""
import discord
from src.dice import parse_rolls_to_string, roll_character

def send_help(message):
    msg = 'Available commands:\n' \
              '"!roll [N]d[D]", rolls N dice with D faces and returns sum and sequence. \n'\
              '  optional:\n'\
              '   - dl: drop lowest\n'\
              '   - d[n]l: drop n lowest\n'\
              '   - dh: drop highest\n'\
              '   - d[n]h: drop n highest\n'\
              '  example: !roll 6d6 dl d2h \n'\
              '"!rollme", rolls 6 character stats with 4d6 drop lowest strategy for each stat.\n'\
              '  optional:\n'\
              '    - [N]d[D], determines the stat generation strategy.\n'\
              '    - dl/d[n]l/dh/d[n]h, see options for !roll.\n' \
              '  example: !rollme 6d6 d2l dh'
    msg = '> ' + message.content + '\n' + msg
    return msg

def log(inmsg, outmsg):
    print('Received message from {}: "{}"\nReplied with:\n {}'.format(
        inmsg.author.name, inmsg.content, outmsg
    ))



with open('token') as f:
    TOKEN = f.read()

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    channel = message.channel
    
    argument = message.content.split(' ')

    command = argument[0]
    options = argument[1:]

    # Send help to specific user
    if command == '!rollbothelp':
        msg = send_help(message)
        await message.author.send(msg)

    # !roll - roll dice
    elif command == '!roll':
        if not options:
            msg = 'Incorrect format. Required format "!roll NdD", ex: "!roll 4d6"'
        else:
            # quote input message + output
            msg = '> ' + message.content + '\n' + parse_rolls_to_string(options)

        await channel.send(msg)

    # Generate character
    elif command == '!rollme':
        # quote input message + output
        msg = '> ' + message.author.name + ': ' + message.content + '\n' + roll_character(options)
        await channel.send(msg)
        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
