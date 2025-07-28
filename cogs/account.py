
import discord
from discord import app_commands, Interaction
from discord.ext import commands
from utils import db
import datetime


class CreditorSelect(discord.ui.Select):
    def __init__(self, members, amount, desc, callback):
        options = [discord.SelectOption(label=member.display_name, value=str(member.id)) for member in members]
        super().__init__(placeholder='選擇代墊人', min_values=1, max_values=1, options=options)
        self.amount = amount
        self.desc = desc
        self.callback_func = callback

    async def callback(self, interaction: Interaction):
        creditor_id = self.values[0]
        await self.callback_func(interaction, creditor_id, self.amount, self.desc)

class DebtorSelect(discord.ui.Select):
    def __init__(self, members, creditor_id, amount, desc, callback):
        options = [discord.SelectOption(label=member.display_name, value=str(member.id)) for member in members if str(member.id) != creditor_id]
        super().__init__(placeholder='選擇還款人', min_values=1, max_values=1, options=options)
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
            await inter.response.edit_message(content='請選擇還款人：', view=view)

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
            await inter.response.edit_message(content=f'✅ 已新增: {amount} 元 - {desc}\n代墊人: <@{creditor_id}>，還款人: <@{debtor_id}>', view=None)

        view = discord.ui.View()
        view.add_item(CreditorSelect(members, amount, desc, creditor_callback))
        await interaction.response.send_message('請選擇代墊人：', view=view)


    @app_commands.command(name='list_all', description='查詢你所有記帳條目')
    async def list_all(self, interaction: Interaction):
        user_id = str(interaction.user.id)
        data = await db.read_data()
        records = data.get(user_id, [])
        if not records:
            await interaction.response.send_message('你還沒有任何記帳紀錄。')
            return
        msg = '\n'.join([
            f"{i+1}. {r['amount']} 元 - {r['desc']} (代墊人: <@{r['creditor']}>，還款人: <@{r['debtor']}>, {r['time'][:10]})" for i, r in enumerate(records)
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
                f"{i+1}. {r['amount']} 元 - {r['desc']} (代墊人: <@{r['creditor']}>, {r['time'][:10]})" for i, r in enumerate(owe)
            ]) + '\n'
        if owed:
            msg += f"{member.display_name} 被欠：\n" + '\n'.join([
                f"{i+1}. {r['amount']} 元 - {r['desc']} (欠款人: <@{r['debtor']}>, {r['time'][:10]})" for i, r in enumerate(owed)
            ])
        if not msg:
            msg = f"{member.display_name} 沒有任何欠債紀錄。"
        await interaction.response.send_message(msg)

    @app_commands.command(name='list_sum', description='列出你與每個人的金額淨結算')
    async def list_sum(self, interaction: Interaction):
        user_id = str(interaction.user.id)
        data = await db.read_data()
        records = data.get(user_id, [])
        if not records:
            await interaction.response.send_message('你還沒有任何記帳紀錄。')
            return
        # 收集所有出現過的成員id
        member_ids = set()
        for r in records:
            member_ids.add(r['creditor'])
            member_ids.add(r['debtor'])
        member_ids.discard(user_id)  # 不要自己

        # 計算與每個人的淨結算
        result = {}
        for other_id in member_ids:
            # 我是債權人，對方是債務人：對方欠我錢
            plus = sum(r['amount'] for r in records if r['creditor'] == user_id and r['debtor'] == other_id)
            # 我是債務人，對方是債權人：我欠對方錢
            minus = sum(r['amount'] for r in records if r['debtor'] == user_id and r['creditor'] == other_id)
            net = plus - minus
            if net != 0:
                result[other_id] = net

        if not result:
            await interaction.response.send_message('你與其他人沒有任何金錢往來。')
            return

        msg = '你與每個人的金額淨結算如下：\n'
        for other_id, net in result.items():
            member = interaction.guild.get_member(int(other_id))
            name = member.display_name if member else f'<@{other_id}>'
            if net > 0:
                msg += f'{name} 欠你 {net} 元\n'
            else:
                msg += f'你欠 {name} {abs(net)} 元\n'
        await interaction.response.send_message(msg)

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
