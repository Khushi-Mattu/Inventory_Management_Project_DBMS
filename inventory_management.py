from tkinter import *
import sqlite3
from typing import Sized

root = Tk()
root.title('Inventory Management System')
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

# Create a database or connect to one
conn = sqlite3.connect('inventory.db')

# Create a cursor
c = conn.cursor()
'''c.execute("""CREATE TABLE IF NOT EXISTS Employee(
    Employee_id varchar(20) primary key, first_name varchar(20), Last_name varchar(20),House_no int,
    streetnm varchar(20),city varchar(20),contact int(10))""")
c.execute("""CREATE TABLE IF NOT EXISTS Purchases(product_id varchar(20)primary key,product_name varchar(20),selling_rate int,
    purchase_rate int, quantity integer,batch_id varchar(20))""")
c.execute("""CREATE TABLE IF NOT EXISTS Customers(customer_id varchar(20) primary key,productid varchar(20),firstname text,lastname text,
house_num int, street_name varchar(20),city varchar(20),contact int)""")
c.execute("""CREATE TABLE IF NOT EXISTS Inventories(street_name varchar(30), city varchar(20), contact varchar(20), owner varchar(20))""")
'''


# Create edit function to update a record
def update_employee():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    record_id = delete_box.get()

    c.execute("""UPDATE Employee SET
        employee_id = :empid,
        first_name = :first,
        last_name = :last,
        house_no = :house_no,
        streetnm = :streetnm,
        city = :city,
        contact = :contact

        WHERE oid = :oid""",
        {
            'empid': empid_editor.get(),
            'first': f_name_editor.get(),
            'last': l_name_editor.get(),
            'house_no': house_no_editor.get(),
            'streetnm': street_name_editor.get(),
            'city': city_editor.get(),
            'contact': contact_editor.get(),
            'oid': record_id
        })


    conn.commit()
    conn.close()

    editor.destroy()
   
def edit_employee():
    global editor
    editor = Tk()
    editor.title('Update a record')
    editor.geometry("400x300")

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    record_id = delete_box.get()
    # Query the database
    c.execute("SELECT * FROM Employee WHERE oid=" + record_id)
    records = c.fetchall()
    
    # Create global variables for text box names
    global empid_editor
    global f_name_editor
    global l_name_editor
    global house_no_editor
    global street_name_editor
    global city_editor
    global contact_editor


    # Create Text Boxes
    empid_editor = Entry(editor, width=15)
    empid_editor.grid(row=0, column=1, padx=20, pady=(10,0))

    f_name_editor = Entry(editor, width=15)
    f_name_editor.grid(row=1, column=1, padx=20)

    l_name_editor = Entry(editor, width=15)
    l_name_editor.grid(row=2, column=1, padx=20)

    house_no_editor = Entry(editor, width=15)
    house_no_editor.grid(row=3, column=1, padx=20)

    street_name_editor = Entry(editor, width=15)
    street_name_editor.grid(row=4, column=1, padx=20)

    city_editor = Entry(editor, width=15)
    city_editor.grid(row=5, column=1, padx=20)

    contact_editor = Entry(editor, width=15)
    contact_editor.grid(row=6, column=1, padx=20)


    # Create Text Box Labels
    empid_label = Label(editor, text="Employee ID")
    empid_label.grid(row=0, column=0, pady=(10,0))

    f_name_label = Label(editor, text="First Name")
    f_name_label.grid(row=1, column=0)

    l_name_label = Label(editor, text="Last Name")
    l_name_label.grid(row=2, column=0)

    house_no_label = Label(editor, text="House Number")
    house_no_label.grid(row=3, column=0)

    street_name_label = Label(editor, text="Street Name")
    street_name_label.grid(row=4, column=0)

    city_label = Label(editor, text="City")
    city_label.grid(row=5, column=0)

    contact_label = Label(editor, text="Contact")
    contact_label.grid(row=6, column=0)

    # Loop through results
    for record in records:
        empid_editor.insert(0, record[0])
        f_name_editor.insert(0, record[1])
        l_name_editor.insert(0, record[2])
        house_no_editor.insert(0, record[3])
        street_name_editor.insert(0, record[4])
        city_editor.insert(0, record[5])
        contact_editor.insert(0, record[6])

    # Create an save button to save edited records
    edit_btn = Button(editor, text="Save Record", command=update_employee)
    edit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10)


# Create function to delete records
def delete_employee():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Delete a record
    c.execute("DELETE FROM Employee WHERE oid= " + delete_box.get())
    delete_box.delete(0, END)

    conn.commit()
    conn.close()


# Create submit function for database
def submit_employee():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Insert into Table
    c.execute("INSERT INTO Employee VALUES (:empid, :f_name, :l_name, :houseno, :streetnm, :city, :contact)", 
            {
                'empid' : empid.get(),
                'f_name': f_name.get(),
                'l_name': l_name.get(),
                'houseno': houseno.get(),
                'streetnm': streetnm.get(),
                'city': city.get(),
                'contact': contact.get()
            }
    )


    conn.commit()
    conn.close()


    # Clear the text boxes
    empid.delete(0, END)
    f_name.delete(0, END)
    l_name.delete(0, END)
    houseno.delete(0, END)
    streetnm.delete(0, END)
    city.delete(0, END)
    contact.delete(0, END)



# Create query function
def query_employee():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Query the database
    c.execute("SELECT *, oid FROM Employee")
    records = c.fetchall()
    #print(records)

    # Loop through results
    print_records = ''
    if records==[]:
        print_records+="Empty Table!"
    else:
        for record in records:
            print_records += str(record[0]) + " " + str(record[1]) +  " " +  str(record[2]) + " " +  str(record[3]) + " " +  str(record[4]) + " " +  str(record[5]) + " " +  str(record[6]) + " " + str(record[7]) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=15, column=0,columnspan=2)
    conn.commit()
    conn.close()


# Create Text Boxes
empid = Entry(root, width=15)
empid.grid(row=1, column=1, padx=20, pady=(10,0))

f_name = Entry(root, width=15)
f_name.grid(row=2, column=1, padx=20)

l_name = Entry(root, width=15)
l_name.grid(row=3, column=1, padx=20)

houseno = Entry(root, width=15)
houseno.grid(row=4, column=1, padx=20)

streetnm = Entry(root, width=15)
streetnm.grid(row=5, column=1, padx=20)

city = Entry(root, width=15)
city.grid(row=6, column=1, padx=20)

contact = Entry(root, width=15)
contact.grid(row=7, column=1, padx=20)

delete_box = Entry(root, width=15)
delete_box.grid(row=12, column=1, pady=5)

# Create Text Box Labels
employee_label = Label(root, text="Employee")
employee_label.grid(row=0, column=1, pady=(10,0))

empid_label = Label(root, text="Employee ID")
empid_label.grid(row=1, column=0)

f_name_label = Label(root, text="First Name")
f_name_label.grid(row=2, column=0)

l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=3, column=0)

houseno_label = Label(root, text="House number")
houseno_label.grid(row=4, column=0)

streetnm_label = Label(root, text="Street name")
streetnm_label.grid(row=5, column=0)

city_label = Label(root, text="City")
city_label.grid(row=6, column=0)

contact_label = Label(root, text="Contact")
contact_label.grid(row=7, column=0)

delete_box_label = Label(root, text="Select ID")
delete_box_label.grid(row=12, column=0, pady=5)



# Create submit button
submit_btn_e = Button(root, text="Add Record", command=submit_employee)
submit_btn_e.grid(row=9, column=0, columnspan=2, pady=10, padx=10)

# Create a Query button
query_btn_e = Button(root, text="Show Records", command=query_employee)
query_btn_e.grid(row=10, column=0, columnspan=2, pady=10, padx=10)

# Create a Delete button
delete_btn_e = Button(root, text="Delete Record", command=delete_employee)
delete_btn_e.grid(row=13, column=0, columnspan=2, pady=10, padx=10)

# Create an update button
edit_btn_e = Button(root, text="Edit Record", command=edit_employee)
edit_btn_e.grid(row=14, column=0, columnspan=2, pady=10, padx=10)

##############################################################################
# Create edit function to update a record
def update_Purchases():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    record_id = delet_box.get()

    c.execute("""UPDATE Purchases SET
        product_id = :pid,
        product_name = :pname,
        selling_rate = :srate,
        purchase_rate = :prate,
        quantity = :qty,
        batch_id = :bid
        

        WHERE oid = :oid""",
        {
            'pid': pid_editor1.get(),
            'pname': pname_editor1.get(),
            'srate': srate_editor1.get(),
            'prate': prate_editor1.get(),
            'qty': qty_editor1.get(),
            'bid': bid_editor1.get(),

            'oid': record_id
        })

    conn.commit()
    conn.close()

    editor1.destroy()

def edit_purchases():
    global editor1
    editor1 = Tk()
    editor1.title('Update a record')
    editor1.geometry("400x300")

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    record_id = delet_box.get()
    # Query the database
    c.execute("SELECT * FROM Purchases WHERE oid=" + record_id)
    records = c.fetchall()
    
    # Create global variables for text box names
    global pid_editor1
    global pname_editor1
    global srate_editor1
    global prate_editor1
    global qty_editor1
    global bid_editor1


    # Create Text Boxes
    pid_editor1 = Entry(editor1, width=15)
    pid_editor1.grid(row=0, column=1, padx=20, pady=(10,0))

    pname_editor1 = Entry(editor1, width=15)
    pname_editor1.grid(row=1, column=1, padx=20)

    srate_editor1 = Entry(editor1, width=15)
    srate_editor1.grid(row=2, column=1, padx=20)

    prate_editor1 = Entry(editor1, width=15)
    prate_editor1.grid(row=3, column=1, padx=20)

    qty_editor1 = Entry(editor1, width=15)
    qty_editor1.grid(row=4, column=1, padx=20)

    bid_editor1 = Entry(editor1, width=15)
    bid_editor1.grid(row=5, column=1, padx=20)


    # Create Text Box Labels
    pid_label = Label(editor1, text="Product ID")
    pid_label.grid(row=0, column=0, pady=(10,0))

    pname_label = Label(editor1, text="Product Name")
    pname_label.grid(row=1, column=0)

    srate_label = Label(editor1, text="Selling rate")
    srate_label.grid(row=2, column=0)

    prate_label = Label(editor1, text="Purchase rate")
    prate_label.grid(row=3, column=0)

    qty_label = Label(editor1, text="Quantity")
    qty_label.grid(row=4, column=0)

    bid_label = Label(editor1, text="Batch ID")
    bid_label.grid(row=5, column=0)

    # Loop through results
    for record in records:
        pid_editor1.insert(0, record[0])
        pname_editor1.insert(0, record[1])
        srate_editor1.insert(0, record[2])
        prate_editor1.insert(0, record[3])
        qty_editor1.insert(0, record[4])
        bid_editor1.insert(0, record[5])


    # Create an save button to save edited records
    edit_bt = Button(editor1, text="Save Record", command=update_Purchases)
    edit_bt.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

# Create function to delete records
def delete_purchases():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Delete a record
    c.execute("DELETE FROM Purchases WHERE oid= " + delet_box.get())
    delet_box.delete(0, END)

    conn.commit()
    conn.close()

# Create submit function for database
def submit_purchases():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Insert into Table
    c.execute("INSERT INTO Purchases VALUES (:pid, :pname, :srate, :prate, :qty, :bid)", 
            {
                'pid' : pid.get(),
                'pname': pname.get(),
                'srate': srate.get(),
                'prate': prate.get(),
                'qty': qty.get(),
                'bid': bid.get(),
            }
    )


    conn.commit()
    conn.close()


    # Clear the text boxes
    pid.delete(0, END)
    pname.delete(0, END)
    srate.delete(0, END)
    prate.delete(0, END)
    qty.delete(0, END)
    bid.delete(0, END)


# Create query function
def query_purchases():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Query the database
    c.execute("SELECT *, oid FROM Purchases")
    records = c.fetchall()
    #print(records)

    # Loop through results
    print_records = ''
    if records==[]:
        print_records+="Empty Table!"
    else:
        for record in records:
            print_records += str(record[0]) + " " + str(record[1]) +  " " +  str(record[2]) + " " +  str(record[3]) + " " +  str(record[4]) + " " +  str(record[5]) + " " +  str(record[6])  + "\n"


    query_label1 = Label(root, text=print_records)
    query_label1.grid(row=15, column=2,columnspan=2)
    conn.commit()
    conn.close()


# Create Text Boxes
pid = Entry(root, width=15)
pid.grid(row=1, column=3, padx=20, pady=(10,0))

pname = Entry(root, width=15)
pname.grid(row=2, column=3, padx=20)

srate = Entry(root, width=15)
srate.grid(row=3, column=3, padx=20)

prate = Entry(root, width=15)
prate.grid(row=4, column=3, padx=20)

qty = Entry(root, width=15)
qty.grid(row=5, column=3, padx=20)

bid = Entry(root, width=15)
bid.grid(row=6, column=3, padx=20)

delet_box = Entry(root, width=15)
delet_box.grid(row=12, column=3, pady=5)

# Create Text Box Labels
purchases_label = Label(root, text="Purchases")
purchases_label.grid(row=0, column=3, pady=(10,0))

pid_label = Label(root, text="Product ID")
pid_label.grid(row=1, column=2)

pname_label = Label(root, text="Product Name")
pname_label.grid(row=2, column=2)

srate_label = Label(root, text="Selling rate")
srate_label.grid(row=3, column=2)

prate_label = Label(root, text="Purchase rate")
prate_label.grid(row=4, column=2)

qty_label = Label(root, text="Quantity")
qty_label.grid(row=5, column=2)

bid_label = Label(root, text="Batch ID")
bid_label.grid(row=6, column=2)

delet_box_label = Label(root, text="Select ID")
delet_box_label.grid(row=12, column=2, pady=5)


# Create submit button
submit_btn_p = Button(root, text="Add Record", command=submit_purchases)
submit_btn_p.grid(row=9, column=2, columnspan=2, pady=10, padx=10)

# Create a Query button
query_btn_p = Button(root, text="Show Records", command=query_purchases)
query_btn_p.grid(row=10, column=2, columnspan=2, pady=10, padx=10)

# Create a Delete button
delete_btn_p = Button(root, text="Delete Record", command=delete_purchases)
delete_btn_p.grid(row=13, column=2, columnspan=2, pady=10, padx=10)

# Create an update button
edit_btn_p = Button(root, text="Edit Record", command=edit_purchases)
edit_btn_p.grid(row=14, column=2, columnspan=2, pady=10, padx=10)

################################################################################

# Create edit function to update a record
def update_customers():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    record_id = dele_box.get()

    c.execute("""UPDATE customers SET
        customer_id = :cid,
        productid = :pid,
        firstname = :first,
        lastname = :last,
        house_num = :house_no,
        street_name = :street_name,
        city = :city,
        contact = :contact

        WHERE oid = :oid""",
        {
            'cid': cid_editor2.get(),
            'pid': pid_editor2.get(),
            'first': f_name_editor2.get(),
            'last': l_name_editor2.get(),
            'house_no': house_no_editor2.get(),
            'street_name': street_name_editor2.get(),
            'city': city_editor2.get(),
            'contact': contact_editor2.get(),

            'oid': record_id
        })


    conn.commit()
    conn.close()

    editor2.destroy()


def edit_customers():
    global editor2
    editor2 = Tk()
    editor2.title('Update a record')
    editor2.geometry("400x300")

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    record_id = dele_box.get()
    # Query the database
    c.execute("SELECT * FROM customers WHERE oid=" + record_id)
    records = c.fetchall()
    
    # Create global variables for text box names
    global cid_editor2
    global pid_editor2
    global f_name_editor2
    global l_name_editor2
    global house_no_editor2
    global street_name_editor2
    global city_editor2
    global contact_editor2


    # Create Text Boxes
    cid_editor2 = Entry(editor2, width=15)
    cid_editor2.grid(row=0, column=1, padx=20, pady=(10,0))

    pid_editor2 = Entry(editor2, width=15)
    pid_editor2.grid(row=1, column=1, padx=20)

    f_name_editor2 = Entry(editor2, width=15)
    f_name_editor2.grid(row=2, column=1, padx=20)

    l_name_editor2 = Entry(editor2, width=15)
    l_name_editor2.grid(row=3, column=1, padx=20)

    house_no_editor2 = Entry(editor2, width=15)
    house_no_editor2.grid(row=4, column=1, padx=20)

    street_name_editor2 = Entry(editor2, width=15)
    street_name_editor2.grid(row=5, column=1, padx=20)

    city_editor2 = Entry(editor2, width=15)
    city_editor2.grid(row=6, column=1, padx=20)

    contact_editor2 = Entry(editor2, width=15)
    contact_editor2.grid(row=7, column=1, padx=20)


    # Create Text Box Labels
    cid_label = Label(editor2, text="Customer ID")
    cid_label.grid(row=0, column=0, pady=(10,0))

    cpid_label = Label(editor2, text="Product ID")
    cpid_label.grid(row=1, column=0)

    fname_label = Label(editor2, text="First Name")
    fname_label.grid(row=2, column=0)

    lname_label = Label(editor2, text="Last Name")
    lname_label.grid(row=3, column=0)

    house_no2_label = Label(editor2, text="House Number")
    house_no2_label.grid(row=4, column=0)

    street_name2_label = Label(editor2, text="Street Name")
    street_name2_label.grid(row=5, column=0)

    city2_label = Label(editor2, text="City")
    city2_label.grid(row=6, column=0)

    contact2_label = Label(editor2, text="Contact")
    contact2_label.grid(row=7, column=0)

    # Loop through results
    for record in records:
        cid_editor2.insert(0, record[0])
        pid_editor2.insert(0, record[1])
        f_name_editor2.insert(0, record[2])
        l_name_editor2.insert(0, record[3])
        house_no_editor2.insert(0, record[4])
        street_name_editor2.insert(0, record[5])
        city_editor2.insert(0, record[6])
        contact_editor2.insert(0, record[7])

    # Create an save button to save edited records
    edit_b = Button(editor2, text="Save Record", command=update_customers)
    edit_b.grid(row=9, column=0, columnspan=2, pady=10, padx=10)

# Create function to delete records
def delete_customers():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Delete a record
    c.execute("DELETE FROM customers WHERE oid= " + dele_box.get())
    dele_box.delete(0, END)

    conn.commit()
    conn.close()


# Create submit function for database
def submit_customers():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Insert into Table
    c.execute("INSERT INTO customers VALUES (:cid, :pid, :f_name, :l_name, :houseno, :streetnm, :city, :contact)", 
            {
                'cid' : cid.get(),
                'pid' : cpid.get(),
                'f_name': fname.get(),
                'l_name': lname.get(),
                'houseno': houseno2.get(),
                'streetnm': streetnm2.get(),
                'city': city2.get(),
                'contact': contact2.get()
            }
    )
    conn.commit()
    conn.close()


    # Clear the text boxes
    cid.delete(0, END)
    cpid.delete(0, END)
    fname.delete(0, END)
    lname.delete(0, END)
    houseno2.delete(0, END)
    streetnm2.delete(0, END)
    city2.delete(0, END)
    contact2.delete(0, END)



# Create query function
def query_customers():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Query the database
    c.execute("SELECT *, oid FROM customers")
    records = c.fetchall()
    #print(records)
    
    # Loop through results
    print_records = ''
    if records==[]:
        print_records+="Empty Table!"
    else:
        for record in records:
            print_records += str(record[0]) + " " + str(record[1]) +  " " +  str(record[2]) + " " +  str(record[3]) + " " +  str(record[4]) + " " +  str(record[5]) + " " +  str(record[6]) + " " + str(record[7]) + " " + str(record[8]) + "\n"
    
    query_label2 = Label(root, text=print_records)
    query_label2.grid(row=15, column=4,columnspan=2)
    conn.commit()
    conn.close()


# Create Text Boxes
cid = Entry(root, width=15)
cid.grid(row=1, column=5, padx=20, pady=(10,0))

cpid = Entry(root, width=15)
cpid.grid(row=2, column=5, padx=20)

fname = Entry(root, width=15)
fname.grid(row=3, column=5, padx=20)

lname = Entry(root, width=15)
lname.grid(row=4, column=5, padx=20)

houseno2 = Entry(root, width=15)
houseno2.grid(row=5, column=5, padx=20)

streetnm2 = Entry(root, width=15)
streetnm2.grid(row=6, column=5, padx=20)

city2 = Entry(root, width=15)
city2.grid(row=7, column=5, padx=20)

contact2 = Entry(root, width=15)
contact2.grid(row=8, column=5, padx=20)

dele_box = Entry(root, width=15)
dele_box.grid(row=12, column=5, pady=5)

# Create Text Box Labels
customers_label = Label(root, text="Customers")
customers_label.grid(row=0, column=5, pady=(10,0))

cid_label = Label(root, text="Customer ID")
cid_label.grid(row=1, column=4)

cpid_label = Label(root, text="Product ID")
cpid_label.grid(row=2, column=4)

fname_label = Label(root, text="First Name")
fname_label.grid(row=3, column=4)

lname_label = Label(root, text="Last Name")
lname_label.grid(row=4, column=4)

houseno2_label = Label(root, text="House number")
houseno2_label.grid(row=5, column=4)

streetnm2_label = Label(root, text="Street name")
streetnm2_label.grid(row=6, column=4)

city2_label = Label(root, text="City")
city2_label.grid(row=7, column=4)

contact2_label = Label(root, text="Contact")
contact2_label.grid(row=8, column=4)

dele_box_label = Label(root, text="Select ID")
dele_box_label.grid(row=12, column=4, pady=5)


# Create submit button
submit_btn_c = Button(root, text="Add Record", command=submit_customers)
submit_btn_c.grid(row=9, column=4, columnspan=2, pady=10, padx=10)

# Create a Query button
query_btn_c = Button(root, text="Show Records", command=query_customers)
query_btn_c.grid(row=10, column=4, columnspan=2, pady=10, padx=10)

# Create a Delete button
delete_btn_c = Button(root, text="Delete Record", command=delete_customers)
delete_btn_c.grid(row=13, column=4, columnspan=2, pady=10, padx=10)

# Create an update button
edit_btn_c = Button(root, text="Edit Record", command=edit_customers)
edit_btn_c.grid(row=14, column=4, columnspan=2, pady=10, padx=10)

##############################################################################
# Create edit function to update a record
def update_inventories():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    record_id = del_box.get()

    c.execute("""UPDATE inventories SET
        street_name = :street_name,
        city = :city,
        contact = :contact,
        owner = :owner

        WHERE oid = :oid""", 
        {
            'street_name': street_name_editor3.get(),
            'city': city_editor3.get(),
            'contact': contact_editor3.get(),
            'owner': owner_editor.get(),

            'oid': record_id
        })


    conn.commit()
    conn.close()

    editor3.destroy()

def edit_inventories():
    global editor3
    editor3 = Tk()
    editor3.title('Update a record')
    editor3.geometry("400x300")

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    record_id = del_box.get()
    # Query the database
    c.execute("SELECT * FROM inventories WHERE oid=" + record_id)
    records = c.fetchall()
    
    # Create global variables for text box names
    global street_name_editor3
    global city_editor3
    global contact_editor3
    global owner_editor


    # Create Text Boxes

    street_name_editor3 = Entry(editor3, width=15)
    street_name_editor3.grid(row=0, column=1, padx=20, pady=(10,0))

    city_editor3 = Entry(editor3, width=15)
    city_editor3.grid(row=1, column=1, padx=20)

    contact_editor3 = Entry(editor3, width=15)
    contact_editor3.grid(row=2, column=1, padx=20)

    owner_editor = Entry(editor3, width=15)
    owner_editor.grid(row=3, column=1, padx=20)

    # Create Text Box Labels
    street_name3_label = Label(editor3, text="Street Name")
    street_name3_label.grid(row=0, column=0, pady=(10,0))

    city3_label = Label(editor3, text="City")
    city3_label.grid(row=1, column=0) 

    contact3_label = Label(editor3, text="Contact")
    contact3_label.grid(row=2, column=0)

    owner_label = Label(editor3, text="Owner")
    owner_label.grid(row=3, column=0)
    # Loop through results
    for record in records:
        street_name_editor3.insert(0, record[0])
        city_editor3.insert(0, record[1])
        contact_editor3.insert(0, record[2])
        owner_editor.insert(0, record[3])
    # Create an save button to save edited records
    edit_butt = Button(editor3, text="Save Record", command=update_inventories)
    edit_butt.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

# Create function to delete records
def delete_inventories():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Delete a record
    c.execute("DELETE FROM inventories WHERE oid= " + del_box.get())
    del_box.delete(0, END)

    conn.commit()
    conn.close()


# Create submit function for database
def submit_inventories():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Insert into Table
    c.execute("INSERT INTO inventories VALUES (:streetnm, :city, :contact, :owner)", 
            {
                'streetnm': streetnm3.get(),
                'city': city3.get(),
                'contact': contact3.get(),
                'owner': owner.get()
            }
    )


    conn.commit()
    conn.close()


    # Clear the text boxes
    streetnm3.delete(0, END)
    city3.delete(0, END)
    contact3.delete(0, END)
    owner.delete(0, END)


# Create query function
def query_inventories():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Query the database
    c.execute("SELECT *, oid FROM inventories")
    records = c.fetchall()
    #print(records)

    # Loop through results
    print_records = ''
    if records==[]:
        print_records+="Empty Table!"
    else:
        for record in records:
            print_records += str(record[0]) + " " + str(record[1]) +  " " +  str(record[2]) + " " +  str(record[3]) + " " +  str(record[4]) + "\n"


    query_label3 = Label(root, text=print_records)
    query_label3.grid(row=15, column=6,columnspan=2)
    conn.commit()
    conn.close()


# Create Text Boxes

streetnm3 = Entry(root, width=15)
streetnm3.grid(row=1, column=7, padx=20, pady=(10,0))

city3 = Entry(root, width=15)
city3.grid(row=2, column=7, padx=20)

contact3 = Entry(root, width=15)
contact3.grid(row=3, column=7, padx=20)

owner = Entry(root, width=15)
owner.grid(row=4, column=7, padx=20)

del_box = Entry(root, width=15)
del_box.grid(row=12, column=7, pady=5)

# Create Text Box Labels
inventories_label = Label(root, text="Inventories")
inventories_label.grid(row=0, column=7, pady=(10,0))

streetnm3_label = Label(root, text="Street name")
streetnm3_label.grid(row=1, column=6)

city3_label = Label(root, text="City")
city3_label.grid(row=2, column=6)

contact3_label = Label(root, text="Contact")
contact3_label.grid(row=3, column=6)

owner_label = Label(root, text="Owner")
owner_label.grid(row=4, column=6)

del_box_label = Label(root, text="Select ID")
del_box_label.grid(row=12, column=6, pady=5)

# Create submit button
submit_btn_i = Button(root, text="Add Record", command=submit_inventories)
submit_btn_i.grid(row=9, column=6, columnspan=2, pady=10, padx=10)

# Create a Query button
query_btn_i = Button(root, text="Show Records", command=query_inventories)
query_btn_i.grid(row=10, column=6, columnspan=2, pady=10, padx=10)

# Create a Delete button
delete_btn_i = Button(root, text="Delete Record", command=delete_inventories)
delete_btn_i.grid(row=13, column=6, columnspan=2, pady=10, padx=10)

# Create an update button
edit_btn_i = Button(root, text="Edit Record", command=edit_inventories)
edit_btn_i.grid(row=14, column=6, columnspan=2, pady=10, padx=10)



# Commit changes
conn.commit()

# Close connection
conn.close()


root.mainloop()