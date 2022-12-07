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

        return formatted_rule.capitalize()

    channels = ctx.guild.channels
    rules = [channel for channel in channels if channel.name.startswith("règle-")]
    chosen_rule = random.choice(rules).name

    embed = discord.Embed()
    embed.add_field(name="La règle choisie est... 🃏", value=format_rule(chosen_rule))

    await ctx.respond(embed=embed)


bot.run(os.getenv("TOKEN"))
