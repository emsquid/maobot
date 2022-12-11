import os
import time
import random
import discord
from dotenv import load_dotenv
from discord.abc import GuildChannel
from discord import ApplicationContext, Member, PermissionOverwrite, Embed

bot = discord.Bot()


def format_rule(rule: str) -> str:
    """Format a channel name to a good looking string"""
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


async def change_permissions(
    author: Member,
    members: list[Member],
    channels: list[GuildChannel],
    permission: PermissionOverwrite,
) -> Embed:
    """Change permissions and return result in an Embed"""
    right_channels: list[GuildChannel] = list()
    wrong_channels: list[GuildChannel] = list()

    for channel in channels:
        if channel.permissions_for(author).manage_channels:
            for member in members:
                await channel.set_permissions(member, overwrite=permission)
            right_channels.append(channel)
        else:
            wrong_channels.append(channel)

    right_names = ", ".join(f"**{channel.name}**" for channel in right_channels)
    right_message = "Les permissions ont bien été changées pour : " + right_names

    wrong_names = ", ".join(f"**{channel.name}**" for channel in wrong_channels)
    wrong_message = "Vous n'êtes pas propriétaire des salons suivants : " + wrong_names

    if len(wrong_channels) == 0:
        title = "Succès ✅"
        message = right_message
    elif len(wrong_channels) == len(channels):
        title = "Erreur ⛔️"
        message = wrong_message
    else:
        title = "Succès avec erreurs ⚠️"
        message = f"{right_message}\n{wrong_message}"

    embed = Embed()
    embed.add_field(name=title, value=message)

    return embed


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
    default=True,
)
@discord.option(
    "membre2",
    description="Sélectionne les membres qui auront accès aux salons",
    default=None,
)
@discord.option(
    "membre3",
    description="Sélectionne les membres qui auront accès aux salons",
    default=None,
)
@discord.option(
    "membre4",
    description="Sélectionne les membres qui auront accès aux salons",
    default=None,
)
@discord.option(
    "membre5",
    description="Sélectionne les membres qui auront accès aux salons",
    default=None,
)
@discord.option(
    "salon2",
    description="Sélectionne les salons auxquels les membres auront accès",
    default=None,
)
@discord.option(
    "salon3",
    description="Sélectionne les salons auxquels les membres auront accès",
    default=None,
)
@discord.option(
    "salon4",
    description="Sélectionne les salons auxquels les membres auront accès",
    default=None,
)
@discord.option(
    "salon5",
    description="Sélectionne les salons auxquels les membres auront accès",
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

    permission = PermissionOverwrite()
    permission.view_channel = True
    permission.read_message_history = voir
    permission.update()

    result_embed = await change_permissions(ctx.author, members, channels, permission)

    await ctx.respond(embed=result_embed, ephemeral=True)


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
    default=None,
)
@discord.option(
    "membre3",
    description="Sélectionne les membres qui n'auront plus accès aux salons",
    default=None,
)
@discord.option(
    "membre4",
    description="Sélectionne les membres qui n'auront plus accès aux salons",
    default=None,
)
@discord.option(
    "membre5",
    description="Sélectionne les membres qui n'auront plus accès aux salons",
    default=None,
)
@discord.option(
    "salon2",
    description="Sélectionne les salons auxquels les membres n'auront plus accès",
    default=None,
)
@discord.option(
    "salon3",
    description="Sélectionne les salons auxquels les membres n'auront plus accès",
    default=None,
)
@discord.option(
    "salon4",
    description="Sélectionne les salons auxquels les membres n'auront plus accès",
    default=None,
)
@discord.option(
    "salon5",
    description="Sélectionne les salons auxquels les membres n'auront plus accès",
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

    permission = PermissionOverwrite()
    permission.view_channel = False
    permission.read_message_history = False
    permission.update()

    result_embed = await change_permissions(ctx.author, members, channels, permission)

    await ctx.respond(embed=result_embed, ephemeral=True)


load_dotenv()
bot.run(os.getenv("TOKEN"))
