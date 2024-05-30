import time
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
        
        self.button_frame = ttk.Frame(root, padding="10 10 10 10", style='TFrame')
        self.button_frame.pack(pady=20, padx=20, fill=tk.X)

        # List of buttons
        buttons = [
            ("Create Table", self.create_table),
            ("Enable Table", self.enable_table),
            ("Disable Table", self.disable_table),
            ("List Tables", self.list_tables),
            ("Scan Table", self.scan_table),
            ("Alter Table", self.alter_table),
            ("Delete Table", self.delete_table),
            ("Truncate Table", self.truncate_table),
            ("Describe Table", self.describe_table),
            ("Add Register", self.add_register),
            ("Get Register", self.get_register),
            ("Delete Register", self.delete_register)
        ]

        # Place buttons in grid
        for index, (text, command) in enumerate(buttons):
            row = index // 6
            column = index % 6
            btn = ttk.Button(self.button_frame, text=text, command=command, style='TButton')
            btn.grid(row=row, column=column, padx=5, pady=5, sticky=tk.W+tk.E)

        # Expand buttons to fill the frame
        for col in range(6):
            self.button_frame.columnconfigure(col, weight=1)

        # Create the treeview for displaying table data
        self.tree_frame = ttk.Frame(root, padding="10 10 10 10", style='TFrame')
        self.tree_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("Row Key", "Column Family", "Column Qualifier", "Timestamp", "Value"), show='headings', style='Treeview')
        y_scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.heading("Row Key", text="Row Key")
        self.tree.heading("Column Family", text="Column Family")
        self.tree.heading("Column Qualifier", text="Column Qualifier")
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.heading("Value", text="Value")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=y_scrollbar.set)
        
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
                                    self.tree.insert("", tk.END, values=(row_key, col_family, qualifier, "", ""))
                                else:
                                    for timestamp, value in timestamp_values.items():
                                        self.tree.insert("", tk.END, values=(row_key, col_family, qualifier, timestamp, value))
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def get_register(self):
        table_name = self.prompt_dialog("Enter table name:")
        row_key = self.prompt_dialog("Enter row key:")
        column_family = self.prompt_dialog("Enter column family: (colmunFamily:columnQualifier)")
        versions = None
        if column_family:
            versions = self.prompt_dialog("Amount of versions to retrieve:")
        if table_name and row_key:
            try:
                register = tableManager.getRegister(table_name, row_key, column=column_family if column_family else None, versions=int(versions) if versions else 1)
                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("Column Family", "Column Qualifier", "Timestamp", "Value")
                for col in self.tree["columns"]:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=200)
                for col_family, qualifiers in register.items():
                    for qualifier, timestamp_values in qualifiers.items():
                        for timestamp, value in timestamp_values.items():
                            self.tree.insert("", tk.END, values=(col_family, qualifier, timestamp, value))
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def alter_table(self):
        table_name = self.prompt_dialog("Enter table name:")
        action = self.prompt_dialog("Enter action (ADD, DROP, MODIFY Column family):")
        column_family = self.prompt_dialog("Enter column family name:")
        if table_name and action and column_family:
            try:
                tableManager.alterTable(table_name, [action, column_family])
                messagebox.showinfo("Success", f"Table '{table_name}' altered successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def delete_table(self):
        table_name = self.prompt_dialog("Enter table name:")
        if table_name:
            try:
                tableManager.dropTable(table_name)
                messagebox.showinfo("Success", f"Table '{table_name}' deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def describe_table(self):
        table_name = self.prompt_dialog("Enter table name:")
        if table_name:
            try:
                description = tableManager.describeTable(table_name)
                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("Column Family", "Attributes")
                for col in self.tree["columns"]:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=200)
                for col_family, attributes in description.items():
                    self.tree.insert("", tk.END, values=(col_family, attributes))
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
        dialog = CustomDialog(self.root, "Input", prompt)
        return dialog.result
    def truncate_table(self):
        table_name = self.prompt_dialog("Enter table name:")
        if table_name:
            start = time.time()
            tableManager.truncateTable(table_name)
            end = time.time()
            messagebox.showinfo("Truncating table", f"Disabling table {table_name}....")
            messagebox.showinfo("Truncating table", f"Dropping table {table_name}....")
            messagebox.showinfo("Truncating table", f"Recreating table {table_name}....")
            messagebox.showinfo("Truncating table", f"Finished truncating {table_name}\n time to finish:{end-start} S")

def on_closing():
    messagebox.showinfo("Closing", "saving changes...")
    tableManager.saveTables()
    messagebox.showinfo("Succes","saved changes")
    root.destroy()       

if __name__ == "__main__":
    root = tk.Tk()
    app = TinyBaseGUI(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    