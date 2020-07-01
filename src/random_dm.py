import random
import re
import shlex

from discord.utils import get

FILTERED_IDS = [615507038344314880, 624952320979107860]

def add_member(name, members):
    members.append(FakeMember(name))
    return members

def remove_member(name, members):
    if '#' in name:
        name, disc = name.split('#')
        print(name, disc)

        members =  [m for m in members 
                    if not (m.discriminator == disc and m.name == name)]
    else:
        members = [m for m in members if m.name != name]

    return members

def join_commands(options):
    options = ' '.join(options)
    options = shlex.split(options)

    return options

def parse_commands(options, members):
    options = join_commands(options)
    print('IN PARSE', options)
    for o in options:
        print(o)
        if o[0] == '-':
            members = remove_member(o[1:], members)
        elif o[0] == '+':
            members = add_member(o[1:], members)
    print([m.name for m in members])

    return members

def to_message(member):
    if member.discriminator:
        return 'Congratulations `{}#{}` - you have been seleted to DM a session!'.format(
            member.name, member.discriminator
        )
    else:
        return 'Congratulations `{}` - you have been seleted to DM a session!'.format(
            member.name
        )


def get_random_dm(options, channel):
    # filter bots
    initial_members = [m for m in channel.members
               if not m.bot]
    members = [m for m in initial_members]

    members = parse_commands(options, members)

    random_dm = random.choice(members)

    print('Selected DM: {}\nFrom initial members: {}\nFiltered pool: {}\n From commands: {}'.format(
        random_dm.name,
        [m.name+'#'+m.discriminator for m in initial_members],
        [m.name+'#'+m.discriminator for m in members],
        ' '.join(options)
    ))

    return to_message(random_dm)

class FakeMember:
    def __init__(self, name, discriminator=''):
        self.name = name
        self.discriminator = discriminator
