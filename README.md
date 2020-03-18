# Roll-bot
Discord bot for rolling D&D related things.

## Invite link: 
```
https://discordapp.com/api/oauth2/authorize?client_id=624952320979107860&permissions=2048&scope=bot
```

## Usage:
```
Available commands:
"!roll [N]d[D]", rolls N (<500) dice with D faces and returns sum and sequence.
  optional:
   - dl: drop lowest
   - d[n]l: drop n lowest
   - dh: drop highest
   - d[n]h: drop n highest
   - +/-[N]d[D]
   - +/-i, where i is an integer
  example: !roll 6d6 dl d2h +4
"!rollme", rolls 6 character stats with 4d6 drop lowest strategy for each stat.
  optional:
    - [N]d[D], determines the stat generation strategy. (4d6 default)
    - dl/d[n]l/dh/d[n]h, see options for !roll.
    - +/-[N]d[D], see options for !roll.  example: !rollme 6d6 d2l +4d4 dh
```

### Examples:

Basic !roll example:
```
!roll 5d6 d2l
```

Interpretation: Roll five six sided dice and drop the 2 lowest

Output: 
```
Individual Rolls: 6, 4, 6
Sum: 16
Dropped: 3, 3
```

Chaining commands:
```
!roll 5d6 dl +3d4 dh +4
```

Interpretation: Roll five six sided dice and drop the lowest, then add the
rolls from three four sided dice, drop the highest from the total dice outcomes
and add 4 to the total sum.

Output:
```
Individual Rolls: 2, 4, 4, 3, 2, 4
Sum: 23
Dropped: 1, 6
```
