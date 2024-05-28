import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import tableManager
import filemanager

class TinyBaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tiny Base GUI")
        
        self.label = tk.Label(root, text="Tiny Base Database Management", font=('Helvetica', 16))
        self.label.pack(pady=20)
        
        self.create_btn = tk.Button(root, text="Create Table", command=self.create_table)
        self.create_btn.pack(pady=5)
        
        self.add_register_btn = tk.Button(root, text="Add Register", command=self.add_register)
        self.add_register_btn.pack(pady=5)
        
        self.list_tables_btn = tk.Button(root, text="List Tables", command=self.list_tables)
        self.list_tables_btn.pack(pady=5)
        
        self.enable_table_btn = tk.Button(root, text="Enable Table", command=self.enable_table)
        self.enable_table_btn.pack(pady=5)
        
        self.disable_table_btn = tk.Button(root, text="Disable Table", command=self.disable_table)
        self.disable_table_btn.pack(pady=5)
        
        self.scan_table_btn = tk.Button(root, text="Scan Table", command=self.scan_table)
        self.scan_table_btn.pack(pady=5)
        
        self.alter_table_btn = tk.Button(root, text="Alter Table", command=self.alter_table)
        self.alter_table_btn.pack(pady=5)
        
        self.delete_table_btn = tk.Button(root, text="Delete Table", command=self.delete_table)
        self.delete_table_btn.pack(pady=5)
        
        self.describe_table_btn = tk.Button(root, text="Describe Table", command=self.describe_table)
        self.describe_table_btn.pack(pady=5)
        
        self.tree = ttk.Treeview(root)
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)
        
    def create_table(self):
        table_name = simpledialog.askstring("Input", "Enter table name:")
        column_families = simpledialog.askstring("Input", "Enter column families (comma-separated):")
        if table_name and column_families:
            try:
                tableManager.createTable([table_name] + column_families.split(","))
                messagebox.showinfo("Success", f"Table '{table_name}' created successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def add_register(self):
        table_name = simpledialog.askstring("Input", "Enter table name:")
        row_key = simpledialog.askstring("Input", "Enter row key:")
        column_family = simpledialog.askstring("Input", "Enter column family:")
        column_qualifier = simpledialog.askstring("Input", "Enter column qualifier:")
        value = simpledialog.askstring("Input", "Enter value:")
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
        table_name = simpledialog.askstring("Input", "Enter table name:")
        if table_name:
            try:
                tableManager.enableTable(table_name)
                messagebox.showinfo("Success", f"Table '{table_name}' enabled successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def disable_table(self):
        table_name = simpledialog.askstring("Input", "Enter table name:")
        if table_name:
            try:
                tableManager.disableTable(table_name)
                messagebox.showinfo("Success", f"Table '{table_name}' disabled successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def scan_table(self):
        table_name = simpledialog.askstring("Input", "Enter table name:")
        if table_name:
            try:
                registers = tableManager.scanTable(table_name)
                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("Row Key", "Column Family", "Column Qualifier", "Value")
                for col in self.tree["columns"]:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=200)
                for row_key, columns in registers.items():
                    for col_family, qualifiers in columns.items():
                        for qualifier, timestamp_values in qualifiers.items():
                            for timestamp, value in timestamp_values.items():
                                self.tree.insert("", tk.END, values=(row_key, col_family, qualifier, value))
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def alter_table(self):
        table_name = simpledialog.askstring("Input", "Enter table name:")
        operation = simpledialog.askstring("Input", "Enter operation (ADD/DROP/MODIFY):")
        column_name = simpledialog.askstring("Input", "Enter column name:")
        column_type = simpledialog.askstring("Input", "Enter column type (if applicable):")
        if table_name and operation and column_name:
            try:
                tableManager.alterTable(table_name, operation, column_name, column_type)
                messagebox.showinfo("Success", f"Table '{table_name}' altered successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def delete_table(self):
        table_name = simpledialog.askstring("Input", "Enter table name:")
        if table_name:
            try:
                tableManager.dropTable(table_name)
                messagebox.showinfo("Success", f"Table '{table_name}' deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def describe_table(self):
        table_name = simpledialog.askstring("Input", "Enter table name:")
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

if __name__ == "__main__":
    root = tk.Tk()
    gui = TinyBaseGUI(root)
    root.mainloop()
