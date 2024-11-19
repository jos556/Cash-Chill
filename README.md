# 💰 Cash & Chill 財務管理系統

<p align="center">
  <img src="https://raw.githubusercontent.com/jos556/Cash-Chill/refs/heads/main/screenshots/main_interface.png" alt="主介面預覽" width="800"/>
</p>

這是一個使用 Python 和 Tkinter 開發的財務管理系統，幫助用戶追蹤和管理個人財務。透過直觀的介面和強大的功能，讓您輕鬆掌握財務狀況！

## ✨ 功能特點

### 📊 即時收支統計

- 即時餘額計算與顯示
- 未來收支預測
- 月度收支統計
- 支出分類佔比分析

### 💹 智能預算警告系統

- 四級警告機制：
  - 🟢 一般提醒 ($1,000)
  - 🔵 警告提醒 ($3,000)
  - 🟡 嚴重警告 ($5,000)
  - 🔴 極度警告 ($10,000)
- 自動觸發視覺提醒
- 聲音警告提示

### 📅 定期交易功能

- 自動週期性交易設定
- 每月重複交易安排
- 智能日期檢查（避免無效日期）
- 重複交易提前提醒

### 📝 交易記錄管理

- 完整交易歷史記錄
- 多維度交易分類
- 自定義備註功能
- 靈活的日期選擇

### 🎨 視覺化分析

- 互動式圓餅圖
- 動態更新圖表
- 客製化圖例設計
- 精美視覺特效

<p align="center">
  <img src="https://raw.githubusercontent.com/jos556/Cash-Chill/refs/heads/main/screenshots/expense_analysis.png" alt="支出分析圖表" width="600"/>
</p>

## 🛠️ 技術實現

### 核心技術

- **Python 3.7+**: 主要開發語言
- **Tkinter**: GUI開發框架
- **Matplotlib**: 資料視覺化
- **tkcalendar**: 日期選擇器
- **FancyBboxPatch**: 自定義視覺元件

### 關鍵類別與方法

class FinanceManager:

#### 初始化與GUI創建

def init(self, root) # 初始化應用程式和設置基本參數

def create\_gui() # 創建圖形使用者介面

#### 交易相關方法

def add\_transaction() # 新增交易記錄

def show\_event\_dialog() # 顯示事件新增對話框

def add\_scheduled\_transaction() # 新增定期交易

#### 數據更新與分析

def update\_monthly\_stats() # 更新月度統計資料

def update\_chart() # 更新圖表顯示

def check\_expense\_warning() # 檢查支出警告

#### 定期任務處理

def check\_scheduled\_events() # 檢查定期事件

#### 警告系統

def show\_warning\_dialog() # 顯示警告對話框

### 📊 資料結構設計

#### 交易記錄��構

python

transaction = {

'date': 'YYYY-MM-DD', # 交易日期

'category': str, # 交易類別

'amount': float, # 交易金額

'type': '收入|支出', # 交易類型

'note': str # 交易備註

}

#### 定期事件結構

scheduled\_event = {

'name': str, # 事件名稱

'amount': float, # 事件金額

'category': str, # 事件類別

'type': str, # 事件類型

'date': datetime, # 事件日期

'is\_monthly': bool # 是否每月重複

}

## 🚀 安裝指南

1. 確保您已安裝 Python 3.7+
2. 安裝所需套件：

   tkinter>=8.6

   matplotlib>=3.5.0

   pandas>=1.3.0

   tkcalendar>=1.6.1

### 系統需求

- Windows 10/11 或 macOS 10.14+
- Python 3.7 或更高版本
- 2GB 以上可用記憶體
- 500MB 可用硬碟空間

## 👥 開發團隊

- **主要開發** - [@jos556](https://github.com/jos556)
- **UI/UX 設計** - [HU, SHIH-CHIEH]
- **測試團隊** - [LIN, LI–SHIN & CHEN, MENG-YUN & HSIEH, CHING HUAI &  CHEN,SHIH-TING]

<p align="center">Made with ❤️ in NTU</p>

## 🐳 Docker 部署

### 使用 Docker 運行

1. 確保已安裝 Docker 和 Docker Compose
2. 克隆專案後，在專案根目錄執行：

#### 構建映像

docker-compose build

#### 運行容器

docker-compose up

#### 停止容器

docker-compose down
