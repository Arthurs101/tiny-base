import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import tableManager
import filemanager

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt):
        self.prompt = prompt
        super().__init__(parent, title=title)

    def body(self, master):
        ttk.Label(master, text=self.prompt).grid(row=0, column=0, padx=10, pady=10)
        self.entry = ttk.Entry(master)
        self.entry.grid(row=0, column=1, padx=10, pady=10)
        return self.entry

    def apply(self):
        self.result = self.entry.get()

class TinyBaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tiny Base GUI")
        self.root.geometry("800x600")  # Set initial window size
        self.root.configure(bg='#f0f8ff')  # Set a light background color
        
        # Apply a theme and customize style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 14), foreground='#333', background='#f0f8ff')
        style.configure('TButton', font=('Helvetica', 12), foreground='#333', background='#87ceeb', padding=10)
        style.configure('TFrame', background='#f0f8ff')
        style.configure('Treeview', font=('Helvetica', 10), background='#ffffff', foreground='#333', fieldbackground='#ffffff')
        style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'), foreground='#333', background='#87ceeb')
        style.map('TButton', background=[('active', '#0052cc')], foreground=[('active', 'white')])
        
        # Create a frame for buttons
        self.button_frame = ttk.Frame(root, padding="10 10 10 10", style='TFrame')
        self.button_frame.pack(pady=20, padx=20, fill=tk.X)

        # Create the label
        self.label = ttk.Label(root, text="Tiny Base Database Management", font=('Helvetica', 20, 'bold'), style='TLabel')
        self.label.pack(pady=20, fill=tk.X)
        
        # Create buttons and place them in the button frame
        self.create_btn = ttk.Button(self.button_frame, text="Create Table", command=self.create_table, style='TButton')
        self.create_btn.pack(side=tk.LEFT, padx=5)
        
        self.add_register_btn = ttk.Button(self.button_frame, text="Add Register", command=self.add_register, style='TButton')
        self.add_register_btn.pack(side=tk.LEFT, padx=5)
        
        self.list_tables_btn = ttk.Button(self.button_frame, text="List Tables", command=self.list_tables, style='TButton')
        self.list_tables_btn.pack(side=tk.LEFT, padx=5)
        
        self.enable_table_btn = ttk.Button(self.button_frame, text="Enable Table", command=self.enable_table, style='TButton')
        self.enable_table_btn.pack(side=tk.LEFT, padx=5)
        
        self.disable_table_btn = ttk.Button(self.button_frame, text="Disable Table", command=self.disable_table, style='TButton')
        self.disable_table_btn.pack(side=tk.LEFT, padx=5)
        
        self.scan_table_btn = ttk.Button(self.button_frame, text="Scan Table", command=self.scan_table, style='TButton')
        self.scan_table_btn.pack(side=tk.LEFT, padx=5)
        
        self.alter_table_btn = ttk.Button(self.button_frame, text="Alter Table", command=self.alter_table, style='TButton')
        self.alter_table_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_table_btn = ttk.Button(self.button_frame, text="Delete Table", command=self.delete_table, style='TButton')
        self.delete_table_btn.pack(side=tk.LEFT, padx=5)
        
        self.describe_table_btn = ttk.Button(self.button_frame, text="Describe Table", command=self.describe_table, style='TButton')
        self.describe_table_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_register_btn = ttk.Button(self.button_frame, text="Delete Register", command=self.delete_register, style='TButton')
        self.delete_register_btn.pack(side=tk.LEFT, padx=5)
        
        # Create the treeview for displaying table data
        self.tree_frame = ttk.Frame(root, padding="10 10 10 10", style='TFrame')
        self.tree_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("Row Key", "Column Family", "Column Qualifier", "Timestamp", "Value"), show='headings', style='Treeview')
        self.tree.heading("Row Key", text="Row Key")
        self.tree.heading("Column Family", text="Column Family")
        self.tree.heading("Column Qualifier", text="Column Qualifier")
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.heading("Value", text="Value")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
    def create_table(self):
        table_name = self.prompt_dialog("Enter table name:")
        column_families = self.prompt_dialog("Enter column families (comma-separated):")
        if table_name and column_families:
            try:
                tableManager.createTable([table_name] + column_families.split(","))
                messagebox.showinfo("Success", f"Table '{table_name}' created successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def add_register(self):
        table_name = self.prompt_dialog("Enter table name:")
        row_key = self.prompt_dialog("Enter row key:")
        column_family = self.prompt_dialog("Enter column family:")
        column_qualifier = self.prompt_dialog("Enter column qualifier:")
        value = self.prompt_dialog("Enter value:")
        if table_name and row_key and column_family and column_qualifier and value:
            try:
                tableManager.addRegisters(table_name, [row_key, f"{column_family}:{column_qualifier}", value])
                messagebox.showinfo("Success", f"Register added to table '{table_name}' successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def list_tables(self):
        tables = tableManager.listTables()
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ("Table Name",)
        self.tree.heading("Table Name", text="Table Name")
        self.tree.column("Table Name", width=200)
        for table in tables:
            self.tree.insert("", tk.END, values=(table,))
    
    def enable_table(self):
        table_name = self.prompt_dialog("Enter table name:")
        if table_name:
            try:
                tableManager.enableTable(table_name)
                messagebox.showinfo("Success", f"Table '{table_name}' enabled successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def disable_table(self):
        table_name = self.prompt_dialog("Enter table name:")
        if table_name:
            try:
                tableManager.disableTable(table_name)
                messagebox.showinfo("Success", f"Table '{table_name}' disabled successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def scan_table(self):
        table_name = self.prompt_dialog("Enter table name:")
        if table_name:
            try:
                registers = tableManager.scanTable(table_name)
                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("Row Key", "Column Family", "Column Qualifier", "Timestamp", "Value")
                for col in self.tree["columns"]:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=200)
                for row_key, columns in registers.items():
                    if not columns:
                        self.tree.insert("", tk.END, values=(row_key, "", "", "", ""))
                    else:
                        for col_family, qualifiers in columns.items():
                            for qualifier, timestamp_values in qualifiers.items():
                                if not timestamp_values:
                                    self.tree.insert("", tk.END, values=(row_key, col_family, qualifier, timestamp, value))
                                else:
                                    for timestamp, value in timestamp_values.items():
                                        self.tree.insert("", tk.END, values=(row_key, col_family, qualifier, timestamp, value))
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def alter_table(self):
        table_name = self.prompt_dialog("Enter table name:")
        operation = self.prompt_dialog("Enter operation (ADD/DROP/MODIFY):")
        column_name = self.prompt_dialog("Enter column name:")
        column_type = self.prompt_dialog("Enter column type (if applicable):")
        if table_name and operation and column_name:
            try:
                tableManager.alterTable(table_name, operation, column_name, column_type)
                messagebox.showinfo("Success", f"Table '{table_name}' altered successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def delete_table(self):
        table_name = self.prompt_dialog("Enter table name:")
        if table_name:
            try:
                tableManager.dropTable(table_name)
                messagebox.showinfo("Success", f"Table '{table_name}' deleted successfully!")
                self.list_tables()  # Refresh the table list
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def describe_table(self):
        table_name = self.prompt_dialog("Enter table name:")
        if table_name:
            try:
                schema = tableManager.describeTable(table_name)
                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("Column Family", "Column Type")
                for col in self.tree["columns"]:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=200)
                for cf, ct in schema.items():
                    self.tree.insert("", tk.END, values=(cf, ct))
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_register(self):
        table_name = self.prompt_dialog("Enter table name:")
        row_key = self.prompt_dialog("Enter row key:")
        column_name = self.prompt_dialog("Enter column name (optional):")
        timestamp = self.prompt_dialog("Enter timestamp (optional):")
        
        if table_name and row_key:
            try:
                tableManager.deleteFromTable(table_name, row_key, column_name if column_name else None, int(timestamp) if timestamp else None)
                messagebox.showinfo("Success", f"Register deleted from table '{table_name}' successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def prompt_dialog(self, prompt):
        dialog = CustomDialog(self.root, title="Input", prompt=prompt)
        return dialog.result
def on_closing():
    messagebox.showinfo("Closing", "saving changes...")
    tableManager.saveTables()
    messagebox.showinfo("Succes","saved changes")
    root.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    gui = TinyBaseGUI(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
