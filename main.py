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


user_strikes = {}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Yomi's Automod"))
    print(f'Yomi is fully online and monitoring words!')

# 3. Welcome Message Logic (Disabled as it requires privileged intents)
# @bot.event
# async def on_member_join(member):
#     channel = discord.utils.get(member.guild.text_channels, name="general")
#     if channel:
#         embed = discord.Embed(
#             title="✨ Welcome!",
#             description=f"Hi {member.mention}! I'm **Yomi**. Glad to have you here! Please follow the rules. <3",
#             color=discord.Color.purple()
#         )
#         embed.set_thumbnail(url=member.display_avatar.url)
#         await channel.send(embed=embed)

# --- ALL YOMI COMMANDS ---

@bot.tree.command(name="yomis_automod_history", description="Check your own strike count")
async def history(interaction: discord.Interaction):
    """User Command (Private)"""
    strikes = user_strikes.get(interaction.user.id, 0)
    await interaction.response.send_message(f"📜 {interaction.user.mention}, you have **{strikes}** strikes.", ephemeral=True)

@bot.tree.command(name="yomis_automod_warn", description="Staff: Check a user's strikes")
@app_commands.checks.has_permissions(manage_messages=True)
async def warn_staff(interaction: discord.Interaction, member: discord.Member):
    """Staff Command"""
    strikes = user_strikes.get(member.id, 0)
    await interaction.response.send_message(f"⚠️ {member.mention} has **{strikes}** strikes.")

@bot.tree.command(name="yomis_automod_clear_history", description="Staff: Reset a user's strikes")
@app_commands.checks.has_permissions(administrator=True)
async def clear_history(interaction: discord.Interaction, member: discord.Member):
    """Staff Command"""
    user_strikes[member.id] = 0
    await interaction.response.send_message(f"🧹 History cleared for {member.mention}. Back to 0!")

@bot.tree.command(name="yomis_automod_kick", description="Staff: Kick a member")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Rules violation"):
    """Staff Command"""
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👞 {member.mention} has been kicked.")

@bot.tree.command(name="yomis_ping", description="Check how fast Yomi is")
async def ping(interaction: discord.Interaction):
    """Utility Command"""
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency * 1000)}ms")

# --- FUN ATTACKS & PRANKS ---

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
    await interaction.response.send_message(f"🐟 {interaction.user.mention} slaps {member.mention} around a bit with a large, wet trout!")

@bot.tree.command(name="yomi_prank", description="Have Yomi pull a prank!")
async def prank(interaction: discord.Interaction):
    pranks = [
        "I just hid your digital socks! 🧦",
        "I swapped your mouse sensitivity to 99,000! 🐭",
        "Why did the computer go to the doctor? Because it had a virus! (Hehe, gotcha!) 💻",
        "I told the other bots you were actually a cat in a human suit. 🐱"
    ]
    await interaction.response.send_message(f"🃏 **Yomi's Prank:** {random.choice(pranks)}")

@bot.tree.command(name="yomi_fortune", description="Ask Yomi to tell your fortune")
async def fortune(interaction: discord.Interaction):
    fortunes = [
        "✨ The stars say you'll have a great day!",
        "🔮 I see a very lucky moment in your near future.",
        "⭐ Trust your gut today, it's leading you somewhere cool.",
        "🌟 Someone is thinking nice things about you right now!",
        "☁️ A small challenge is coming, but you've totally got this."
    ]
    await interaction.response.send_message(f"**{interaction.user.display_name}'s Fortune:** {random.choice(fortunes)}")

@bot.tree.command(name="yomi_hug", description="Give someone a warm hug!")
async def hug(interaction: discord.Interaction, member: discord.Member):
    if member == interaction.user:
        await interaction.response.send_message(f"🫂 {interaction.user.mention}, I'm giving YOU a huge hug! You're doing great.")
    else:
        await interaction.response.send_message(f"🫂 {interaction.user.mention} wrapped their arms around {member.mention} for a big, warm hug!")

@bot.tree.command(name="yomi_coinflip", description="Flip a coin!")
async def coinflip(interaction: discord.Interaction):
    result = random.choice(["Heads! 🪙", "Tails! 🪙"])
    await interaction.response.send_message(f"I flipped a coin for you... it's **{result}**")

@bot.tree.command(name="yomi_rps", description="Play Rock, Paper, Scissors with Yomi!")
async def rps(interaction: discord.Interaction, choice: str):
    user_choice = choice.lower()
    if user_choice not in ["rock", "paper", "scissors"]:
        await interaction.response.send_message("Please pick Rock, Paper, or Scissors!", ephemeral=True)
        return

    yomi_choice = random.choice(["rock", "paper", "scissors"])

    if user_choice == yomi_choice:
        result = "It's a tie! Great minds think alike. 🤝"
    elif (user_choice == "rock" and yomi_choice == "scissors") or \
         (user_choice == "paper" and yomi_choice == "rock") or \
         (user_choice == "scissors" and yomi_choice == "paper"):
        result = "You won! You're too good at this. 🏆"
    else:
        result = "I won! Better luck next time. 😋"

    await interaction.response.send_message(f"You chose **{user_choice}** and I chose **{yomi_choice}**. {result}")

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
                # 4th violation = 15 second timeout
                await message.author.timeout(datetime.timedelta(seconds=15), reason="4th strike")
                await message.channel.send(f"🔇 {message.author.mention} timed out for 15 seconds (Strike 4).")

            elif current == 5:
                # 5th violation = 20 second timeout
                await message.author.timeout(datetime.timedelta(seconds=20), reason="5th strike")
                await message.channel.send(f"🔇 {message.author.mention} timed out for 20 seconds (Strike 5).")

            elif current >= 6:
                await message.channel.send(f"🚨 **FINAL WARNING** {message.author.mention}: Next time you say a banned word, you will be BANNED.")

            else:
                # Strikes 1, 2, and 3
                await message.channel.send(f"⚠️ {message.author.mention}, that word is banned! Strikes: {current}/3", delete_after=5)

        except discord.Forbidden:
            print("Error: Hierarchy issue. Move Yomi role higher!")

    await bot.process_commands(message)
# --- STRIKE SYSTEM & RESET ---

# This creates a 'memory' for strikes while the bot is running
user_strikes = {} 

@bot.tree.command(name="yomi_forgive", description="Reset all strikes for a user")
@commands.has_permissions(manage_messages=True) # Only mods can use this!
async def forgive(interaction: discord.Interaction, member: discord.Member):
    if member.id in user_strikes:
        user_strikes[member.id] = 0
        await interaction.response.send_message(f"😇 Yomi has cleared the record for {member.mention}. Back to zero strikes!")
    else:
        await interaction.response.send_message(f"{member.display_name} didn't have any strikes anyway! They're an angel. ✨")

@bot.tree.command(name="yomi_check_strikes", description="See how many strikes someone has")
async def check_strikes(interaction: discord.Interaction, member: discord.Member):
    strikes = user_strikes.get(member.id, 0)
    await interaction.response.send_message(f"📊 {member.display_name} currently has **{strikes}** strikes.") @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        msg_content = message.content.lower()
        if any(word in msg_content for word in BANNED_WORDS):
            await message.delete()

            # Add a strike
            user_id = message.author.id
            user_strikes[user_id] = user_strikes.get(user_id, 0) + 1
            current_strikes = user_strikes[user_id]

            await message.channel.send(
                f"⚠️ {message.author.mention}, n-no c-cussing it makes me feel hot~ uwu  **{current_strikes}** strikes. "
                "Be careful!", delete_after=10
            )
            return

        await bot.process_commands(message
    await bot.process_commands(message)

# Railway will use the TOKEN variable you set in their dashboard
bot.run(os.environ.get('TOKEN'))
