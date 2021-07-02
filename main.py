from replit import db
import weapons
import requests
import discord
import random
import time
import json
import os

client = discord.Client()

# Status if 2B will respond to their name or not
if "responding" not in weapons.list_all():
  db["responding"] = True
  print("Responding set to True")

# Quotes that 2B can say
two_b_quotes = [
  "The machines don't have feelings. You said it yourself.",
  "Everything that lives is designed to end. We are perpetually trapped in a never-ending spiral of life and death. Is this a curse? Or some kind of punishment? I often think about the god who blessed us with this cryptic puzzle...and wonder if we'll ever get the chance to kill him.",
  "Stop complaining.",
  "It always... ends like this...",
  "What is it that separates machines from androids like us? The machines have grown emotions. ...Consciousness. The final screams they summoned on the edge of their death... They still echo within me.",
  "Take care... of 9S.",
  "You son of a... I'll kill you!",
  "You know nothing about humanity!",
  "All this help for no personal gain? I know she's pretty, but-",
  "Well, aren't we generous?",
  "Stop complaining."
]

# Greetings that 2B will respond to and reply with
greetings = ["hey 2b","hi 2b","yo 2b","hello 2b","greetings 2b","hiya 2b","yooo 2b","evening 2b","morning 2b"]

# Used as output for systemcheck
protocols = ["Activating IFF","Activating FCS","Initializing Pod Connection","Activating Inertia Control System"]

system_check = ("""
```Initializing Tactics Log
Memory Unit: Green
Vitals: Green
Black Box Temperature: Normal
Black Box Pressure: Normal
Equipment Status: Green
All Systems Green
Combat Preparation Complete```
""")

def get_anime_quote():
  response = requests.get("https://animechan.vercel.app/api/random")
  json_data = json.loads(response.text)
  quote = json_data['quote'] + " -" + json_data['character'] + " from " + json_data['anime']
  return(quote)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event # Prints when bot goes live
async def on_ready():
  #await client.change_presence(activity=discord.Game(name=f"On {len(client.guilds)} servers"))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="Birth of a Wish"))
  print('Android Unit {0.user}'.format(client) + ' is active')

@client.event
async def on_message(message):
  # Bot ignores messages from itself
  if message.author == client.user:
    return
  
  msg = message.content

  # Commands
  if msg.startswith("!help"):
    await message.channel.send("```!about, !anime, !inspire, !gif, !yorha, !systemcheck, !selfdestruct, !enabled true/false !weapon, !list, !add, !del```")

  if msg.startswith("!about"):
    await message.channel.send("""
    *YoRHa No.2 Type B (Battle) or 2B serves as the protagonist of Route A in NieR:Automata. She is a YoRHa android created to battle the machine lifeforms that have invaded the planet on behalf of the surviving humans. She served during the 14th Machine War.*
    """)

  if msg.startswith("!yorha"):
    await message.channel.send(file=discord.File('gifs/about/YoRHa.gif'))
    await message.channel.send("*YoRHa is an elite military force of androids charged by the Council of Humanity with fighting the invading aliens and their machine lifeforms. Stationed on the thirteenth orbital base, known as the Bunker, they are constantly fighting to reclaim Earth for the human race.*")

  if msg.startswith("!anime"):
    await message.channel.send(get_anime_quote())

  if msg.startswith("!inspire"):
    await message.channel.send(get_quote())
  
  if msg.startswith("!gif"):
    file = random.choice(os.listdir("gifs/collection"))
    await message.channel.send(file=discord.File('gifs/collection/' + file))

  if msg.startswith("!selfdestruct"):
    await message.channel.send(f"I would rather not do that right now {message.author.name}")

  if msg.startswith("!systemcheck"):
    await message.channel.send("`Commencing System Check...`")
    time.sleep(1)

    for check in protocols:
      await message.channel.send(check)
      time.sleep(.6)

    await message.channel.send(system_check)

  if msg.startswith("!enabled"): # Toggle bots ability to detect its name in messages
    value = msg.split("!enabled ",1)[1]
    if value.lower() == "true":
      #db["responding"] = True
      weapons.set_responding(True)
      await message.channel.send("YoRHa No.2 Type B now responding")
    else:
      #db["responding"] = False
      weapons.set_responding(False)
      await message.channel.send("YoRHa No.2 Type B responding now off")

  # Weapon queries
  if msg.startswith("!add"):
    if weapons.parse(msg):
      await message.channel.send("I added that to my database")
    else:
      await message.channel.send("I could not add that")

  if msg.startswith("!del"):
    msg = msg.strip("!del ")
    if weapons.delete_weapon(msg):
      await message.channel.send("I have erased that entry from my database.")
    else:
      await message.channel.send("I could not erase that entry.")

  if msg.startswith("!list"):
    result = ""
    weaponList = weapons.list_weapons()
    for item in weaponList:
      result = result + item + "\n"
    await message.channel.send("Here are the weapons that are currently in my database: \n" + result)

  if msg.startswith("!listall"): # TESTING
    await message.channel.send(weapons.list_all())

  if msg.startswith("!weapon"):
    msg = msg.strip("!weapon ")

    if msg == "": # if user enters just "!weapon"
      await message.channel.send("Please specify which weapon you would like to learn about.\n !list can be used to view all weapons.")
      return

    description = weapons.get_weapon(msg)
    if description:
      await message.channel.send(f"**{msg}**: {description}")
    else:
      matches = weapons.search_weapons(msg)
      if matches:
        for key in matches:
          await message.channel.send(f"**{key}**: {matches[key]}")
      else:
        await message.channel.send("Sorry, I could not fine that weapon in my database..")

  # 2B will respond if their name is detected
  if db["responding"]:
    if "2b" in msg.lower() and msg.lower() not in greetings:
      await message.channel.send(random.choice(two_b_quotes))

    if msg.lower() in greetings: # Check for any messages found in "greetings" list
      # 2b will reply with a random greeting with "2b" stripped from string
      reply = random.choice(greetings)
      reply = reply.split(' ',1)[0]
      await message.channel.send(f"{reply} {message.author.name}")

# start
client.run(os.environ['Tkn'])
