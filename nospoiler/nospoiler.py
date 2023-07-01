"""
MIT License

Copyright (c) 2022-present ltzmax

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import logging
import re
from typing import Union

import discord
from redbot.core import Config, app_commands, commands
from redbot.core.utils.chat_formatting import box

SPOILER_REGEX = re.compile(r"(?s)\|\|(.+?)\|\|")

log = logging.getLogger("red.maxcogs.nospoiler")


class NoSpoiler(commands.Cog):
    """No spoiler in this server."""

    __author__ = "MAX"
    __version__ = "1.5.0"
    __docs__ = "https://github.com/ltzmax/maxcogs/blob/master/nospoiler/README.md"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=1234567890, force_registration=True
        )
        default_guild = {
            "enabled": False,
            "log_channel": None,
        }
        self.config.register_guild(**default_guild)

    def format_help_for_context(self, ctx):
        """Thanks Sinbad!"""
        pre = super().format_help_for_context(ctx)
        return f"{pre}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}\nDocs: {self.__docs__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """handle spoiler messages"""
        if message.guild is None:
            return
        if not await self.config.guild(message.guild).enabled():
            return
        if not message.guild.me.guild_permissions.manage_messages:
            if await self.config.guild(message.guild).enabled():
                await self.config.guild(message.guild).enabled.set(False)
                log.info(
                    f"Spoiler filter is now disabled because I don't have manage_messages permission."
                )
            return
        if await self.bot.cog_disabled_in_guild(self, message.guild):
            return
        if message.author.bot:
            return
        if await self.bot.is_automod_immune(message.author):
            return
        if SPOILER_REGEX.search(message.content):
            log_channel = await self.config.guild(message.guild).log_channel()
            if log_channel:
                log_channel = message.guild.get_channel(log_channel)
                if log_channel:
                    embed = discord.Embed(
                        title="Spoiler message deleted",
                        description=f"**Author:** {message.author.mention} ({message.author.id}) \n**Channel:** {message.channel.mention}\n**Message:**\n{message.content}",
                        color=await self.bot.get_embed_color(log_channel),
                    )
                    await log_channel.send(embed=embed)
            await message.delete()
            return
        if attachments := message.attachments:
            for attachment in attachments:
                if attachment.is_spoiler():
                    log_channel = await self.config.guild(message.guild).log_channel()
                    if log_channel:
                        log_channel = message.guild.get_channel(log_channel)
                        if log_channel:
                            embed = discord.Embed(
                                title="Spoiler attachment deleted",
                                description=f"**Author:** {message.author.mention} ({message.author.id})\n**Channel:** {message.channel.mention}\n**Attachment:**\n{message.content} {attachment.url}",
                                color=await self.bot.get_embed_color(log_channel),
                            )
                            await log_channel.send(embed=embed)
                    await message.delete()

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        """handle edits"""
        if payload.guild_id is None:
            return
        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return
        if not await self.config.guild(guild).enabled():
            return
        if not guild.me.guild_permissions.manage_messages:
            if await self.config.guild(guild).enabled():
                await self.config.guild(guild).enabled.set(False)
                log.info(
                    f"Spoiler filter is now disabled because I don't have manage_messages permission."
                )
            return
        if await self.bot.cog_disabled_in_guild(self, guild):
            return
        channel = guild.get_channel(payload.channel_id)
        if channel is None:
            return
        try:
            message = await channel.fetch_message(payload.message_id)
        except discord.NotFound:
            return
        if await self.bot.is_automod_immune(message.author):
            return
        if message.author.bot:
            return
        if SPOILER_REGEX.search(message.content):
            log_channel = await self.config.guild(guild).log_channel()
            if log_channel:
                log_channel = guild.get_channel(log_channel)
                if log_channel:
                    embed = discord.Embed(
                        title="Spoiler message edited",
                        description=f"**Author:** {message.author.mention}\n**Channel:** {message.channel.mention}\n**Message:** {message.content}",
                        color=await self.bot.get_embed_color(log_channel),
                    )
                    await log_channel.send(embed=embed)
            await message.delete()

    @commands.group()
    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    async def nospoiler(self, ctx):
        """Manage the spoiler filter settings."""

    @nospoiler.command()
    async def toggle(self, ctx):
        """Toggle the spoiler filter on or off.

        Spoiler filter is disabled by default.
        """
        if not ctx.bot_permissions.manage_messages:
            msg = (
                f"{self.bot.user.name} does not have permission to `manage_messages` to remove spoiler.\n"
                "It need this permission before you can enable the spoiler filter. "
                f"Else {self.bot.user.name} will not be able to remove any spoiler messages."
            )
            return await ctx.send(msg, ephemeral=True)
        enabled = await self.config.guild(ctx.guild).enabled()
        if enabled:
            await self.config.guild(ctx.guild).enabled.set(False)
            await ctx.send("Spoiler filter is now disabled.")
        else:
            await self.config.guild(ctx.guild).enabled.set(True)
            await ctx.send("Spoiler filter is now enabled.")

    @nospoiler.command()
    async def logchannel(self, ctx, channel: discord.TextChannel = None):
        """Set the channel where the bot will log the deleted spoiler messages.

        If the channel is not set, the bot will not log the deleted spoiler messages.
        """
        if (
            not channel.permissions_for(ctx.me).send_messages
            or not channel.permissions_for(ctx.me).embed_links
        ):
            msg = (
                f"{self.bot.user.name} does not have permission to `send_messages` or `embed_links` to send log messages.\n"
                "It need this permission before you can set the log channel. "
                f"Else {self.bot.user.name} will not be able to send any log messages."
            )
            return await ctx.send(msg)
        if channel is None:
            await self.config.guild(ctx.guild).log_channel.set(None)
            await ctx.send("Log channel has been reset.")
        else:
            await self.config.guild(ctx.guild).log_channel.set(channel.id)
            await ctx.send(f"Log channel has been set to {channel.mention}.")

    @nospoiler.command(aliases=["view", "views"])
    @commands.bot_has_permissions(embed_links=True)
    async def settings(self, ctx):
        """Show the settings."""
        config = await self.config.guild(ctx.guild).all()
        enabled = config["enabled"]
        log_channel = config["log_channel"]
        embed = discord.Embed(
            title="Spoiler Filter Settings",
            description=f"Spoiler filter is currently **{'enabled' if enabled else 'disabled'}**\nLog Channel: {log_channel}.",
            color=await ctx.embed_color(),
        )
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @nospoiler.command()
    async def version(self, ctx: commands.Context):
        """Shows the version of the cog."""
        version = self.__version__
        author = self.__author__
        embed = discord.Embed(
            title="Cog Information",
            description=box(
                f"{'Cog Author':<11}: {author}\n{'Cog Version':<10}: {version}",
                lang="yaml",
            ),
            color=await ctx.embed_color(),
        )
        await ctx.send(embed=embed)
