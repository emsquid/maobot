import os
import time
import random
import discord
from discord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot()


def format_rule(rule: str) -> str:
    words = rule.split("-")
    formatted_rule = ""

    for word in words:
        if word in ["d", "l"]:
            formatted_rule += word + "'"
        else:
            formatted_rule += word + " "

    return formatted_rule.capitalize()


@bot.event
async def on_ready():
    print(f"{time.strftime('[%d-%m-%Y %H:%M:%S]',time.localtime())}")
    print(f"{bot.user} is ready and online!")


@bot.slash_command(
    name="règle",
    description="Choisi une règle au hasard parmi toutes celles existantes",
)
async def regle(ctx: Context):
    rules = list(
        set(
            channel.name.strip()
            for channel in ctx.guild.channels
            if channel.name.startswith("règle-") and channel.name != "règle-de"
        )
    )

    def generate_embed(allowed: bool = True) -> discord.Embed:
        if allowed:
            chosen_rule = rules.pop(random.randrange(len(rules)))

            embed = discord.Embed()
            embed.add_field(
                name="La règle choisie est... 🃏", value=format_rule(chosen_rule)
            )
        else:
            embed = discord.Embed()
            embed.add_field(name="Erreur ⛔️", value="Vous ne pouvez pas faire ça")

        return embed

    def generate_view() -> discord.ui.View:
        reroll_button = discord.ui.Button(label="Reroll")
        reroll_button.callback = reroll

        return discord.ui.View(reroll_button, disable_on_timeout=True)

    async def reroll(interaction: discord.Interaction):
        if interaction.user == ctx.author:
            if len(rules) > 1:
                await interaction.response.edit_message(embed=generate_embed())
            else:
                await interaction.response.edit_message(
                    embed=generate_embed(), view=None
                )
        else:
            await interaction.response.send_message(
                embed=generate_embed(False), ephemeral=True
            )

    await ctx.respond(embed=generate_embed(), view=generate_view())


bot.run(os.getenv("TOKEN"))
