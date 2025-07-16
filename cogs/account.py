
import discord
from discord import app_commands, Interaction
from discord.ext import commands
from utils import db
import datetime


class CreditorSelect(discord.ui.Select):
    def __init__(self, members, amount, desc, callback):
        options = [discord.SelectOption(label=member.display_name, value=str(member.id)) for member in members]
        super().__init__(placeholder='選擇債權人', min_values=1, max_values=1, options=options)
        self.amount = amount
        self.desc = desc
        self.callback_func = callback

    async def callback(self, interaction: Interaction):
        creditor_id = self.values[0]
        await self.callback_func(interaction, creditor_id, self.amount, self.desc)

class DebtorSelect(discord.ui.Select):
    def __init__(self, members, creditor_id, amount, desc, callback):
        options = [discord.SelectOption(label=member.display_name, value=str(member.id)) for member in members if str(member.id) != creditor_id]
        super().__init__(placeholder='選擇債務人', min_values=1, max_values=1, options=options)
        self.creditor_id = creditor_id
        self.amount = amount
        self.desc = desc
        self.callback_func = callback

    async def callback(self, interaction: Interaction):
        debtor_id = self.values[0]
        await self.callback_func(interaction, self.creditor_id, debtor_id, self.amount, self.desc)

class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='add', description='新增記帳: /add 金額 內容')
    @app_commands.describe(amount='金額', desc='內容')
    async def add(self, interaction: Interaction, amount: float, desc: str):
        # 取得所有成員（僅限目前頻道可見成員）
        members = [m for m in interaction.guild.members if not m.bot]
        async def creditor_callback(inter, creditor_id, amount, desc):
            # 選擇債務人
            view = discord.ui.View()
            view.add_item(DebtorSelect(members, creditor_id, amount, desc, debtor_callback))
            await inter.response.edit_message(content='請選擇債務人：', view=view)

        async def debtor_callback(inter, creditor_id, debtor_id, amount, desc):
            # 寫入資料庫
            user_id = str(inter.user.id)
            data = await db.read_data()
            record = {
                'creditor': creditor_id,
                'amount': amount,
                'debtor': debtor_id,
                'desc': desc,
                'time': datetime.datetime.now().isoformat()
            }
            data.setdefault(user_id, []).append(record)
            await db.write_data(data)
            creditor = interaction.guild.get_member(int(creditor_id))
            debtor = interaction.guild.get_member(int(debtor_id))
            await inter.response.edit_message(content=f'✅ 已新增: {amount} 元 - {desc}\n債權人: {creditor.display_name}，債務人: {debtor.display_name}', view=None)

        view = discord.ui.View()
        view.add_item(CreditorSelect(members, amount, desc, creditor_callback))
        await interaction.response.send_message('請選擇債權人：', view=view, ephemeral=True)


    @app_commands.command(name='list_all', description='查詢你所有記帳條目')
    async def list_all(self, interaction: Interaction):
        user_id = str(interaction.user.id)
        data = await db.read_data()
        records = data.get(user_id, [])
        if not records:
            await interaction.response.send_message('你還沒有任何記帳紀錄。')
            return
        msg = '\n'.join([
            f"{i+1}. {r['amount']} 元 - {r['desc']} (債權人: <@{r['creditor']}>，債務人: <@{r['debtor']}>, {r['time'][:10]})" for i, r in enumerate(records)
        ])
        await interaction.response.send_message(f'你的所有記帳條目：\n{msg}')

    @app_commands.command(name='list', description='查詢指定成員的欠債與被欠債')
    @app_commands.describe(member='要查詢的成員')
    async def list(self, interaction: Interaction, member: discord.Member):
        user_id = str(interaction.user.id)
        data = await db.read_data()
        records = data.get(user_id, [])
        if not records:
            await interaction.response.send_message('你還沒有任何記帳紀錄。')
            return
        owe = []
        owed = []
        for r in records:
            if r['debtor'] == str(member.id):
                owe.append(r)
            if r['creditor'] == str(member.id):
                owed.append(r)
        msg = ''
        if owe:
            msg += f"{member.display_name} 欠別人：\n" + '\n'.join([
                f"{i+1}. {r['amount']} 元 - {r['desc']} (債權人: <@{r['creditor']}>, {r['time'][:10]})" for i, r in enumerate(owe)
            ]) + '\n'
        if owed:
            msg += f"{member.display_name} 被欠：\n" + '\n'.join([
                f"{i+1}. {r['amount']} 元 - {r['desc']} (債務人: <@{r['debtor']}>, {r['time'][:10]})" for i, r in enumerate(owed)
            ])
        if not msg:
            msg = f"{member.display_name} 沒有任何欠債紀錄。"
        await interaction.response.send_message(msg)

    @app_commands.command(name='list_sum', description='列出你所有記帳條目的金額加總')
    async def list_sum(self, interaction: Interaction):
        user_id = str(interaction.user.id)
        data = await db.read_data()
        records = data.get(user_id, [])
        if not records:
            await interaction.response.send_message('你還沒有任何記帳紀錄。')
            return
        total = sum(r['amount'] for r in records)
        await interaction.response.send_message(f'你的所有記帳金額加總為：{total} 元')

    @app_commands.command(name='del', description='刪除記帳: /del 編號 (用 /list 查編號)')
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

def calulate(record, user): # 將每個人的欠還款做計算
    summary =[m for m in user if not m.bot]
    summary = sum(summary)

async def setup(bot):
    await bot.add_cog(Account(bot))
