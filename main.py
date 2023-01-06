import os
import time
import random
import discord
import src.helper as helper
from dotenv import load_dotenv
from discord.abc import GuildChannel
from discord.ui import Button, View
from discord import ApplicationContext, Member, PermissionOverwrite, Embed

bot = discord.Bot(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{time.strftime('[%d-%m-%Y %H:%M:%S]', time.localtime())}")
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="atouts",
                   description="Génère aléatoirement une règles intégrant les atouts")
async def atouts(ctx: ApplicationContext):
    atouts_id: list[int] = [1040270798604226570, 1040265350274621590]
    embed = Embed()
    embed.add_field(name=f"La règle choisie est la règle {bot.get_channel(atouts_id.pop(random.randrange(len(atouts_id)))).name.replace('règle-', '')}", value="")

    await ctx.respond(embed=embed)


@bot.slash_command(
    name="règle",
    description="Choisi une règle au hasard parmi toutes celles existantes",
)
@discord.option(
    name="inconnues",
    description="Cherche aussi parmi les règles que vous ne connaissez pas (défaut: Faux)",
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

    def generate_embed(allowed: bool = True) -> Embed:
        if allowed:
            chosen_rule = rules.pop(random.randrange(len(rules)))

            return helper.create_embed(
                "La règle choisie est... 🃏", helper.format_rule(chosen_rule)
            )
        else:
            return helper.create_embed("Erreur ⛔️", "Vous ne pouvez pas faire ça")

    def generate_view() -> View:
        reroll_button = Button(label="Reroll")
        reroll_button.callback = reroll

        return View(reroll_button, disable_on_timeout=True)

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
    description="Les membres pourront voir la règle (défaut: Vrai)",
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

    result_embed = await helper.change_permissions(
        ctx.author, members, channels, permission
    )

    await ctx.respond(embed=result_embed, ephemeral=True)


@bot.slash_command(
    name="supprimer", description="Supprimer des joueurs de vos salons de règles"
)
@discord.option(
    "membre1",
    description="Sélectionne un membre qui n'auront plus accès aux salons",
    required=True,
)
@discord.option(
    "salon1",
    description="Sélectionne un salon auquel les membres n'auront plus accès",
    required=True,
)
@discord.option(
    "membre2",
    description="Sélectionne un membre qui n'auront plus accès aux salons",
    default=None,
)
@discord.option(
    "membre3",
    description="Sélectionne un membre qui n'auront plus accès aux salons",
    default=None,
)
@discord.option(
    "membre4",
    description="Sélectionne un membre qui n'auront plus accès aux salons",
    default=None,
)
@discord.option(
    "membre5",
    description="Sélectionne un membre qui n'auront plus accès aux salons",
    default=None,
)
@discord.option(
    "salon2",
    description="Sélectionne un salon auquel les membres n'auront plus accès",
    default=None,
)
@discord.option(
    "salon3",
    description="Sélectionne un salon auquel les membres n'auront plus accès",
    default=None,
)
@discord.option(
    "salon4",
    description="Sélectionne un salon auquel les membres n'auront plus accès",
    default=None,
)
@discord.option(
    "salon5",
    description="Sélectionne un salon auquel les membres n'auront plus accès",
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

    result_embed = await helper.change_permissions(
        ctx.author, members, channels, permission
    )

    await ctx.respond(embed=result_embed, ephemeral=True)


@bot.slash_command(
    name="résumé",
    description="Affichage de toutes les personnes pouvant voir vos règles",
)
async def resume(ctx: ApplicationContext):
    author_categories = helper.get_categories(ctx.author, ctx.guild)

    # prevent someone with no categories from trying
    if len(author_categories) == 0:
        error_embed = helper.create_embed("Erreur ⛔️", "Vous n'avez aucune catégorie")

        return await ctx.respond(embed=error_embed, ephemeral=True)

    resume_channel = await helper.get_resume_channel(author_categories[0])

    await ctx.respond(
        embed=helper.create_embed(
            "Succès ✅",
            f"Allez dans le salon suivant : {resume_channel.mention} !",
        ),
        ephemeral=True,
    )

    # create message
    message = ""
    nb_rules = 0

    for category in author_categories:
        for channel in category.channels:
            if channel.name.startswith("règle-") and channel.name != "règle-de":
                member_names = ", ".join(
                    member.display_name
                    for member in channel.members
                    if not channel.permissions_for(member).administrator
                )

                message += f"{channel.mention}:\n{member_names}\n"
                nb_rules += 1

    # send message
    embed = helper.create_embed(
        f"Règles de {ctx.author.display_name} ({nb_rules}) 📏",
        message,
    )

    await resume_channel.purge()
    await resume_channel.send(embed=embed)


@bot.slash_command(
    name="classement",
    description="Obtenez le classement de ceux qui connaissent le plus de règles",
)
@discord.option(
    name="cache",
    description="Compte aussi les règles dont seul le nom est visible (défaut: Vrai)",
    default=True,
)
@discord.option(
    name="votres",
    description="Compte aussi les règles qui vous appartiennent (défaut: Faux)",
    default=False,
)
async def classement(ctx: ApplicationContext, cache: bool, votres: bool):
    rules_count = helper.count_known_rules_for_member(ctx.guild, cache, votres)
    # create message
    message = ""

    real_max = max(rules_count.values())
    rank = 1

    for n in range(real_max, -1, -1):
        members_id = helper.get_keys_from_value(rules_count, n)

        if len(members_id) >= 1:
            message += f"{rank} "
            for id in members_id:
                message += f"- **{ctx.guild.get_member(id).display_name}** "
            message += f"avec **{n}** règles\n"

            rank += 1

    embed = helper.create_embed("Classement 🏆", message)

    await ctx.respond(embed=embed)


@bot.slash_command(
    name="aide",
    description="Obtenez toutes les commandes disponibles",
)
async def aide(ctx: ApplicationContext):
    message = "Voici toutes les commandes :\n"
    for command in bot.walk_application_commands():
        message += f"**{command.name}**: {command.description}\n"

    await ctx.respond(embed=helper.create_embed("Aide 📚", message))


load_dotenv()
bot.run(os.getenv("TOKEN"))
