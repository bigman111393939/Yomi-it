import discord
import os
import datetime
import random
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
    "fag", "cunt", "pedo", "nga", "black monkey", "kink", 
    "feditsh", "pussy", "shut up","negro",
]

# Global strike storage
user_strikes = {}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Yomi's Automod"))
    print(f'Yomi is live on Railway!')

# --- UTILITY COMMANDS ---

@bot.tree.command(name="yomi_wake_up", description="Check if Yomi is awake")
async def wakeup(interaction: discord.Interaction):
    await interaction.response.send_message(f"👀 **Yomi is wide awake on Railway!** Latency: {round(bot.latency * 1000)}ms")

@bot.tree.command(name="yomis_ping", description="Check how fast Yomi is")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency * 1000)}ms")

# --- STAFF & MODERATION COMMANDS ---

@bot.tree.command(name="yomis_automod_history", description="Check a user's strike count")
async def history(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    strikes = user_strikes.get(target.id, 0)
    await interaction.response.send_message(f"📜 {target.display_name} has **{strikes}** strikes.", ephemeral=True)

@bot.tree.command(name="yomis_automod_clear_history", description="Staff: Reset a user's strikes")
@app_commands.checks.has_permissions(administrator=True)
async def clear_history(interaction: discord.Interaction, member: discord.Member):
    user_strikes[member.id] = 0
    await interaction.response.send_message(f"🧹 History cleared for {member.mention}. Back to 0!")

@bot.tree.command(name="yomi_forgive", description="Reset all strikes for a user")
@app_commands.checks.has_permissions(manage_messages=True)
async def forgive(interaction: discord.Interaction, member: discord.Member):
    user_strikes[member.id] = 0
    await interaction.response.send_message(f"😇 Yomi has cleared the record for {member.mention}!")

@bot.tree.command(name="yomis_automod_kick", description="Staff: Kick a member")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Rules violation"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👞 {member.mention} has been kicked.")

# --- FUN & ATTACK COMMANDS ---

@bot.tree.command(name="yomi_attack", description="Launch a silly attack at someone!")
async def attack(interaction: discord.Interaction, member: discord.Member):
    attacks = [
        "launched a giant 🐥 **Rubber Duck** at",
        "threw a 🥧 **Cream Pie** directly at the face of",
        "tickled the toes of",
        "summoned a ☁️ **Rain Cloud** to follow around",
        "hit with a 🎈 **Balloon Sword** (it didn't pop!)"
    ]
    attack_move = random.choice(attacks)
    await interaction.response.send_message(f"⚔️ **YOMI BATTLE:** {interaction.user.mention} {attack_move} {member.mention}!")

@bot.tree.command(name="yomi_slap", description="Slap someone with a fish!")
async def slap(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"🐟 {interaction.user.mention} slaps {member.mention} around with a large, wet trout!")

@bot.tree.command(name="yomi_fortune", description="Ask Yomi to tell your fortune")
async def fortune(interaction: discord.Interaction):
    fortunes = ["✨ Great day ahead!", "🔮 Lucky moment coming!", "⭐ Trust your gut!", "🌟 You are loved!"]
    await interaction.response.send_message(f"**{interaction.user.display_name}'s Fortune:** {random.choice(fortunes)}")

@bot.tree.command(name="yomi_hug", description="Give someone a warm hug!")
async def hug(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"🫂 {interaction.user.mention} gives {member.mention} a warm hug!")

# --- AUTOMOD & MESSAGE LOGIC ---

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg_content = message.content.lower()
    
    # Banned Word Detection
    if any(word in msg_content for word in BANNED_WORDS):
        user_id = message.author.id
        user_strikes[user_id] = user_strikes.get(user_id, 0) + 1
        current = user_strikes[user_id]

        try:
            await message.delete()
            
            if current == 4:
                await message.author.timeout(datetime.timedelta(seconds=5), reason="4th strike")
                await message.channel.send(f"🔇 {message.author.mention} timed out (Strike 4).")
            elif current == 5:
                await message.author.timeout(datetime.timedelta(seconds=5), reason="5th strike")
                await message.channel.send(f"🔇 {message.author.mention} timed out (Strike 5).")
            elif current >= 6:
                await message.channel.send(f"🚨 **FINAL WARNING** {message.author.mention}: Next time is a BAN.")
            else:
                await message.channel.send(f"⚠️ {message.author.mention}, no bad words! it makes me feel hot~ ngh~! Strikes: {current}", delete_after=5)
        
        except discord.Forbidden:
            print("Permission error: Check Yomi's role position.")

    await bot.process_commands(message)
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg_content = message.content.lower()
    
    # Banned Word Detection
    if any(word in msg_content for word in BANNED_WORDS):
        user_id = message.author.id
        user_strikes[user_id] = user_strikes.get(user_id, 0) + 1
        current = user_strikes[user_id]

        try:
            await message.delete()
            
            # Dramatic Anime-style responses
            responses = [
                f"H-hey! {message.author.mention}, 💗uwu~ you can't say that here! Baka! (Strike {current})",
                f"🚫 Stop right there, {message.author.mention}! 🐺My ears are sensitive to those words! (Strike {current})",
                f"💢 Oh my gosh... {message.author.mention}, that's so rude! I'm giving you a strike for that. ({current}/3)",
                f"🥺 Why would you say something so mean, {message.author.mention}?? I'm deleting that!"
            ]
            
            if current >= 6:
                await message.channel.send(f"🚨 **FINAL WARNING** {message.author.mention}: I'm losing my patience... one more and you're out!")
            else:
                await message.channel.send(random.choice(responses), delete_after=10)
        
        except discord.Forbidden:
            print("Permission error: Check Yomi's role position.")

    await bot.process_commands(message)
# Run the bot
bot.run(os.environ.get('TOKEN'))
     
