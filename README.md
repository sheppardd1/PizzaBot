# PizzaBot
A Discord bot for organizing pizza ordering

## Purpose: 
 - Allow users to request a specific number of pizza slices.
 - The cost of the extra slices is split because on one of two algorithms as defined by the hard-coded `SCALE_EXTRA_SLICES` boolean.

## Usage:
 - All actions are done with slash commands. 
 - The only command is "/pizza"
 - The command requires exactly 1 argument.
 - The arguments are case-insensitive.

## Usage examples:
 - Request 2 slices: /pizza 2
 - Request the total number of pizzas that need to be ordered: /pizza total
 - Tell the bot that the total cost is $50 and see the cost breakdown: /pizza $50
 - Reset all values: /pizza reset
 - Get help: /pizza help

## A few notes:
 - If a user calls the bot with a number multiple times, their "slices" array value will be updated, not appended to the array.
 - If a user runs the bot with a bad argument, print out a little help menu.
 - Your guild's ID and the bot's key value must be stored in a file called keys.py in the same directory as this script.

## Algorithms Explanation:
 - Algorithm example: Alice requests 3 slices and Bob requests 1 slice; 1 pizza (8 slices) needs to be ordered for $10.
    - Algorithm 1: Alice pays $7.50 and is allotted 6 slices. Bob pays $2.50 and is allotted 2 slices. 0 extra slices remain.
       - Alice: made 3/4 of the request, so she pays for 3/4 of the total. She gets 3/4 of the slices (rounded down).
       - Bob: made 1/4 of the request, so he pays for 1/4 of the total. He gets 1/4 of the slices (rounded down).
    - Algorithm 2: Alice pays $6.25 for her 3 slices. Bob pays $3.75 for his 1 slice. 4 extra slices remain.
       - The cost per slice is $1.25
       - The cost of the extras is $5 total
       - Alice: ordered 3 slices, so she pays $3.75 for those 3 slices plus $2.50 (half the cost of the extra slices).
       - Bob: ordered 1 slice, so he pays $1.25 for that slice plus $2.50 (half the cost of the extra slices).
 - Another algorithm example: Alice requests 2 slices and Bob requests 1 slice; 1 pizza (8 slices) needs to be ordered for $10.
    - Algorithm 1: Alice pays $6.67 (2/3 of cost) and is allotted 5 slices. Bob pays $3.33 (1/3 of cost) and is allotted 2 slices. 1 extra slice remains.
       - Alice: made 2/3 of the request, so she pays for 2/3 of the total. She gets 2/3 of the slices (rounded down).
       - Bob: made 1/3 of the request, so he pays for 1/3 of the total. He gets 1/3 of the slices (rounded down).
    - Algorithm 2: Alice pays $5.62 for her 2 slices. Bob pays $4.38 for his 1 slice. 5 extra slices remain.
       - The cost per slice is $1.25
       - The cost of the extras is $6.25 total
       - Alice: ordered 2 slices, so she pays $2.50 for those 2 slices plus $3.125 (half the cost of the extra slices).
       - Bob: ordered 1 slice, so he pays $1.25 for that slice plus $3.125 (half the cost of the extra slices).
