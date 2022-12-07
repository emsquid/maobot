import os
import random
import discord
from discord.ext.commands import Context
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
async def regle(ctx: Context):
    def format_rule(rule: str) -> str:
        words = rule.split("-")
        formatted_rule = ""

        for word in words:
            if word in ["d", "l"]:
                formatted_rule += word + "'"
            else:
                formatted_rule += word + " "

        return formatted_rule.capitalize()

    rules = set(
        channel.name
        for channel in ctx.guild.channels
        if channel.name.startswith("règle-")
    )
    chosen_rule = random.choice(rules)

    embed = discord.Embed()
    embed.add_field(name="La règle choisie est... 🃏", value=format_rule(chosen_rule))

    await ctx.respond(embed=embed)


bot.run(os.getenv("TOKEN"))
