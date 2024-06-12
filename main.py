import discord
from discord.ext import commands, tasks
import asyncio
import sqlite3
import math
import aiohttp
from datetime import datetime, timedelta, timezone
import random
import subprocess
from colors import color_names, color_list
import time
def install_pillow():
    try:
        # Run the pip installation command for Pillow
        subprocess.check_call(['pip', 'install', '-U', 'requests'])
        subprocess.check_call(['pip', 'install', '-U', 'json'])
        print("Pillow installed successfully!")
    except subprocess.CalledProcessError as e:
        print("Error occurred during Pillow installation:", e)

# Call the install_pillow function to install Pillow
install_pillow()

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
import numpy as np
import requests
import json


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-', intents=intents)
TOKEN = 'Your BOT Token'
guild_id = 'Your guild id'

# Connect to the database
connection = sqlite3.connect('levels.db')
cursor = connection.cursor()
last_message_timestamps = {}
# Create the levels table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS levels (
        user_id INTEGER PRIMARY KEY,
        level INTEGER DEFAULT 1,
        exp INTEGER DEFAULT 0,
        time REAL DEFAULT NULL,
        ballcoin INTEGER DEFAULT 0,
        claim_prize TEXT DEFAULT NULL,
        giveaway_boost INTEGER DEFAULT 0,
        insult INTEGER DEFAULT 0,
        joke INTEGER DEFAULT 0,
        OG_Claim BOOL DEFAULT TRUE,
        is_membership BOOL DEFAULT FALSE,
        palette TEXT DEFAULT RED,
        custom_role_id INTEGER DEFAULT 0,
        membership_date TEXT DEFAULT NULL
    )
''')

connection.commit()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    check_membership_time.start()

@bot.event
async def on_message(message):
    ctx =  await bot.get_context(message)
    import time
    if message.author.bot:
        print(message.author.bot, message.author)
        return  # Ignore the bot's own messages
    author = message.author
    cursor.execute('''
           SELECT time FROM levels WHERE user_id = ?''', (author.id,))
    result = cursor.fetchone()
    now = time.time()
    if result:
        last_message_time = result[0]
    else:
        last_message_time = result

    # Process the message content here
    message_content = message.content
    if len(message_content.split()) >= 3 and (last_message_time == None or now - last_message_time >= 45)  and message.channel.name != 'bots' and message.channel.name != 'speakerphone':
        exp_gain = random.randint(14,18)
        a = random.randint(1,50)
        if a == 50:
            b = random.randint(1, 20)
            embed = discord.Embed(title="Baller Loot Box", description="Congratulations, a baller lootbox has dropped",
                                  color=0xBA110F)
            if b <= 10:
                joke = 3
                insult = 0
                giveaway_boost = 0
                embed.add_field(name="Baller Loot", value="Joke Scroll = 3", inline=False)
            if b > 10 and b <= 15:
                joke = 5
                insult = 2
                giveaway_boost = 0
                embed.add_field(name="Baller Loot", value="Insult Scroll = 2\nJoke Scroll = 5", inline=False)
            if b > 15 and b <= 19:
                joke = 7
                insult = 4
                giveaway_boost = 0
                embed.add_field(name="Baller Loot", value="Insult Scroll = 4\nJoke Scroll = 7", inline=False)
            if b == 20:
                joke = 10
                insult = 5
                giveaway_boost = 1
                embed.add_field(name="Baller Loot", value="Giveaway Boost = 1\nInsult Scroll = 2\nJoke Scroll = 5",
                                inline=False)

            cursor.execute('''UPDATE levels SET giveaway_boost = giveaway_boost + ?, insult = insult + ?,
                                           joke = joke + ? WHERE user_id = ?''',
                           (giveaway_boost, insult, joke, author.id))
            await ctx.send(embed=embed)
        last_message_time = time.time()
    else:
        exp_gain = 0
    print(f'Message content: {message_content}')
    print(f'Author: {author}')
    #print(f'Word count: {word_count}')
    if exp_gain:
        print(f'Exp gain: {exp_gain}')


    # Update the user's level and exp
    cursor.execute('''
        INSERT OR IGNORE INTO levels (user_id) VALUES (?)''', (author.id,))
    cursor.execute('''
        UPDATE levels SET exp = exp + ?, time = ? WHERE user_id = ?''', (exp_gain,last_message_time, author.id))
    connection.commit()

    # Check if the user leveled up
    cursor.execute('''
        SELECT level, exp, ballcoin FROM levels WHERE user_id = ?''', (author.id,))
    result = cursor.fetchone()
    if result:
        level = result[0]
        exp = result[1]
        ballcoin = result[2]
        exp_required = math.ceil((level + 5) ** 2.8)  # Formula for exp requirement increase (10 times harder)
        ballcoin = round(((level -1)**1.10*100)/10)*10 +50
        if ballcoin > 200:
            ballcoin = 200
        if exp >= exp_required:
            # Reset exp to 0 after level up
            new_exp = exp - exp_required
            cursor.execute('''
                       UPDATE levels SET level = level + 1, exp = ?, ballcoin = ballcoin + ? WHERE user_id = ?''', (new_exp, ballcoin, author.id))
            await message.channel.send(f'{author.name} has leveled up to level {level + 1} and has gained {ballcoin} ball coins')



    await bot.process_commands(message)

@bot.command()
async def level(ctx, user: discord.Member = None):
    print(ctx.guild.id)
    if user == None:
        user = ctx.author
    author = ctx.message.author
    cursor.execute('''
        SELECT level, exp FROM levels WHERE user_id = ?''', (author.id,))
    result = cursor.fetchone()
    if result:
        level = result[0]
        exp = result[1]
        exp_required = math.ceil((level + 5) ** 2.8)
        response = f'Hello {author.name}! Your current level is {level}.'
        response += f' You have {exp} exp. Next level requires {exp_required} exp.'
        balls = Image.open('balls.jpg')
        avatar_url = str(author.avatar.url)
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    avatar_image = Image.open(BytesIO(data))
                    avatar_image = avatar_image.resize((400, 400))

                    # Create a circular mask
                    mask = Image.new("L", (400, 400), 0)
                    mask_array = np.array(mask)
                    h, w = mask_array.shape[:2]
                    radius = min(w, h) // 2
                    center = (w // 2, h // 2)
                    y, x = np.ogrid[:h, :w]
                    mask_array[((y - center[1]) ** 2 + (x - center[0]) ** 2) < radius ** 2] = 255
                    mask = Image.fromarray(mask_array)

                    # Create a new image with transparent background for the avatar
                    circular_avatar = Image.new("RGBA", (400, 400), (0, 0, 0, 0))

                    # Paste the cropped avatar onto the blank image using the mask
                    circular_avatar.paste(avatar_image, (0, 0), mask=mask)

                    # Create a new image with transparent background for the result
                    result_image = Image.new("RGBA", balls.size, (0, 0, 0, 0))

                    # Paste the circular avatar onto the result image
                    result_image.paste(circular_avatar, (53, 47))

                    # Paste the result image onto the balls image
                    balls.paste(result_image, (0, 0), mask=result_image)

                    balls.save('profile.jpg')
                    baller =Image.open('profile.jpg')
                    I1 = ImageDraw.Draw(baller)
                    # Custom font style and font size (different for different texts)
                    myFont = ImageFont.truetype('minecraft_font.ttf', 40)
                    myFont2 = ImageFont.truetype('minecraft_font.ttf', 135)
                    myFont3 = ImageFont.truetype('minecraft_font.ttf', 45)

                    # Add Text to an image
                    I1.text((425, 42), author.name, font=myFont, fill=(255, 255, 255))
                    I1.text((800, 128), f'Level {str(level)}', font=myFont2, fill=(255, 255, 255))
                    I1.text((1050, 646), f'exp: {str(exp)}/{str(exp_required)}', font=myFont3, fill=(255, 255, 255))
                    exp_per = exp/exp_required
                    bar_fill_x = (1350 * exp_per) + 128
                    I1.rectangle([(128,718),(bar_fill_x,849)], fill = (255,0,0))
                    baller.save('profilewt.jpg')
                    await ctx.send(file=discord.File('profilewt.jpg', filename='profilewt.jpg'))
                else:
                    await ctx.send("Failed to retrieve avatar image.")

    else:
        response = f'Hello {author.name}! You have not earned any levels yet.'
    await ctx.send(response)


@bot.command()
async def balls(ctx):
    user = ctx.message.author
    cursor.execute('SELECT OG_Claim FROM levels WHERE user_id = ?',(user.id,))
    result = cursor.fetchone()
    OG_time_str = "2023-03-01 00:00:00"
    OG_time = datetime.strptime(OG_time_str,"%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    join_date = user.joined_at
    balls = result[0]
    if join_date < OG_time:
        if balls:
            embed = discord.Embed(title= "**Congratulations, you're an OG Baller**",
                                  description="**__The OG Baller Pack__**\n\n**Joke Scroll** = 10\n\n**Roast Scroll** = 5\n\n**Giveaway Boost** = 1",
                                  color= 0xBA110F)
            await ctx.send(embed=embed)
            cursor.execute('''UPDATE levels SET giveaway_boost = giveaway_boost + 1, insult = insult + 5,
                            joke = joke + 10, OG_Claim = False WHERE user_id = ?''',(user.id,))

        else:
            await ctx.send("You've already claimed the OG baller pack")
    else:
        await ctx.send("You're not an OG Baller")
    connection.commit()



@bot.command(name= 'ballcoin', aliases=['bc'])
async def ballcoin(ctx):
    is_owner = discord.utils.get(ctx.author.roles, name='Owner') is not None
    is_big_menacing_role = discord.utils.get(ctx.author.roles, name='menacing hammer') is not None
    args = ctx.message.content.split()
    author = ctx.message.author
    if (is_owner or is_big_menacing_role) and len(args) == 4 and (args[1] == 'give' or args[1] == 'take'):
        if len(args) >= 2 and len(args)  < 3:
            await ctx.send("Invalid command usage!")
            return
        action = args[1].lower()
        # allows users to use mentions or user_id (as per Lectryn's request)
        try:
            target_user = ctx.message.mentions[0]
            target_user_id = str(target_user.id)
        except:
            target_user_id = str(args[2])
            target_user =  await bot.fetch_user(target_user_id)
        cursor.execute('''
              SELECT ballcoin FROM levels WHERE user_id = ?''', (target_user_id,))
        result = cursor.fetchone()
        ballcoins = result[0]
        if action == 'give':
            amount = int(args[3])
            ballcoins += amount
            cursor.execute('''
                    UPDATE levels SET ballcoin = ? WHERE user_id = ?''', (ballcoins, target_user_id))
            connection.commit()
            await ctx.send(f"Gave {amount} ballcoins to {target_user.name}")
        elif action == 'take':
            amount = int(args[3])
            ballcoins -= amount
            if ballcoins < 0:
                ballcoins = 0
            cursor.execute('''
                                UPDATE levels SET ballcoin = ? WHERE user_id = ?''', (ballcoins, target_user_id))
            connection.commit()
            await ctx.send(f"Took {amount} ballcoins from {target_user.name}")
        else:
            await ctx.send("Invalid action. Please use 'give' or 'take'.")
    if len(args) == 1:
        user_id = str(ctx.author.id)
        cursor.execute('''
                      SELECT ballcoin FROM levels WHERE user_id = ?''', (user_id,))
        result = cursor.fetchone()
        ballcoins = result[0]
        if ballcoins > 0:
            await ctx.send(f"You have {ballcoins} ballcoins.")
        else:
            await ctx.send("You don't have any ballcoins.")
    if len(args) == 2:
        #ballcoin daily reward claim
        if args[1] == 'claim':
            user_id = str(ctx.author.id)
            current_time = datetime.now()
            cursor.execute('''SELECT claim_prize, ballcoin FROM levels WHERE user_id =? ''', (user_id,))
            result = cursor.fetchone()
            claim_prize = result[0]
            if claim_prize is not None:
                claim_prize_obj = datetime.strptime(claim_prize, "%Y-%m-%d %H:%M:%S.%f")
            print(claim_prize)
            if claim_prize is None or claim_prize_obj.date() < current_time.date():
                await ctx.send("The reward can be claimed.")
                is_100m = discord.utils.get(ctx.author.roles,name = '100m Networth 💸') is not None
                is_500m = discord.utils.get(ctx.author.roles, name = '500m Networth 💸💸') is not None
                is_BILLION= discord.utils.get(ctx.author.roles, name = 'BILLION Networth💸💸💸') is not None
                is_combat = discord.utils.get(ctx.author.roles, name= 'Combat psychopath ⚔️' ) is not None
                is_mining = discord.utils.get(ctx.author.roles, name='Mining sociopath 🗿') is not None
                is_enchanting = discord.utils.get(ctx.author.roles, name='Enchanting insanity 📚') is not None
                is_foraging = discord.utils.get(ctx.author.roles, name='Foraging lunatic 🪓') is not None
                is_farming = discord.utils.get(ctx.author.roles, name='Farming maniac 🌾') is not None
                role_list = [(is_farming, 'Farming maniac 🌾'), (is_100m,'100m Networth 💸' ), (is_500m,'500m Networth 💸💸'), (is_BILLION,'BILLION Networth💸💸💸'), (is_foraging,'Foraging lunatic 🪓'), (is_combat,'Combat psychopath ⚔️'), (is_mining,'Mining sociopath 🗿'), (is_enchanting,'Enchanting insanity 📚')]
                ballcoins = result[1]
                role_count= 0
                embed = discord.Embed(
                    title="Daily Reward :trophy: ",
                    description="The daily ballcoin pack :package:",
                    color=0xBA110F
                )
                embed.add_field(name='', value='', inline=False)
                for role in role_list:
                    if role[0]:
                        ballcoins += 50
                        print("yeahhhh")
                        role_count +=1
                        embed.add_field(name=role[1], value= f' You received 50 ballcoins ', inline= False)

                    else:
                        print("wtf")

                claim_prize = str(current_time)
                print(claim_prize, current_time)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='', value=f'Congratulations! In total, You recieved {role_count*50} ballcoins :moneybag:.  ', inline=False)
                cursor.execute('''UPDATE levels SET claim_prize = ?, ballcoin = ? WHERE user_id =?''', (claim_prize, ballcoins, user_id))
                connection.commit()
                if role_count != 0:
                    await ctx.send(embed=embed)

            else:
                await ctx.send(f'The reward cannot be claimed. Try again on {current_time.date() + timedelta(days=1)}')
        #ballcoin shop
        if args[1] == 'shop':
            Embed =  discord.Embed
            embed = Embed( title="The joke scroll",
                    description="They say that bakerballs2000 used to be a stand-up comedian before he retired and settled in the balls discord server. Make the bot generate a random joke.\n\nPrice = 50 ballcoins\n\ncommand = -ballcoin buy 1 {amount}\n\n usage = -joke",
                    color=0xBA110F)
            embed.set_thumbnail(url='https://i.imgflip.com/7b8imn.jpg')
            embed.set_footer(text="Page 1 of 6")
            message = await ctx.send(embed=embed)

            # Add reactions for pagination
            reactions = ['⬅️', '➡️']
            for reaction in reactions:
                await message.add_reaction(reaction)

            # Pagination loop
            page = 1
            while True:
                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0,
                                                        check=lambda r, u: u == ctx.author and str(
                                                            r.emoji) in reactions)
                except asyncio.TimeoutError:
                    await message.clear_reactions()
                    break

                if str(reaction.emoji) == '➡️' and page < 6:
                    page += 1
                elif str(reaction.emoji) == '⬅️' and page > 1:
                    page -= 1
                else:
                    continue

                # Update the embed content based on the current page

                if page == 1:
                    embed = Embed(title="The joke scroll",
                                  description="They say that bakerballs2000 used to be a stand-up comedian before he retired and settled in the balls discord server. Make the bot generate a random joke.\n\nPrice = 50 ballcoins\n\ncommand = -ballcoin buy 1 {amount}\n\n usage = -joke",
                                  color=0xBA110F)
                    embed.set_thumbnail(url='https://i.imgflip.com/7b8imn.jpg')
                if page == 2:
                    embed = Embed(title="The Roast Scroll",
                                  description="Losing an argument? well what about a 2v1? Generates a random insult to one-up your friends\n\nPrice = 200 ballcoins\n\ncommand = -ballcoin buy 2 {amount}\n\n usage = -roast (user) ",
                                  color=0xBA110F)
                    embed.set_thumbnail(url='https://static01.nyt.com/images/2021/04/30/multimedia/30xp-meme/29xp-meme-videoSixteenByNineJumbo1600-v6.jpg')
                elif page == 3:
                    embed = Embed(title="The Luck Scroll",
                                  description="It is stated that a mad magician after losing every lucky draw in existence made this priceless scroll. Increases giveaway chance to two times.\n\nPrice = 500 ballcoins\n\ncommand = -ballcoin buy 3 {amount}\n\nusage = automatically applies to next giveaway",
                                  color=0xBA110F)
                    embed.set_thumbnail(url='https://memesfeel.com/wp-content/uploads/2022/05/Good-luck-memes-2.jpeg')
                elif page == 4:
                    embed = Embed(title="The Exp Scroll",
                                  description="Who needs to grind exp when you can just buy your way through. Gives 500 exp on use.\n\nPrice = 2000 ballcoins\n\ncommand = -ballcoin buy 4 {amount}\n\nusage = Automatically gives 500 exp",
                                  color=0xBA110F)
                    embed.set_thumbnail(url='https://www.memecreator.org/static/images/memes/5475704.jpg')
                elif page == 5:
                    embed = Embed(title="The Balls Membership (1 Month)",
                                  description='''Baller membership, sought with desire,\n
                                                 Unlocking perks, taking us higher.\n
                                                 Custom roles shine, colors ablaze,\n
                                                 In this exclusive club, we dance and amaze.\n\n
                                                 Price = 3000 ballcoins\n\n
                                                 Command = -bc buy 5
                                                 \n\nusage = -membership\n\n
                                                 **Perks:**\n\n**Custom Role:** Do -membership role {rolename} to make or change a role\n\n**Custom Color Palette:** Do -membership palette to check the color palettes \n\n**Joke Scroll:** 5\n\n**Roast Scroll:** 10\n\n**Giveaway Boost:** 1''',
                                  color=0xBA110F)
                    embed.set_thumbnail(url='https://images3.memedroid.com/images/UPLOADED673/63739b4b4ac8e.jpeg')
                elif page == 6:
                    embed = Embed(title="The Custom Command Scroll",
                                  description="Every word I speak echoes with the purpose of building a timeless legacy. Through my actions and the stories I leave behind, I strive to inspire hearts and minds long after my voice has faded. For my legacy is not measured in years, but in the profound impact I impart upon this world, shaping the lives of those who follow in my footsteps. Write your very own custom command.\n\nPrice = 25000 ballcoins\n\ncommand = -ballcoin buy 6\n\nusage = Contact the big menacing role (maximum uses = 2)",
                                  color=0xBA110F)
                    embed.set_thumbnail(url='https://i.redd.it/zpafdzk3eev91.png')

                embed.set_footer(text=f"Page {page} of 6")
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)
    #ballcoin buy from shop
    if len(args) == 3 or len(args) == 4:
        if len(args) == 3:
            args.append('1')
        amount = int(args[3])
        if args[1] == 'buy':
            if args[2] == '1':
                cursor.execute('''
                           SELECT ballcoin FROM levels WHERE user_id = ?''', (author.id,))
                result = cursor.fetchone()
                ballcoins = result[0]
                if int(ballcoins) >= (amount*50):
                    ballcoins -= (amount*50)
                    cursor.execute('''
                            UPDATE levels SET ballcoin = ?, joke = joke + ? WHERE user_id = ?''', (ballcoins,amount,author.id))
                    await ctx.send(f"You have successfully bought {amount} Joke Scroll")
                else:
                    await ctx.send("You lack money, peasant.")
            if args[2] == '2':
                cursor.execute('''
                            SELECT ballcoin FROM levels WHERE user_id = ?''', (author.id,))
                result = cursor.fetchone()
                ballcoins = result[0]
                if int(ballcoins) >= (amount*200):
                    ballcoins -= (amount*200)
                    cursor.execute('''
                            UPDATE levels SET ballcoin = ?, insult = insult + ? WHERE user_id = ?''',
                                   (ballcoins, amount, author.id))
                    await ctx.send(f"You have successfully bought {amount} Roast Scroll")
                else:
                    await ctx.send("You lack money, peasant.")
            if args[2] == '3':
                cursor.execute('''
                            SELECT ballcoin FROM levels WHERE user_id = ?''', (author.id,))
                result = cursor.fetchone()
                ballcoins = result[0]
                if int(ballcoins) >=(amount*500):
                    ballcoins -= (amount*500)
                    cursor.execute('''
                            UPDATE levels SET ballcoin = ?, giveaway_boost = giveaway_boost + ? WHERE user_id = ?''',
                                   (ballcoins, amount, author.id))
                    await ctx.send(f"You have successfully bought {amount} Giveaway Scroll")
                else:
                    await ctx.send("You lack money, peasant.")
            if args[2] == '4':
                cursor.execute('''
                                       SELECT ballcoin FROM levels WHERE user_id = ?''', (author.id,))
                result = cursor.fetchone()
                ballcoins = result[0]
                if int(ballcoins) >= (amount*2000):
                    ballcoins -= (amount*2000)
                    total_exp = amount*500
                    cursor.execute('''
                            UPDATE levels SET ballcoin = ?, exp = exp + ? WHERE user_id = ?''',
                                   (ballcoins, total_exp, author.id))
                    await ctx.send(f"You have successfully gained {total_exp} exp")
                else:
                    await ctx.send("You lack money, peasant.")
            if args[2] == '5' and args[3] == '1':
                cursor.execute('''
                            SELECT ballcoin, is_membership FROM levels WHERE user_id = ?''', (author.id,))
                result = cursor.fetchone()
                ballcoins = result[0]
                is_membership = result[1]
                if not is_membership:
                    if int(ballcoins) >= 3000:
                        ballcoins -= 3000
                        membership_date = str(datetime.now())
                        cursor.execute('''
                            UPDATE levels SET ballcoin = ?, is_membership = ?, joke = joke + 10, insult = insult + 5,
                             giveaway_boost = giveaway_boost + 1, membership_date = ? WHERE user_id = ?''',(ballcoins, True, membership_date,  author.id))
                        await ctx.send("You have successfully become a Baller. Try -membership for more information")
                    else:
                        await ctx.send("You lack money, peasant.")
                else:
                    await ctx.send("You already have The Balls Membership")


            if args[2] == '6':
                cursor.execute('''
                                       SELECT ballcoin FROM levels WHERE user_id = ?''', (author.id,))
                result = cursor.fetchone()
                ballcoins = result[0]
                if int(ballcoins) >= 25000:
                    ballcoins -= 25000
                    cursor.execute('''
                                       UPDATE levels SET ballcoin = ? WHERE user_id = ?''', (ballcoins, author.id))
                    await ctx.send(
                        "You have successfully gained The Custom Command Scroll. DM or ping a big menacing role to proceed further, Take a screenshot as proof.")
                else:
                    await ctx.send("You lack money, peasant.")
            connection.commit()
#short commands for performing simple tasks. I was too lazy to implement them separately.
@bot.command(name= 'joke', aliases=['roast', 'inventory','exp', 'leaderboard'])
async def use(ctx):
    args = ctx.message.content.split()
    author = ctx.message.author
    if len(args) == 1: # the joke, inventory and leaderboard commands have one argument
        if args[0] == '-joke':
            cursor.execute('''
                        SELECT joke FROM levels WHERE user_id = ?''', (author.id,))
            result = cursor.fetchone()
            jokes = result[0]
            if jokes > 0:
                limit = 1
                api_url = 'https://api.api-ninjas.com/v1/jokes?limit={}'.format(limit)
                response = requests.get(api_url, headers={'X-Api-Key': 'QbQSNxt+T9vGGyMlwsEQuA==u3Wh919GZAs0VPf1'})
                if response.status_code == requests.codes.ok:
                    api_response = response.text
                    response_data = json.loads(api_response)
                    # Extract the joke from the response
                    joke = response_data[0]["joke"]
                    await ctx.send(joke)
                    cursor.execute('''
                                    UPDATE levels SET joke = joke - 1 WHERE user_id = ?''', (author.id,))
                    connection.commit()
            else:
                await ctx.send("You don't have any joke scrolls")

        #check your items
        if args[0] == '-inventory':
            cursor.execute('''
                                    SELECT joke, insult, giveaway_boost FROM levels WHERE user_id = ?''', (author.id,))
            result = cursor.fetchone()
            jokes = result[0]
            insult = result[1]
            giveaway_boost = result[2]
            embed = discord.Embed(title= '**__Inventory__**', description= f'\n**Joke Scroll** :scroll:\n{jokes}\n\n**Roast Scroll** :scroll: \n{insult}\n\n**Luck Scroll** :scroll: \n{giveaway_boost}', color=0xBA110F )
            embed.set_thumbnail(url=str(author.avatar.url))
            connection.commit()

            await ctx.send(embed=embed)

            #leaderboard
        if args[0] =='-leaderboard':
            author_ = ctx.message.author
            cursor.execute('SELECT level, exp, user_id FROM levels ORDER BY level DESC, exp DESC')
            result = cursor.fetchall()
            rank = 1
            embed = discord.Embed(title='**__Leaderboard__**  :page_with_curl: ', description='', color=0xBA110F )
            #empty spcaces
            embed.add_field(name='\u200b',
                            value='',
                            inline=False)

            for results in result:
                user_id = results[2]
                level = results[0]
                exp = results[1]
                if rank == 1:
                    medal = ' :first_place: '
                elif rank == 2:
                    medal = ' :second_place: '
                elif rank == 3:
                    medal = ' :third_place: '
                else:
                    medal = ''
                try:
                    user = await bot.fetch_user(user_id)
                    username = user.name
                except:
                    username = user_id
                if rank < 11:
                    embed.add_field(name=f'**__{rank}. {username}__** {medal} ',
                                    value=f'**Rank**: *{rank}*  |  **Level**: *{level}*   |  **Exp**: *{exp}*\n',
                                    inline=False)
                    embed.add_field(name=' ', value='', inline=False)

                if author_.id == user_id:
                    await ctx.send(f'Your rank is {rank}')
                rank += 1



            await ctx.send(embed=embed)


    if len(args) == 2: # the roast command has two arguments
        # roast command
        if args[0] == '-roast':
            target_user = ctx.message.mentions[0]
            cursor.execute('''
                                   SELECT insult FROM levels WHERE user_id = ?''', (author.id,))
            result = cursor.fetchone()
            insult = result[0]
            if insult > 0:
                url = "https://insult.mattbas.org/api/insult"

                # Send a GET request to the API endpoint
                response = requests.get(url)

                # Extract the insult from the response
                insult = response.text

                # Print the insult
                await ctx.send(f'{target_user} {insult}')
                cursor.execute('''
                                                   UPDATE levels SET insult = insult - 1 WHERE user_id = ?''', (author.id,))
                connection.commit()
            else:
                await ctx.send("You don't have any roast scrolls")



    if len(args) == 4: # the exp command has 4 arguments
        is_owner = discord.utils.get(ctx.author.roles, name='Owner') is not None
        is_big_menacing_role = discord.utils.get(ctx.author.roles, name='menacing hammer') is not None
        if args[0] == '-exp' and (is_big_menacing_role or is_owner):
            try:
                target_user = ctx.message.mentions[0]
                target_user_id = str(target_user.id)
            except:
                target_user_id = args[2]
                target_user =  await bot.fetch_user(target_user_id)
            amount = args[3]
            cursor.execute('''
                        SELECT exp FROM levels WHERE user_id = ?''', (target_user_id,))
            result = cursor.fetchone()
            exp = result[0]
            if args[1] == 'give':
                cursor.execute('''
                         UPDATE levels SET exp = exp + ? WHERE user_id = ?''',
                               (amount, target_user_id))
                await ctx.send(f"Gave {amount} exp to {target_user.name}")
                connection.commit()
            if args[1] == 'take':
                xp =  int(exp) - int(amount)
                if xp < 0:
                    xp = 0
                cursor.execute('''
                         UPDATE levels SET exp = ? WHERE user_id = ?''',
                               (xp, target_user_id))
                await ctx.send(f"Took {amount} exp from {target_user.name}")
                connection.commit()

@bot.command(name = 'membership')
async def membership(ctx):
    message = ctx.message
    args = message.content.split()
    author = message.author
    cursor.execute('SELECT is_membership FROM levels where user_id = ?', (author.id,))
    result = cursor.fetchone()
    if isinstance(author, discord.Member):
        guild = ctx.guild
        member = guild.get_member(author.id)
    is_membership = result[0]
    rolename =''
    for roles in args[2:]:
        rolename = (rolename +' '+ roles)
    rolename = rolename.strip()
    if is_membership:
        if len(args) == 1:
            embed = discord.Embed(title= "**Congratulations, you're a certified Baller.**",
                              description="**Perks:**\n\n**Custom Role:** Do -membership role {rolename} to make or change a role\n\n**Custom Color Palette:** Do -membership palette to check the color palettes \n\n**Joke Scroll:** 5\n\n**Roast Scroll:** 10\n\n**Giveaway Boost:** 1",
                              color=0xBA110F)
            await ctx.send(embed=embed)
        if len(args) >= 3:
            if args[1] == 'role':
                await ctx.send(f"Are you sure you want to call your role {rolename}. Write 'yes' or 'no'. ")
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel and \
                        m.content.lower() in ['yes', 'no']
                yesorno = await bot.wait_for('message', check=check, timeout = 30 )
                if yesorno.content.lower() == 'yes':
                    cursor.execute('SELECT custom_role_id FROM levels WHERE user_id = ?', (author.id,))
                    role_id = cursor.fetchone()
                    role_id = role_id[0]
                    print('ok')
                    if role_id == 0:
                        guild = ctx.guild
                        print(rolename)
                        existing_role = discord.utils.get(await ctx.guild.fetch_roles(), name=rolename)

                        if not existing_role:
                            role = await guild.create_role(name=rolename)
                            await ctx.send(f"Role '{rolename}' has been created.")
                            role = discord.utils.get(await ctx.guild.fetch_roles(), name=rolename)
                            await member.add_roles(role)
                            role_positions = await guild.fetch_roles()

                            # Find the position of the role you want to move the created role above
                            target_role_name = 'Senior Moderator'
                            target_role = discord.utils.get(role_positions, name=target_role_name)

                            # Move the created role above the target role
                            await role.edit(position=target_role.position + 1)

                            # After modifying the role's position, you may need to refresh the role's cache
                            role = discord.utils.get(guild.roles, name=rolename)
                            await ctx.send(f"Your custom role is '{rolename}'. You can change it using -membership role (rolename)")
                            cursor.execute('UPDATE levels SET custom_role_id = ? WHERE user_id = ?',(role.id, author.id))
                            connection.commit()
                        else:
                            await ctx.send(f"Role '{rolename}' already exists.")

                    if role_id:
                        role = ctx.guild.get_role(role_id)
                        if role:
                            await role.edit(name=rolename)
                            await ctx.send(f"Role '{role.name}' has been updated.")
                if yesorno.content.lower() == 'no':
                    await ctx.send(f"role '{rolename}' was not created")
        if len(args) == 2:
            if args[1] == 'palette':
                embed = discord.Embed(title='**__Color Names__**',
                                      description="**Write -membership palette {color} to use a color**",
                                      color=0xBA110F)

                for i in range(0, len(color_list), 10):
                    field_values = ', '.join(color_list[i:i + 10])
                    embed.add_field(name='\u200b', value=field_values, inline=True)
                await ctx.send(embed=embed)
        if len(args) == 3 and args[1] == 'palette':
            cursor.execute('SELECT custom_role_id from levels WHERE user_id =?',(author.id,))
            result =cursor.fetchone()
            role_id = result[0]
            if role_id:
                if args[2] in color_list:
                    role = ctx.guild.get_role(role_id)
                    color_name = args[2]
                    rgb_values = color_names.get(color_name)
                    color = discord.Color.from_rgb(*rgb_values)
                    await role.edit(color=color)
                    await ctx.send("Role Color has been updated")
                else:
                    ctx.send("The color does not exist. Try -membership palette for more information")
            else:
                await ctx.send("You don't have a custom role. Try -membership for more information")

    else:
        await ctx.send("You don't have The Balls Membership. Try -bc shop for more info.")


@tasks.loop(seconds=1000)
async def check_membership_time():
    cursor.execute('SELECT membership_date, user_id, custom_role_id FROM levels WHERE is_membership = TRUE')
    results = cursor.fetchall()
    guild = bot.get_guild(guild_id)
    if results:
        for result in results:
            membership_date = result[0]
            user_id = result[1]
            custom_role_id = result[2]
            current_time = datetime.now()
            membership_date_object = datetime.strptime(membership_date, "%Y-%m-%d %H:%M:%S.%f")
            time_difference = current_time - membership_date_object
            days_difference = time_difference.days
            if days_difference > 30:
                role = guild.get_role(custom_role_id)
                if role:
                    await role.delete()
                cursor.execute('''UPDATE levels SET custom_role_id = 0, is_membership = FALSE,
                     membership_date = NULL WHERE user_id = ?''',(user_id,))
                connection.commit()





bot.run(TOKEN)

