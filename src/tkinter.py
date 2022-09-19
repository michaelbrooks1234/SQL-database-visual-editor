from tkinter import *
import os
from src.database import *
from functools import partial
import time



class Window:
    
    def __init__(self, width, height):
        self.height = height
        self.width = width
        return None

    def setup_landing(self):
        
        files_in_directory = os.listdir("./src/")
        self.databases = []
        count = 0

        for i in range(len(files_in_directory)):
            if(files_in_directory[i][-2:None] == "db"):
                self.databases.append(files_in_directory[i])
                count += 1
        
        self.window = Tk()
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(False, False)

        frame = Frame(self.window)
        frame["bg"] = "white"
        frame.place(relheight=1, relwidth=1)

        label = Label(frame, text="Select Database to Edit:", font=("Helvetica bold", 20), anchor=CENTER, bg="white")
        label.pack(pady=20)

        container_of_databases = Canvas(frame)
        container_of_databases["bg"] = "white"
        container_of_databases.place(relheight=0.6, relwidth=0.6, relx=0.2, rely=0.2)

        scrollbar_y = Scrollbar(self.window, orient=VERTICAL, command=container_of_databases.yview)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        container_of_databases.configure(yscrollcommand=scrollbar_y.set)

        frame_container = Frame(container_of_databases, bg="white")
        container_of_databases.create_window((0,0), window=frame_container, anchor=NW)

        for i in range(count):
            Button(frame_container, text=f"{self.databases[i][0:-3]}", font=("Helvetica bold", 20), command=partial(self.open_database, self.databases[i])).grid(sticky=W, column=0, row=i)
        
        Button(frame_container, text="Create New Database", font=("Helvetica bold", 20), command=lambda: self.open_database("new")).grid(sticky=W, column=0, row=count)
        Button(frame_container, text="Exit", font=("Helvetica bold", 20), command=lambda: self.window.destroy()).grid(sticky=W, column=0, row=count+1)


        frame_container.update_idletasks()
        container_of_databases.configure(scrollregion=container_of_databases.bbox("all"))

        self.window.mainloop()

        return None



        
    def open_database(self, database_name):

        if(database_name=="new"):
            return self.get_database_name()

        self.window.destroy()

        self.database = DataBase(f"./src/{database_name}")

        tables = self.database.get_database_tables()

        self.database_view_window(tables)

        return None

    def get_database_name(self):
        
        new_window = Toplevel(self.window, bg="white")
        new_window.title("DatabaseName")
        new_window.geometry("200x100")
        new_window.resizable(False, False)

        Label(new_window, bg="white",text="Database Name").pack(anchor=CENTER, pady=5)
        entry = Entry(new_window, bg="white")
        entry.pack(anchor=CENTER, pady=5)
        Button(new_window, text="Ok", command=lambda: self.check_database_name(entry.get())).pack(anchor=CENTER, pady=5)
        
        return None

    def check_database_name(self, name):
        if(name != ""):
            return self.open_database(f"{name}.db")
        else:
            self.new_table_failed()

        return None 

    def get_column_count(self):

        new_window = Toplevel(self.window, bg="white")
        new_window.title("Creation Failed")
        new_window.geometry("200x100")
        new_window.resizable(False, False)

        Label(new_window, bg="white",text="Column Count:").pack(anchor=CENTER, pady=5)
        entry = Entry(new_window, bg="white")
        entry.pack(anchor=CENTER, pady=5)
        Button(new_window, text="Ok", command=lambda: self.check_count(entry.get(), new_window)).pack(anchor=CENTER, pady=5)
        
        return None
        
    def check_count(self, count, window):
        try:
            count_valid = int(count, base=10)
            self.setup_new_database(count_valid)
        except:
            self.get_column_count() 
        window.destroy() 

    def setup_new_database(self, count):

        try:
            self.new_window.destroy()
        except:
            None
 
        self.new_window = Toplevel(self.window, bg="white")  
        self.new_window.title("New Window")
        self.new_window.geometry("500x350")
        self.new_window.resizable(False, False)

        container = Canvas(self.new_window, bg="white")
        container.place(rely=0.05, relwidth=.8, relx=0.1, relheight=0.6)

        scrollbar_x = Scrollbar(self.new_window, orient=HORIZONTAL, command=container.xview)
        scrollbar_x.pack(side=BOTTOM, fill=X)
        container.configure(xscrollcommand=scrollbar_x.set)

        frame_container = Frame(container, bg="white")
        container.create_window((0,0), window=frame_container, anchor=NW)
        
        Label(self.new_window, text="Add Columns:", font=("Helvetica bold", 12), bg="white").place(rely=0.01, relheight=0.05, relx=0.4)

        columns = []

        for i in range(count):
                entry = Entry(frame_container,width=10, font=("Helvetica bold", 15), bg="lightgray")
                entry.grid(column=i, row=1, pady=5)
                columns.append(entry) 

        label = Label(container, font=("Helvetica bold", 8), bg="white", text="Table Name").place(relwidth=0.2, relx=0.3, relheight=0.1, rely=0.75)
        entry = Entry(container, font=("Helvetica bold", 15), bg="lightgray")
        entry.place(relwidth=0.2, relx=0.3, relheight=0.1, rely=0.85) 
        Button(container, text="confirm", command=lambda: self.check_new_table_columns(columns, entry.get())).place(relwidth= 0.2, relx=0.6, relheight=0.2, rely=0.8)
            
        frame_container.update_idletasks()
        container.configure(scrollregion=container.bbox("all"))
                    
        return None

    def check_new_table_columns(self, columns, table):
 
        if(table == ""):
            return self.new_table_failed()

        column_values = []
        for i in range(len(columns)):
            if(columns[i].get() != ""):
                column_values.append(columns[i].get())
            else:
                return self.new_table_failed() 
        self.database.create_new_table(column_values, table)
        time.sleep(1)
        self.window.destroy()
        self.new_window.destroy()
        self.database_view_window(self.tables, f"T_{table}")
    
    def new_table_failed(self):

        new_window = Toplevel(self.window, bg="white")
        new_window.title("Creation Failed")
        new_window.geometry("200x100")
        new_window.resizable(False, False)

        Label(new_window, bg="white",text="Empty Inputs").pack(anchor=CENTER, pady=5)

        Button(new_window, text="Ok", command=lambda: new_window.destroy()).place(relheight=0.25, relwidth=0.3, relx=0.35, rely=0.35)
        
        return None


    def go_back(self):
        try:
            self.window.destroy()
        except:
            None
        
        self.setup_landing()

        return None

    def database_view_window(self, tables, table=None):

        try:
            self.scrollbar_x.destroy()
            self.scrollbar_x = None
        except:
            None

        self.window = Tk()
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(False, False)

        self.tables = tables
        self.table = table

        self.frame = Canvas(self.window)
        self.frame["bg"] = "white"
        self.frame.place(relheight=1, relwidth=1)

        label = Label(self.window, text="Select Table:", font=("Helvetica bold", 20), anchor=CENTER, bg="white")
        label.pack(pady=10)



        container = Frame(self.frame, bg="white")
        container.place(relheight=0.8, relwidth=0.8)

        Button(container, text="back", command=self.go_back).place(height=30, width=60, rely=0.1, relx=0)


        self.scrollbar_x = Scrollbar(self.window, orient=HORIZONTAL, command=self.frame.xview)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)
        self.frame.configure(xscrollcommand=self.scrollbar_x.set)

        

        self.frame.create_window((0,0), window=container)

        for i in range(len(tables)):
            Button(container, text=f"{tables[i][0]}", font=("Helvetica bold", 20), command=partial(self.open_table, tables[i][0], tables)).grid(column=i, row=0, sticky=W, pady=50)

        Button(container, text="New Table", font=("Helvetica bold", 20), command=lambda: self.get_column_count()).grid(column=len(tables),row=0, sticky=W, pady=50)

        container.update_idletasks()
        self.frame.configure(scrollregion=self.frame.bbox("all"))

        if(table is not None):
            self.open_table(table, tables)

        self.window.mainloop()

        return None

    def open_table(self, table, tables):

        try:
            self.container.destroy()
            self.scrollbar_x.destroy()
            self.scrollbar_y.destroy()
        except:
            None

        self.table = table
        data = self.database.get_formatted_table(table)
        table_data = data[0]
        columns = data[1]


        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.container = Canvas(self.frame, bg="white")
        self.container.place(rely=0.2, relwidth=.8, relx=0.1, relheight=0.6)

        self.scrollbar_x = Scrollbar(self.window, orient=HORIZONTAL, command=self.container.xview)
        self.scrollbar_y = Scrollbar(self.window, orient=VERTICAL, command=self.container.yview)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)
        self.container.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)
        self.container.configure(yscrollcommand=self.scrollbar_y.set)
        
        self.frame_container = Frame(self.container, bg="white")
        self.container.create_window((0,0), window=self.frame_container, anchor=NW)

        for i in range(len(table_data)):
            for j in range(len(table_data[i])):
                if(i == 0):
                    label=Label(self.frame_container, padx=30, relief=GROOVE , text=f"{columns[j][0]}", font=("Helvetica bold", 10), anchor=W, bg="white")
                    label.grid(sticky=W, column=j, row=0)

                label=Label(self.frame_container, padx=30, text=f"{table_data[i][j]}", font=("Helvetica bold", 10), anchor=W, bg="white")
                label.grid(sticky = W, column=j, row=i+1)

                if(j != 0):
                    button=Button(self.frame_container, padx=5, text="Edit", font=("Helvetica bold", 5))
                    button.grid(sticky=W, column=j, row=i+1)
                    button.configure(command=partial(self.open_confirmation, i, columns[j][0], table, tables))

        Button(self.frame_container, padx=5, text="Add New Entry", font=("Helvetica bold", 15), height=1, command=lambda: self.create_new_entry(table, columns)).grid(sticky=W, pady=20, padx=10, column=0, row=len(table_data)+1)

        self.frame_container.update_idletasks()
        self.container.configure(scrollregion=self.container.bbox("all"))


        self.window.mainloop()
        
        return None

    def create_new_entry(self, table, columns):

        columns_parsed = []

        for i in range(len(columns)):
            if(i != 0):
                columns_parsed.append(columns[i][0])

        try:
            self.new_window.destroy()
        except:
            None
 
        self.new_window = Toplevel(self.window, bg="white")  
        self.new_window.title("New Window")
        self.new_window.geometry("500x350")
        self.new_window.resizable(False, False)

        container = Canvas(self.new_window, bg="white")
        container.place(rely=0.05, relwidth=.8, relx=0.1, relheight=0.6)

        scrollbar_x = Scrollbar(self.new_window, orient=HORIZONTAL, command=container.xview)
        scrollbar_x.pack(side=BOTTOM, fill=X)
        container.configure(xscrollcommand=scrollbar_x.set)

        frame_container = Frame(container, bg="white")
        container.create_window((0,0), window=frame_container, anchor=NW)
        
        Label(self.new_window, text="Edit Entry:", font=("Helvetica bold", 12), bg="white").place(rely=0.01, relheight=0.05, relx=0.4)

        labels = []
        entries = []

        for i in range(len(columns_parsed)):

            label = Label(frame_container, font=("Helvitca bold", 10), bg="white", text=f"{columns_parsed[i]}")
            label.grid(column=i, row=0, pady=35, padx=5)
            labels.append(label)
            
            entry = Entry(frame_container, width=10, font=("Helvetica bold", 15), bg="lightgray")
            entry.grid(column=i, row=1)
            entries.append(entry)        
            
            
        frame_container.update_idletasks()
        container.configure(scrollregion=container.bbox("all"))

        button = Button(self.new_window, text="Confirm", command= lambda: self.create_new_entry_authorize(table, entries))
        button.place(relheight=0.1, relwidth=0.2, relx=0.2, rely=0.5)

        button2 = Button(self.new_window, text="Cancel", command=lambda: self.new_window.destroy())
        button2.place(relheight=0.1, relwidth=0.2, relx=0.6, rely=0.5)


        return None

    def create_new_entry_authorize(self, table, entries):

        entries_text = []

        for i in range(len(entries)):
            if(entries[i].get() == ""):
                return self.create_new_entry_failed()
            else:
                entries_text.append(entries[i].get())
        
        if(self.database.add_new_entry(table, entries_text)):
            return self.create_new_entry_success()
        else:
            return self.create_new_entry_failed()        

    def create_new_entry_success(self):

        new_window = Toplevel(self.window, bg="white")  
        new_window.title("Creation Success")
        new_window.geometry("200x100")
        new_window.resizable(False, False)

        Label(new_window, bg="white",text="Entry Creation Success!").pack(anchor=CENTER, pady=5)

        Button(new_window, text="Ok", command=lambda: self.refresh()).place(relheight=0.25, relwidth=0.3, relx=0.35, rely=0.35)

        return None
    
    def refresh(self):

        try:
            self.window.destroy()
        except Error as e:
            print(f"{e}")

        if(self.table):
            self.database_view_window(self.tables, self.table)
        else:
            self.database_view_window(self.tables)

        return None

    def create_new_entry_failed(self):

        new_window = Toplevel(self.window, bg="white")
        new_window.title("Creation Failed")
        new_window.geometry("200x100")
        new_window.resizable(False, False)

        Label(new_window, bg="white",text="Entry Creation Failed, invalid input").pack(anchor=CENTER, pady=5)

        Button(new_window, text="Ok", command=lambda: new_window.destroy()).place(relheight=0.25, relwidth=0.3, relx=0.35, rely=0.35)
        
        return None

    def open_confirmation(self, primary_key, column, table, tables):

        try:
            self.new_window.destroy()
        except:
            None
 
        self.new_window = Toplevel(self.window, bg="lightgray")  
        self.new_window.title("New Window")
        self.new_window.geometry("400x200")
        self.new_window.resizable(False, False)



        entry = Entry(self.new_window, font=("Helvetica bold", 15))
        entry.place(rely=0.2, relheight=0.25, relwidth=0.5, relx=0.25)

        button = Button(self.new_window, text="Confirm", command= lambda: self.confirm_change(entry.get(), primary_key, column, table, tables))
        button.place(relheight=0.25, relwidth=0.4, relx=0.1, rely=0.5)

        button2 = Button(self.new_window, text="Cancel", command=lambda: self.new_window.destroy())
        button2.place(relheight=0.25, relwidth=0.4, relx=0.5, rely=0.5)


        return None

    def confirm_change(self, new_value, primary_key, column, table, tables):

        self.new_window.destroy()

        self.database.update_database_entry(new_value, primary_key, column, table)

        self.window.destroy()
        
        self.database_view_window(tables, table)
        return None
