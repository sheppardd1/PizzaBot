'''
Purpose: 
 - Allow users to request a specific number of pizza slices.
 - The payment can be calculated by one of two algorithms based on a hard-coded boolean:
    - Algorithm 1: Each person pays proportionally to how many slices they requested. Their alloted slice count may be increased from what they requested.
        --> SCALE_EXTRA_SLICES = True
    - Algorithm 2: The cost of the extra slices is divided evenly amonst each person.
        --> SCALE_EXTRA_SLICES = False

Payment Splitting Algorithms
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

# determine how to pay for extra slices - see note at the top of the page for description
SCALE_EXTRA_SLICES = False

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
        # if value is nonzero positive quantity
        if int(item) > 0:
            # store value in a dictionary with key=username
            slices[interaction.user.name] = (int(item))
            # print number of slices requested
            await interaction.response.send_message(f"{interaction.user.name} requested {slices[interaction.user.name]} slices.")
        # else if value is bad, but we already have this user listed in dict
        elif interaction.user.name in slices: 
            del slices[interaction.user.name]   # remove them from the dict
            await interaction.response.send_message(f"{interaction.user.name} requested {0} slices.")
        # else if value is bad and we haven't recorded them in the dict yet
        else:
            await interaction.response.send_message(f"Invalid value. type `/pizza help` for help.")

    # if resetting all values, wipe variables and print confirmation
    elif item.upper() == "RESET":
        slices = {}
        full_cost = 0
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
        full_cost = float(item[1:])
        sum_slices = sum(slices.values())
        if sum_slices != 0:

            slices_scaled, cost, extra_slices, results = price_math(slices, full_cost)
    
            # get string of results
            results += "Here is the breakdown:\n"
            # person gets N slices for $M (requested X slices)
            for k, v in slices.items():
                 if SCALE_EXTRA_SLICES:
                     results += f"- **{k}** gets {slices_scaled[k]} slices for **${cost[k]:.2f}** (requested {slices[k]})\n"
                 else:
                    results += f"- **{k}** gets {slices_scaled[k]} slices for **${cost[k]:.2f}**\n"
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
            '`/pizza N` (Request N slices for yourself)')
        
def price_math(slices_dict, total_cost):
    """Determine how much each person owes and how many extra slices are available.

    Input Args:
    slices_dict -- dictionary of person-to-slices -- {'person1': N, 'person2': M, ...}
    total_cost -- the cost of the whole order as provided by the user

    Output Values:
    1: dictionary of person-to-allowed-slices (this equals slices_dict if not SCALE_EXTRA_SLICES, else is scaled based on extra slices)
    2: dictionary of person-to-cost
    3: integer number of extra unclaimed slices
    4: string of partial results message
    """

    # do the 'total' calculations in case user didn't run that function yet
    total_requested_slices = sum(slices_dict.values())
    total_pizzas = -(-total_requested_slices // SLICES_PER_PIZZA)
    if total_pizzas == 1:
        results = f"We need to buy {total_pizzas} pizza."
    else:
        results = f"We need to buy {total_pizzas} pizzas."

    # if we want cost of extra slices to be split amongst each person in proportion to number of slices they requested
    if SCALE_EXTRA_SLICES:
        # get percentage of ordered slices to total slices
        slice_ratio = total_requested_slices / (total_pizzas * SLICES_PER_PIZZA)
        # get cost per person (cost * ratio requested)
        cost = slices_dict.copy()
        for k, v in slices_dict.items():
            cost[k] = total_cost * slices_dict[k] / total_requested_slices
        # get available slices per person by scaling based on number they requested
        slices_scaled = slices_dict.copy()
        for k, v in slices_dict.items():
            slices_scaled[k] = int(v / slice_ratio)
        # get number of extra slices not assigned due to rounding 
        extra_slices = total_pizzas * SLICES_PER_PIZZA - sum(slices_scaled.values())
        return slices_scaled, cost, extra_slices, results
    
    # else we want each person to pay the same amount to cover the extra slices
    else:
        # get number of extra slices
        extra_slices = total_pizzas * SLICES_PER_PIZZA - total_requested_slices
        cost_per_slice = total_cost / (total_pizzas * SLICES_PER_PIZZA)
        cost = {}
        for k, v in slices_dict.items():
            cost[k] = (slices_dict[k] + (extra_slices / len(slices_dict))) * cost_per_slice
        return slices_dict, cost, extra_slices, results


# tell us when everything is ready to go
@client.event
async def on_ready():

    await bot_cmd_tree.sync(guild=discord.Object(id=my_guild))
    print("Ready!") 

# actually run the bot
client.run(bot_id)

