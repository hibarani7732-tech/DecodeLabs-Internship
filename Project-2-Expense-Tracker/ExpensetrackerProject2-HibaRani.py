"""
EXPENSE TRACKER PRO - FULLY WORKING VERSION
All features: Delete Last, Reset History, Loan Management, Budget Alerts
No external libraries required
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker Pro - DecodeLabs")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Data storage (Accumulator variables)
        self.total_accumulator = 0.0
        self.budget_limit = 5000.0
        self.expenses_list = []
        self.loan_balance = 0.0  # Track loan balance
        self.data_file = "expenses_data.json"
        
        # Load saved data
        self.load_data()
        
        # Create interface
        self.setup_gui()
        self.update_all_displays()
        
    def setup_gui(self):
        """Create all GUI components"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # ========== TITLE SECTION ==========
        title_label = ttk.Label(main_frame, text="💰 EXPENSE TRACKER PRO", 
                                font=('Arial', 20, 'bold'))
        title_label.pack(pady=(0, 5))
        
        subtitle = ttk.Label(main_frame, text="DecodeLabs Internship Project - With Loan Management",
                            font=('Arial', 10, 'italic'))
        subtitle.pack(pady=(0, 15))
        
        # ========== INPUT SECTION ==========
        input_frame = ttk.LabelFrame(main_frame, text="📝 ADD NEW EXPENSE", padding="15")
        input_frame.pack(fill="x", pady=(0, 10))
        
        # Row 1: Amount and Description
        row1 = tk.Frame(input_frame)
        row1.pack(fill="x", pady=5)
        
        tk.Label(row1, text="Amount ($):", font=('Arial', 11, 'bold')).pack(side="left", padx=(0, 10))
        self.amount_entry = tk.Entry(row1, font=('Arial', 14), width=15)
        self.amount_entry.pack(side="left", padx=(0, 20))
        self.amount_entry.bind('<Return>', lambda e: self.add_expense())
        
        tk.Label(row1, text="Description:", font=('Arial', 11, 'bold')).pack(side="left", padx=(0, 10))
        self.desc_entry = tk.Entry(row1, font=('Arial', 11), width=30)
        self.desc_entry.pack(side="left")
        
        # Row 2: Category and Date
        row2 = tk.Frame(input_frame)
        row2.pack(fill="x", pady=5)
        
        tk.Label(row2, text="Category:", font=('Arial', 11, 'bold')).pack(side="left", padx=(0, 10))
        self.category_var = tk.StringVar()
        categories = ['Food', 'Transport', 'Bills', 'Entertainment', 'Shopping', 'Healthcare', 'Education', 'Other']
        self.category_dropdown = ttk.Combobox(row2, textvariable=self.category_var, values=categories, width=20)
        self.category_dropdown.pack(side="left", padx=(0, 20))
        self.category_dropdown.set('Select Category')
        
        tk.Label(row2, text="Date (YYYY-MM-DD):", font=('Arial', 11, 'bold')).pack(side="left", padx=(0, 10))
        self.date_entry = tk.Entry(row2, font=('Arial', 11), width=15)
        self.date_entry.pack(side="left")
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Row 3: Add Button
        row3 = tk.Frame(input_frame)
        row3.pack(fill="x", pady=10)
        
        self.add_btn = tk.Button(row3, text="➕ ADD EXPENSE", command=self.add_expense, 
                                 bg='#4CAF50', fg='white', font=('Arial', 11, 'bold'), width=20)
        self.add_btn.pack()
        
        # ========== SUMMARY SECTION ==========
        summary_frame = ttk.LabelFrame(main_frame, text="📊 FINANCIAL SUMMARY", padding="15")
        summary_frame.pack(fill="x", pady=(0, 10))
        
        # Total spent
        total_container = tk.Frame(summary_frame)
        total_container.pack(fill="x", pady=5)
        
        tk.Label(total_container, text="TOTAL SPENT:", font=('Arial', 12, 'bold')).pack(side="left", padx=(0, 20))
        self.total_label = tk.Label(total_container, text="$0.00", font=('Arial', 18, 'bold'), fg='blue')
        self.total_label.pack(side="left")
        
        # Budget setting
        budget_container = tk.Frame(summary_frame)
        budget_container.pack(fill="x", pady=5)
        
        tk.Label(budget_container, text="BUDGET LIMIT ($):", font=('Arial', 11, 'bold')).pack(side="left", padx=(0, 10))
        self.budget_entry = tk.Entry(budget_container, font=('Arial', 11), width=12)
        self.budget_entry.pack(side="left", padx=(0, 10))
        self.budget_entry.insert(0, str(self.budget_limit))
        
        self.set_budget_btn = tk.Button(budget_container, text="SET BUDGET", command=self.set_budget_limit,
                                        bg='#2196F3', fg='white', font=('Arial', 10, 'bold'))
        self.set_budget_btn.pack(side="left")
        
        # Remaining budget
        remaining_container = tk.Frame(summary_frame)
        remaining_container.pack(fill="x", pady=5)
        
        tk.Label(remaining_container, text="REMAINING:", font=('Arial', 12, 'bold')).pack(side="left", padx=(0, 20))
        self.remaining_label = tk.Label(remaining_container, text="$5000.00", font=('Arial', 14, 'bold'), fg='green')
        self.remaining_label.pack(side="left")
        
        # ========== LOAN MANAGEMENT SECTION ==========
        self.loan_frame = ttk.LabelFrame(main_frame, text="💰 LOAN MANAGEMENT", padding="15")
        
        loan_display_frame = tk.Frame(self.loan_frame)
        loan_display_frame.pack(fill="x", pady=5)
        
        tk.Label(loan_display_frame, text="OVER BUDGET AMOUNT:", font=('Arial', 11, 'bold')).pack(side="left", padx=(0, 10))
        self.over_budget_label = tk.Label(loan_display_frame, text="$0.00", font=('Arial', 12, 'bold'), fg='red')
        self.over_budget_label.pack(side="left", padx=(0, 20))
        
        tk.Label(loan_display_frame, text="LOAN BALANCE:", font=('Arial', 11, 'bold')).pack(side="left", padx=(0, 10))
        self.loan_balance_label = tk.Label(loan_display_frame, text="$0.00", font=('Arial', 12, 'bold'), fg='orange')
        self.loan_balance_label.pack(side="left")
        
        # Loan controls
        loan_control_frame = tk.Frame(self.loan_frame)
        loan_control_frame.pack(fill="x", pady=10)
        
        tk.Label(loan_control_frame, text="Amount ($):", font=('Arial', 11)).pack(side="left", padx=(0, 10))
        self.loan_entry = tk.Entry(loan_control_frame, font=('Arial', 11), width=15)
        self.loan_entry.pack(side="left", padx=(0, 10))
        
        self.add_loan_btn = tk.Button(loan_control_frame, text="TAKE LOAN", command=self.take_loan,
                                      bg='#FF9800', fg='white', font=('Arial', 10, 'bold'))
        self.add_loan_btn.pack(side="left", padx=5)
        
        self.repay_loan_btn = tk.Button(loan_control_frame, text="REPAY LOAN", command=self.repay_loan,
                                        bg='#9C27B0', fg='white', font=('Arial', 10, 'bold'))
        self.repay_loan_btn.pack(side="left", padx=5)
        
        # Initially hide loan frame (shown only when needed)
        
        # ========== PROGRESS BAR ==========
        progress_frame = ttk.LabelFrame(main_frame, text="📊 BUDGET PROGRESS", padding="10")
        progress_frame.pack(fill="x", pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(fill="x", pady=5)
        
        self.progress_label = tk.Label(progress_frame, text="Budget Usage: 0%", font=('Arial', 10))
        self.progress_label.pack()
        
        # ========== HISTORY TABLE ==========
        history_frame = ttk.LabelFrame(main_frame, text="📋 TRANSACTION HISTORY", padding="10")
        history_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Create Treeview
        columns = ('ID', 'Date', 'Description', 'Category', 'Amount', 'Type')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=12)
        
        self.history_tree.heading('ID', text='#')
        self.history_tree.heading('Date', text='Date')
        self.history_tree.heading('Description', text='Description')
        self.history_tree.heading('Category', text='Category')
        self.history_tree.heading('Amount', text='Amount ($)')
        self.history_tree.heading('Type', text='Type')
        
        self.history_tree.column('ID', width=50)
        self.history_tree.column('Date', width=120)
        self.history_tree.column('Description', width=300)
        self.history_tree.column('Category', width=120)
        self.history_tree.column('Amount', width=100)
        self.history_tree.column('Type', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ========== STATUS BAR ==========
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill="x", pady=(0, 5))
        
        self.status_label = tk.Label(status_frame, text="✅ Ready", relief=tk.SUNKEN, anchor=tk.W, 
                                      font=('Arial', 9), bg='#f0f0f0')
        self.status_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.count_label = tk.Label(status_frame, text="Transactions: 0", relief=tk.SUNKEN, 
                                     font=('Arial', 9), bg='#f0f0f0', width=20)
        self.count_label.pack(side="right")
        
        # ========== CONTROL BUTTONS ==========
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=5)
        
        self.delete_expense_btn = tk.Button(button_frame, text="🗑️ DELETE LAST EXPENSE", 
                                            command=self.delete_last_expense,
                                            bg='#f44336', fg='white', font=('Arial', 10, 'bold'))
        self.delete_expense_btn.pack(side="left", padx=5)
        
        self.delete_loan_btn = tk.Button(button_frame, text="💸 DELETE LAST LOAN", 
                                         command=self.delete_last_loan,
                                         bg='#FF5722', fg='white', font=('Arial', 10, 'bold'))
        self.delete_loan_btn.pack(side="left", padx=5)
        
        self.reset_history_btn = tk.Button(button_frame, text="⚠️ RESET EXPENSE HISTORY", 
                                           command=self.reset_expense_history,
                                           bg='#FF9800', fg='white', font=('Arial', 10, 'bold'))
        self.reset_history_btn.pack(side="left", padx=5)
        
        self.reset_all_btn = tk.Button(button_frame, text="🔥 RESET EVERYTHING", 
                                       command=self.reset_everything,
                                       bg='#9C27B0', fg='white', font=('Arial', 10, 'bold'))
        self.reset_all_btn.pack(side="left", padx=5)
        
        self.export_btn = tk.Button(button_frame, text="💾 EXPORT DATA", 
                                    command=self.export_data,
                                    bg='#607D8B', fg='white', font=('Arial', 10, 'bold'))
        self.export_btn.pack(side="right", padx=5)
        
        # Load existing data into treeview
        self.refresh_history_display()
        self.update_loan_visibility()
    
    # ========== LOAN MANAGEMENT ==========
    
    def take_loan(self):
        """Take a loan"""
        loan_str = self.loan_entry.get().strip()
        
        if not loan_str:
            messagebox.showwarning("Input Error", "Please enter loan amount!")
            return
        
        try:
            loan_amount = float(loan_str)
            if loan_amount <= 0:
                messagebox.showwarning("Invalid Amount", "Loan amount must be positive!")
                return
            
            # Update loan balance
            self.loan_balance += loan_amount
            
            # Record loan transaction
            transaction = {
                'id': len(self.expenses_list) + 1,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'description': 'LOAN TAKEN',
                'category': 'Loan',
                'amount': loan_amount,
                'type': 'Loan Taken'
            }
            self.expenses_list.append(transaction)
            
            # Update displays
            self.refresh_history_display()
            self.update_loan_display()
            self.save_data()
            
            # Clear entry
            self.loan_entry.delete(0, tk.END)
            
            self.status_label.config(text=f"💰 Loan taken: ${loan_amount:.2f}", fg='orange')
            messagebox.showinfo("Loan Taken", f"Loan of ${loan_amount:.2f} has been added!\n\nTotal Loan Balance: ${self.loan_balance:.2f}")
            
        except ValueError:
            messagebox.showerror("Invalid Data", "Please enter a valid number!")
            self.status_label.config(text="❌ Invalid loan amount!", fg='red')
    
    def repay_loan(self):
        """Repay loan"""
        if self.loan_balance <= 0:
            messagebox.showinfo("No Loan", "No outstanding loan to repay!")
            return
        
        repay_str = self.loan_entry.get().strip()
        
        if not repay_str:
            # If no amount, offer to repay full
            confirm = messagebox.askyesno("Repay Loan", 
                                         f"Current loan balance: ${self.loan_balance:.2f}\n\n"
                                         f"Repay full amount?")
            if confirm:
                repay_amount = self.loan_balance
            else:
                return
        else:
            try:
                repay_amount = float(repay_str)
                if repay_amount <= 0:
                    messagebox.showwarning("Invalid Amount", "Repayment amount must be positive!")
                    return
                if repay_amount > self.loan_balance:
                    confirm = messagebox.askyesno("Exceeds Loan", 
                                                 f"Repayment (${repay_amount:.2f}) exceeds loan (${self.loan_balance:.2f})\n\n"
                                                 f"Repay full loan amount?")
                    if confirm:
                        repay_amount = self.loan_balance
                    else:
                        return
            except ValueError:
                messagebox.showerror("Invalid Data", "Please enter a valid number!")
                return
        
        # Update loan balance
        self.loan_balance -= repay_amount
        
        # Record repayment transaction
        transaction = {
            'id': len(self.expenses_list) + 1,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'description': 'LOAN REPAYMENT',
            'category': 'Loan Repayment',
            'amount': repay_amount,
            'type': 'Loan Repayment'
        }
        self.expenses_list.append(transaction)
        
        # Update displays
        self.refresh_history_display()
        self.update_loan_display()
        self.save_data()
        
        # Clear entry
        self.loan_entry.delete(0, tk.END)
        
        self.status_label.config(text=f"💰 Loan repaid: ${repay_amount:.2f}", fg='green')
        messagebox.showinfo("Loan Repaid", f"Repaid ${repay_amount:.2f}\nRemaining Loan: ${self.loan_balance:.2f}")
    
    def delete_last_loan(self):
        """Delete the last loan-related transaction"""
        # Find last loan transaction
        last_loan_index = -1
        for i in range(len(self.expenses_list) - 1, -1, -1):
            if self.expenses_list[i]['category'] in ['Loan', 'Loan Repayment']:
                last_loan_index = i
                break
        
        if last_loan_index == -1:
            messagebox.showinfo("No Loan", "No loan transactions to delete!")
            return
        
        last_loan = self.expenses_list[last_loan_index]
        
        confirm = messagebox.askyesno("Delete Loan Transaction", 
                                     f"Delete this loan transaction?\n\n"
                                     f"Type: {last_loan['type']}\n"
                                     f"Amount: ${last_loan['amount']:.2f}\n"
                                     f"Date: {last_loan['date']}\n\n"
                                     f"This will adjust your loan balance.")
        
        if confirm:
            # Adjust loan balance
            if last_loan['category'] == 'Loan':
                self.loan_balance -= last_loan['amount']
            else:  # Loan Repayment
                self.loan_balance += last_loan['amount']
            
            # Remove transaction
            self.expenses_list.pop(last_loan_index)
            
            # Re-index IDs
            for i, exp in enumerate(self.expenses_list):
                exp['id'] = i + 1
            
            # Update displays
            self.refresh_history_display()
            self.update_loan_display()
            self.save_data()
            
            self.status_label.config(text=f"💸 Deleted loan transaction", fg='orange')
            messagebox.showinfo("Deleted", "Loan transaction has been deleted.")
    
    # ========== RESET FUNCTIONS ==========
    
    def delete_last_expense(self):
        """Delete only the last regular expense"""
        # Find last non-loan expense
        last_expense_index = -1
        for i in range(len(self.expenses_list) - 1, -1, -1):
            if self.expenses_list[i]['category'] not in ['Loan', 'Loan Repayment']:
                last_expense_index = i
                break
        
        if last_expense_index == -1:
            messagebox.showinfo("Nothing to Delete", "No regular expenses to delete!")
            return
        
        last_expense = self.expenses_list[last_expense_index]
        
        confirm = messagebox.askyesno("Delete Last Expense", 
                                     f"Delete this expense?\n\n"
                                     f"Amount: ${last_expense['amount']:.2f}\n"
                                     f"Description: {last_expense['description']}\n"
                                     f"Category: {last_expense['category']}")
        
        if confirm:
            # Subtract from total
            self.total_accumulator -= last_expense['amount']
            
            # Remove transaction
            self.expenses_list.pop(last_expense_index)
            
            # Re-index IDs
            for i, exp in enumerate(self.expenses_list):
                exp['id'] = i + 1
            
            # Update displays
            self.refresh_history_display()
            self.update_all_displays()
            self.update_loan_visibility()
            self.save_data()
            
            self.status_label.config(text=f"🗑️ Deleted: {last_expense['description']} (-${last_expense['amount']:.2f})", fg='orange')
            messagebox.showinfo("Deleted", f"Expense deleted: ${last_expense['amount']:.2f}")
    
    def reset_expense_history(self):
        """Reset all regular expenses but keep loans"""
        regular_expenses = [e for e in self.expenses_list if e['category'] not in ['Loan', 'Loan Repayment']]
        
        if not regular_expenses:
            messagebox.showinfo("Nothing to Reset", "No regular expenses to reset!")
            return
        
        confirm = messagebox.askyesno("Reset Expense History", 
                                     f"Reset ALL regular expenses?\n\n"
                                     f"This will delete {len(regular_expenses)} transactions.\n"
                                     f"Total amount: ${sum(e['amount'] for e in regular_expenses):.2f}\n\n"
                                     f"Loan transactions will be preserved.\n\n"
                                     f"Are you sure?")
        
        if confirm:
            # Keep only loan transactions
            self.expenses_list = [e for e in self.expenses_list if e['category'] in ['Loan', 'Loan Repayment']]
            
            # Reset total accumulator
            self.total_accumulator = 0.0
            
            # Re-index IDs
            for i, exp in enumerate(self.expenses_list):
                exp['id'] = i + 1
            
            # Update displays
            self.refresh_history_display()
            self.update_all_displays()
            self.update_loan_visibility()
            self.save_data()
            
            self.status_label.config(text="⚠️ Expense history reset! Loans preserved.", fg='orange')
            messagebox.showinfo("Reset Complete", "All regular expenses have been deleted.")
    
    def reset_everything(self):
        """Complete reset of all data"""
        if not self.expenses_list and self.total_accumulator == 0 and self.loan_balance == 0:
            messagebox.showinfo("Nothing to Reset", "No data to reset!")
            return
        
        # Triple confirmation
        confirm1 = messagebox.askyesno("⚠️ DANGER ZONE ⚠️", 
                                      f"This will reset EVERYTHING:\n\n"
                                      f"• {len(self.expenses_list)} transactions\n"
                                      f"• Total spent: ${self.total_accumulator:.2f}\n"
                                      f"• Loan balance: ${self.loan_balance:.2f}\n"
                                      f"• Budget limit: ${self.budget_limit:.2f}\n\n"
                                      f"THIS CANNOT BE UNDONE!\n\n"
                                      f"Continue?",
                                      icon='warning')
        
        if confirm1:
            confirm2 = messagebox.askyesno("FINAL WARNING", 
                                          "Are you ABSOLUTELY sure?\n\nAll data will be permanently deleted!",
                                          icon='warning')
            
            if confirm2:
                # Reset all data
                self.total_accumulator = 0.0
                self.budget_limit = 5000.0
                self.expenses_list = []
                self.loan_balance = 0.0
                
                # Reset input fields
                self.budget_entry.delete(0, tk.END)
                self.budget_entry.insert(0, "5000")
                self.loan_entry.delete(0, tk.END)
                
                # Update displays
                self.refresh_history_display()
                self.update_all_displays()
                self.update_loan_display()
                self.save_data()
                
                self.status_label.config(text="🔥 ALL DATA RESET! 🔥", fg='red')
                messagebox.showinfo("Complete Reset", "All data has been reset to initial state.")
    
    # ========== CORE FUNCTIONS ==========
    
    def add_expense(self):
        """Add expense with budget checking"""
        # Validate amount
        amount_str = self.amount_entry.get().strip()
        
        if not amount_str:
            messagebox.showwarning("Input Error", "Please enter an expense amount!")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showwarning("Invalid Amount", "Expense must be greater than zero!")
                return
        except ValueError:
            messagebox.showerror("Invalid Data", "Please enter a valid number!")
            self.status_label.config(text="❌ Invalid amount!", fg='red')
            return
        
        # Validate description
        description = self.desc_entry.get().strip()
        if not description:
            messagebox.showwarning("Missing Description", "Please enter a description!")
            return
        
        # Validate category
        category = self.category_var.get()
        if category == 'Select Category' or not category:
            messagebox.showwarning("Missing Category", "Please select a category!")
            return
        
        # Validate date
        date = self.date_entry.get().strip()
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD format")
            return
        
        # Check if expense will exceed budget
        will_exceed = (self.total_accumulator + amount) > self.budget_limit
        
        if will_exceed and self.budget_limit > 0:
            over_amount = (self.total_accumulator + amount) - self.budget_limit
            response = messagebox.askyesno("Budget Alert!", 
                                          f"⚠️ This expense will exceed your budget!\n\n"
                                          f"Current: ${self.total_accumulator:.2f}\n"
                                          f"New expense: ${amount:.2f}\n"
                                          f"Budget: ${self.budget_limit:.2f}\n"
                                          f"Will exceed by: ${over_amount:.2f}\n\n"
                                          f"Add expense anyway?")
            
            if not response:
                return
        
        # Update total
        self.total_accumulator += amount
        
        # Create transaction
        transaction = {
            'id': len(self.expenses_list) + 1,
            'date': date,
            'description': description,
            'category': category,
            'amount': amount,
            'type': 'Expense'
        }
        
        self.expenses_list.append(transaction)
        
        # Update displays
        self.refresh_history_display()
        self.update_all_displays()
        self.update_loan_visibility()
        self.save_data()
        
        # Clear inputs
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.category_dropdown.set('Select Category')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        self.amount_entry.focus()
        
        self.status_label.config(text=f"✅ Added: ${amount:.2f} - {description}", fg='green')
        
        # Show warning if over budget
        if self.total_accumulator > self.budget_limit:
            messagebox.showwarning("Budget Exceeded!", 
                                  f"You have exceeded your budget!\n\n"
                                  f"Budget: ${self.budget_limit:.2f}\n"
                                  f"Total: ${self.total_accumulator:.2f}\n"
                                  f"Over by: ${self.total_accumulator - self.budget_limit:.2f}\n\n"
                                  f"Consider taking a loan from the Loan Management section.")
    
    def set_budget_limit(self):
        """Update budget limit"""
        try:
            new_limit = float(self.budget_entry.get())
            if new_limit <= 0:
                messagebox.showwarning("Invalid Budget", "Budget must be greater than zero!")
                return
            
            self.budget_limit = new_limit
            self.update_all_displays()
            self.update_loan_visibility()
            self.save_data()
            
            self.status_label.config(text=f"💰 Budget set to ${self.budget_limit:.2f}", fg='blue')
            messagebox.showinfo("Budget Updated", f"Budget limit set to ${self.budget_limit:.2f}")
            
        except ValueError:
            messagebox.showerror("Invalid Data", "Please enter a valid number!")
            self.status_label.config(text="❌ Invalid budget amount!", fg='red')
    
    # ========== DISPLAY METHODS ==========
    
    def refresh_history_display(self):
        """Refresh the transaction history table"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add all transactions
        for expense in self.expenses_list:
            # Set tag for color coding
            tag = ''
            if expense['category'] == 'Loan':
                tag = 'loan'
            elif expense['category'] == 'Loan Repayment':
                tag = 'repayment'
            
            self.history_tree.insert('', 'end', values=(
                expense['id'],
                expense['date'],
                expense['description'],
                expense['category'],
                f"${expense['amount']:.2f}",
                expense.get('type', 'Expense')
            ), tags=(tag,))
        
        # Configure colors
        self.history_tree.tag_configure('loan', background='#FFF3E0')
        self.history_tree.tag_configure('repayment', background='#E8F5E9')
        
        # Update count
        self.count_label.config(text=f"Transactions: {len(self.expenses_list)}")
    
    def update_all_displays(self):
        """Update all financial displays"""
        # Update total
        self.total_label.config(text=f"${self.total_accumulator:.2f}")
        
        # Update remaining budget
        remaining = self.budget_limit - self.total_accumulator
        if remaining >= 0:
            self.remaining_label.config(text=f"${remaining:.2f}", fg='green')
        else:
            self.remaining_label.config(text=f"${abs(remaining):.2f} OVER", fg='red')
        
        # Update progress bar
        if self.budget_limit > 0:
            usage = (self.total_accumulator / self.budget_limit) * 100
            usage = min(100, usage)
            self.progress_bar['value'] = usage
            self.progress_label.config(text=f"Budget Usage: {usage:.1f}%")
            
            if usage < 70:
                self.progress_label.config(fg='green')
            elif usage < 90:
                self.progress_label.config(fg='orange')
            else:
                self.progress_label.config(fg='red')
    
    def update_loan_display(self):
        """Update loan-related displays"""
        # Update loan balance label
        self.loan_balance_label.config(text=f"${self.loan_balance:.2f}")
        
        # Update over budget amount
        if self.total_accumulator > self.budget_limit:
            over_budget = self.total_accumulator - self.budget_limit
            self.over_budget_label.config(text=f"${over_budget:.2f}", fg='red')
        else:
            self.over_budget_label.config(text="$0.00", fg='green')
    
    def update_loan_visibility(self):
        """Show/hide loan management section"""
        if self.total_accumulator > self.budget_limit or self.loan_balance > 0:
            if not self.loan_frame.winfo_ismapped():
                self.loan_frame.pack(fill="x", pady=(0, 10))
            self.update_loan_display()
        else:
            if self.loan_frame.winfo_ismapped():
                self.loan_frame.pack_forget()
    
    # ========== DATA PERSISTENCE ==========
    
    def save_data(self):
        """Save all data to JSON file"""
        try:
            data = {
                'total_accumulator': self.total_accumulator,
                'budget_limit': self.budget_limit,
                'loan_balance': self.loan_balance,
                'expenses': self.expenses_list
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
                
        except Exception as e:
            print(f"Error saving: {e}")
    
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                self.total_accumulator = data.get('total_accumulator', 0.0)
                self.budget_limit = data.get('budget_limit', 5000.0)
                self.loan_balance = data.get('loan_balance', 0.0)
                self.expenses_list = data.get('expenses', [])
                
            except Exception as e:
                print(f"Error loading: {e}")
    
    def export_data(self):
        """Export data to text file"""
        if not self.expenses_list:
            messagebox.showinfo("No Data", "No data to export!")
            return
        
        filename = f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("EXPENSE TRACKER REPORT\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 70 + "\n\n")
                
                f.write(f"TOTAL SPENT: ${self.total_accumulator:.2f}\n")
                f.write(f"BUDGET LIMIT: ${self.budget_limit:.2f}\n")
                f.write(f"LOAN BALANCE: ${self.loan_balance:.2f}\n\n")
                
                f.write("-" * 70 + "\n")
                f.write("TRANSACTION HISTORY:\n")
                f.write("-" * 70 + "\n\n")
                
                for exp in self.expenses_list:
                    f.write(f"[{exp['id']}] {exp['date']}\n")
                    f.write(f"    {exp['description']} - {exp['category']}\n")
                    f.write(f"    Amount: ${exp['amount']:.2f}\n\n")
                
                f.write("=" * 70 + "\n")
                f.write("End of Report\n")
            
            messagebox.showinfo("Export Successful", f"Report saved to:\n{filename}")
            self.status_label.config(text=f"💾 Data exported", fg='blue')
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error: {str(e)}")

# ========== MAIN ==========

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()