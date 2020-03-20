import os
import time

from src.dice import do_roll_instruction
from src.dice import Rolls

class RollBotError(Exception):
    pass

def timed(func):
    def func_wrapper(*args, **kwargs):
        before = time.time()
        out = func(*args, *kwargs)
        time_elapsed = round(1000 * (time.time() - before), 2)
        print('Operation time: {}ms'.format(time_elapsed))
        return out
    return func_wrapper

def raises_error(func):
    def func_wrapper(*args, **kwargs):
        out = func(*args, *kwargs)
        if out == 1:
            raise RollBotError("Invalid input format.")
        return out
    return func_wrapper

@raises_error
def get_cr_interval(cr):
    if cr >= 0 and cr <=4:
        return '0-4' 
    elif cr >= 5 and cr <=10:
        return '5-10'
    elif cr >= 11 and cr <=16:
        return '11-16'
    elif cr >= 17:
        return '17'
    else:
        return -1

def is_in_interval(i, interval):
    interval = interval.split('-')
    if len(interval) == 2:
        lower = int(interval[0])
        higher = int(interval[1])
        return (i >= lower and i <= higher)
    elif len(interval) == 1:
        return i == int(interval[0])
    else:
        return False

def roll_on_table(file_contents, dice):
    # Calculate treasure
    roll = do_roll_instruction(Rolls([]), dice).sum()
    for line in file_contents:
        line_contents = line.split(',')
        if is_in_interval(roll, line_contents[0]):
            return line_contents
    return False

def get_gems_or_art(line):
    if line == '-':
        return []

    loot = []

    line_contents = line.split(' ')

    n = do_roll_instruction(Rolls([]), line_contents[0]).sum()
    value = line_contents[1]
    currency = line_contents[2].lower()
    category = line_contents[3].lower()# gems or art
    
    path = 'assets/item-tables/{}/{}.csv'.format(category, value)

    with open(path) as f:
        file_contents = f. read().splitlines() 
    dice = '1' + file_contents[0].split(',')[0]
    
    for _ in range(n):
        l = roll_on_table(file_contents[1:], dice)
        # some clean up
        l = ','.join(l[1:])
        l = l.replace('"', '')
        l = l.split(' (')[0] # remove description
        l = l + ' (' + value + currency + ')'
        loot.append(l)
    unique = set(loot)

    loot = ['{}x {}'.format(loot.count(item), item) for item in unique]

    return loot

def get_magic_items(line):
    if line == '-':
        return []
    commands = line.replace('Roll ', '').replace('.', '')
    commands = commands.split(' and ')

    loot = []
    
    for command in commands:
        c = command.split(' ')
        if c[0] == 'once':
            n = 1
        else:
            n = do_roll_instruction(Rolls([]), c[0]).sum()
        table = c[-1]

        path = 'assets/item-tables/magic-items/{}.csv'.format(table)

        with open(path) as f:
            table = f. read().splitlines() 
        dice = '1' + table[0].split(',')[0]

        for _ in range(n):
            line = roll_on_table(table[1:], dice)
            line = ','.join(line[1:])
            line = line.replace('"', '')
        loot.append(line)
    return loot

def get_hoard_loot(cr):
    cr_interval = get_cr_interval(int(cr[0]))

    path = 'assets/treasure-tables/hoard'\
         + '/' + '{}.csv'.format(cr_interval)
        
    with open(path, 'r') as f:
        contents = f. read().splitlines() 
        
    # Calculate coins
    coin_header = contents[0].split(',')
    coin_table = contents[1]
    coin_table = coin_table.lower().split(',')
    coins = dict(zip(coin_header[1:], coin_table[1:]))
    coins = {c: v.split(' x ') for c, v in coins.items() if v != '-'}
    coins = {c: do_roll_instruction(Rolls([]), v[0]).sum() * int(v[1])
                for c, v in coins.items()}

    # roll on treasur table
    dice = '1' + contents[2].split(',')[0]
    treasure_line = roll_on_table(contents[3:], dice)
    gems_or_art = get_gems_or_art(treasure_line[1])
    magic_items = get_magic_items(treasure_line[2])

    coins = ', '.join(["{}{}".format(v, c) for c, v in coins.items()])
    items = ', '.join(gems_or_art + magic_items)

    str = 'Coins: {}'.format(coins)
    str += '\nItems: {}'.format(items) * (len(items) > 0)
    str = '```' + str + '```'

    return str # '```\nItems: {}```'.format(coins, items)


def main():
    get_hoard_loot(11)

if __name__ == '__main__':
    main()