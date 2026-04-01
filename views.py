import tkinter as tk
from tkinter import ttk, messagebox
import utils
import calendar
from datetime import datetime, timedelta

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart-Task Academic Project Manager")
        self.geometry("800x600")
        self.minsize(600, 500)
        
        try:
            # Use 'clam' theme for a better cross-platform look
            self.style = ttk.Style(self)
            self.style.theme_use('clam')
        except tk.TclError:
            pass
        
        # Notebook for Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Dashboard Tab
        self.dashboard_tab = DashboardTab(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        
        # Task Management Tab
        self.tasks_tab = TasksTab(self.notebook)
        self.notebook.add(self.tasks_tab, text="Task Management")
        
        # Calendar Tab
        self.calendar_tab = CalendarTab(self.notebook)
        self.notebook.add(self.calendar_tab, text="Calendar")

class DashboardTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        header = ttk.Label(self, text="Academic Summary", font=("Helvetica", 24, "bold"))
        header.pack(pady=30)
        
        frame = ttk.Frame(self)
        frame.pack(pady=10)
        
        self.total_label = ttk.Label(frame, text="Total Tasks: 0", font=("Helvetica", 14))
        self.total_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.completed_label = ttk.Label(frame, text="Completed Tasks: 0", font=("Helvetica", 14))
        self.completed_label.grid(row=0, column=1, padx=20, pady=10)
        
        self.next_deadline_label = ttk.Label(self, text="Next Immediate Deadline: None", font=("Helvetica", 16, "bold"), foreground="#cc0000")
        self.next_deadline_label.pack(pady=40)

    def update_metrics(self, total, completed, next_deadline_info):
        self.total_label.config(text=f"Total Tasks: {total}")
        self.completed_label.config(text=f"Completed Tasks: {completed}")
        self.next_deadline_label.config(text=f"Next Immediate Deadline: {next_deadline_info}")

class CalendarTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_date = datetime.now().date()
        self.tasks = []
        
        # Navigation
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", pady=10, padx=10)
        
        self.prev_btn = ttk.Button(nav_frame, text="< Prev Month", command=self.prev_month)
        self.prev_btn.pack(side="left", padx=5)
        
        self.month_label = ttk.Label(nav_frame, text="", font=("Helvetica", 16, "bold"))
        self.month_label.pack(side="left", expand=True)
        
        self.next_btn = ttk.Button(nav_frame, text="Next Month >", command=self.next_month)
        self.next_btn.pack(side="right", padx=5)
        
        # Main content area
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Grid for calendar
        self.cal_frame = ttk.Frame(content_frame)
        self.cal_frame.pack(side="left", fill="both", expand=True)
        
        # Side panel for tasks of selected day
        self.side_panel = ttk.LabelFrame(content_frame, text="Tasks for Selected Day")
        self.side_panel.pack(side="right", fill="y", padx=10)
        
        self.day_tasks_listbox = tk.Listbox(self.side_panel, width=35, font=("Helvetica", 10))
        self.day_tasks_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.build_calendar()
        
    def prev_month(self):
        first_day = self.current_date.replace(day=1)
        prev_month_last_day = first_day - timedelta(days=1)
        self.current_date = prev_month_last_day.replace(day=1)
        self.build_calendar()
        
    def next_month(self):
        days_in_month = calendar.monthrange(self.current_date.year, self.current_date.month)[1]
        next_month_first_day = self.current_date.replace(day=days_in_month) + timedelta(days=1)
        self.current_date = next_month_first_day
        self.build_calendar()

    def set_tasks(self, tasks):
        self.tasks = tasks
        self.build_calendar()
        
    def build_calendar(self):
        for widget in self.cal_frame.winfo_children():
            widget.destroy()
            
        year = self.current_date.year
        month = self.current_date.month
        
        self.month_label.config(text=f"{calendar.month_name[month]} {year}")
        
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, d in enumerate(days):
            lbl = ttk.Label(self.cal_frame, text=d, font=("Helvetica", 10, "bold"), anchor="center")
            lbl.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            self.cal_frame.columnconfigure(i, weight=1)
            
        cal = calendar.monthcalendar(year, month)
        
        for row, week in enumerate(cal):
            self.cal_frame.rowconfigure(row+1, weight=1)
            for col, day in enumerate(week):
                if day == 0:
                    frm = ttk.Frame(self.cal_frame, relief="ridge", borderwidth=1)
                    frm.grid(row=row+1, column=col, sticky="nsew", padx=1, pady=1)
                else:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    day_tasks = [t for t in self.tasks if t.deadline == date_str]
                    
                    frame = tk.Frame(self.cal_frame, relief="ridge", borderwidth=1, bg="white")
                    frame.grid(row=row+1, column=col, sticky="nsew", padx=1, pady=1)
                    
                    # Make it clickable
                    frame.bind("<Button-1>", lambda e, d=date_str, t=day_tasks: self.show_tasks_for_day(d, t))
                    
                    lbl = tk.Label(frame, text=str(day), bg="white", font=("Helvetica", 10))
                    lbl.pack(anchor="ne", padx=2, pady=2)
                    lbl.bind("<Button-1>", lambda e, d=date_str, t=day_tasks: self.show_tasks_for_day(d, t))
                    
                    if day_tasks:
                        pending = len([t for t in day_tasks if t.status == "Pending"])
                        completed = len([t for t in day_tasks if t.status == "Completed"])
                        
                        indicator_text = []
                        if pending > 0: indicator_text.append(f"{pending} pending")
                        if completed > 0: indicator_text.append(f"{completed} done")
                        
                        t_lbl = tk.Label(frame, text="\\n".join(indicator_text), bg="white", fg="#cc0000" if pending > 0 else "green", font=("Helvetica", 8))
                        t_lbl.pack(anchor="center", expand=True)
                        t_lbl.bind("<Button-1>", lambda e, d=date_str, t=day_tasks: self.show_tasks_for_day(d, t))

    def show_tasks_for_day(self, date_str, tasks):
        self.side_panel.config(text=f"Tasks: {date_str}")
        self.day_tasks_listbox.delete(0, tk.END)
        if not tasks:
            self.day_tasks_listbox.insert(tk.END, "No tasks scheduled.")
        else:
            for t in tasks:
                prefix = "[✓]" if t.status == "Completed" else "[ ]"
                self.day_tasks_listbox.insert(tk.END, f"{prefix} {t.title}")

class TasksTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Top filters control panel
        filter_frame = ttk.LabelFrame(self, text="Filters & Search")
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Status:").pack(side="left", padx=5)
        self.status_var = tk.StringVar(value="All")
        self.status_combo = ttk.Combobox(filter_frame, textvariable=self.status_var, values=["All", "Pending", "Completed"], state="readonly", width=12)
        self.status_combo.pack(side="left", padx=5)
        
        ttk.Label(filter_frame, text="Priority:").pack(side="left", padx=5)
        self.priority_var = tk.StringVar(value="All")
        self.priority_combo = ttk.Combobox(filter_frame, textvariable=self.priority_var, values=["All", "High", "Medium", "Low"], state="readonly", width=12)
        self.priority_combo.pack(side="left", padx=5)
        
        self.filter_btn = ttk.Button(filter_frame, text="Apply Filters")
        self.filter_btn.pack(side="left", padx=15)
        
        # Task List
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("ID", "Title", "Description", "Deadline", "Priority", "Status", "Urgency")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            width = 40 if col == "ID" else 100
            if col == "Title": width = 150
            if col == "Description": width = 180
            if col == "Urgency": width = 120
            self.tree.column(col, width=width, anchor="center")
            
        # Deadline Tracker tags
        self.tree.tag_configure("red", background="#ffcccc")
        self.tree.tag_configure("orange", background="#ffe5b4")
        self.tree.tag_configure("goldenrod", background="#fffacd")
        self.tree.tag_configure("forest green", background="#d4edda")
        self.tree.tag_configure("black", background="#e9ecef", foreground="#6c757d")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Action Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        self.add_btn = ttk.Button(btn_frame, text="Add New Task")
        self.add_btn.pack(side="left", padx=5)
        
        self.edit_btn = ttk.Button(btn_frame, text="Edit Selected")
        self.edit_btn.pack(side="left", padx=5)

        self.complete_btn = ttk.Button(btn_frame, text="Mark Complete")
        self.complete_btn.pack(side="left", padx=5)

        self.delete_btn = ttk.Button(btn_frame, text="Delete Selected")
        self.delete_btn.pack(side="right", padx=5)

    def populate_list(self, tasks):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for t in tasks:
            days_left = utils.calculate_days_until(t.deadline)
            color_tag = utils.get_urgency_color(days_left)
            
            urgency_str = f"{days_left} days left" if days_left is not None else "Invalid Date"
            if days_left is not None and days_left < 0:
                urgency_str = f"Overdue by {abs(days_left)} days"
            elif days_left == 0:
                urgency_str = "Due Today!"

            if t.status == "Completed":
                color_tag = "black"
                urgency_str = "Done"

            self.tree.insert("", "end", values=(t.id, t.title, t.description, t.deadline, t.priority, t.status, urgency_str), tags=(color_tag,))

    def get_selected_task_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task first.")
            return None
        item_values = self.tree.item(selected[0], "values")
        return int(item_values[0])

class TaskForm(tk.Toplevel):
    def __init__(self, parent, task=None):
        super().__init__(parent)
        self.title("Task Details")
        self.geometry("350x380")
        self.resizable(False, False)
        self.grab_set()  # Modal window
        
        self.task = task
        self.result = None

        container = ttk.Frame(self, padding="20 20 20 20")
        container.pack(fill="both", expand=True)
        
        ttk.Label(container, text="Title: *").pack(anchor="w", pady=(0,2))
        self.title_entry = ttk.Entry(container, width=40)
        self.title_entry.pack(fill="x", pady=(0,10))
        
        ttk.Label(container, text="Description:").pack(anchor="w", pady=(0,2))
        self.desc_entry = ttk.Entry(container, width=40)
        self.desc_entry.pack(fill="x", pady=(0,10))
        
        ttk.Label(container, text="Deadline (YYYY-MM-DD): *").pack(anchor="w", pady=(0,2))
        self.deadline_entry = ttk.Entry(container, width=40)
        self.deadline_entry.pack(fill="x", pady=(0,10))
        
        f = ttk.Frame(container)
        f.pack(fill="x", pady=(0,10))
        
        ttk.Label(f, text="Priority:").grid(row=0, column=0, sticky="w")
        self.priority_var = tk.StringVar(value="Low")
        self.priority_combo = ttk.Combobox(f, textvariable=self.priority_var, values=["High", "Medium", "Low"], state="readonly", width=12)
        self.priority_combo.grid(row=0, column=1, padx=10, sticky="w")
        
        ttk.Label(f, text="Status:").grid(row=1, column=0, sticky="w", pady=(10,0))
        self.status_var = tk.StringVar(value="Pending")
        self.status_combo = ttk.Combobox(f, textvariable=self.status_var, values=["Pending", "Completed"], state="readonly", width=12)
        self.status_combo.grid(row=1, column=1, padx=10, pady=(10,0), sticky="w")
        
        if self.task:
            self.title_entry.insert(0, self.task.title)
            if self.task.description: self.desc_entry.insert(0, self.task.description)
            if self.task.deadline: self.deadline_entry.insert(0, self.task.deadline)
            self.priority_var.set(self.task.priority)
            self.status_var.set(self.task.status)
            
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", pady=20)
        
        save_btn = ttk.Button(btn_frame, text="Save Task", command=self.save)
        save_btn.pack(side="right")

    def save(self):
        title = self.title_entry.get().strip()
        desc = self.desc_entry.get().strip()
        deadline = self.deadline_entry.get().strip()
        priority = self.priority_var.get()
        status = self.status_var.get()
        
        # User input validation via try-except and messagebox
        if not title:
            messagebox.showerror("Validation Error", "Task Title is heavily required!", parent=self)
            return
            
        if not deadline:
            messagebox.showerror("Validation Error", "Deadline is greatly required!", parent=self)
            return
            
        import utils
        from datetime import datetime
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation Error", "Deadline must be precisely in YYYY-MM-DD format!", parent=self)
            return

        self.result = {
            "title": title,
            "description": desc,
            "deadline": deadline,
            "priority": priority,
            "status": status
        }
        self.destroy()
