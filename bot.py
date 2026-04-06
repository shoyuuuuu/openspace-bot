import discord
from discord import app_commands
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

PRESENTATION_CHANNEL_NAME = "présentations"

class PresentationModal(discord.ui.Modal, title="📋 Nouvelle recrue — Open Space"):
    alias = discord.ui.TextInput(
        label="Nom / Alias",
        placeholder="Comment tu t'appelles ?",
        required=True,
        max_length=50
    )
    role = discord.ui.TextInput(
        label="Ce que tu fais",
        placeholder="Rappeur, beatmaker, auteur...",
        required=True,
        max_length=100
    )
    sound = discord.ui.TextInput(
        label="Ton son en 3 mots",
        placeholder="Ex : sombre, lo-fi, cinématique",
        required=True,
        max_length=60
    )
    city = discord.ui.TextInput(
        label="Basé à",
        placeholder="Ville ou région",
        required=False,
        max_length=50
    )
    link = discord.ui.TextInput(
        label="Un lien",
        placeholder="Spotify, SoundCloud, Instagram...",
        required=False,
        max_length=200
    )

    async def on_submit(self, interaction: discord.Interaction):
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

        city_line = f"\n📍 Basé à : {self.city.value}" if self.city.value else ""
        link_line = f"\n🔗 {self.link.value}" if self.link.value else ""

        message = (
            f"📋 **Nouvelle recrue**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"**{self.alias.value}**\n"
            f"💼 {self.role.value}\n"
            f"🎵 {self.sound.value}"
            f"{city_line}"
            f"{link_line}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )

        await channel.send(message)
        await interaction.response.send_message(
            "Ta fiche a été déposée dans #présentations. Bienvenue dans les locaux.",
            ephemeral=True
        )

@tree.command(
    name="présentation",
    description="Remplis ta fiche et rejoins l'équipe"
)
async def presentation(interaction: discord.Interaction):
    await interaction.response.send_modal(PresentationModal())

@client.event
async def on_ready():
    await tree.sync()
    print(f"Open Space Bot connecté en tant que {client.user}")

token = os.environ.get("DISCORD_TOKEN")
if not token:
    raise ValueError("DISCORD_TOKEN manquant")

client.run(token)
