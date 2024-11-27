# 引入需要之套件 tkinter , matplotlib , pandas , datetime , tkcalendar
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, date, timedelta
from matplotlib.patches import FancyBboxPatch
from tkcalendar import DateEntry  # 需安裝 pip install tkcalendar (cammand)

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]  # 字體為微軟正黑體
plt.rcParams["axes.unicode_minus"] = False  # 解決負號顯示問題


# 在 FinanceManager 類別前添加薪資輸入視窗類別
class SalaryInputDialog:
    def __init__(self):
        self.salary = None
        self.dialog = tk.Tk()
        self.dialog.title("薪資設定")
        self.dialog.geometry("400x300")
        
        # 設置視窗樣式
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Microsoft JhengHei", 14, "bold"))
        style.configure("Custom.TLabel", font=("Microsoft JhengHei", 12))
        style.configure("Custom.TButton", font=("Microsoft JhengHei", 12))
        
        # 創建主框架
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # 標題
        ttk.Label(
            main_frame,
            text="請輸入每月固定薪資",
            style="Title.TLabel"
        ).pack(pady=(0, 20))
        
        # 薪資輸入框
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill="x", pady=10)
        
        ttk.Label(
            input_frame,
            text="薪資金額：",
            style="Custom.TLabel"
        ).pack(side="left")
        
        self.salary_entry = ttk.Entry(
            input_frame,
            font=("Microsoft JhengHei", 12),
            width=15
        )
        self.salary_entry.pack(side="left", padx=5)
        
        # 薪資入帳日期選擇
        date_frame = ttk.Frame(main_frame)
        date_frame.pack(fill="x", pady=20)
        
        ttk.Label(
            date_frame,
            text="入帳日期：",
            style="Custom.TLabel"
        ).pack(side="left")
        
        self.date_entry = DateEntry(
            date_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            font=("Microsoft JhengHei", 12)
        )
        self.date_entry.pack(side="left", padx=5)
        
        # 確認按鈕
        ttk.Button(
            main_frame,
            text="確認",
            command=self.confirm,
            style="Custom.TButton"
        ).pack(pady=20)
        
        # 說明文字
        ttk.Label(
            main_frame,
            text="此設定將自動記錄每月固定薪資收入",
            font=("Microsoft JhengHei", 10),
            foreground="gray"
        ).pack(pady=(10, 0))
        
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.dialog.mainloop()
    
    def confirm(self):
        try:
            salary = float(self.salary_entry.get())
            if salary <= 0:
                messagebox.showerror("錯誤", "請輸入大於0的金額")
                return
            
            self.salary = salary
            self.salary_date = self.date_entry.get_date().day
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的金額")
    
    def on_closing(self):
        if messagebox.askokcancel("關閉", "確定要關閉嗎？\n若未設定薪資將無法啟動系統"):
            self.dialog.destroy()
            sys.exit()

# 主要財務管理class
class FinanceManager:
    # 初始化應用程式和設置基本參數
    def __init__(self, root, monthly_salary, salary_date):
        self.root = root
        self.root.title("Cash & Chill - 財務管理系統")
        self.monthly_salary = monthly_salary
        self.salary_date = salary_date

        # 獲取螢幕尺寸和設置視窗
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 1400
        window_height = int(screen_height * 0.9)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 初始化數據
        self.balance = 0
        self.transactions = []
        self.categories = ["飲食", "交通", "購物", "娛樂", "醫療", "其他"]

        # 定義列和對應的中文名稱
        self.columns = ("date", "category", "amount", "type", "note")
        self.column_names = {
            "date": "日期",
            "category": "類別",
            "amount": "金額",
            "type": "類型",
            "note": "備註",
        }

        # 添加預算警告閾值
        self.warning_thresholds = {
            "normal": 1000,  # 一般提醒
            "warning": 3000,  # 警告提醒
            "danger": 5000,  # 嚴重警告
            "extreme": 10000,  # 極度警告
        }

        self.create_gui()
        self.update_monthly_stats()  # 初始化時更新月度統計

        # 定期檢查排程事件
        self.check_scheduled_events()
        root.after(3600000, self.check_scheduled_events)  # 每小時檢查一次

        # 在初始化完成後，自動添加每月薪資
        self.add_monthly_salary()

    # 創建圖形使用者介面
    def create_gui(self):
        # 設置整體風格
        style = ttk.Style()
        style.configure("Main.TFrame", background="#f0f0f0")
        style.configure("Custom.TLabel", font=("Microsoft JhengHei", 13))
        style.configure("Title.TLabel", font=("Microsoft JhengHei", 14, "bold"))
        style.configure("Balance.TLabel", font=("Microsoft JhengHei", 16, "bold"))
        style.configure("Custom.TButton", font=("Microsoft JhengHei", 13))

        style.configure('BigButton.TButton', font=('Microsoft JhengHei', 16, 'bold'))
        style.configure("Custom.TRadiobutton", font=("Microsoft JhengHei", 14))
        # 修改這裡：為 LabelFrame 添加正確的樣式
        style.configure("BigTitle.TLabelframe.Label", font=("Microsoft JhengHei", 16, "bold"))  # 修改標籤字體
        style.configure("BigTitle.TLabelframe", borderwidth=2)  # 設置邊框

        # 主框架
        main_frame = ttk.Frame(self.root, style="Main.TFrame", padding="20")
        main_frame.pack(fill="both", expand=True)

        # 創建左右兩個框架
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        # === 左側內容 ===
        # 新增事件按鈕
        event_button = ttk.Button(
            left_frame,
            text="➕ 新增事件",
            command=self.show_event_dialog,
            style="BigButton.TButton",
        )
        event_button.pack(fill="x", pady=(0, 15))

        # 帳戶資訊區域
        balance_frame = ttk.LabelFrame(
            left_frame,
            text="帳戶資訊",
            padding="15",
            relief="groove",
            style="BigTitle.TLabelframe"  # 使用正確的樣式名稱
        )
        balance_frame.pack(fill="x", pady=(0, 15))

        # 當前餘額 - 使用大字體和醒目顏色
        ttk.Label(balance_frame, text="當前餘額", style="Title.TLabel").pack(anchor="w")

        self.balance_label = ttk.Label(
            balance_frame, text=f"${self.balance:,.2f}", style="Balance.TLabel"
        )
        self.balance_label.pack(anchor="w", pady=(5, 15))

        # 未來收支資訊 - 使用網格布局
        info_frame = ttk.Frame(balance_frame)
        info_frame.pack(fill="x")

        self.current_month_income_label = ttk.Label(
            info_frame, text="未來收入：$0.00", style="Custom.TLabel"
        )
        self.current_month_income_label.pack(side="left", padx=(0, 20))

        self.current_month_expense_label = ttk.Label(
            info_frame, text="未來支出：$0.00", style="Custom.TLabel"
        )
        self.current_month_expense_label.pack(side="left")

        # 新增交易區域
        transaction_frame = ttk.LabelFrame(
            left_frame,
            text="新增交易",
            padding="16",
            relief="groove",
            style="BigTitle.TLabelframe"  # 使用正確的樣式名稱
        )
        transaction_frame.pack(fill="x", pady=(0, 15))

        # 使用網格布局來排列輸入欄位
        grid_frame = ttk.Frame(transaction_frame)
        grid_frame.pack(fill="x", padx=5)

        # 金額輸入
        ttk.Label(grid_frame, text="金額：", style="Custom.TLabel").grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )

        self.amount_entry = ttk.Entry(
            grid_frame, font=("Microsoft JhengHei", 11), width=15
        )
        self.amount_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # 類別選擇
        ttk.Label(grid_frame, text="類別：", style="Custom.TLabel").grid(
            row=0, column=2, sticky="e", padx=5, pady=5
        )

        self.category_combobox = ttk.Combobox(
            grid_frame,
            values=self.categories,
            font=("Microsoft JhengHei", 11),
            width=15,
        )
        self.category_combobox.set(self.categories[0])
        self.category_combobox.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        # 日期選擇
        ttk.Label(grid_frame, text="日期：", style="Custom.TLabel").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )

        self.date_entry = DateEntry(
            grid_frame,
            width=15,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            font=("Microsoft JhengHei", 11),
        )
        self.date_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # 備註輸入
        ttk.Label(grid_frame, text="備註：", style="Custom.TLabel").grid(
            row=1, column=2, sticky="e", padx=5, pady=5
        )

        self.note_entry = ttk.Entry(
            grid_frame, font=("Microsoft JhengHei", 11), width=15
        )
        self.note_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        # 交易類型選擇
        type_frame = ttk.Frame(transaction_frame)
        type_frame.pack(fill="x", pady=10)

        self.transaction_type = tk.StringVar(value="expense")
        ttk.Radiobutton(
            type_frame,
            text="支出",
            variable=self.transaction_type,
            value="expense",
            style="Custom.TRadiobutton",
        ).pack(side="left", padx=20)

        ttk.Radiobutton(
            type_frame,
            text="收入",
            variable=self.transaction_type,
            value="income",
            style="Custom.TRadiobutton",
        ).pack(side="left", padx=20)

        # 提交按鈕
        ttk.Button(
            transaction_frame,
            text="新增交易",
            command=self.add_transaction,
            style="Custom.TButton",
        ).pack(pady=10)

        # 圖表區域
        chart_frame = ttk.LabelFrame(
            left_frame,
            text="支出分析",
            padding="15",
            relief="groove",
            style="BigTitle.TLabelframe"  # 使用正確的樣式名稱
        )
        chart_frame.pack(fill="x", pady=(0, 15))

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(pady=5)

        # === 右側內容 ===
        # 交易歷史列表
        history_frame = ttk.LabelFrame(
            right_frame,
            text="交易歷史",
            padding="15",
            relief="groove",
            style="BigTitle.TLabelframe"  # 使用正確的樣式名稱
        )
        history_frame.pack(fill="both", expand=True)

        # 創建表格容器
        tree_frame = ttk.Frame(history_frame)
        tree_frame.pack(fill="both", expand=True, pady=5)

        # 創建滾動條
        tree_scroll_y = ttk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side="right", fill="y")

        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        # 創建交易列表
        self.transaction_tree = ttk.Treeview(
            tree_frame,
            columns=("delete_btn",) + self.columns,  # 添加刪除按鈕列
            show="headings",
            height=26,
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
        )

        # 設置刪除按鈕列
        self.transaction_tree.heading("delete_btn", text="", anchor="center")
        self.transaction_tree.column(
            "delete_btn", 
            width=35,  
            minwidth=35, 
            anchor="center"
        )

        # 設置其他列標題和寬度
        for col in self.columns:
            self.transaction_tree.heading(
                col, 
                text=self.column_names[col], 
                anchor="center"
            )
            if col == "date":
                self.transaction_tree.column(
                    col, 
                    width=130,  
                    minwidth=130, 
                    anchor="center"
                )
            elif col == "type":
                self.transaction_tree.column(
                    col, 
                    width=100,  
                    minwidth=100, 
                    anchor="center"
                )
            elif col == "amount":
                self.transaction_tree.column(
                    col, 
                    width=130,  
                    minwidth=130, 
                    anchor="center"
                )
            elif col == "category":
                self.transaction_tree.column(
                    col, 
                    width=130,  
                    minwidth=130, 
                    anchor="center"
                )
            else:  # note
                self.transaction_tree.column(
                    col, 
                    width=180, 
                    minwidth=180, 
                    anchor="w"
                )

        # 綁定點擊事件
        self.transaction_tree.bind("<Button-1>", self.on_tree_click)

        # 添加刪除按鈕的樣式
        style.configure(
            "Delete.TLabel",
            font=("Microsoft JhengHei", 12, "bold"),
            foreground="red"
        )

        # 放置表格
        self.transaction_tree.pack(side="left", fill="both", expand=True)

    # 顯示事件新增對話框
    def show_event_dialog(self):
        # 創建新視窗並設置更大的尺寸
        dialog = tk.Toplevel(self.root)
        dialog.title("新增事件")
        dialog.geometry("800x800")  # 加大視窗尺寸

        # 設置視窗為模態
        dialog.transient(self.root)
        dialog.grab_set()

        # 創建主框架並添加padding
        main_frame = ttk.Frame(dialog, padding="30")  # 增加整體邊距
        main_frame.pack(fill="both", expand=True)

        # 創建樣式
        style = ttk.Style()
        style.configure("EventDialog.TLabel", font=("Microsoft JhengHei", 16))  # 加大標籤字體
        style.configure("EventDialog.TRadiobutton", font=("Microsoft JhengHei", 16))  # 加大選項按鈕字體
        style.configure("EventDialog.TButton", font=("Microsoft JhengHei", 16))  # 加大按鈕字體

        # 創建表單
        ttk.Label(main_frame, text="事件名稱：", style="EventDialog.TLabel").pack(pady=15)
        name_entry = ttk.Entry(
            main_frame, 
            font=("Microsoft JhengHei", 16),  # 加大輸入框字體
            width=35  # 加寬輸入框
        )
        name_entry.pack(pady=10)

        ttk.Label(main_frame, text="金額：", style="EventDialog.TLabel").pack(pady=15)
        amount_entry = ttk.Entry(
            main_frame, 
            font=("Microsoft JhengHei", 16), 
            width=35
        )
        amount_entry.pack(pady=10)

        ttk.Label(main_frame, text="類別：", style="EventDialog.TLabel").pack(pady=15)
        category_combobox = ttk.Combobox(
            main_frame,
            values=self.categories,
            font=("Microsoft JhengHei", 16),
            width=34
        )
        category_combobox.set(self.categories[0])
        category_combobox.pack(pady=10)

        # 交易類型選擇框架
        type_frame = ttk.Frame(main_frame)
        type_frame.pack(pady=20)

        ttk.Label(
            type_frame, 
            text="交易類型：", 
            style="EventDialog.TLabel"
        ).pack(side="left", padx=15)
        
        transaction_type = tk.StringVar(value="expense")

        def update_date_label(*args):
            date_label_text = "收入日期：" if transaction_type.get() == "income" else "支出日期："
            date_label.config(text=date_label_text)

        ttk.Radiobutton(
            type_frame,
            text="支出",
            variable=transaction_type,
            value="expense",
            style="EventDialog.TRadiobutton",
            command=update_date_label
        ).pack(side="left", padx=25)

        ttk.Radiobutton(
            type_frame,
            text="收入",
            variable=transaction_type,
            value="income",
            style="EventDialog.TRadiobutton",
            command=update_date_label
        ).pack(side="left", padx=25)

        # 日期選擇框架
        date_frame = ttk.Frame(main_frame)
        date_frame.pack(pady=20)

        date_label = ttk.Label(
            date_frame, 
            text="支出日期：", 
            style="EventDialog.TLabel"
        )
        date_label.pack(side="left", padx=15)

        current_date = datetime.now()
        date_entry = DateEntry(
            date_frame,
            width=20,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            font=("Microsoft JhengHei", 16),
            year=current_date.year,
            month=current_date.month,
            day=current_date.day
        )
        date_entry.pack(side="left", padx=15)

        # 每月重複選項
        repeat_frame = ttk.Frame(main_frame)
        repeat_frame.pack(pady=20)

        is_monthly = tk.BooleanVar(value=False)
        tk.Checkbutton(
            repeat_frame,
            text="每月重複",
            variable=is_monthly,
            font=("Microsoft JhengHei", 16)
        ).pack(pady=15)

        # 保存按鈕
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=25)

        save_button = ttk.Button(
            button_frame, 
            text="保存", 
            command=lambda: save_event(),
            style="EventDialog.TButton"
        )
        save_button.pack(pady=15)

        def save_event():
            try:
                name = name_entry.get()
                amount = float(amount_entry.get())
                category = category_combobox.get()
                selected_date = date_entry.get_date()

                if not name:
                    messagebox.showerror("錯誤", "請輸入事件名稱")
                    return

                # 如果是支出，檢查是否需要顯示警告
                if transaction_type.get() == "expense":
                    self.check_expense_warning(amount)

                # 創建事件
                event = {
                    "name": name,
                    "amount": amount,
                    "category": category,
                    "type": "支出" if transaction_type.get() == "expense" else "收入",
                    "date": selected_date,
                    "is_monthly": is_monthly.get(),
                }

                if not hasattr(self, "scheduled_events"):
                    self.scheduled_events = []

                self.scheduled_events.append(event)

                # 添加交易記錄
                current_date = datetime.now().date()
                transaction_date = selected_date

                # 創建交易記錄
                transaction = {
                    "date": transaction_date.strftime("%Y-%m-%d"),
                    "category": category,
                    "amount": amount,
                    "type": event["type"],
                    "note": name,
                }

                self.transactions.append(transaction)

                # 更新交易列表顯示
                self.transaction_tree.insert(
                    "",
                    "end",
                    values=(
                        "×",  # 使用更小的符號
                        transaction["date"],
                        transaction["category"],
                        f"${transaction['amount']:.2f}",
                        transaction["type"],
                        transaction["note"],
                    ),
                )

                # 更新統計和圖表
                self.update_monthly_stats()
                self.update_chart()

                dialog.destroy()
                messagebox.showinfo("成功", "事件新增")

            except ValueError:
                messagebox.showerror("錯誤", "請輸入有效的金額")

        # 設置初始焦點
        name_entry.focus()

    def add_scheduled_transaction(self, event, date):
        transaction = {
            "date": date.strftime("%Y-%m-%d"),
            "category": event["category"],
            "amount": event["amount"],
            "type": event["type"],
            "note": event["name"],
        }

        self.transactions.append(transaction)

        # 更新交易列表顯示
        self.transaction_tree.insert(
            "",
            "end",
            values=(
                "×",  # 使用更小的符號
                transaction["date"],
                transaction["category"],
                f"${transaction['amount']:.2f}",
                transaction["type"],
                transaction["note"],
            ),
        )

        # 更新統計和圖表
        self.update_monthly_stats()
        self.update_chart()

    # 檢查定期事件
    def check_scheduled_events(self):
        if not hasattr(self, "scheduled_events"):
            return

        current_date = datetime.now()
        next_month = current_date.replace(day=1) + timedelta(days=32)
        next_month = next_month.replace(day=1)

        for event in self.scheduled_events:
            if event["is_monthly"]:
                # 檢查是否需要添加下個月的交易
                try:
                    next_transaction_date = next_month.replace(day=event["day"])
                    # 檢查是否已經存在該交易
                    exists = any(
                        t["date"] == next_transaction_date.strftime("%Y-%m-%d")
                        and t["note"] == event["name"]
                        for t in self.transactions
                    )
                    if not exists:
                        self.add_scheduled_transaction(event, next_transaction_date)
                except ValueError:
                    # 處理無效日期（如2月30日）
                    continue

    # 顯示警告對話框
    def update_monthly_stats(self):
        # 獲取當前日期和時間
        current_datetime = datetime.now()

        # 計算當前餘額和未來收支
        current_balance = 0
        incoming_income = 0
        incoming_expense = 0

        for transaction in self.transactions:
            # 將交易日期字符串轉換為 datetime 對象
            trans_date = datetime.strptime(transaction["date"], "%Y-%m-%d")

            if trans_date.date() <= current_datetime.date():
                # 計算當前餘額（今天及之前的交易）
                if transaction["type"] == "收入":
                    current_balance += transaction["amount"]
                else:
                    current_balance -= transaction["amount"]
            else:
                # 計算未來收支（未來的交易）
                if transaction["type"] == "收入":
                    incoming_income += transaction["amount"]
                else:
                    incoming_expense += transaction["amount"]

        # 更新顯示
        self.balance_label.config(text=f"${current_balance:,.2f}")
        self.current_month_income_label.config(
            text=f"未來收入：${incoming_income:,.2f}"
        )
        self.current_month_expense_label.config(
            text=f"未來支出：${incoming_expense:,.2f}"
        )

    def add_transaction(self):
        try:
            # 獲取並驗證金額
            amount_str = self.amount_entry.get().strip()  # 移除空白
            if not amount_str:  # 檢查是否為空
                messagebox.showerror("錯誤", "請輸入金額")
                return
            amount = float(amount_str)
            if amount <= 0:  # 檢查是否為正數
                messagebox.showerror("錯誤", "請輸入大於0的金額")
                return

            category = self.category_combobox.get()
            transaction_type = self.transaction_type.get()
            note = self.note_entry.get()
            selected_date = self.date_entry.get_date()

            # 檢查是否為當月且在當前日期之後的交易
            current_datetime = datetime.now()
            if (
                selected_date.year == current_datetime.year
                and selected_date.month == current_datetime.month
            ):

                # 如果是支出，檢查是否需要顯示警告
                if transaction_type == "expense":
                    self.check_expense_warning(amount)

                # 創建交易記錄
                transaction = {
                    "date": selected_date.strftime("%Y-%m-%d"),
                    "category": category,
                    "amount": amount,
                    "type": "支出" if transaction_type == "expense" else "入",
                    "note": note,
                }

                self.transactions.append(transaction)

                # 更新交易列表顯示
                self.transaction_tree.insert(
                    "",
                    "end",
                    values=(
                        "×",  # 使用更小的符號
                        transaction["date"],
                        transaction["category"],
                        f"${transaction['amount']:.2f}",
                        transaction["type"],
                        transaction["note"],
                    ),
                )

                # 清空輸入
                self.amount_entry.delete(0, tk.END)
                self.note_entry.delete(0, tk.END)

                # 更新統計和圖表
                self.update_monthly_stats()
                self.update_chart()

            else:
                messagebox.showwarning("警告", "只能添加當月的交易記錄")

        except ValueError as e:
            print(f"Debug - ValueError: {str(e)}")  # 添加調試信息
            messagebox.showerror("錯誤", "請輸入有效的金額")

    def update_chart(self):
        # 清空現有圖表
        self.ax.clear()
        self.fig.clear()

        # 創建子圖，左邊是餅圖，右邊是標籤列表
        gs = self.fig.add_gridspec(1, 2, width_ratios=[1, 1.2])  # 調整左右比例
        ax1 = self.fig.add_subplot(gs[0])  # 餅圖
        ax2 = self.fig.add_subplot(gs[1])  # 標籤列表

        # 統計各類別支出
        expenses = {}
        total_expense = 0
        for transaction in self.transactions:
            if transaction["type"] == "支出":
                category = transaction["category"]
                amount = transaction["amount"]
                expenses[category] = expenses.get(category, 0) + amount
                total_expense += amount

        if expenses:
            # 準備數據
            labels = list(expenses.keys())
            sizes = list(expenses.values())
            colors = ["#FF9999", "#66B2FF", "#99FF99", "#FFCC99", "#FF99CC", "#99CCFF"]

            # 繪製餅圖（不顯示標籤和百分比）
            wedges, _ = ax1.pie(sizes, colors=colors, shadow=True, startangle=90)

            # 設置餅圖標題
            ax1.set_title("月度支出分析", pad=20, fontsize=16, fontweight="bold")

            # 創建藥丸式標籤列表
            legend_elements = []
            for i, (label, size) in enumerate(zip(labels, sizes)):
                percentage = size / total_expense * 100
                legend_elements.append(f"{label}\n${size:,.0f} ({percentage:.1f}%)")

            # 繪製藥丸式標籤
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, len(legend_elements) + 0.5)

            for i, (text, color) in enumerate(zip(legend_elements, colors)):
                y = len(legend_elements) - i - 0.5
                # 使用 FancyBboxPatch 創建圓角矩形
                pill = FancyBboxPatch(
                    (0.1, y - 0.3),  # (x, y)
                    0.8,  # width
                    0.6,  # height
                    boxstyle="round,pad=0.1,rounding_size=0.2",
                    facecolor=color,
                    alpha=0.3,
                    edgecolor=color,
                    linewidth=2,
                    transform=ax2.transData,
                    zorder=2,
                )
                ax2.add_patch(pill)
                # 添加文字
                ax2.text(
                    0.5,
                    y,
                    text,
                    ha="center",
                    va="center",
                    fontsize=12,
                    fontweight="bold",
                    transform=ax2.transData,
                )

            # 隱藏座標軸
            ax2.axis("off")

            # 調整布局
            self.fig.tight_layout(pad=1.5)  

        # 更新畫布
        self.canvas.draw()

    def check_expense_warning(self, new_expense_amount):
        # 更新當月累計支出
        current_date = datetime.now()
        current_month_expenses = (
            sum(
                transaction["amount"]
                for transaction in self.transactions
                if (
                    transaction["type"] == "支出"
                    and datetime.strptime(transaction["date"], "%Y-%m-%d").month
                    == current_date.month
                )
            )
            + new_expense_amount
        )

        # 計算薪資剩餘金額
        remaining_salary = self.monthly_salary - current_month_expenses
        salary_warning = self.monthly_salary * 0.1  # 薪資的10%

        # 檢查是否需要顯示薪資警告
        salary_warning_message = ""
        if remaining_salary <= salary_warning:
            salary_warning_message = "\n\n💰 注意：您的薪資所剩不到10%！"

        # 根據累計支出金額顯示不同級別的提醒
        if current_month_expenses >= self.warning_thresholds["extreme"]:
            self.show_warning_dialog(
                "支出警告！",
                f"您本月的支出已經超過 $10,000！\n"
                f"目前支出：${current_month_expenses:,.0f}\n"
                f"剩餘金額：${remaining_salary:,.0f}\n"
                f"月薪：${self.monthly_salary:,.0f}\n"
                f"請立即控制支出！這樣下去會破產的！{salary_warning_message}",
                "red",
            )
        elif current_month_expenses >= self.warning_thresholds["danger"]:
            self.show_warning_dialog(
                "支出提醒",
                f"您本月的支出已經超過 $5,000！\n"
                f"目前支出：${current_month_expenses:,.0f}\n"
                f"剩餘金額：${remaining_salary:,.0f}\n"
                f"月薪：${self.monthly_salary:,.0f}\n"
                f"支出金額已經很高了，請謹慎使用金錢！{salary_warning_message}",
                "orange",
            )
        elif current_month_expenses >= self.warning_thresholds["warning"]:
            self.show_warning_dialog(
                "溫馨提醒",
                f"您本月的支出已經超過 $3,000！\n"
                f"目前支出：${current_month_expenses:,.0f}\n"
                f"剩餘金額：${remaining_salary:,.0f}\n"
                f"月薪：${self.monthly_salary:,.0f}\n"
                f"請注意控制支出節奏。{salary_warning_message}",
                "darkblue",
            )
        elif current_month_expenses >= self.warning_thresholds["normal"]:
            self.show_warning_dialog(
                "友善提醒",
                f"您本月的支出已經超過 $1,000！\n"
                f"目前支出：${current_month_expenses:,.0f}\n"
                f"剩餘金額：${remaining_salary:,.0f}\n"
                f"月薪：${self.monthly_salary:,.0f}\n"
                f"請留意支出情況。{salary_warning_message}",
                "green",
            )

    def show_warning_dialog(self, title, message, color):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x300")  # 加大對話框尺寸

        # 設置視窗為模態
        dialog.transient(self.root)
        dialog.grab_set()

        # 創建框架
        frame = ttk.Frame(dialog, padding="30")
        frame.pack(fill="both", expand=True)

        # 顯示警告信息
        message_label = tk.Label(
            frame,
            text=message,
            font=("Microsoft JhengHei", 16, "bold"),  # 加大字體並設為粗體
            fg=color,
            wraplength=400,  # 加寬文字換行寬度
            justify="center",
        )
        message_label.pack(pady=30)

        # 確認按鈕
        ttk.Button(
            frame,
            text="我知道了",
            command=dialog.destroy,
            style="Warning.TButton"  # 使用新樣式
        ).pack(pady=20)

        # 設置按鈕樣式
        style = ttk.Style()
        style.configure(
            "Warning.TButton",
            font=("Microsoft JhengHei", 14, "bold"),  # 加大按鈕字體並設為粗體
            padding=10
        )

        # 播放警告音效
        dialog.bell()

    # 在 FinanceManager 類別中添加處理每月薪資的方法
    def add_monthly_salary(self):
        # 獲取當前日期
        current_date = datetime.now()
        
        # 創建薪資交易記錄
        salary_transaction = {
            "date": current_date.replace(day=self.salary_date).strftime("%Y-%m-%d"),
            "category": "薪資",
            "amount": self.monthly_salary,
            "type": "收入",
            "note": "每月固定薪資"
        }
        
        # 添加到交易列表
        self.transactions.append(salary_transaction)
        
        # 更新交易列表顯示
        self.transaction_tree.insert(
            "",
            "end",
            values=(
                "×",  # 使��更小的符號
                salary_transaction["date"],
                salary_transaction["category"],
                f"${salary_transaction['amount']:.2f}",
                salary_transaction["type"],
                salary_transaction["note"],
            ),
        )
        
        # 更新統計和圖表
        self.update_monthly_stats()
        self.update_chart()

    def on_tree_click(self, event):
        # 獲取點擊的區域
        region = self.transaction_tree.identify_region(event.x, event.y)
        if region == "cell":
            # 獲取點擊的列和行
            item = self.transaction_tree.identify_row(event.y)
            column = self.transaction_tree.identify_column(event.x)
            
            # 如果點擊的是刪除按鈕列
            if column == "#1":  # 第一列是刪除按鈕
                # 確認是否要刪除
                if messagebox.askyesno("確認刪除", "確定要刪除這筆交易記錄嗎？"):
                    # 獲取該行的所有值
                    values = self.transaction_tree.item(item)["values"]
                    
                    # 從交易列表中找到並刪除對應的交易
                    for i, transaction in enumerate(self.transactions):
                        if (
                            transaction["date"] == values[1]  # date
                            and transaction["category"] == values[2]  # category
                            and f"${transaction['amount']:.2f}" == values[3]  # amount
                            and transaction["type"] == values[4]  # type
                            and transaction["note"] == values[5]  # note
                        ):
                            # 刪除交易
                            del self.transactions[i]
                            # 從樹狀圖中刪除該行
                            self.transaction_tree.delete(item)
                            # 更新統計和圖表
                            self.update_monthly_stats()
                            self.update_chart()
                            break


if __name__ == "__main__":
    # 先顯示薪資輸入視窗
    salary_dialog = SalaryInputDialog()
    if salary_dialog.salary is None:
        sys.exit()
    
    # 啟動主程式
    root = tk.Tk()
    app = FinanceManager(root, salary_dialog.salary, salary_dialog.salary_date)
    root.mainloop()
