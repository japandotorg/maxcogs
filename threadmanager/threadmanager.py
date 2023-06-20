import discord
from redbot.core import commands


class ThreadManager(commands.Cog):
    """close, lock, open and unlock threads. You are also able to create threads."""

    __author__ = "MAX"
    __version__ = "1.0.2"
    __docs__ = "https://github.com/ltzmax/maxcogs/blob/master/threadmanager/README.md"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}\nDocs: {self.__docs__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.hybrid_group(aliases=["threads"])
    @commands.has_permissions(manage_threads=True, manage_messages=True)
    @commands.bot_has_permissions(manage_threads=True, manage_messages=True)
    async def thread(self, ctx):
        """Manage close, lock, open and unlock threads and also create threads."""

    @thread.command()
    async def close(self, ctx):
        """Close a thread.

        Note this does both lock and close.
        """
        audit_reason = f"Thread closed by {ctx.author} (ID: {ctx.author.id})"
        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.send("This isn't a thread.")
        # So it doesn't reopen the thread.
        await ctx.send(f"Closed thread.")
        await ctx.channel.edit(locked=True, archived=True, reason=audit_reason)

    @thread.command()
    async def lock(self, ctx):
        """Lock a thread."""
        audit_reason = f"Thread locked by {ctx.author} (ID: {ctx.author.id})"
        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.send("This isn't a thread.")
        await ctx.channel.edit(locked=True, reason=audit_reason)
        await ctx.send(f"Locked thread.")

    @thread.command(with_app_command=False)  # Chant use slash in archived threads.
    async def unlock(self, ctx):
        """Unlock a thread."""
        audit_reason = f"Thread unlocked by {ctx.author} (ID: {ctx.author.id})"
        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.send("This isn't a thread.")
        await ctx.channel.edit(locked=False, reason=audit_reason)
        await ctx.send(f"Unlocked thread.")

    @thread.command(with_app_command=False)  # Chant use slash in archived threads.
    async def open(self, ctx):
        """Open a thread.

        Note this does both unlock and open.
        """
        audit_reason = f"Thread opened by {ctx.author} (ID: {ctx.author.id})"
        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.send("This isn't a thread.")
        await ctx.channel.edit(locked=False, archived=False, reason=audit_reason)
        await ctx.send(f"Opened thread.")

    @thread.command()
    @commands.bot_has_permissions(manage_channels=True, manage_threads=True)
    async def create(self, ctx, name: str):
        """Create a thread.

        Note: This will create a thread in the category under same channel you run the command in.
        (You will not be automatic joined to the thread, you will have to look in the thread list.)
        """
        if not isinstance(ctx.channel, discord.TextChannel):
            return await ctx.send("This isn't a text channel.")
        if len(name) > 100:
            return await ctx.send("Thread name can't be longer than 100 characters.")
        await ctx.channel.create_thread(name=name, auto_archive_duration=1440)
        await ctx.send("Thread created.")
