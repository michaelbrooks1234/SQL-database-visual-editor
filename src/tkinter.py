from tkinter import *
import os
from src.database import *
from functools import partial



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



    def database_view_window(self, tables):

        self.window = Tk()
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(False, False)

        self.frame = Frame(self.window)
        self.frame["bg"] = "white"
        self.frame.place(relheight=1, relwidth=1)

        label = Label(self.frame, text="Select Table:", font=("Helvetica bold", 20), anchor=CENTER, bg="white")
        label.pack(pady=10)

        container = Frame(self.frame, bg="white")
        container.place(relheight=0.1, relwidth=0.8, rely=0.1)

        for i in range(len(tables)):
            Button(container, text=f"{tables[i][0]}", font=("Helvetica bold", 20), command=partial(self.open_table, tables[i][0])).pack(side = LEFT)



        self.window.mainloop()

        return None

    def open_table(self, table):

        try:
            self.container.destroy()
            self.scrollbar_x.destroy()
            self.scrollbar_y.destroy()
        except:
            self.container=None

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
                label=Label(self.frame_container, padx=20, text=f"{table_data[i][j]}", font=("Helvetica bold", 10), anchor=W, bg="white", bd=10)
                label.grid(sticky = W, column=j, row=i)

                if(j != 0):
                    button=Button(self.frame_container, padx=5, text="Edit", font=("Helvetica bold", 5), command=partial(self.edit_entry, [i, columns[j][0]], table))
                    button.grid(sticky= W, column=j, row=i)

        self.frame_container.update_idletasks()
        self.container.configure(scrollregion=self.container.bbox("all"))


        self.window.mainloop()
        
        return None

    def edit_entry(self, index, table):
        
        self.database.update_database_entry(index, table)

        return None 