import enum
import os
import time
import random
import discord
from discord import ApplicationContext, Member, TextChannel, PermissionOverwrite, Embed
from dotenv import load_dotenv
from discord.abc import GuildChannel

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
    print(f"{time.strftime('[%d-%m-%Y %H:%M:%S]', time.localtime())}")
    print(f"{bot.user} is ready and online!")


@bot.slash_command(
    name="règle",
    description="Choisi une règle au hasard parmi toutes celles existantes",
)
@discord.option(
    "inconnues",
    description="Cherche aussi parmi les règles que vous ne connaissez pas",
    required=False,
    default=False,
)
async def regle(ctx: ApplicationContext, inconnues: bool):
    rules = list(
        set(
            channel.name.strip()
            for channel in ctx.guild.channels
            if channel.name.startswith("règle-")
            and channel.name != "règle-de"
            and (inconnues or channel.permissions_for(ctx.author).view_channel)
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


@bot.slash_command(name="add", description="ajouter des joueurs à vos salons de règles")
@discord.option("membre1",
                description="Sélectionne les membres qui auront accès aux salons",
                required=True,
                default=None)
@discord.option("salon1",
                description="Sélectionne les salons axquels les membres auront accès",
                required=True,
                default=None)
@discord.option("membre2",
                description="Sélectionne les membres qui auront accès aux salons",
                required=False,
                default=None)
@discord.option("membre3",
                description="Sélectionne les membres qui auront accès aux salons",
                required=False,
                default=None)
@discord.option("membre4",
                description="Sélectionne les membres qui auront accès aux salons",
                required=False,
                default=None)
@discord.option("membre5",
                description="Sélectionne les membres qui auront accès aux salons",
                required=False,
                default=None)
@discord.option("salon2",
                description="Sélectionne les salons axquels les membres auront accès",
                required=False,
                default=None)
@discord.option("salon3",
                description="Sélectionne les salons axquels les membres auront accès",
                required=False,
                default=None)
@discord.option("salon4",
                description="Sélectionne les salons axquels les membres auront accès",
                required=False,
                default=None)
@discord.option("salon5",
                description="Sélectionne les salons axquels les membres auront accès",
                required=False,
                default=None)
@discord.option(name="voir_la_regle",
                description="Les membres pourront juste voir le salon mais pas la règle",
                required=False,
                default=True)
async def add(ctx: ApplicationContext, membre1: Member, salon1: GuildChannel, membre2: Member, membre3: Member,
              membre4: Member, membre5: Member, salon2: GuildChannel, salon3: GuildChannel, salon4: GuildChannel,
              salon5: GuildChannel, voir_la_regle: bool):
    members = [membre1, membre2, membre3, membre4, membre5]
    channels = [salon1, salon2, salon3, salon4, salon5]

    def generate_embed() -> Embed:
        embed = Embed()

        if len(members) == 0 or len(channels) == 0:
            embed.add_field(name="Erreur ⛔️", value="Les données fournies ne sont pas valides")
        elif len(wrong_channels) == 0:
            embed.add_field(name="Succès !!", value="Tous les membres ont maintenant accaès aux salons")
        elif len(wrong_channels) == len(channels):
            embed.add_field(name="Erreur ⛔️", value="Vous êtes propriétaire d'aucun salon fourni")
        else:
            val = "Les modifications n'ont pas pu être appliquées pour les salons suivants car vous n'êtes pas propriétaires de ces salons : " + \
                  wrong_channels[0].name
            for i in range(1, len(wrong_channels)):
                val += ", " + wrong_channels[i].name
            embed.add_field(name="Succès avec erreurs", value=val)
        return embed

    wrong_channels: list[GuildChannel] = list()

    perm = PermissionOverwrite()
    perm.view_channel = True
    perm.read_messages = True
    perm.read_message_history = voir_la_regle

    perm.update()

    print(ctx.author)
    for channel in channels:
        if channel is not None:
            if channel.permissions_for(ctx.author).manage_channels:
                for member in members:
                    if member is not None:
                        await channel.set_permissions(member, overwrite=perm)
            else:
                wrong_channels.append(channel)

    await ctx.respond(embed=generate_embed())


bot.run(os.getenv("TOKEN"))
