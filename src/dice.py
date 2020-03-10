import numpy as np

def is_message(func):
    """Function decorator that ensures that the
    returned value is a string
    
    Args:
        func (function): the target function
    
    Returns:
        func: the target function, wrapped.
    """
    def func_wrapper(*args, **kwargs):
        returned_value = func(*args, **kwargs)
        assert isinstance(returned_value, str)
        return returned_value
    return func_wrapper

def dice(d):
    """A dice module that rolls a dice with d sides.
    
    Args:
        d (int): the number of faces of the dice
    
    Returns:
        int: [1, d]
    """
    return np.random.randint(1, d+1)

def roll_dice(n, d):
    """rolls n (int) dice with value d (int)
    
    Args:
        n (int): number of dices to roll
        d (int): dice face value
    
    Returns:
        Rolls: Object containing the rolls
    """
    r = Rolls([])

    for _ in range(n):
        i = dice(d)
        r.append(i)

    return r

def parse_rolls(args):
    """Parses inputs from discord message to roll
    a specific number of dice with additional options.

    Required format for roll:
    "!roll [N]d[D] [options]" (note that "!roll" is 
        trimmed from the string)

    Possible options: 
    dl - drop lowest
    d[n]l - drop n lowest 
    dh - drop highest
    d[n]h - drop n highest
    
    Args:
        options (str): input from discord message
    
    Returns:
        str : Bot message
    """
    try: 
        n, d = args[0].split('d')
        rolls = roll_dice(int(n),int(d))
    except:
        return 'Invalid input format ("!roll NdD" Ex: "!roll 4d6")'

    if len(args) > 1:
        for o in args[1:]:
            error = parse_options(rolls, o)
            if error: 
                return error

    return rolls

@is_message
def parse_rolls_to_string(args):
    return parse_rolls(args).__str__()

def parse_options(rolls, option):
    """Parses the options of the discord message
    
    Args:
        rolls (Rolls): generated rolls in a Rolls object.
        option (str): message parts of the input
    
    Returns:
        str: potential error message
    """
    try: 
        if option[0] == 'd':
            instruction = option[-1]

            if len(option) > 2:
                n = int(option[1:-1])
            else: 
                n = 1

            for _ in range(n):
                rolls.drop(instruction)

            return ''
        else: 
            return 'Error: Invalid option(s): {}'.format(option)
    except: 
        return 'Error: Invalid option(s): {}'.format(option)

@is_message    
def roll_character(args):
    if args:
        c = Character()
        c.roll_stats(args)
    else:
        c = Character()
        c.roll_stats(['4d6', 'dl'])
    return c.__str__()

class Rolls():
    """Class for managing an array of rolls.

    Has handy functions for adding rolls to the array, 
    calculating the sum, dropping lowest or highest.
    """    
        
    def __init__(self, rolls):
                
        self.rolls = rolls
        self.dropped = []

    def __repr__(self):        
        return ', '.join(self.rolls)

    def __str__(self):
        rolls = ', '.join([str(r) for r in self.rolls])
        rolls = 'Individual Rolls: ' + rolls

        s = '\nSum: {}'.format(self.sum())

        if self.dropped:
            drop = '\nDropped: {}'.format(', '.join([str(r) for r in self.dropped]))
        else: 
            drop = ''

        return rolls + s + drop
    
    def append(self, s):
        self.rolls.append(s)

    def sum(self):
        return sum(self.rolls)

    def drop_lowest(self):
        self.dropped.append(
            self.rolls.pop(np.argmin(self.rolls))
        )

    def drop_highest(self):
        self.dropped.append(
            self.rolls.pop(np.argmax(self.rolls))
        )
    
    def drop(self, instruction):
        if instruction == 'l':
            self.drop_lowest()
        elif instruction == 'h':
            self.drop_highest()

class Character:

    def __init__(self):
        self.stats = {'STR': 0,
                      'DEX': 0,
                      'CON': 0,
                      'INT': 0,
                      'WIS': 0,
                      'CHA': 0}

    def roll_stats(self, command):
        for stat in self.stats:
            rolls = parse_rolls(command)
            self.stats[stat] = rolls.sum()
    
    def __str__(self):
        s = ''

        for stat in self.stats:
            s += stat + ': ' + str(self.stats[stat]) + '\n'

        return s