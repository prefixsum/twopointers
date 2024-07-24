from disnake.ext import commands
import disnake
from config_manager import load_config, save_config


def setup(bot):
    @bot.slash_command(description="Manage alert settings")
    async def alert(inter):
        pass

    @alert.sub_command(description="Enable a specific type of alert in a channel")
    async def enable(
        inter,
        type: str = commands.Param(
            choices=["daily_problem", "weekly_contest", "biweekly_contest"]
        ),
        channel: disnake.TextChannel = None,
    ):
        if not channel:
            channel = inter.channel
        config = load_config(inter.guild.id)
        config[type] = {"channel_id": channel.id, "enabled": True}
        save_config(inter.guild.id, config)
        await inter.response.send_message(
            f"Enabled `{type}` alerts in {channel.mention}."
        )

    @alert.sub_command(description="Disable a specific type of alert")
    async def disable(
        inter,
        type: str = commands.Param(
            choices=["daily_problem", "weekly_contest", "biweekly_contest"]
        ),
    ):
        config = load_config(inter.guild.id)
        if type in config and config[type]["enabled"]:
            config[type]["enabled"] = False
            save_config(inter.guild.id, config)
            await inter.response.send_message(f"Disabled {type} alerts.")
        else:
            await inter.response.send_message(
                f"{type} alerts are not enabled or do not exist."
            )

    @alert.sub_command(description="List all alert settings")
    async def list(inter):
        config = load_config(inter.guild.id)
        if config:
            descriptions = []
            for alert_type, settings in config.items():
                enabled_status = "enabled" if settings["enabled"] else "disabled"
                channel = bot.get_channel(settings["channel_id"])
                channel_name = channel.mention if channel else "unknown channel"
                descriptions.append(
                    f"`{alert_type}` alerts {enabled_status} in {channel_name}"
                )
            description = "\n".join(descriptions)
        else:
            description = "No alerts have been configured."
        await inter.response.send_message(description)
