import discord
import os
import datetime
from discord.ext import commands
from discord import app_commands

# 1. Setup Intents
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Slash commands synced!")

bot = MyBot()

# 2. Banned Words List
BANNED_WORDS = [
    "fuck", "shit", "bitch", "nigger", "faggot", "whore", "slut", 
    "rape", "nigga", "dick", "cock", "bastred", "head", "ass", "hole", 
    "faggot", "fag", "cunt", "pedo", "nga", "black monkey", "kink", 
    "feditsh", "pussy", "shut up"
]

user_strikes = {}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Yomi's Automod"))
    print(f'Yomi is live on Railway!')

# --- WAKE UP COMMAND ---
@bot.tree.command(name="yomi_wake_up", description="Check if Yomi is awake")
async def wakeup(interaction: discord.Interaction):
    await interaction.response.send_message(f"👀 **Yomi is wide awake on Railway!** Latency: {round(bot.latency * 1000)}ms")

# --- OTHER COMMANDS ---
@bot.tree.command(name="yomi_slap", description="Slap someone with a fish!")
async def slap(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"🐟 {interaction.user.mention} slapped {member.mention} with a giant fish!")

@bot.tree.command(name="yomis_automod_history", description="Check your strike count")
async def history(interaction: discord.Interaction):
    strikes = user_strikes.get(interaction.user.id, 0)
    await interaction.response.send_message(f"📜 You have **{strikes}** strikes.", ephemeral=True)

# --- AUTOMOD LOGIC ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg_content = message.content.lower()
    if any(word in msg_content for word in BANNED_WORDS):
        user_id = message.author.id
        user_strikes[user_id] = user_strikes.get(user_id, 0) + 1
        current = user_strikes[user_id]
        
        try:
            await message.delete()
            if current == 4:
                await message.author.timeout(datetime.timedelta(seconds=15), reason="4th strike")
                await message.channel.send(f"🔇 {message.author.mention} timed out for 15s.")
            elif current == 5:
                await message.author.timeout(datetime.timedelta(seconds=20), reason="5th strike")
                await message.channel.send(f"🔇 {message.author.mention} timed out for 20s.")
            elif current >= 6:
                await message.channel.send(f"🚨 **FINAL WARNING** {message.author.mention}: Next time is a BAN.")
            else:
                await message.channel.send(f"⚠️ {message.author.mention}, that word is banned! Strike: {current}/3", delete_after=5)
        except discord.Forbidden:
            print("Permission error.")

    await bot.process_commands(message)

# Railway will use the TOKEN variable you set in their dashboard
bot.run(os.environ.get('TOKEN'))
