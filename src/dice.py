import random
import re

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

def is_roll_instruction(instruction):
    """returns True if instruction is XdY

    Args:
        instruction (bool): True if instruction is XdY where X and Y are ints
    """

    if re.match('^\d+[d]\d+$', instruction):
        return True
    else: 
        return False

def is_drop_instruction(instruction):
    """returns True if instruction is XdY

    Args:
        instruction (bool): True if instruction is XdY where X and Y are ints

    Returns:
        bool: True if drop instruction
    """

    if re.match('^[d][hl]$', instruction):
        return True
    elif re.match('^[d]\d+[lh]$', instruction): 
        return True
    else:
        return False

def is_math_expression(instruction):
    """Returns True if the instructions contains a
    mathematical expression

    Args:
        instruction ([type]): [description]

    Returns:
        bool: True if instruction is math expr.
    """
    # +/-i
    if re.match('^[\+\-]\d+$', instruction):
        return True
    # +/-NdD
    elif re.match('^[\+\-]\d+[d]\d+$', instruction):
        return True
    else:
        return False

def do_roll_instruction(rolls, instruction):
    """Parses roll instruction from 'NdD' to int(N) and int(D)
    
    Args:
        instruction (str): roll instruction
    
    Raises:
        IndexError: 
    
    Returns:
        [type]: [description]
    """
    n, d = instruction.split('d')

    n = int(n)
    d = int(d)

    if n < 0 or d < 0:
        raise IndexError('No negative roll numbers or dice types allowed')
    elif n >= 500:
        raise IndexError('Maximum dice restricted to <= 500')

    rolls.add(roll_dice(n, d))
    
    return rolls

def do_drop_instruction(rolls, instruction):
    """Parses drop instruction from 'dNl/h' to function 
    
    Args:
        instruction (str): roll instruction

    Returns:
        int, str: number of drops to make, which type to drop ('l' or 'h')
    """ 
    drop_type = instruction[-1]

    if len(instruction) > 2:
        n = int(instruction[1:-1])
    else:
        n = 1

    for _ in range(n):
        rolls.drop(drop_type)

    return rolls

def do_math_instruction(rolls, instruction):

    if re.match('^[\+]\d+$', instruction):
        rolls.add(int(instruction[1:]))

    elif re.match('^[\-]\d+$', instruction):
        rolls.subtract(int(instruction[1:]))

    elif re.match('^\+\d+[d]\d+$', instruction):
        rolls.add(do_roll_instruction(Rolls([]), instruction[1:]))

    elif re.match('^\-\d+[d]\d+$', instruction):
        rolls.subtract(do_roll_instruction(Rolls([]), instruction[1:]))

    else:
        return # TODO: Error here
    
    return rolls

def dice(d):
    """A dice module that rolls a dice with d sides.
    
    Args:
        d (int): the number of faces of the dice
    
    Returns:
        int: [1, d]
    """
    return random.randint(1, d)

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


@is_message
def parse_rolls_to_string(args):
    """Parses rolls to string
    
    Args:
        args str: string with roll settings/options
        (ex '4d6 dl')
    
    Returns:
        str: outgoing message
    """    
    try:
        return perform_instruction(Rolls([]), args).__str__()
    except:
        return '```Incorrect format, check !rollbothelp for list of commands.```'

def perform_instruction(rolls, options, rd=0):
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
    +[N]d[D] - Adds a separate roll to the tally
    -[N]d[D] - subtracts a roll from the tally
    
    Args:
        options (str): input from discord message
    
    Returns:
        Rolls : total rolls
    """

    if not options:
        return rolls

    if rd == 0 and not is_roll_instruction(options[0]):
        raise IndexError('Incorrect format. see !rollbothelp for instructions')

    if is_roll_instruction(options[0]):
        rolls = do_roll_instruction(rolls, options[0])
        return perform_instruction(rolls, options[1:], rd+1)

    elif is_drop_instruction(options[0]):
        
        rolls = do_drop_instruction(rolls, options[0])
        return perform_instruction(rolls, options[1:], rd+1)

    elif is_math_expression(options[0]):
        rolls = do_math_instruction(rolls, options[0])
        return perform_instruction(rolls, options[1:], rd+1)

    else: 
        raise IndexError('Incorrect option {}'.format(options[0]))

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
    """Rolls character stats
    
    Args:
        args (str): Stat generation strategy from message (default 4d6 dl)
    
    Returns:
        str: Message to return to user
    """
    c = Character()
    if args:
        c.roll_stats(args)
    else:
        c.roll_stats(['4d6', 'dl'])
    return c.__str__()

def argmax(xs):
    """argmax because stdlib does not have argmax
    
    Args:
        xs (list): list or array of rolls
    
    Returns:
        int: index of the first greatest value of the list
    """    
    return max(enumerate(xs), key=lambda x: x[1])[0]

def argmin(xs):
    """argmin because stdlib does not have argmin
    
    Args:
        xs (list): list or array of rolls
    
    Returns:
        int: index of the first lowest value of the list
    """    
    return min(enumerate(xs), key=lambda x: x[1])[0]

class Rolls():
    """Class for managing an array of rolls.

    Has handy functions for adding rolls to the array, 
    calculating the sum, dropping lowest or highest.
    """    
        
    def __init__(self, rolls):
                
        self.rolls = rolls
        self.dropped = []
        self.bias = 0

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

        return '```' + rolls + s + drop + '```'
    
    def append(self, s):
        self.rolls.append(s)

    def add(self, s):
        if isinstance(s, int):
            self.bias += s
        elif isinstance(s, list):
            self.rolls.extend(s)
        elif isinstance(s, Rolls):
            self.rolls.extend(s.rolls)
    
    def subtract(self, s):
        if isinstance(s, int):
            self.bias -= s
        elif isinstance(s, list):
            self.rolls.extend([-i for i in s])
        elif isinstance(s, Rolls):
            self.rolls.extend([-i for i in s.rolls])

    def sum(self):
        return sum(self.rolls) + self.bias

    def drop_lowest(self):
        self.dropped.append(
            self.rolls.pop(argmin(self.rolls))
        )

    def drop_highest(self):
        self.dropped.append(
            self.rolls.pop(argmax(self.rolls))
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

    def roll_stats(self, instructions):
        for stat in self.stats:
            rolls = perform_instruction(Rolls([]), instructions)
            self.stats[stat] = rolls.sum()
    
    def __str__(self):
        s = ''

        for stat in self.stats:
            s += stat + ': ' + str(self.stats[stat]) + ' | '
        s = s[:-3]

        s = '```' + s + '```'

        return s

if __name__ == '__main__':
    assert is_roll_instruction('4d6') == True
    assert is_roll_instruction('20d5') == True
    assert is_roll_instruction('2d50') == True
    assert is_roll_instruction('40d50') == True
    assert is_roll_instruction('4D6') == False
    assert is_roll_instruction('dl') == False
    assert is_roll_instruction('dh') == False
    assert is_roll_instruction('+') == False
    assert is_roll_instruction('-') == False
    assert is_roll_instruction('+4d6') == False
    assert is_roll_instruction('-4d6') == False
    assert is_roll_instruction('bajs') == False

    assert is_drop_instruction('dl') == True
    assert is_drop_instruction('dh') == True
    assert is_drop_instruction('d2l') == True
    assert is_drop_instruction('d2h') == True
    assert is_drop_instruction('d2hl') == False
    assert is_drop_instruction('d2lh') == False
    assert is_drop_instruction('d20l') == True
    assert is_drop_instruction('d20h') == True
    assert is_drop_instruction('4d20ls') == False
    assert is_drop_instruction('4d20') == False
    assert is_drop_instruction('bajs') == False

    assert is_math_expression('+4') == True
    assert is_math_expression('-4') == True
    assert is_math_expression('+4d4') == True
    assert is_math_expression('-4d4') == True
    assert is_math_expression('+4') == True
    assert is_math_expression('4d6') == False
    assert is_math_expression('dl') == False
    assert is_math_expression('d6l') == False
    assert is_math_expression('-') == False
    assert is_math_expression('+') == False
    assert is_math_expression('bajs') == False

    # rolls = Rolls([])
    # rolls.add([1, 2, 3, 4, 5, 6])

    # do_drop_instruction(rolls, 'd2l')
    # assert rolls.sum() == sum([3, 4, 5, 6])

    # do_drop_instruction(rolls, 'd2h')
    # assert rolls.sum() == sum([3, 4])

    # do_drop_instruction(rolls, 'dh')
    # assert rolls.sum() == sum([3])

    # do_drop_instruction(rolls, 'dl')
    # assert rolls.sum() == 0

    # do_math_instruction(rolls, '+4')
    # assert rolls.sum() == 4

    # rolls.add([1, 2, 3, 4, 5, 6])

    print(parse_rolls_to_string(['4d6', 'dl', 'dh', '-4d4', '+10']))
    c = Character()
    c.roll_stats(['4d6', 'dl'])
    print(c)