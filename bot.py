import discord
import os

bot = discord.Bot()

PRESENTATION_CHANNEL_NAME = "présentations"

class PresentationModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="📋 Nouvelle recrue — Open Space")
        self.add_item(discord.ui.InputText(
            label="Nom / Alias",
            placeholder="Comment tu t'appelles ?",
            required=True,
            max_length=50
        ))
        self.add_item(discord.ui.InputText(
            label="Ce que tu fais",
            placeholder="Rappeur, beatmaker, auteur...",
            required=True,
            max_length=100
        ))
        self.add_item(discord.ui.InputText(
            label="Ton son en quelques mots",
            placeholder="Ex : sombre, lo-fi, cinématique",
            required=True,
            max_length=100
        ))
        self.add_item(discord.ui.InputText(
            label="Un lien",
            placeholder="Spotify, SoundCloud, Instagram...",
            required=False,
            max_length=200
        ))
        self.add_item(discord.ui.InputText(
            label="Un mot pour te présenter",
            placeholder="Dis ce que tu veux...",
            required=False,
            style=discord.InputTextStyle.long,
            max_length=300
        ))

    async def callback(self, interaction: discord.Interaction):
        channel = discord.utils.get(
            interaction.guild.text_channels,
            name=PRESENTATION_CHANNEL_NAME
        )
        if not channel:
            await interaction.response.send_message(
                f"Le channel `#{PRESENTATION_CHANNEL_NAME}` est introuvable.",
                ephemeral=True
            )
            return

        values = [child.value for child in self.children]
        link_line = f"\n{values[3]}" if values[3] else ""
        note_line = f"\n\n{values[4]}" if values[4] else ""

        message = (
            f"📋 **Nouvelle recrue**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Nom / Alias : **{values[0]}**\n"
            f"Ce que tu fais : {values[1]}\n"
            f"Ton son : {values[2]}"
            f"{link_line}"
            f"{note_line}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )

        await channel.send(message)
        await interaction.response.send_message(
            "Ta fiche a été déposée dans #présentations. Bienvenue dans les locaux.",
            ephemeral=True
        )

@bot.slash_command(name="présentation", description="Remplis ta fiche et rejoins l'équipe")
async def presentation(ctx: discord.ApplicationContext):
    await ctx.send_modal(PresentationModal())

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name="Open Space")
    if guild:
        await bot.sync_commands(guild_ids=[guild.id])
        print(f"Commandes synchronisées sur {guild.name}")
    print(f"Open Space Bot connecté en tant que {bot.user}")

token = os.environ.get("DISCORD_TOKEN")
if not token:
    raise ValueError("DISCORD_TOKEN manquant")

bot.run(token)
