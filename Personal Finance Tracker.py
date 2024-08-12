import tkinter as tk
from tkinter import ttk
import datetime
import json

# Global dictionary to store transactions
Transactions = {}

# Load transaction JSON file function
def load_transactions():
    try:
        with open ("Transactions.json","r") as file:
            Transaction = json.load(file)
            Transactions.update(Transaction)
    except FileNotFoundError:
            return {}

# Save transaction to JSON file function
def save_transaction():
    with open ("Transactions.json","w") as file:
            json.dump(Transactions, file, indent = 4)

# Add a new transaction function
def add_transaction():
    print ("\n--- Add Transactions ---")
    category = input("Enter the category for transaction : ")
    while True:
        try:
            amount = float(input("Enter the amount of transaction : "))
        except ValueError:
            print ("Invalid input!. Please try again..")
        else:
            break
    while True:
        transaction_type = input("Enter the transaction type(Income/Expense) : ").capitalize()
        if transaction_type in ("Income","Expense"):
            break
        else:
            print ("Invalid input!. Please enter Income or Expense.")
    transaction_date = input("Enter the transaction date (yyyy-mm-dd) : ")

    Transactions.setdefault(category, []).append({"amount": amount, "type": transaction_type, "date": transaction_date})
    print ("\n--- Transaction Added Successfully! ---")
    save_transaction()

# Bulk and transaction
def bulk_add_transactions():
    print ("\n--- Bulk Transactions ---")
    try:
        file_name = input("Enter the file name containing bulk transactions with extension (.txt/.json): ")
        with open(file_name, 'r') as file:
            bulk_transactions = {}
            for line in file:
                data = line.strip().split(" | ")
                if len(data) != 4:
                    print (f"Invalid transaction format : {line}")
                    continue

                amount = float(data[0])
                category = data[1]
                transaction_type = data[2]
                transaction_date = data[3]
                bulk_transactions.setdefault(category, []).append({"amount": amount, "type": transaction_type, "date": transaction_date})

        for category, transactions in bulk_transactions.items():
            print (f"\n{category:}")
            for transaction in transactions:
                print (f"| Amount : {transaction['amount']} | Type : {transaction['type']} | Date : {transaction['date']} |")

        for category,transactions in bulk_transactions.items():
            Transactions.setdefault(category,[]).extend(transactions)
        
        save_transaction()
        print ("\n--- Transaction read from file and saved successfully. ---")
    except FileNotFoundError:
        print (f"{file_name} File not found!. Please try again..")
    except Exception as e:
        print (f"An error occurred from the file : {e}")

# View all transaction function
def view_transaction():
    print ("\n --- Transaction History ---")
    if not Transactions:
        print ("No transactions to display.")
        return

    for detail, all_Transactions in Transactions.items():
        print (f"\n{detail}:")
        for Transaction in all_Transactions:
            print (f"| Amount : {Transaction['amount']} | Type : {Transaction['type']} | Date : {Transaction['date']} |")

# Update transaction function
def update_transaction():
    view_transaction()
    if not Transactions : 
        return
    print ("\n--- Updating Transaction ---")
    name_of_transaction = input("Enter the name of transaction to update : ")

    if name_of_transaction in Transactions:
        idx = int(input("Enter the index of transaction you want to edit : ")) - 1
        if 0 <= idx < len(Transactions[name_of_transaction]):
            transaction = Transactions[name_of_transaction][idx]

            while True:
                try:
                    amount = float(input("Enter the new amount of transaction : "))
                except ValueError:
                    print ("Invalid input!. Please try again..")
                else:
                    break
            while True:
                transaction_type = input("Enter the new transaction type(Income/Expense) : ").capitalize()
                if transaction_type in ("Income","Expense"):
                    break
                else:
                    print ("Invalid input!. Please enter Income or Expense.")
            transaction_date = input("Enter the new transaction date (yyyy-mm-dd) : ")

            Transactions[name_of_transaction][idx] = {"amount": amount, "type": transaction_type, "date": transaction_date}
            save_transaction()
            print ("\n--- Transaction Updated successfully ---")
        else:
            print ("Invaild index!. Please try again..")
    else:
        print ("Transaction name was not found!. Please try again..")

# Delete transaction function
def delete_transaction():
    print ("\n--- Delete transaction ---")                    
    view_transaction()
    if not Transactions: return

    name_of_transaction = input("Enter the name of transaction to update : ")
    if name_of_transaction in Transactions:
        if name_of_transaction not in Transactions:
            print ("Transaction name was not found!. Please try again..")
        else:
            del Transactions[name_of_transaction]
            save_transaction()
            print ("\n--- Transaction Deleted Successfully ---")

# Summery display function
def display_summery():
    total_income = 0
    total_expense = 0

    for transaction in Transactions.values():
        for tr in transaction:
            try:
                if tr['type'] == "Income":
                    total_income += tr['amount']
                elif tr['type'] == "Expense":
                    total_expense += tr['amount']
                else:
                    print ("Invaild category")

            except Exception as e:
                print (f"An error occurred : {e}")

    print ("\n--- Transaction Summery ---")
    print (f"Total Income : {total_income}")
    print (f"Total Expense : {total_expense}")
    total = total_income - total_expense
    print (f"Net Income : {total}")

class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.title_font = ('Arial', 16, 'bold')
        self.create_widgets()
        self.transactions = self.load_transactions("Transactions.json")
        self.display_transactions(self.transactions)
        self.reverse_sorting = {'Category': False, 'Amount': False, 'Date': False}

    def create_widgets(self):
        # Frame for table and scrollbar
        self.lable1 = ttk.Label(self.root, text='Personal Finance Tracker', font=('Arial', 16, 'bold'))
        self.lable1.pack(pady=10)

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)
        
        # Treeview for displaying transactions
        self.table = ttk.Treeview(self.frame, columns=('Category', 'Amount', 'Date'), show='headings')
        self.table.heading('Category', text='Category',command=lambda: self.sort_by_column('Category'))
        self.table.heading('Amount', text='Amount', command=lambda: self.sort_by_column('Amount'))
        self.table.heading('Date', text='Date', command=lambda: self.sort_by_column('Date'))
        self.table.pack(side='left', fill='both', expand=True)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.table.yview)
        scrollbar.pack(side='right', fill='y')
        self.table.configure(yscrollcommand=scrollbar.set)

        # Search bar and buttons
        self.searchVar = tk.StringVar()
        self.searchEntry = tk.Entry(self.root, textvariable=self.searchVar)
        self.searchEntry.pack(side='top', padx=10, pady=5)
        searchButton = ttk.Button(self.root, text='Search', command=self.search_transactions)
        searchButton.pack(side='top', padx=10, pady=5)
        

    def load_transactions(self, filename):
        try:
            with open (filename, 'r') as file:
                data = json.load(file)
                transactions = []
                for category, entries in data.items():
                    for entry in entries:
                        transactions.append({"Category": category, "Amount": entry["amount"], "Date": entry["date"]})
                return transactions
        except FileNotFoundError:
            print ("")
            return []
        
    def display_transactions(self, transactions):
        # Remove existing entries
        for item in self.table.get_children():
            self.table.delete(item)

        # Add transactions to the treeview
        for transaction in transactions:
            self.table.insert('','end',values=(transaction["Category"], transaction["Amount"], transaction["Date"]))
    
    def search_transactions(self):
        # Placeholder for search functionality
        keyword = self.searchVar.get()
        if keyword:
            results = [transaction for transaction in self.transactions if keyword.lower() in transaction["Category"].lower()]
            self.display_transactions(results)
        else:
            self.display_transactions(self.transactions)

    def sort_by_column(self, col):
        # Pleceholder for sorting functionality
        current_data = self.table.get_children('')
        column_values = [(self.table.set(item, col), item) for item in current_data]
        column_values.sort(reverse=self.reverse_sorting[col])
        
        # Rearrange items in sorted order
        for index, (val, item) in enumerate(column_values):
            self.table.move(item, '', index)
        
        # Switch sorting order for the column
        self.reverse_sorting[col] = not self.reverse_sorting[col]


# Main menu function
def main_menu():
    load_transactions()
    while True:
        print ("\n--- Personal Finance Tracker ---")
        print (". Add Transaction --> 1")
        print (". View Transactions --> 2")
        print (". View as GUI with Search and Sort --> 3 ")
        print (". Update Transactions --> 4")
        print (". Delete Transactions --> 5")
        print (". Display Summery --> 6")
        print (". Bulk Add Transaction --> 7")
        print (". Exit --> 8")
        while True:
            try:
                choice = input ("Enter your choice : ")
            except ValueError:
                print ("Invalid input!. Please try again ..")
            else:
                break

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transaction()
        elif choice == "3":
            root = tk.Tk()
            app = FinanceTrackerGUI(root)
            app.display_transactions(app.transactions)
            root.mainloop()
        elif choice == "4":
            update_transaction()
        elif choice == "5":
            delete_transaction()
        elif choice == "6":
            display_summery()
        elif choice == "7":
            bulk_add_transactions()
        elif choice == "8":
            print ("Exiting Program ...")
            break
        else:
            print ("Invaild choice!. Please try again ..")

# Run the program
if __name__ == "__main__":
    main_menu()
