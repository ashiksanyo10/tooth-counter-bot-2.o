import os
import discord
from discord.ext import commands
from discord import Embed
from dotenv import load_dotenv
import json

def configure():
    load_dotenv()

configure()
    

bt = os.getenv('API_KEY')

# File to save the counts
COUNT_FILE = 'counts.json'

# Load counts from the file if it exists
def load_counts():
    if os.path.exists(COUNT_FILE):
        try:
            with open(COUNT_FILE, 'r') as file:
                data = json.load(file)
                return data.get('cids_count', 57), data.get('edc_count', 29)
        except Exception as e:
            print(f"Error reading counts file: {e}")
            return 57, 29
    return 57, 29

# Save counts to the file
def save_counts(cids_count, edc_count):
    try:
        with open(COUNT_FILE, 'w') as file:
            json.dump({'cids_count': cids_count, 'edc_count': edc_count}, file)
    except Exception as e:
        print(f"Error saving counts file: {e}")

cids_count, edc_count = load_counts()

# Initial save to ensure the file is created if it does not exist
save_counts(cids_count, edc_count)

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def update_counts(channel, operation):
    global cids_count, edc_count

    if operation == '🦷':
        edc_count += 1
        await channel.send(f"**Ka-ching!** 💰\n"
                           f"Guess what? Another tooth decided to hide under the pillow and wait for the Tooth Fairy! 🦷🎉\n"
                           f"Now, our grand total of knocked-out teeth is {cids_count + edc_count}! Keep smiling! 😁🪥")
    elif operation == '🦴':
        edc_count -= 1
        await channel.send(f"**Oh snap!** 🤗\n"
                           f"No teeth extraction this time, but remember to brush well! 🪥🦷\n"
                           f"Total tooth knocked out is still {cids_count + edc_count}, keep shining those pearly whites! 😁🪥")

    # Save counts to the file after updating
    save_counts(cids_count, edc_count)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hi(ctx):
    await ctx.send("Hey Cutie <3")
    
@bot.command()
async def info(ctx):
    await ctx.send("🌟✨ Hey there, Adorable Smiles! ✨🌈\n"
                   "I'm your Fluffy Tooth Fairy Bot, fluttering in to keep track of the whimsical tooth tales spun by our Dayana!💖\n"
                   "Get ready for a sprinkle of enchantment as we journey together through the magical realm of tooth extractions! 🌟🦷✨")

@bot.command()
async def total(ctx):
    total_count = cids_count + edc_count
    await ctx.send(f"🦄🌈 Tooth Count Update: {total_count}! Keep sparkling, little teeth! 😁✨")

@bot.command()
async def tap(ctx, operation):
    if operation == '🦷' or operation == '🦴':
        await update_counts(ctx.channel, operation)
    else:
        await ctx.send("🚫 Invalid operation. Use 🦷 to add or 🦴 to subtract.")

@bot.command(name='guide')
async def custom_help(ctx):
    embed = Embed(
        title="🌟✨ **Tooth Fairy Bot Commands** ✨🦷",
        description="Embark on this whimsical journey with the Tooth Fairy Bot 🌈🪥✨",
        color=0xFFD700  # You can set the color to something visually appealing
    )

    commands_list = [
        ("`!hi`", "Greet the tooth fairy bot with a cute message!🎀"),
        ("`!info`", "Learn about the magical tooth fairy bot and its purpose 💾"),
        ("`!total`", "Discover the total count of bravely departed teeth 💎"),
        ("`!tap 🦷`", "Increase the tooth count with a sprinkle of magic 👻"),
        ("`!tap 🦴`", "Decrease the tooth count, sometimes we make a mistake 😛!"),
        ("`!guide`", "Display this enchanting list of commands 🧰"),
        ("`!ToothBank`", "View the current counts stored in the JSON file 📊")  # Added new command
    ]

    for command, description in commands_list:
        embed.add_field(name=command, value=description, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def ToothBank(ctx):
    try:
        with open(COUNT_FILE, 'r') as file:
            data = json.load(file)
            cids_count = data.get('cids_count', 57)
            edc_count = data.get('edc_count', 29)
            await ctx.send(f"Current counts stored in the JSON file:\n"
                           f"CID Count: {cids_count}\n"
                           f"EDC Count: {edc_count}\n"
                           f"Total Count: {cids_count + edc_count}")
    except FileNotFoundError:
        await ctx.send("Counts file not found. Default values are being used.")

bot.run(bt)
