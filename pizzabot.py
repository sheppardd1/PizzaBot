'''
Purpose: 
 - Allow users to request a specific number of pizza slices.
 - Each person pays proportionally to how many slices they requested.

Usage:
 - All actions are done with slash commands. 
 - The only command is "/pizza"
 - The command requires exactly 1 argument.
 - The arguments are case-insensitive.

Usage examples:
 - Request 2 slices: /pizza 2
 - Request the total number of pizzas that need to be ordered: /pizza total
 - Tell the bot that the total cost is $50 and see the cost breakdown: /pizza $50
 - Reset all values: /pizza reset
 - Get help: /pizza help

A few notes:
 - If a user calls the bot with a number multiple times, their "slices" array value will be updated, not appended to the array.
 - If a user runs the bot with a bad argument, print out a little help menu.
 - Your guild's ID and the bot's key value must be stored in a file called keys.py in the same directory as this script.

Is it well-organized and optimized? No. Does it work? Yes (I think so).
'''

import discord                      # pip install discord.py
from discord import app_commands
from keys import my_guild, bot_id   # this is the local keys.py file that should be saved in same directory

# initiate values for later use
slices = {}
total_cost = 0
num_pizzas = 0
SLICES_PER_PIZZA = 8

# function to determine if a string can be converted to a float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# set things up
intents = discord.Intents.none()                # set up intents and opt out of them by using none()
client = discord.Client(intents=intents)        # create a client instance
bot_cmd_tree = app_commands.CommandTree(client) # create command tree instance to make commands for bot

# set up the command tree
@bot_cmd_tree.command(
    name="pizza",
    description="Get pizza! Type \"/pizza help\" for options.",
    guild=discord.Object(id=my_guild)   # my_guild is defined in keys.py file
)

# set up async function to respond to commands
async def get_input(interaction, item: str):
    global slices
    # if numeric, user is requesting N slices
    if item.isnumeric():
        # store value in a dictionary with key=username
        slices[interaction.user.name] = (int(item))
        # print number of slices requested
        await interaction.response.send_message(f"{interaction.user.name} requested {slices[interaction.user.name]} slices.")
    # if resetting all values, wipe variables and print confirmation
    elif item.upper() == "RESET":
        slices = {}
        total_cost = 0
        num_pizzas = 0
        await interaction.response.send_message(f"Values have been reset.")
    # if user is requesting total number of pizzas to order, divide total by SLICES_PER_PIZZA and round up
    elif item.upper() == "TOTAL":
        sum_slices = sum(slices.values())
        if sum_slices == 0:
            await interaction.response.send_message("Error: No slices have been requested yet.")
        else:
            num_pizzas = -(-sum_slices // SLICES_PER_PIZZA)
            if num_pizzas == 1:
                msg = f"We need to buy {num_pizzas} pizza."
                msg += f"\nPlease enter the total cost of the pizza (example: `/pizza $12.34`)."
            else:
                msg = f"We need to buy {num_pizzas} pizzas."
                msg += f"\nPlease enter the total cost of the pizzas (example: `/pizza $12.34`)."
            await interaction.response.send_message(msg)
    # if user entered money value (starts with '$')
    elif item.startswith('$') and is_float(item[1:]):
        # get stats: cost and total slices ordered
        total_cost = float(item[1:])
        sum_slices = sum(slices.values())
        if sum_slices != 0:
            # do the 'total' calculations in case user didn't run that function yet
            sum_slices = sum(slices.values())
            num_pizzas = -(-sum_slices // SLICES_PER_PIZZA)
            if num_pizzas == 1:
                results = f"We need to buy {num_pizzas} pizza.\n"
            else:
                results = f"We need to buy {num_pizzas} pizzas.\n"

            # get percentage of ordered slices to total slices
            slice_ratio = sum_slices / (num_pizzas * SLICES_PER_PIZZA)
    
            # get cost per person (cost * ratio requested)
            cost = slices.copy()
            for k, v in cost.items():
                cost[k] = total_cost * slices[k] / sum_slices
    
            # get available slices per person by scaling based on number they requested
            slices_scaled = slices.copy()
            for k, v in slices_scaled.items():
                slices_scaled[k] = int(v / slice_ratio)
   
            # print number of extra slices not assigned due to rounding 
            extra_slices = num_pizzas * SLICES_PER_PIZZA - sum(slices_scaled.values())
    
            # get string of results
            results += "Here is the breakdown:\n"
            # person gets N slices for $M (requested X slices)
            for k, v in slices.items():
                 results += f"- **{k}** gets {slices_scaled[k]} slices for **${cost[k]:.2f}** (requested {slices[k]})\n"
            # extras
            if extra_slices == 1:
                results += f"There will be {extra_slices} extra slice."
            else:
                results += f"There will be {extra_slices} extra slices."

            # send the message
            await interaction.response.send_message(results)

        # don't divide by 0
        else:
            await interaction.response.send_message("Error: No slices have been requested yet.")
    
    # else, command is invalid - print help menu
    else:
        await interaction.response.send_message('Welcome to the pizza ordering bot! \n'
            'Enter a command like this: `/pizza <command>`\n'
            'Here are the available commands:\n'
            '`/pizza help` (Display this help message)\n'
            '`/pizza reset` (Reset all values)\n'
            '`/pizza total` (Calculate the number of pizzas needed)\n'
            '`/pizza $N` (Set the total cost to $N and calculate how much each person owes)\n'
            '`/pizza N` (Request N slices)') 

# tell us when everything is ready to go
@client.event
async def on_ready():

    await bot_cmd_tree.sync(guild=discord.Object(id=my_guild))
    print("Ready!") 

# actually run the bot
client.run(bot_id)

