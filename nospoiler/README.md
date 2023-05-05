# NoSpoiler Help

No spoiler in this server.

# nospoiler (Hybrid Command)
 - Usage: `[p]nospoiler `
 - Slash Usage: `/nospoiler `
 - Restricted to: `ADMIN`
 - Checks: `server_only`

Manage the spoiler filter settings.

## nospoiler settings (Hybrid Command)
 - Usage: `[p]nospoiler settings `
 - Slash Usage: `/nospoiler settings `
 - Aliases: `view, views, setting, showsettings, and showsetting`

Show the settings.

## nospoiler toggle (Hybrid Command)
 - Usage: `[p]nospoiler toggle `
 - Slash Usage: `/nospoiler toggle `

Toggle the spoiler filter on or off.<br/><br/>Spoiler filter is disabled by default.

## nospoiler ignorechannel (Hybrid Command)
 - Usage: `[p]nospoiler ignorechannel <channel> `
 - Slash Usage: `/nospoiler ignorechannel <channel> `

Add or remove ignore a channel from the spoiler filter.<br/><br/>If a channel is ignored, spoiler messages will not be deleted.<br/>Note: you cannot ignore a voice chat channel.

Extended Arg Info
> ### channel: Union[discord.channel.TextChannel, discord.threads.Thread, discord.channel.ForumChannel]
>
>
>     1. Lookup by ID.
>     2. Lookup by mention.
>     3. Lookup by name
>
>
## nospoiler reset (Hybrid Command)
 - Usage: `[p]nospoiler reset `
 - Slash Usage: `/nospoiler reset `
 - Aliases: `clear`
 - Cooldown: `2 per 120.0 seconds`

Reset all settings back to default.<br/><br/>This will disable the spoiler filter and remove all ignored channels.

## nospoiler version (Hybrid Command)
 - Usage: `[p]nospoiler version `
 - Slash Usage: `/nospoiler version `

Shows the version of the cog.

## nospoiler set (Hybrid Command)
 - Usage: `[p]nospoiler set `
 - Slash Usage: `/nospoiler set `

Settings to manage custom messages sent.<br/><br/>This is when spoiler message(s) is deleted, it will send a custom message telling users they're not allowed to.

### nospoiler set message (Hybrid Command)
 - Usage: `[p]nospoiler set message [message] `
 - Slash Usage: `/nospoiler set message [message] `

Set the message to send when a user sends a spoiler message.<br/><br/>If no message is provided, the default message will be sent.<br/>If you want to disable the message, use [p]nospoiler set togglemessage.

Extended Arg Info
> ### message: str = None
> ```
> Something like: hello you cant do this stuff
> ```

### nospoiler set togglemessage (Hybrid Command)
 - Usage: `[p]nospoiler set togglemessage `
  - Aliases: `togglemsg`
 - Slash Usage: `/nospoiler set togglemessage `

Enable or disable the message to send when a user sends a spoiler message.<br/><br/>If the message is disabled, the bot will delete the spoiler message without sending a message.