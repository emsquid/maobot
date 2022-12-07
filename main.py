import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(
    name="règle",
    description="Choisi une règle au hasard parmi toutes celles existantes",
)
async def regle(ctx):
    def format_rule(rule: str) -> str:
        words = rule.split("-")
        formatted_rule = ""

        for word in words:
            if word in ["d", "l"]:
                formatted_rule += word + "'"
            else:
                formatted_rule += word + " "

        return formatted_rule

    rules = [
        channel for channel in ctx.guild.channels if channel.name.startswith("règle")
    ]
    chosen_rule = random.choice(rules).name

    await ctx.respond(f"La règle choisie est: **{format_rule(chosen_rule)}**")


bot.run(os.getenv("TOKEN"))
