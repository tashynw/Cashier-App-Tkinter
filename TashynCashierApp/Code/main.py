from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
from tkinter import ttk
from ttkbootstrap import Style
from tkinter.font import Font
import sqlite3
import tkinter as tk

root=Tk()
style=Style("flatly")
root.title('Tashyn Cashier App')
root.iconbitmap('shop.ico') #FIND ICON
root.geometry('1920x1080')
root.pack_propagate(0)

#create database or connect
conn=sqlite3.connect('items_book.db')


#create cursor
c=conn.cursor()

#create table
'''
c.execute (""" CREATE TABLE addresses (
	item_type text,
	item_name text,
	item_price real
	)
	""")
'''


#Defining Font
regFont=Font(
	family="Helvetica",
	size=11,
	weight="bold"
	)
regFont2=Font(
	family="Helvetica",
	size=9,
	weight="bold"
	)




#<FUNCTIONS>

#functions relevant to database management

#function to add records to database
def submit():
	
	
	if item_type.get().isspace() or len(item_type.get())==0 or item_name.get().isspace() or len(item_name.get())==0 or item_price.get().isspace() or len(item_price.get())==0:
		#checks if the string is only a space or it is empty
		emptydata()

	else:
		#create database or connect
		conn=sqlite3.connect('items_book.db')
		#create cursor
		c=conn.cursor()

		c.execute("SELECT *, oid FROM addresses")
		records=c.fetchall()

		namelst=[x[1] for x in records]

		if item_name.get() in namelst:
			#check for duplicate item names
			duplicate_entry()

		else:
			if len(item_name.get()) not in range(4,16):
				#Controls the name of the size to keep buttons neat on the main screen (soon to be updated)
				invalid_namesize()

			else:
				#simple function to check the boolean of a variable relative to being a float
				def isfloat(num):
				    try:
				    	float(num)
				    	return True
				    except ValueError:
				        return False
				if isfloat(item_price.get()) or item_price.get().isnumeric():
					c.execute("INSERT INTO addresses VALUES (:item_type,:item_name,:item_price)",
						{
							'item_type': item_type.get(),
							'item_name': item_name.get(),
							'item_price': item_price.get(),
					
						})
					
					#clear screen

					item_type.delete(0,END)
					item_name.delete(0,END)
					item_price.delete(0,END)
				
				else:

					#check that a float of integer is entered
					wrongprice_type()

		#commit changes
		conn.commit()

		#close connection
		conn.close()


#function to output data in the database to query
def query():
	#create database or connect
	conn=sqlite3.connect('items_book.db')
	#create cursor
	c=conn.cursor()
	
	#Query database
	c.execute("SELECT *, oid FROM addresses")
	records=c.fetchall()

	global typereturn
	global namereturn
	global pricereturn
	global oidreturn

	#Accessor functions for the db ADT (list of tuples)
	def typereturn(tup):
		return tup[0]

	def namereturn(tup):
		return tup[1]

	def pricereturn(tup):
		return tup[2]

	def oidreturn(tup):
		return tup[3]


	
	#Loop through results
	print_records=""
	for i in records:
		print_records+= str(oidreturn(i)) + "  " + str(typereturn(i)) +"  "+str(namereturn(i))+"  "+str(pricereturn(i)) + "  " + "\n\n"

	query_label=ttk.Label(secondfileframe,text=print_records,font=regFont,style="primary.TLabel")
	query_label.grid(row=15,column=0,columnspan=2)
			



	#commit changes
	conn.commit()
	#close connection
	conn.close()


	#clear screen
	item_type.delete(0,END)
	item_name.delete(0,END)
	item_price.delete(0,END)


#function to delete a record from the database
def delete_item_func():
	#create database or connect
	conn=sqlite3.connect('items_book.db',isolation_level = None)
	#create cursor
	c=conn.cursor()

	c.execute("SELECT *, oid FROM addresses")
	records=c.fetchall()

	
	if not deletebox.get().isnumeric():
		#check if a number is inputted
		integer_test()

	else:

		if int(deletebox.get()) > len(records) + 1 or int(deletebox.get()) < 0:
		#check if the number inputted to edit o delete is valid
			invalid_int()

		else:
			#Delete a record
			c.execute("DELETE from addresses WHERE oid= " + deletebox.get())


			#VACUUM database to remove empty spaces after bulk deleting
			conn.execute("VACUUM")

			#commit changes
			conn.commit()

			#close connection
			conn.close()

			#clear screen
			deletebox.delete(0,END)
		



#functions to edit and update the database

def update():

	if item_type_editor.get().isspace() or len(item_type_editor.get())==0 or item_name_editor.get().isspace() or len(item_name_editor.get())==0 or item_price_editor.get().isspace() or len(item_price_editor.get())==0:
		#checks if the string is only a space or it is empty
		emptydata()

	else:
		#create database or connect
		conn=sqlite3.connect('items_book.db')
		#create cursor
		c=conn.cursor()

		c.execute("SELECT *, oid FROM addresses")
		records=c.fetchall()
	

		namelst=[x[1] for x in records]
		namelst.remove(original_name)

		if item_name_editor.get() in namelst and item_name_editor != original_name:
			#check for duplicate item names
			duplicate_entry()

		else:
			def isfloat(num):
			    try:
			    	float(num)
			    	return True
			    except ValueError:
			        return False

			if isfloat(item_price_editor.get()) or item_price_editor.get().isnumeric():
				c.execute("""UPDATE addresses SET
								item_type = :itemtype,
								item_name = :itemname,
								item_price = :itemprice

								WHERE oid= :oid""",
								{
								'itemtype': item_type_editor.get(),
								'itemname': item_name_editor.get(),
								'itemprice': item_price_editor.get(),
								

								'oid': deletebox.get()



								})
				
			else:
	
				#check that a float or integer is entered
				wrongprice_type()
	

		#commit changes
		conn.commit()
		#close connection
		conn.close()
		#clear screen
		deletebox.delete(0,END)
		editor.destroy()


#Opens the editor window for a item
def edit():
	global editor
	#create database or connect
	conn=sqlite3.connect('items_book.db')
	#create cursor
	c=conn.cursor()

	record_id=deletebox.get()

	c.execute("SELECT *, oid FROM addresses")
	records=c.fetchall()

	if not deletebox.get().isnumeric():
		#check if a number is inputted
		integer_test()

	else:

		if int(deletebox.get()) > len(records) + 1 or int(deletebox.get()) < 0:
		#check if the number inputted to edit o delete is correct
			invalid_int()


		else:

	
			#Query database
			c.execute("SELECT * FROM addresses WHERE oid = " + record_id)
			records=c.fetchall()

			global original_name
			original_name=records[0][1]
			
			#Making new window

			editor=Toplevel(root)
			editor.title('Database Editor Window')
			editor.iconbitmap('shop.ico')
			editor.geometry("400x400")
			

			#global variables to use in other func
			global item_type_editor
			global item_name_editor
			global item_price_editor

			#ADT functions relevant to the database
			def typereturn(i):
				return i[0]

			def namereturn(i):
				return i[1]

			def pricereturn(i):
				return i[2]
			
			#create text boxes

			item_type_editor=ttk.Entry(editor,width=30,style="success.TEntry",state="focused")
			item_type_editor.grid(row=0,column=1,padx=20)

			item_name_editor=ttk.Entry(editor,width=30,style="success.TEntry",state="focused")
			item_name_editor.grid(row=1,column=1,padx=20)

			item_price_editor=ttk.Entry(editor,width=30,style="success.TEntry",state="focused")
			item_price_editor.grid(row=2,column=1,padx=20)


			#create text box labels
			item_type_label=ttk.Label(editor,text='Item Type',font=regFont,style="primary.TLabel")
			item_type_label.grid(row=0,column=0)

			item_name_label=ttk.Label(editor,text='Item Name',font=regFont,style="primary.TLabel")
			item_name_label.grid(row=1,column=0)

			item_price_label=ttk.Label(editor,text='Item Price',font=regFont,style="primary.TLabel")
			item_price_label.grid(row=2,column=0)

			
			#Loop through results
			for i in records:
				item_type_editor.insert(0,typereturn(i))
				item_name_editor.insert(0,namereturn(i))
				item_price_editor.insert(0,pricereturn(i))



			#create save button
			save_btn=ttk.Button(editor,text='Update record',command=update,style="primary.TButton")
			save_btn.grid(row=6,column=0,columnspan=2,padx=10,pady=10)

			#commit changes
			conn.commit()
			#close connection
			conn.close()


#Functions to output elements sum into the main subframe
def button_press(name):
	#Logic to sum contents
	if len(customersumoutput.get()) == 0:
		#Logic to output sum of first
		for i in cost_lst:
			if name==i[0]:
				customersumoutput.insert(0,i[1])
	else:
		#Logic to keep summing
		currentval=customersumoutput.get()
		customersumoutput.delete(0,END)
		for i in cost_lst:
			if name==i[0]:
				val=i[1]
		
		val = float(val) + float(currentval)
		customersumoutput.insert(0,val)




style.configure('custom.TFrame', background='#Dfe6e8', relief='sunken')

#Function to fill the frame outputting the different elements
def subframe_filler():

	#clear contents in frame firstly
	
	for widgets in submainframe.winfo_children():
		widgets.destroy()


	#create database or connect
	conn=sqlite3.connect('items_book.db')
	#create cursor
	c=conn.cursor()
	
	#Query database
	c.execute("SELECT *, oid FROM addresses")
	records=c.fetchall()
	
	#Loop through results
	print_records=""
	
	global names_lst
	names_lst=[str(i[1]) for i in records]

	
	#mainsubframe
	items_frame=ttk.Frame(submainframe,width=1850,height=10,borderwidth = 0,style="custom.TFrame")
	items_frame.pack(padx=25,pady=5,fill="both")
	
	global items_label


	for i in range(len(names_lst)):
		
		if i % 14 == 0 and i!=0:
			items_frame=ttk.Frame(submainframe,width=1850,height=10,borderwidth = 0,style="custom.TFrame")
			items_frame.pack(padx=25,pady=5,fill="both")

			items_label=ttk.Button(items_frame,text=names_lst[i],command= lambda i=i:button_press(names_lst[i]),style="primary.TButton")
			items_label.pack(side=tk.LEFT,anchor=NW,padx=20,pady=20)
		else:
			items_label=ttk.Button(items_frame,text=names_lst[i],command= lambda i=i:button_press(names_lst[i]),style="primary.TButton")
			items_label.pack(side=tk.LEFT,anchor=NW,padx=20,pady=20)
	
	#Process costs
	
	def getname(tup):
		return tup[1]

	def getcost(tup):
		return tup[2]

	global cost_lst
	cost_lst=[(getname(i),getcost(i)) for i in records]

	
	#commit changes
	conn.commit()
	#close connection
	conn.close()




#The file section in the navbar
def add_item():
	
	filewindow=Toplevel(root)
	filewindow.title('Cashier Database Window')
	filewindow.iconbitmap('shop.ico')

	
	global item_type
	global item_name
	global item_price
	global deletebox
	global secondfileframe

	#--Scrollbar logic--

	#adding main frame
	mainfile_frame=Frame(filewindow)
	mainfile_frame.pack(fill=BOTH,expand=1)

	#CREATE A CANVAS
	file_canvas=Canvas(mainfile_frame)
	file_canvas.pack(side=LEFT,fill=BOTH,expand=1)

	#Add scrollbar to mainframe
	file_scrollbar=ttk.Scrollbar(mainfile_frame,orient='vertical',command=file_canvas.yview,style='Vertical.TScrollbar')
	file_scrollbar.pack(side=RIGHT,fill=Y)

	
	#Configure the canvas
	file_canvas.configure(yscrollcommand=file_scrollbar.set)
	file_canvas.bind('<Configure>',lambda e: file_canvas.configure(scrollregion=file_canvas.bbox("all")))

	#Create another frame
	secondfileframe=Frame(file_canvas)

	#Add that new frame to a window in the canvas
	file_canvas.create_window((0,0),window=secondfileframe,anchor="nw")



	
	#create text boxes
	#filewindow
	item_type=ttk.Entry(secondfileframe,width=30,style="success.TEntry",state="focused")
	item_type.grid(row=0,column=1,padx=20)

	item_name=ttk.Entry(secondfileframe,width=30,style="success.TEntry",state="focused")
	item_name.grid(row=1,column=1,padx=20)

	item_price=ttk.Entry(secondfileframe,width=30,style="success.TEntry",state="focused")
	item_price.grid(row=2,column=1,padx=20)
 	
	deletebox=ttk.Entry(secondfileframe,width=30,style="success.TEntry",state="focused")
	deletebox.grid(row=10,column=1)
 	

	#create text box labels
	item_type_label=ttk.Label(secondfileframe,text='Item Type',font=regFont,style="primary.TLabel")
	item_type_label.grid(row=0,column=0)

	item_name_label=ttk.Label(secondfileframe,text='Item Name',font=regFont,style="primary.TLabel")
	item_name_label.grid(row=1,column=0)

	item_price_label=ttk.Label(secondfileframe,text='Item Price',font=regFont,style="primary.TLabel")
	item_price_label.grid(row=2,column=0)


	deletebox_label=ttk.Label(secondfileframe,text='Select ID#',font=regFont,style="primary.TLabel")
	deletebox_label.grid(row=10,column=0)
	


	#create submit button
	submit_btn=ttk.Button(secondfileframe,text='Add record to database',command=submit,style="primary.TButton")
	submit_btn.grid(row=6,column=0,columnspan=2,padx=10,pady=10)


	#create query button
	query_btn=ttk.Button(secondfileframe,text='Show Records',command=query,style="primary.TButton")
	query_btn.grid(row=7,column=0,columnspan=2,padx=10,pady=10,ipadx=137)


	#create delete button
	deletebutton=ttk.Button(secondfileframe, text='Delete a record',command=delete_item_func,style="primary.TButton")
	deletebutton.grid(row=11,column=0,columnspan=2,padx=10,pady=10,ipadx=130)



	#Create an update/edit button
	updatebutton=ttk.Button(secondfileframe,text="Edit a record",command=edit,style="primary.TButton")
	updatebutton.grid(row=13,column=0,columnspan=2,padx=10,pady=10,ipadx=135)

	#Create a refresh screen button
	refreshbutton=ttk.Button(secondfileframe,text="Refresh Screen",command=subframe_filler,style="primary.TButton")
	refreshbutton.grid(row=14,column=0,columnspan=2,padx=10,pady=10,ipadx=135)

	



#Button to output info page (in toolbar) (Documentation screen)
def infopage():
	infowindow=Toplevel(root)
	infowindow.title('Documentation')
	infowindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(infowindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")

	titletext=ttk.Label(mainframe,
		text="Documentation",
		font=regFont,style='info.TLabel')
	titletext.pack(anchor='center',pady=5)
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,
		text="The app's purpose is to calculate costs and the change for a small store. Firstly, go in the file menu and add items, ensuring that the correct data types are inputted. \n After doing this, You can click the refresh screen where the item name will be placed on the screen as a button. \n Click the different buttons and the total will be outputted in the customer total box. \n You can then input the customers money into the respective entry box and clicking compute will output the change. \n The user also has the choice of rounding the change. \n You can also manipulate the database clicking the show records button. All the items in the databse will be outputted below \n and can be seen by extending the screen from pulling down on the buttom of the screen when in windowed form \n To edit or delete a record, input the respective ID which is the first number of each row then click the respective buttons. \n Expect an update coming soon for this project!.\n Thanks for using my app! \U0001f600",
		font=regFont2,style='info.TLabel')
	errortext.pack(anchor='center',pady=25,padx=10)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=infowindow.destroy,style="info.TButton")
	errorbutton.pack(pady=10)


#Button at the end to clear screen
def clearscreen():
	customersumoutput.delete(0,END)
	changeoutput.delete(0,END)
	moneyinput.delete(0,END)

#Button at the end to compute
def compute():
	changeoutput.delete(0,END)

	#create database or connect
	conn=sqlite3.connect('items_book.db')
	#create cursor
	c=conn.cursor()
	
	#Query database
	c.execute("SELECT *, oid FROM addresses")
	records=c.fetchall()

	if len(records)==0:
		empty_database()
	else:


		if len(customersumoutput.get())==0 or ' ' in customersumoutput.get() or len(moneyinput.get())==0 or ' ' in moneyinput.get():
			#if empty/has an empty space
			emptyparameter()
		else:
			inputlst=[x for x in moneyinput.get() if x.isalpha()]
			inputdot=[x for x in moneyinput.get() if x == '.']
			#if not moneyinput.get().isnumeric():
			if len(inputlst)>0 or len(inputdot)>1:
				#Error message(input isnt only numbers)
				stringdetected()
			else:
				total=[x for x in customersumoutput.get() if x.isalpha()]
				if len(total)>0 and len(customersumoutput.get())>0:
					#if a string is present in the total bar
					stringintotal()
				else:
					def isfloat(num):
					    try:
					    	float(num)
					    	return True
					    except ValueError:
					        return False
					if not isfloat(moneyinput.get()):
						#Error if not a float
						stringdetected()
					else:
						if not isfloat(customersumoutput.get()):
							stringintotal()
						else:
							money=float(moneyinput.get())
							total=float(customersumoutput.get())
							if money<total:
							#Error message (money short) (FINISH!)
								insufficientmoney()
							else:
								change=money-total
								changeoutput.insert(0,change)
	

	#commit changes
	conn.commit()
	#close connection
	conn.close()


#Button at the end to round off value
def roundval():
	change=float(changeoutput.get())
	changeoutput.delete(0,END)
	change=round(change,0)
	changeoutput.insert(0,change)


'''Functions to output errors'''

#Frontend relative

#if the customer summer or input is empty
def emptyparameter():
	errorwindow=Toplevel(root)
	errorwindow.title('Error Window')
	errorwindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(errorwindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,text="The Customer's Total or Customer's Input is empty!",font=regFont2,style='warning.TLabel')
	errortext.pack(anchor='center',pady=25)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=errorwindow.destroy,style="warning.TButton")
	errorbutton.pack(pady=10)

#if string is in the money input
def stringdetected():
	errorwindow=Toplevel(root)
	errorwindow.title('Error Window')
	errorwindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(errorwindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,text="String entered into the input! Double check value entered",font=regFont2,style='warning.TLabel')
	errortext.pack(anchor='center',pady=25)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=errorwindow.destroy,style="warning.TButton")
	errorbutton.pack(pady=10)

#if customer's money is short
def insufficientmoney():
	errorwindow=Toplevel(root)
	errorwindow.title('Error Window')
	errorwindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(errorwindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,text="Customer's money is short!",font=regFont2,style='warning.TLabel')
	errortext.pack(anchor='center',pady=25)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=errorwindow.destroy,style="warning.TButton")
	errorbutton.pack(pady=10)

#if user types string into the box
def stringintotal():
	errorwindow=Toplevel(root)
	errorwindow.title('Error Window')
	errorwindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(errorwindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,text="Do not type into the total entry!",font=regFont2,style='warning.TLabel')
	errortext.pack(anchor='center',pady=25)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=errorwindow.destroy,style="warning.TButton")
	errorbutton.pack(pady=10)

#If user wants to compute with an empty database
def empty_database():
	errorwindow=Toplevel(root)
	errorwindow.title('Error Window')
	errorwindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(errorwindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,text="Start adding items to the database under the file menu!",font=regFont2,style='warning.TLabel')
	errortext.pack(anchor='center',pady=25)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=errorwindow.destroy,style="warning.TButton")
	errorbutton.pack(pady=10)


#Backend relative

def emptydata():
	#if any parameter entered to the backend is empty of just has spaces
	errorwindow=Toplevel(root)
	errorwindow.title('Error Window')
	errorwindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(errorwindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,text="Empty parameter detected. Fill every choice!",font=regFont2,style='warning.TLabel')
	errortext.pack(anchor='center',pady=25)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=errorwindow.destroy,style="warning.TButton")
	errorbutton.pack(pady=10)

	#clear screen
	item_type.delete(0,END)
	item_name.delete(0,END)
	item_price.delete(0,END)

def duplicate_entry():
	#if item name already present in the database
	errorwindow=Toplevel(root)
	errorwindow.title('Error Window')
	errorwindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(errorwindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,text="This item is already in the database!",font=regFont2,style='warning.TLabel')
	errortext.pack(anchor='center',pady=25)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=errorwindow.destroy,style="warning.TButton")
	errorbutton.pack(pady=10)

	#clear screen
	item_type.delete(0,END)
	item_name.delete(0,END)
	item_price.delete(0,END)

def wrongprice_type():
	#if the price isnt an int or float
	errorwindow=Toplevel(root)
	errorwindow.title('Error Window')
	errorwindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(errorwindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,text="The datatype of the price is incorrect! Enter an integer or a float!",font=regFont2,style='warning.TLabel')
	errortext.pack(anchor='center',pady=25)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=errorwindow.destroy,style="warning.TButton")
	errorbutton.pack(pady=10)

	#clear screen
	item_type.delete(0,END)
	item_name.delete(0,END)
	item_price.delete(0,END)

def integer_test():
	#if the number into the select id is not an integer
	errorwindow=Toplevel(root)
	errorwindow.title('Error Window')
	errorwindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(errorwindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,text="Enter an integer!",font=regFont2,style='warning.TLabel')
	errortext.pack(anchor='center',pady=25)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=errorwindow.destroy,style="warning.TButton")
	errorbutton.pack(pady=10)

def invalid_int():
	#if the number is outside the range
	errorwindow=Toplevel(root)
	errorwindow.title('Error Window')
	errorwindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(errorwindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,text="Invalid choice! Choose an integer based on the id of the item below!",font=regFont2,style='warning.TLabel')
	errortext.pack(anchor='center',pady=25)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=errorwindow.destroy,style="warning.TButton")
	errorbutton.pack(pady=10)

def invalid_namesize():
	#if the number is outside the range
	errorwindow=Toplevel(root)
	errorwindow.title('Error Window')
	errorwindow.iconbitmap('shop.ico')

	mainframe=ttk.Frame(errorwindow,width=200,height=100,borderwidth=0)
	mainframe.pack(anchor="w",fill="both")
	
	
	#widgets to fill frame
	errortext=ttk.Label(mainframe,text="The name entered should be between 4 and 15!",font=regFont2,style='warning.TLabel')
	errortext.pack(anchor='center',pady=25)

	errorbutton=ttk.Button(mainframe,text="Close",width=7,command=errorwindow.destroy,style="warning.TButton")
	errorbutton.pack(pady=10)




'''DESIGN OF MAIN WINDOW'''

#MAIN FRAME
main_frame=Frame(root,borderwidth = 0)
main_frame.pack(fill=BOTH,expand=1)

#CREATE A CANVAS
my_canvas=Canvas(main_frame,highlightthickness=0)
my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

#Add scrollbar to mainframe
myscrollbar=ttk.Scrollbar(main_frame,orient='vertical',command=my_canvas.yview,style='Vertical.TScrollbar')
myscrollbar.pack(side=RIGHT,fill=Y)

#Scroll with command of middle mouse

def _on_mouse_wheel(event):
    my_canvas.yview_scroll(-1 * int((event.delta / 90)), "units")

my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

#Configure the canvas
my_canvas.configure(yscrollcommand=myscrollbar.set)
my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

#Create another frame
secondframe=Frame(my_canvas,borderwidth = 0)

#Add that new frame to a window in the canvas
my_canvas.create_window((0,0),window=secondframe,anchor="nw")



#<TOOLBAR FRAME>
toolbar=ttk.Frame(secondframe,style="primary.TFrame")
toolbar.pack(fill='both',expand=True)

#Try to order drop down buttons


additem=ttk.Button(toolbar,text="File",command=add_item,style="primary.TButton")
additem.grid(row=0,column=0)

space6=ttk.Label(toolbar,text="  ",font=(None,10),style="primary.Inverse.TLabel").grid(row=0,column=1)
space7=ttk.Label(toolbar,text="  ",font=(None,10),style="primary.Inverse.TLabel").grid(row=0,column=2)
space8=ttk.Label(toolbar,text="  ",font=(None,10),style="primary.Inverse.TLabel").grid(row=0,column=3)
space9=ttk.Label(toolbar,text="  ",font=(None,10),style="primary.Inverse.TLabel").grid(row=0,column=4)

infopagebutton=ttk.Button(toolbar,text="App Info.",command=infopage,style="primary.TButton")
infopagebutton.grid(row=0,column=5)


#MAIN SUB FRAME 

#to fill the canvas
def onCanvasConfigure(e):
    subframe_canvas.itemconfig('frame', height=subframe_canvas.winfo_height(), width=subframe_canvas.winfo_width())

#--Scrollbar logic--
#create main body frame
secondmainframe=ttk.Frame(secondframe,width=1850,height=800,borderwidth = 0,style="custom.TFrame")
secondmainframe.pack_propagate(0)
secondmainframe.pack(padx=25,pady=70,expand=True,fill="both")

#create canvas
subframe_canvas=Canvas(secondmainframe)
subframe_canvas.pack(side=LEFT,fill=BOTH,expand=1)

#add scrollbar to frame
subframe_scrollbar=ttk.Scrollbar(secondmainframe,orient='vertical',command=subframe_canvas.yview,style='Vertical.TScrollbar')
subframe_scrollbar.pack(side=RIGHT,fill=Y)


#configure canvas
subframe_canvas.configure(yscrollcommand=subframe_scrollbar.set)
subframe_canvas.bind('<Configure>',lambda e: subframe_canvas.configure(scrollregion=subframe_canvas.bbox("all")))

#create another frame

submainframe=ttk.Frame(subframe_canvas,width=1850,height=800,borderwidth = 0,style="custom.TFrame")

#Add that new frame to a window in the canvas

subframe_canvas.create_window((0,0),window=submainframe,anchor="nw",tags="frame")

subframe_canvas.bind("<Configure>", onCanvasConfigure)



style.configure('custom.TFrame', background='#Dfe6e8', relief='sunken')

mainsubframe=ttk.Frame(submainframe,width=1850,height=800,style="custom.TFrame")
mainsubframe.pack_propagate(0)
mainsubframe.pack(padx=25,pady=70,expand=True,fill="both")





subframe_filler()



moneylabel=ttk.Label(secondframe,text="Enter customer's money",font=regFont,style="primary.TLabel").pack(anchor="w",padx=79,)
moneyinput=ttk.Entry(secondframe,width=15,style="success.TEntry",state="focused")
moneyinput.place(x=260,y=968)



#<Label and Form to output Customer's Total>

#trying to make space 
space1=Label(secondframe,text=" ",font=(None,10)).pack()
space2=Label(secondframe,text=" ",font=(None,10)).pack()

customersumlabel=ttk.Label(secondframe,text="Customer's Total",font=regFont,style="primary.TLabel")
customersumlabel.pack()

space3=Label(root,text=" ",font=(None,10)).pack()
space4=Label(secondframe,text=" ",font=(None,10)).pack()



customersumoutput=ttk.Entry(secondframe,width=260,style="success.TEntry",font=regFont2,state="active",justify=CENTER)
customersumoutput.pack()

space4=Label(secondframe,text=" ",font=(None,10)).pack()
space5=Label(secondframe,text=" ",font=(None,10)).pack()

changelabel=ttk.Label(secondframe,text="Change",font=regFont,style="primary.TLabel")
changelabel.pack()


space18=Label(secondframe,text=" ",font=(None,10)).pack()


changeoutput=ttk.Entry(secondframe,width=260,style="success.TEntry",font=regFont2,state="active",justify=CENTER)
changeoutput.pack(padx=20)

space19=Label(secondframe,text=" ",font=(None,10)).pack()


#LAST LINE WITH Clear, Compute and Round

clearbutton=ttk.Button(secondframe,text="Clear",width=12,command=clearscreen,style="primary.TButton")
clearbutton.place(x=685,y=1309)

computebutton=ttk.Button(secondframe,text="Compute",width=12,command=compute,style="primary.TButton")
computebutton.pack(padx=20,pady=60)

roundbutton=ttk.Button(secondframe,text="Round",width=12,command=roundval,style="primary.TButton")
roundbutton.place(x=1105,y=1309)




#commit changes
conn.commit()



#close connection
conn.close()



root.mainloop()