import discord
from discord.ext import commands
from discord.ui import Button, View

# ===========================================
# ==========  НАСТРОЙКИ (ВСТАВЛЕНЫ ПРЯМО) ==========
# ===========================================
TOKEN = "MTUwODAzMDk3Mjg3NTExNjU2NQ.G60fmw.ZwIeW5MFlI521L_Uc2EPdBhRTNUuul_vSO9hDs"
VERIFIED_ROLE_ID = 1470685292817285225  # ID роли которую ВЫДАЁМ
ROLE_TO_REMOVE_ID = 1474180838244745278  # ID роли которую СНИМАЕМ
YOUR_USER_ID = 1497266013954248867  # ТВОЙ ID
# ===========================================
# ===========================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

def is_owner(ctx):
    return ctx.author.id == YOUR_USER_ID

# ===========================================
# ==========  КНОПКА ВЕРИФИКАЦИИ ==========
# ===========================================
class VerifyButton(Button):
    def __init__(self):
        super().__init__(
            label="Верифицироваться",
            style=discord.ButtonStyle.danger,
            emoji="✅",
            custom_id="kx_verify_button"
        )
    
    async def callback(self, interaction: discord.Interaction):
        role_to_give = interaction.guild.get_role(VERIFIED_ROLE_ID)
        role_to_remove = interaction.guild.get_role(ROLE_TO_REMOVE_ID)
        
        if role_to_give is None:
            await interaction.response.send_message(
                "❌ **Ошибка!** Роль верификации не найдена.",
                ephemeral=True
            )
            return
        
        if role_to_give in interaction.user.roles:
            await interaction.response.send_message(
                "✅ **Вы уже верифицированы!**",
                ephemeral=True
            )
            return
        
        await interaction.user.add_roles(role_to_give)
        
        removed_text = ""
        if role_to_remove is not None and role_to_remove in interaction.user.roles:
            await interaction.user.remove_roles(role_to_remove)
            removed_text = f"\n- Снята роль {role_to_remove.name}"
        
        success_embed = discord.Embed(
            title="🎉 **ДОБРО ПОЖАЛОВАТЬ В KX COMMUNITY!** 🎉",
            description=(
                f"```diff\n"
                f"+ Верификация успешно пройдена!\n"
                f"+ Теперь вам открыты все каналы{removed_text}\n"
                f"+ Приятного общения!\n"
                f"```"
            ),
            color=discord.Color.green()
        )
        success_embed.set_footer(text="KX Community ❤️")
        
        await interaction.response.send_message(embed=success_embed, ephemeral=True)

class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(VerifyButton())

# ===========================================
# ==========  ОТПРАВКА СООБЩЕНИЯ ==========
# ===========================================
async def send_verify_message(channel):
    embed = discord.Embed(
        title="🔴 **KX COMMUNITY** 🔴",
        description="",
        color=discord.Color.red()
    )
    
    embed.add_field(
        name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        value="",
        inline=False
    )
    
    embed.add_field(
        name="✨ **ДОБРО ПОЖАЛОВАТЬ НА СЕРВЕР!** ✨",
        value=(
            "🔴 Этот сервер требует верификации для получения доступа ко всем каналам.\n"
            "🔴 Вы можете верифицироваться, нажав на кнопку ниже.\n\n"
            "**🔴 ВЕРИФИЦИРОВАТЬСЯ** 🔴"
        ),
        inline=False
    )
    
    embed.add_field(
        name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        value="",
        inline=False
    )
    
    embed.add_field(
        name="✅ **ПОСЛЕ ВЕРИФИКАЦИИ ВАМ ОТКРОЕТСЯ:**",
        value=(
            "🔹 Все текстовые и голосовые каналы\n"
            "🔹 Доступ к эксклюзивному контенту\n"
            "🔹 Участие в ивентах и розыгрышах\n"
            "🔹 Общение с активным сообществом"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚠️ **ПРАВИЛА СЕРВЕРА:**",
        value=(
            "🔸 Уважайте других участников\n"
            "🔸 Без токсичности и оскорблений\n"
            "🔸 Не спамить и не флудить\n"
            "🔸 Соблюдайте правила Discord"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔴 **ВАЖНО:**",
        value="🔴 Нажимая на кнопку, вы автоматически соглашаетесь с правилами сервера **KX Community**.",
        inline=False
    )
    
    embed.add_field(
        name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        value="",
        inline=False
    )
    
    embed.set_footer(text="KX Community | Нажми на кнопку для верификации 🔴")
    
    view = VerifyView()
    await channel.send(embed=embed, view=view)

# ===========================================
# ==========  КОМАНДЫ ==========
# ===========================================

@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} успешно запущен!")
    print(f"🔴 KX Community - бот верификации активен!")
    print(f"👑 Твой ID: {YOUR_USER_ID}")
    print(f"✅ Роль для выдачи: {VERIFIED_ROLE_ID}")
    print(f"❌ Роль для снятия: {ROLE_TO_REMOVE_ID}")
    bot.add_view(VerifyView())

@bot.command()
@commands.check(is_owner)
async def verify(ctx):
    await send_verify_message(ctx.channel)
    confirm_embed = discord.Embed(
        description="✅ **Сообщение с верификацией отправлено!**",
        color=discord.Color.green()
    )
    await ctx.send(embed=confirm_embed, delete_after=3)

@bot.command(name="v")
@commands.check(is_owner)
async def short_verify(ctx):
    await send_verify_message(ctx.channel)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def verify_user(ctx, member: discord.Member):
    role_give = ctx.guild.get_role(VERIFIED_ROLE_ID)
    role_remove = ctx.guild.get_role(ROLE_TO_REMOVE_ID)
    
    if role_give is None:
        await ctx.send("❌ **Ошибка!** Роль верификации не найдена.")
        return
    
    if role_give in member.roles:
        await ctx.send(f"✅ {member.mention} **уже верифицирован!**")
        return
    
    await member.add_roles(role_give)
    
    remove_text = ""
    if role_remove and role_remove in member.roles:
        await member.remove_roles(role_remove)
        remove_text = f"\n- Снята роль {role_remove.mention}"
    
    embed = discord.Embed(
        title="✅ **Роль верификации выдана!**",
        description=f"{member.mention} теперь верифицирован в **KX Community**!{remove_text}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def unverify(ctx, member: discord.Member):
    role = ctx.guild.get_role(VERIFIED_ROLE_ID)
    if role is None:
        await ctx.send("❌ **Ошибка!** Роль не найдена.")
        return
    if role not in member.roles:
        await ctx.send(f"⚠️ {member.mention} **не верифицирован.**")
        return
    await member.remove_roles(role)
    embed = discord.Embed(
        title="🔴 **Роль снята!**",
        description=f"{member.mention} больше не верифицирован.",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def verify_stats(ctx):
    role = ctx.guild.get_role(VERIFIED_ROLE_ID)
    if role is None:
        await ctx.send("❌ **Ошибка!** Роль не найдена.")
        return
    verified_count = len(role.members)
    total_members = ctx.guild.member_count
    percentage = round((verified_count / total_members) * 100, 1)
    embed = discord.Embed(
        title="📊 **СТАТИСТИКА ВЕРИФИКАЦИИ**",
        description=(
            f"🔴 **Верифицировано:** {verified_count}/{total_members}\n"
            f"🔴 **Процент:** {percentage}%\n"
            f"🔴 **Осталось:** {total_members - verified_count}"
        ),
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@verify.error
async def verify_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(
            "❌ **Доступ запрещён!** Только владелец может использовать эту команду.",
            delete_after=5
        )
        await ctx.message.delete()

# ===========================================
# ==========  ЗАПУСК ==========
# ===========================================
if __name__ == "__main__":
    print("🔴 Запуск бота KX Community...")
    bot.run(TOKEN)