import os
import discord
from discord.ext import commands
from database import conn, cursor

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")

LOG_MUON_DO_ID = int(os.getenv("LOG_MUON_DO_ID"))
LOG_DONATE_ID = int(os.getenv("LOG_DONATE_ID"))
LOG_XE_GIAP_ID = int(os.getenv("LOG_XE_GIAP_ID"))

def get_target(message):
    return message.mentions[0].mention if message.mentions else "Không tag"

def time_str(message):
    return message.created_at.strftime("%d/%m/%Y %H:%M:%S")

# ===== EMBEDS =====
def embed_log(title, color, message, target, content, log_id):
    embed = discord.Embed(
        title=title,
        color=color,
        timestamp=message.created_at
    )
    embed.add_field(name="🆔 Mã log", value=f"`{log_id}`", inline=False)
    embed.add_field(name="👤 Người ghi", value=message.author.mention, inline=True)
    embed.add_field(name="🧑‍🤝‍🧑 Người liên quan", value=target, inline=True)
    embed.add_field(name="📄 Nội dung", value=content, inline=False)
    embed.set_footer(text="CIARA • Crew Log System")
    return embed

@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    target = get_target(message)
    content = message.content
    t = time_str(message)

    if message.channel.id == LOG_MUON_DO_ID:
        cursor.execute(
            "INSERT INTO log_muon_do (author, target, item, time) VALUES (?, ?, ?, ?)",
            (str(message.author), target, content, t)
        )
        conn.commit()
        log_id = cursor.lastrowid
        await message.channel.send(
            embed=embed_log("📦 LOG MƯỢN ĐỒ", 0x3498DB, message, target, content, f"MUON-{log_id}")
        )

    elif message.channel.id == LOG_DONATE_ID:
        cursor.execute(
            "INSERT INTO log_donate (author, target, amount, time) VALUES (?, ?, ?, ?)",
            (str(message.author), target, content, t)
        )
        conn.commit()
        log_id = cursor.lastrowid
        await message.channel.send(
            embed=embed_log("💰 LOG DONATE", 0x2ECC71, message, target, content, f"DONATE-{log_id}")
        )

    elif message.channel.id == LOG_XE_GIAP_ID:
        cursor.execute(
            "INSERT INTO log_xe_giap (author, target, vehicle, time) VALUES (?, ?, ?, ?)",
            (str(message.author), target, content, t)
        )
        conn.commit()
        log_id = cursor.lastrowid
        await message.channel.send(
            embed=embed_log("🚗 LOG XE / GIÁP", 0xE67E22, message, target, content, f"XE-{log_id}")
        )

    await bot.process_commands(message)

# ===== LỆNH XÓA LOG =====
@bot.command()
@commands.has_permissions(administrator=True)
async def xoalog(ctx, loai: str, log_id: int):
    tables = {
        "muon": "log_muon_do",
        "donate": "log_donate",
        "xe": "log_xe_giap"
    }

    if loai not in tables:
        await ctx.send("❌ Sai loại log (muon / donate / xe)")
        return

    cursor.execute(
        f"DELETE FROM {tables[loai]} WHERE id = ?",
        (log_id,)
    )
    conn.commit()

    if cursor.rowcount == 0:
        await ctx.send("⚠️ Không tìm thấy ID log")
    else:
        await ctx.send(f"✅ Đã xóa log `{loai.upper()}-{log_id}`")

bot.run(TOKEN)
