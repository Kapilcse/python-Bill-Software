from tkinter import *
import random
from tkinter import messagebox
import os

root = Tk()
root.title("Billing Slip")
root.geometry("1280x720")

bg_color = "#4D0039"

# Variable initialization
c_name = StringVar()
c_phone = StringVar()
item = StringVar()
Rate = StringVar()
Quantity = StringVar()
bill_no = StringVar()
x = random.randint(1000, 9999)
bill_no.set(str(x))

global items
items = []

def welcome():
    header = (
        "\t Welcome"
        f'\n\nBill Number :\t\t{bill_no.get()}'
        f'\n Customer Name:\t\t{c_name.get()}'
        f"\n Phone Number:\t\t{c_phone.get()}"
        f"\n======================================\n"
        "Product\t\tQty\t\tPrice\n"
        f"\n======================================\n"
    )
    textarea.delete(1.0, END)
    textarea.insert(END, header)
    textarea.configure(font='arial 15 bold')

    # Add all items
    for item in items:
        textarea.insert(END, f'{item["name"]}\t\t{item["qty"]}\t\t{item["price"]:.2f}\n')
    update_total()

def additm():
    try:
        n = float(Rate.get())
        q = int(Quantity.get())
        
        if item.get() == "":
            messagebox.showerror("Error", "Please enter the item")
        elif q <= 0:
            messagebox.showerror("Error", "Quantity must be greater than 0")
        elif n <= 0:
            messagebox.showerror("Error", "Rate must be greater than 0")
        else:
            m = q * n
            items.append({"name": item.get(), "qty": q, "price": m})
            # Clear the fields after adding
            item.set('')
            Rate.set('')
            Quantity.set('')
    except ValueError:
        messagebox.showerror("Error", "Invalid rate or quantity value")

def update_total():
    total_amount = sum(item["price"] for item in items)
    lines = textarea.get(1.0, END).splitlines()
    for i, line in enumerate(lines):
        if "Total Paybill Amount:" in line:
            textarea.delete(f"{i+1}.0", f"{i+1}.end")
            textarea.insert(f"{i+1}.0", f"Total Paybill Amount:\t\t\t{total_amount:.2f}\n")
            return
    textarea.insert(END, f"\n======================================\n")
    textarea.insert(END, f"Total Paybill Amount:\t\t\t{total_amount:.2f}\n")
    textarea.insert(END, f"\n======================================\n")

def gbill():
    if c_name.get() == '' or c_phone.get() == '':
        messagebox.showerror("Customer Details", "Customer details are mandatory")
    elif not items:
        messagebox.showerror("Item Details", "No items have been added")
    else:
        welcome()
        savebill()

def savebill():
    if not os.path.exists("bills"):
        os.makedirs("bills")
    op = messagebox.askyesno('Save Bill', 'Do you want to save the bill?')
    if op:
        bill_details = textarea.get(1.0, END)
        try:
            with open(f"bills/{bill_no.get()}.txt", 'w') as f1:
                f1.write(bill_details)
            messagebox.showinfo('Saved', f'Bill no: {bill_no.get()} saved successfully')
        except IOError as e:
            messagebox.showerror('Error', f'Error saving bill: {e}')

def clear():
    c_name.set('')
    c_phone.set('')
    item.set('')
    Rate.set('')
    Quantity.set('')
    global items
    items = []
    welcome()

def exit_app():
    op = messagebox.askyesno("Exit", "Do you really want to exit?")
    if op:
        root.destroy()

def search_bill():
    bill_number = search_entry.get()
    if bill_number == "":
        messagebox.showerror("Error", "Please enter a bill number to search")
        return
    try:
        with open(f"bills/{bill_number}.txt", 'r') as file:
            bill_content = file.read()
            textarea.delete(1.0, END)
            textarea.insert(END, bill_content)
    except FileNotFoundError:
        messagebox.showerror("Error", "Bill not found")

# GUI setup
title = Label(root, text="Billing Software", bg=bg_color, fg='white', font=("Times new roman", 25, 'bold'), relief=GROOVE, bd=12)
title.pack(fill=X)

F1 = LabelFrame(root, text='Customer Details', font=('Times new roman', 18, 'bold'), relief=GROOVE, bd=10, bg=bg_color, fg='gold')
F1.place(x=0, y=80, relwidth=1)

c_name_label = Label(F1, text="Customer Name", font=('times new roman', 18, 'bold'), relief=GROOVE, bg=bg_color, fg='white')
c_name_label.grid(row=0, column=0, padx=10, pady=5)
c_name_txt = Entry(F1, width=15, font='arial 15 bold', relief=SUNKEN, textvariable=c_name)
c_name_txt.grid(row=0, column=1, padx=10, pady=5)

c_phone_label = Label(F1, text="Phone no.", font=('times new roman', 18, 'bold'), relief=GROOVE, bg=bg_color, fg='white')
c_phone_label.grid(row=0, column=2, padx=10, pady=5)
c_phone_txt = Entry(F1, width=15, font='arial 15 bold', relief=SUNKEN, textvariable=c_phone)
c_phone_txt.grid(row=0, column=3, padx=10, pady=5)

search_label = Label(F1, text="Search Bill No.", font=('times new roman', 18, 'bold'), bg=bg_color, fg='lightgreen')
search_label.grid(row=0, column=4, padx=10, pady=5)

search_entry = Entry(F1, width=15, font='arial 15 bold')
search_entry.grid(row=0, column=5, padx=10, pady=5)

search_btn = Button(F1, text='Search Bill', font='arial 15 bold', padx=5, pady=10, bg='Blue', width=13, command=search_bill)
search_btn.grid(row=0, column=6, padx=10, pady=5)

F2 = LabelFrame(root, text='Product Details', font=('Times new roman', 18, 'bold'), relief=GROOVE, bd=10, bg=bg_color, fg='gold')
F2.place(x=20, y=180, width=630, height=500)

itm_label = Label(F2, text='Product Name', font=('times new roman', 18, 'bold'), bg=bg_color, fg='lightgreen')
itm_label.grid(row=0, column=0, padx=30, pady=20)
itm_txt = Entry(F2, width=20, font='arial 15 bold', textvariable=item)
itm_txt.grid(row=0, column=1, padx=30, pady=20)

rate_label = Label(F2, text='Product Rate', font=('times new roman', 18, 'bold'), bg=bg_color, fg='lightgreen')
rate_label.grid(row=1, column=0, padx=30, pady=20)
rate_txt = Entry(F2, width=20, font='arial 15 bold', textvariable=Rate)
rate_txt.grid(row=1, column=1, padx=30, pady=20)

quantity_label = Label(F2, text='Product Quantity', font=('times new roman', 18, 'bold'), bg=bg_color, fg='lightgreen')
quantity_label.grid(row=2, column=0, padx=30, pady=20)
quantity_txt = Entry(F2, width=20, font='arial 15 bold', textvariable=Quantity)
quantity_txt.grid(row=2, column=1, padx=30, pady=20)

btn1 = Button(F2, text='Add Item', font='arial 15 bold', padx=5, pady=10, bg='Blue', width=15, command=additm)
btn1.grid(row=3, column=0, padx=10, pady=30)

btn2 = Button(F2, text='Generate Bill', font='arial 15 bold', padx=5, pady=10, bg='Blue', width=15, command=gbill)
btn2.grid(row=3, column=1, padx=10, pady=30)

btn3 = Button(F2, text='Clear', font='arial 15 bold', padx=5, pady=10, bg='Blue', width=15, command=clear)
btn3.grid(row=4, column=0, padx=10, pady=30)

btn4 = Button(F2, text='Exit', font='arial 15 bold', padx=5, pady=10, bg='Blue', width=15, command=exit_app)
btn4.grid(row=4, column=1, padx=10, pady=30)

F3 = Frame(root, relief=GROOVE, bd=10)
F3.place(x=700, y=180, width=500, height=500)

bill_title = Label(F3, text='Bill Area', font='arial 15 bold', relief=GROOVE, bd=17).pack(fill=X)
scroll_y = Scrollbar(F3, orient=VERTICAL)
textarea = Text(F3, yscrollcommand=scroll_y.set)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_y.config(command=textarea.yview)
textarea.pack()

welcome()  # Initialize the text area

root.mainloop()
