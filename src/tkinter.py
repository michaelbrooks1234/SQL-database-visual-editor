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

        container_of_databases = Frame(frame)
        container_of_databases["bg"] = "white"
        container_of_databases.place(relheight=0.6, relwidth=0.6, relx=0.2, rely=0.2)


        for i in range(count):
            Button(container_of_databases, text=f"{self.databases[i][0:-3]}", font=("Helvetica bold", 20), command=partial(self.open_database, self.databases[i])).place(y=60*i) 

        new_database_button = Button(container_of_databases, text="Create New Database", font=("Helvetica bold", 20), command=lambda: self.open_database("new"))
        new_database_button.place(y=60*count)

        self.window.mainloop()

        return None



        
    def open_database(self, database_name):

        self.window.destroy()

        self.database = DataBase(f"./src/{database_name}")

        tables = self.database.get_database_tables()

        self.database_view_window(tables)

        return None


    def go_back(self):
        try:
            self.window.destroy()
        except:
            None
        
        self.setup_landing()

        return None

    def database_view_window(self, tables, table=None):

        self.window = Tk()
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(False, False)

        self.frame = Frame(self.window)
        self.frame["bg"] = "white"
        self.frame.place(relheight=1, relwidth=1)

        label = Label(self.frame, text="Select Table:", font=("Helvetica bold", 20), anchor=CENTER, bg="white")
        label.pack(pady=10)

        Button(self.frame, text="back", command=self.go_back).place(relheight=0.05, relwidth=0.1, rely=0, relx=0)


        container = Frame(self.frame, bg="white")
        container.place(relheight=0.1, relwidth=0.8, rely=0.1)

        for i in range(len(tables)):
            Button(container, text=f"{tables[i][0]}", font=("Helvetica bold", 20), command=partial(self.open_table, tables[i][0], tables)).pack(side = LEFT)

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
                if(j == 0 and i < len(table_data[i])):
                    label=Label(self.frame_container, padx=30, relief=GROOVE , text=f"{columns[i][0]}", font=("Helvetica bold", 10), anchor=W, bg="white")
                    label.grid(sticky=W, column=i, row=0)

                label=Label(self.frame_container, padx=30, text=f"{table_data[i][j]}", font=("Helvetica bold", 10), anchor=W, bg="white")
                label.grid(sticky = W, column=j, row=i+1)

                if(j != 0):
                    button=Button(self.frame_container, padx=5, text="Edit", font=("Helvetica bold", 5))
                    button.grid(sticky=W, column=j, row=i+1)
                    button.configure(command=partial(self.open_confirmation, i, columns[j][0], table, tables))

        self.frame_container.update_idletasks()
        self.container.configure(scrollregion=self.container.bbox("all"))


        self.window.mainloop()
        
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

        Label(self.new_window, text="Edit Entry:", font=("Helvetica bold", 12), bg="lightgray").pack(pady=2, side=TOP)

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
