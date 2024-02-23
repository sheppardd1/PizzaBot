# PizzaBot
A Discord bot for organizing pizza ordering

## Purpose: 
 - Allow users to request a specific number of pizza slices.
 - Each person pays proportionally to how many slices they requested.

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
