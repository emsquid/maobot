import os
import time
import random
import discord
from dotenv import load_dotenv
from discord.abc import GuildChannel
from discord import ApplicationContext, Member, PermissionOverwrite, Embed

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
        embed = Embed()

        if allowed:
            chosen_rule = rules.pop(random.randrange(len(rules)))

            embed.add_field(
                name="La règle choisie est... 🃏", value=format_rule(chosen_rule)
            )
        else:
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


@bot.slash_command(
    name="ajouter", description="Ajouter des joueurs à vos salons de règles"
)
@discord.option(
    "membre1",
    description="Sélectionne les membres qui auront accès aux salons",
    required=True,
)
@discord.option(
    "salon1",
    description="Sélectionne les salons auxquels les membres auront accès",
    required=True,
)
@discord.option(
    name="voir",
    description="Les membres pourront voir la règle",
    required=False,
    default=True,
)
@discord.option(
    "membre2",
    description="Sélectionne les membres qui auront accès aux salons",
    required=False,
    default=None,
)
@discord.option(
    "membre3",
    description="Sélectionne les membres qui auront accès aux salons",
    required=False,
    default=None,
)
@discord.option(
    "membre4",
    description="Sélectionne les membres qui auront accès aux salons",
    required=False,
    default=None,
)
@discord.option(
    "membre5",
    description="Sélectionne les membres qui auront accès aux salons",
    required=False,
    default=None,
)
@discord.option(
    "salon2",
    description="Sélectionne les salons auxquels les membres auront accès",
    required=False,
    default=None,
)
@discord.option(
    "salon3",
    description="Sélectionne les salons auxquels les membres auront accès",
    required=False,
    default=None,
)
@discord.option(
    "salon4",
    description="Sélectionne les salons auxquels les membres auront accès",
    required=False,
    default=None,
)
@discord.option(
    "salon5",
    description="Sélectionne les salons auxquels les membres auront accès",
    required=False,
    default=None,
)
async def ajouter(
    ctx: ApplicationContext,
    membre1: Member,
    salon1: GuildChannel,
    voir: bool,
    membre2: Member,
    membre3: Member,
    membre4: Member,
    membre5: Member,
    salon2: GuildChannel,
    salon3: GuildChannel,
    salon4: GuildChannel,
    salon5: GuildChannel,
):
    members = list(filter(None, [membre1, membre2, membre3, membre4, membre5]))
    channels = list(filter(None, [salon1, salon2, salon3, salon4, salon5]))
    wrong_channels: list[GuildChannel] = list()

    perm = PermissionOverwrite()
    perm.view_channel = True
    perm.read_message_history = voir
    perm.update()

    for channel in channels:
        if channel.permissions_for(ctx.author).manage_channels:
            for member in members:
                await channel.set_permissions(member, overwrite=perm)
        else:
            wrong_channels.append(channel)

    def generate_embed() -> Embed:
        embed = Embed()

        if len(wrong_channels) == 0:
            names = ", ".join(f"**{channel.name}**" for channel in channels)
            message = "Tous les membres ont maintenant accès à : " + names

            embed.add_field(name="Succès ✅", value=message)
        elif len(wrong_channels) == len(channels):
            message = "Vous n'êtes propriétaire d'aucun des salons fournis"
            embed.add_field(name="Erreur ⛔️", value=message)
        else:
            names = ", ".join(f"**{channel.name}**" for channel in wrong_channels)
            message = (
                "Les modifications n'ont pas pu être appliquées pour les salons suivants car vous n'êtes pas propriétaires : "
                + names
            )

            embed.add_field(name="Succès avec erreurs ⚠️", value=message)

        return embed

    await ctx.respond(embed=generate_embed(), ephemeral=True)


@bot.slash_command(
    name="supprimer", description="Supprimer des joueurs de vos salons de règles"
)
@discord.option(
    "membre1",
    description="Sélectionne les membres qui n'auront plus accès aux salons",
    required=True,
)
@discord.option(
    "salon1",
    description="Sélectionne les salons auxquels les membres n'auront plus accès",
    required=True,
)
@discord.option(
    "membre2",
    description="Sélectionne les membres qui n'auront plus accès aux salons",
    required=False,
    default=None,
)
@discord.option(
    "membre3",
    description="Sélectionne les membres qui n'auront plus accès aux salons",
    required=False,
    default=None,
)
@discord.option(
    "membre4",
    description="Sélectionne les membres qui n'auront plus accès aux salons",
    required=False,
    default=None,
)
@discord.option(
    "membre5",
    description="Sélectionne les membres qui n'auront plus accès aux salons",
    required=False,
    default=None,
)
@discord.option(
    "salon2",
    description="Sélectionne les salons auxquels les membres n'auront plus accès",
    required=False,
    default=None,
)
@discord.option(
    "salon3",
    description="Sélectionne les salons auxquels les membres n'auront plus accès",
    required=False,
    default=None,
)
@discord.option(
    "salon4",
    description="Sélectionne les salons auxquels les membres n'auront plus accès",
    required=False,
    default=None,
)
@discord.option(
    "salon5",
    description="Sélectionne les salons auxquels les membres n'auront plus accès",
    required=False,
    default=None,
)
async def supprimer(
    ctx: ApplicationContext,
    membre1: Member,
    salon1: GuildChannel,
    membre2: Member,
    membre3: Member,
    membre4: Member,
    membre5: Member,
    salon2: GuildChannel,
    salon3: GuildChannel,
    salon4: GuildChannel,
    salon5: GuildChannel,
):
    members = list(filter(None, [membre1, membre2, membre3, membre4, membre5]))
    channels = list(filter(None, [salon1, salon2, salon3, salon4, salon5]))
    wrong_channels: list[GuildChannel] = list()

    perm = PermissionOverwrite()
    perm.view_channel = False
    perm.read_message_history = False
    perm.update()

    for channel in channels:
        if channel.permissions_for(ctx.author).manage_channels:
            for member in members:
                await channel.set_permissions(member, overwrite=perm)
        else:
            wrong_channels.append(channel)

    def generate_embed() -> Embed:
        embed = Embed()

        if len(wrong_channels) == 0:
            names = ", ".join(f"**{channel.name}**" for channel in channels)
            message = "Tous les membres n'ont plus accès à : " + names

            embed.add_field(name="Succès ✅", value=message)
        elif len(wrong_channels) == len(channels):
            message = "Vous n'êtes propriétaire d'aucun des salons fournis"
            embed.add_field(name="Erreur ⛔️", value=message)
        else:
            names = ", ".join(f"**{channel.name}**" for channel in wrong_channels)
            message = (
                "Les modifications n'ont pas pu être appliquées pour les salons suivants car vous n'êtes pas propriétaires : "
                + names
            )

            embed.add_field(name="Succès avec erreurs ⚠️", value=message)

        return embed

    await ctx.respond(embed=generate_embed(), ephemeral=True)


load_dotenv()
bot.run(os.getenv("TOKEN"))
