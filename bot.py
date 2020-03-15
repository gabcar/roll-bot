"""bot.py

Author: Gabriel Carrizo
"""
import datetime
import importlib

import discord
import src.dice

with open('token') as f:
    TOKEN = f.read()

CLIENT = discord.Client()

def send_help(message):
    msg = '```Available commands:\n' \
              '"!roll [N]d[D]", rolls N (<500) dice with D faces and returns sum and sequence. \n'\
              '  optional:\n'\
              '   - dl: drop lowest\n'\
              '   - d[n]l: drop n lowest\n'\
              '   - dh: drop highest\n'\
              '   - d[n]h: drop n highest\n'\
              '   - +/-[N]d[D]\n'\
              '   - +/-i, where i is an integer\n'\
              '  example: !roll 6d6 dl d2h +4 \n'\
              '"!rollme", rolls 6 character stats with 4d6 drop lowest strategy for each stat.\n'\
              '  optional:\n'\
              '    - [N]d[D], determines the stat generation strategy. (4d6 default)\n'\
              '    - dl/d[n]l/dh/d[n]h, see options for !roll.\n' \
              '    - +/-[N]d[D], see options for !roll.' \
              '  example: !rollme 6d6 d2l +4d4 dh```'
    msg = '> ' + message.content + '\n' + msg
    return msg

def log_message(inmsg):
    timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
    log_message = timestamp + ': Received message\nfrom: {}-{}: "{}"'.format(
        inmsg.guild.name,
        inmsg.channel.name,
        inmsg.author.name,
        inmsg.content
    )
    return  log_message

def log_action(outmsg):
    timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())

    if outmsg:
        log_message = '\nReplied with:\n {}'.format(
            outmsg
        )
    else:
        log_message = 'NO ACTION'

    return log_message

@CLIENT.event
async def on_message(message):

    # we do not want the bot to reply to itself
    if message.author == CLIENT.user:
        return
    # we dont care about messages that dont start with '!'
    if message.content[0] != '!':
        return

    log = log_message(message)

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
            msg = '> ' + message.author.name + ': '+ \
                message.content + '\n' + src.dice.parse_rolls_to_string(options)
        await channel.send(msg)
        
    # !rollme - Generate character
    elif command == '!rollme':
        # quote input message + output
        msg = '> ' + message.author.name + ': ' + message.content + \
            '\n' + src.dice.roll_character(options)
        await channel.send(msg)

    # Ignore logging commands that are not for rollbot
    else:
        return
    
    log += log_action(msg)

    print(log)
   
@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    print('------')

def main():
    CLIENT.run(TOKEN)

if __name__ == '__main__':
    main()
