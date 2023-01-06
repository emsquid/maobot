from discord.abc import GuildChannel
from discord import (
    Guild,
    Member,
    Embed,
    ChannelType,
    TextChannel,
    CategoryChannel,
    PermissionOverwrite,
)


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


def create_embed(title: str, message: str) -> Embed:
    """Return a discord embed"""
    embed = Embed()
    embed.add_field(name=title, value=message)
    return embed


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

    return create_embed(title, message)


def get_categories(member: Member, guild: Guild) -> CategoryChannel:
    """Return the category belonging to the member"""
    categories = []

    for category in guild.categories:
        if category.permissions_for(member).manage_channels:
            categories.append(category)

    return categories


async def get_resume_channel(category: CategoryChannel) -> TextChannel:
    """Return the resume channel from the category, create it if it doesn't exist"""
    for channel in category.channels:
        if channel.name == "mes-règles":
            return channel

    return await category.create_text_channel("mes-règles")


def count_known_rules_for_member(
    guild: Guild, cache: bool, owns: bool
) -> dict[int:int]:
    """Return a dictionnary with member id as key and the rules they know as value"""
    rules_count: dict[int:int] = dict()

    for channel in guild.channels:
        if channel.type != ChannelType.category:
            for member in channel.members:
                if (
                    channel.name.startswith("règle")
                    and not channel.name == "règle-de"
                    and (not channel.permissions_for(member).administrator)
                    and (not channel.permissions_for(member).manage_channels or owns)
                    and (channel.permissions_for(member).read_message_history or cache)
                ):
                    rules_count[member.id] = rules_count.get(member.id, 0) + 1

    return rules_count


def get_keys_from_value(dic: dict[int:int], value: int) -> list[int]:
    """Return all keys matching value"""
    val_list: list[int] = list()
    for key, v in dic.items():
        if v == value:
            val_list.append(key)

    return val_list
