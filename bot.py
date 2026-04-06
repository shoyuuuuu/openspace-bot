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
            label="Ton son en 3 mots",
            placeholder="Ex : sombre, lo-fi, cinématique",
            required=True,
            max_length=60
        ))
        self.add_item(discord.ui.InputText(
            label="Basé à",
            placeholder="Ville ou région",
            required=False,
            max_length=50
        ))
        self.add_item(discord.ui.InputText(
            label="Un lien",
            placeholder="Spotify, SoundCloud, Instagram...",
            required=False,
            max_length=200
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
        city_line = f"\n📍 Basé à : {values[3]}" if values[3] else ""
        link_line = f"\n🔗 {values[4]}" if values[4] else ""

        message = (
            f"📋 **Nouvelle recrue**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"**{values[0]}**\n"
            f"💼 {values[1]}\n"
            f"🎵 {values[2]}"
            f"{city_line}"
            f"{link_line}\n"
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
    await bot.sync_commands()
    print(f"Open Space Bot connecté en tant que {bot.user}")

token = os.environ.get("DISCORD_TOKEN")
if not token:
    raise ValueError("DISCORD_TOKEN manquant")

bot.run(token)
