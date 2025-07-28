# 記帳 discord bot

模板 fork 自 [Dong-Chen-1031](https://github.com/Dong-Chen-1031)<br>

Account bot 可以很好的解決朋友之間代墊金額記不清的情況，並做到隨時清算帳目。詳情可參考下方使用說明

## ✨ 特色功能

- 🔧 **模組化設計** - 使用 Cogs 系統，功能模組獨立且易於維護
- 🔄 **熱重載** - 開發時無需重啟機器人即可重載模組
- 🛡️ **權限控制** - 開發者指令具有權限保護機制
- 📝 **完整日誌** - 使用 Rich 庫美化輸出，支援檔案和控制台雙重記錄
- ⚡ **斜線指令** - 支援現代化的 Discord 斜線指令
- 🎨 **美化界面** - 統一的 Embed 樣式和互動式按鈕

## 📁 專案結構

```
Discord-py-cogs/
├── bot.py              # 機器人主程式入口
├── settings.py         # 配置文件管理
├── requirements.txt    # 依賴套件清單
├── README.md          # 專案說明文件
├── .env               # 環境變數配置
├── data.json          # 記帳資料庫
├── cogs/              # 功能模組目錄
|   ├── account.py     # 記帳指令核心引擎
│   ├── dev_cog.py     # 開發者工具模組
│   └── example_cog.py # 範例模組
├── utils/             # 工具函數目錄
|   ├── db.py          # 讀寫 data.json
│   ├── log.py         # 日誌系統
│   ├── ui.py          # UI 工具函數
│   └── types.py       # 型別定義
└── logs/              # 日誌檔案目錄
    └── 2025-06-22.log # 每日日誌檔案
```

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 環境設定

在專案根目錄創建 `.env` 檔案：

```env
DISCORD_BOT_TOKEN=你的機器人Token
```

### 3. 配置開發者ID

編輯 `settings.py` 中的開發者ID：

```python
DEV_ID = [
    123456789012345678,  # 替換為你的 Discord 用戶 ID
    987654321098765432   # 可以添加多個開發者 ID
]
```

### 4. 運行機器人

```bash
python bot.py
```
在 terminal 中顯示「已同步 X 個斜線指令」表示成功運行

## 🗣 使用說明
所有指令<br>
<img width="732" height="793" alt="image" src="https://github.com/user-attachments/assets/c7a9de4e-a86a-4fd1-b64e-397ce442eb64" /><br>
add 指令記錄了誰幫誰代墊了多少，以及該筆帳的使用地方。<br>
del 指令將刪除還清的項目。<br>
list 指令顯示指定使用者未清算(**註1**)過的帳目<br>
list_all 指令顯示所有未清算過的帳目<br>
list_sum 將所有帳目清算<br>

<br>
註1：清算方式如下。若 A 幫 B 代墊了 1 塊錢，在此之後 B 幫 A 代墊了 2 塊錢。清算時會將 2 - 1 得出 A 需還 B 1 塊錢。

### 1. add 指令
<img width="665" height="200" alt="image" src="https://github.com/user-attachments/assets/7f91ea4d-9b86-46a9-a93b-2c05d3602b7d" />
<img width="1234" height="307" alt="image" src="https://github.com/user-attachments/assets/76652496-858d-4457-bdfe-778f1b4800d4" />
<img width="1231" height="336" alt="image" src="https://github.com/user-attachments/assets/cfe9dca7-ff90-4890-a0d2-690d03af0164" />

### 2. del 指令
<img width="443" height="210" alt="image" src="https://github.com/user-attachments/assets/5efd6938-2fd6-4916-a928-aaeed0f863f1" />
<img width="701" height="215" alt="image" src="https://github.com/user-attachments/assets/bd0360ff-ac78-4e37-a779-597453fa434a" />

### 3. list 指令
<img width="886" height="858" alt="image" src="https://github.com/user-attachments/assets/de2b56d6-8d0f-4be3-b7e1-2b0d3ef87a2d" />
<img width="1062" height="312" alt="image" src="https://github.com/user-attachments/assets/76e1895c-03a8-40b7-80da-c9380501b085" /><br>
(圖片中的代墊人已在程式碼中修正成還款人)

### 4. list_all 指令
<img width="1394" height="304" alt="image" src="https://github.com/user-attachments/assets/f3366a72-d2d0-4132-8ddd-8b9e0bb96445" />

### 5. list_sum 指令
<img width="784" height="278" alt="image" src="https://github.com/user-attachments/assets/55822703-312e-40c0-a153-277fc67834cc" />


## 🔧 開發者工具

### 指令前綴
- 開發者指令前綴：`.dev `

### 🎮 可用指令

#### 📦 模組管理指令

##### `.dev load <模組名稱/all>`
載入指定的模組或所有模組
```
.dev load example_cog    # 載入 example_cog 模組
.dev load all           # 載入所有模組
```

##### `.dev unload <模組名稱/all>`
卸載指定的模組或所有模組
```
.dev unload example_cog  # 卸載 example_cog 模組
.dev unload all         # 卸載所有模組
```

##### `.dev reload [模組名稱/all]`
重新載入指定的模組或所有模組
```
.dev reload example_cog  # 重新載入 example_cog 模組
.dev reload all          # 重新載入所有模組
.dev reload              # 顯示互動式按鈕選擇模組
```

#### 🔄 系統管理指令

##### `.dev restart`
重啟機器人
```
.dev restart            # 完全重啟機器人程序
```

##### `.dev test`
可在程式碼中放置簡單的邏輯，測試機器人是否正常運作
```
.dev test               # 回應「測試成功！」確認機器人狀態
```

##### `.dev del_all`
刪除 data.json 中的所有資料
```
.dev del_all            # 如果成功，將在 discord 中顯示「已將所有資料清除」
                        # 如果資料為空，將在 discord 中顯示「目前沒有資料」
```

### 🎯 互動式模組管理
當使用 `.dev reload` 不帶參數時，機器人會顯示互動式按鈕界面：

![互動式模組管理界面](https://github.com/Dong-Chen-1031/Discord.py-Cogs-Bot-Template/blob/main/screenshots/reload.png?raw=true)

- **All 按鈕** - 重載所有模組
- **個別模組按鈕** - 重載特定模組
- **即時反饋** - 顯示載入結果和錯誤訊息
- **自動更新** - 按鈕點擊後自動刷新界面

### 🔒 權限保護
- 所有開發者指令都有權限檢查
- 只有在 `settings.py` 中定義的 `DEV_ID` 可以使用
- 非授權用戶嘗試使用會被拒絕

### ⚡ 自動重載功能
如果在 `settings.py` 中設定 `AUTO_RELOAD = True`：
- 自動監控 `cogs/` 目錄下的檔案變更
- 檔案儲存時自動重載對應模組
- 適合開發時使用，生產環境建議關閉

## 📝 創建新模組

### 基本模組範本

在 `cogs/` 目錄下創建新的 `.py` 檔案：

```python
import logging
from discord.ext import commands
from discord import app_commands, Interaction
from utils.log import log

class YourCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="example", description="範例指令")
    async def example_command(self, interaction: Interaction):
        await interaction.response.send_message("Hello World!")

async def setup(bot: commands.Bot):
    await bot.add_cog(YourCog(bot))
    logging.info(f'{__name__} 已載入')
```

### 模組自動載入

所有在 `cogs/` 目錄下的 `.py` 檔案會在機器人啟動時自動載入。

## 🛠️ 核心組件

### Bot 主程式 (`bot.py`)
- 機器人初始化
- 自動載入所有模組
- 斜線指令同步
- 異步啟動流程

### 設定管理 (`settings.py`)
- 環境變數載入
- 開發者權限配置
- 機器人基本設定

### 日誌系統 (`utils/log.py`)
- Rich 美化輸出
- 檔案和控制台雙重記錄
- 自動按日期分類日誌
- 快速日誌函數

### UI 工具 (`utils/ui.py`)
- 統一的 Embed 樣式
- 開發者專用樣式
- 可自訂顏色和內容

## 📚 使用範例

### 基本指令回應
```python
@app_commands.command(name="ping", description="檢查機器人延遲")
async def ping(self, interaction: Interaction):
    latency = round(self.bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! 延遲: {latency}ms")
```

### 使用日誌系統
```python
from utils.log import log

# 記錄用戶互動
log(interaction, command_used="ping")

# 記錄一般資訊
log("機器人已啟動")
```

### 使用 UI 工具
```python
from utils.ui import info_embed, dev_embed

# 建立資訊嵌入
embed = info_embed("操作成功完成！")
await interaction.response.send_message(embed=embed)
```

## 🔒 權限系統

機器人內建開發者權限系統：

- 在 `settings.py` 中設定開發者 Discord ID
- 開發者可以使用模組重載等管理功能
- 非開發者無法執行敏感操作

## 📋 依賴套件

- `discord.py` - Discord API 包裝器
- `python-dotenv` - 環境變數管理
- `rich` - 美化控制台輸出
- `watchdog` - 檔案監控 (用於自動重載)

## 📄 授權條款

此專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 🆘 常見問題

### Q: 機器人無法啟動？
A: 請檢查：
- `.env` 檔案是否正確設定
- Discord Bot Token 是否有效

### Q: 模組重載失敗？
A: 請檢查：
- 模組語法是否正確
- 是否有權限執行開發者指令
- 查看日誌檔案了解詳細錯誤

### Q: 斜線指令不出現？
A: 請確認：
- 機器人有足夠的權限
- 指令已正確同步
- 等待 Discord 更新 (可能需要幾分鐘)

## 📞 聯絡資訊

如有問題或建議，歡迎開啟 Issue 或聯絡專案維護者。

---
