from discord import app_commands, Interaction
from discord.ext import commands
from utils import db
import datetime

class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='add', description='新增記帳: !add 金額 內容')
    async def add(self, interaction: Interaction, amount: float, *, desc: str):
        user_id = str(interaction.user.id)
        data = await db.read_data()
        record = {
            'amount': amount,
            'desc': desc,
            'time': datetime.datetime.now().isoformat()
        }
        data.setdefault(user_id, []).append(record)
        await db.write_data(data)
        await interaction.response.send_message(f'✅ 已新增: {amount} 元 - {desc}')

    @app_commands.command(name='list', description='查詢記帳: !list')
    async def list(self, interaction: Interaction):
        user_id = str(interaction.user.id)
        data = await db.read_data()
        records = data.get(user_id, [])
        if not records:
            await interaction.response.send_message('你還沒有任何記帳紀錄。')
            return
        msg = '\n'.join([
            f"{i+1}. {r['amount']} 元 - {r['desc']} ({r['time'][:10]})" for i, r in enumerate(records)
        ])
        await interaction.response.send_message(f'你的記帳紀錄：\n{msg}')

    @app_commands.command(name='del', description='刪除記帳: !del 編號 (用 !list 查編號)')
    async def delete(self, interaction: Interaction, idx: int):
        user_id = str(interaction.user.id)
        data = await db.read_data()
        records = data.get(user_id, [])
        if 1 <= idx <= len(records):
            removed = records.pop(idx-1)
            await db.write_data(data)
            await interaction.response.send_message(f"已刪除: {removed['amount']} 元 - {removed['desc']}")
        else:
            await interaction.response.send_message('無效的編號。')

async def setup(bot):
    await bot.add_cog(Account(bot))
