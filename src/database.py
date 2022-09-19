from sqlite3 import *
from sqlite3 import Error
import os
import random
import math



class DataBase:
    
    def __init__(self, path):
        
        connecty = None

        if(path == "new"):
            return self.create_new_database()

        try:
            connecty = connect(path)
        except Error as e:
            print(f"The error {e} has occurred")
        
        self.connection = connecty
        self.cursor = connecty.cursor()

        return None

    def get_database_tables(self):
        result = self.cursor.execute("SELECT name FROM sqlite_master").fetchall()
        return result
    
    def create_new_table(self, columns, table):

        columns.insert(0, "primary_key")
        columns_tuple = tuple(columns)

        print(columns_tuple)

        self.cursor.execute(f"CREATE TABLE T_{table}{columns_tuple}")
        self.connection.commit()
        
        return None
    
    def get_formatted_table(self, table):
        result = self.cursor.execute(f"SELECT * FROM {table}").fetchall()

        return [result, self.cursor.description]

    def add_new_entry(self, table, entries):

        if(self.cursor.execute(f"SELECT MAX(primary_key) FROM {table}").fetchone()[0] is not None):
            new_primary_key = self.cursor.execute(f"SELECT MAX(primary_key) FROM {table}").fetchone()[0]+1
        else:
            new_primary_key = 0 
        entries.insert(0, new_primary_key)        
        entries_tuple = tuple(entries)

        try:
            self.cursor.execute(f"INSERT INTO {table} VALUES {entries_tuple}")
            self.connection.commit()
            return True
        except:
            return False
 
    def initialize_movies_database(self):

        self.cursor.executescript("""
        BEGIN;
        CREATE TABLE movies(primary_key, title, year, score);
        CREATE TABLE actors(primary_key, name, movie);
        CREATE TABLE directors(primary_key, name, networth, movie);
        COMMIT;
        """)
        
        #add abunch of values for all of these

        data_for_movies = [
            (0, "The Shawshank Redemption", 1994, 9.2),
            (1, "The Godfather", 1972, 9.2),
            (2, "The Dark Knight", 2008, 9.0),
            (3, "The Godfather Part II", 1974, 9.0),
            (4, "12 Angry Men", 1957, 8.9),
            (5, "Schindler's List", 1993, 8.9),
            (6, "The Lord of the Rings: The Return of the King", 2003, 8.9),
            (7, "Pulp Fiction", 1994, 8.8),
            (8, "The Good, The Bad and the Ugly", 1966, 8.8),
            (9, "The Lord of the Rings: the Fellowship of the Ring", 2001, 8.8),
            (10, "Forrest Gump", 1994, 8.8),
            (11, "Fight Club", 1999, 8.7),
        ]

        data_for_actors = [
            (0, "Time Robbins", "The Shawshank Redemption"),
            (1, "Marlon Brando", "The Godfather"),
            (2, "Christian Bale", "The Dark Knight"),
            (3, "Al Pacino", "The Godfather Part II"),
            (4, "Henry Fonda", "12 Angry Men"),
            (5, "Liam Neeson", "Schindler's List"),
            (6, "Elijah Wood", "The Lord of the Rings: The Return of the King"),
            (7, "John Travolta", "Pulp Fiction"),
            (8, "Elijah Wood", "The Lord of the Rings: The Fellowship of the Ring"),
            (9, "Clint Eastwood", "The Good, The Bad and the Ugly"),
            (10, "Tom Hanks", "Forrest Gump"),
            (11, "Brad Pitt", "Fight Club"),
        ]

        data_for_directors = [
            (0,"Frank Darabont", 100_000_000, "The Shawshank Redemption" ),
            (1,"Francis Ford Coppola", 400_000_000, "The Godfather"),
            (2,"Christopher Nolan", 250_000_000, "The Dark Knight"),
            (3,"Francis Ford Coppola", 400_000_000, "The Godfather Part II"),
            (4,"Sidney Lumet", 1_500_000, "12 Angry Men"),
            (5,"Steven Spielberg", 4_000_000_000, "Schindler's List"),
            (6,"Peter Jackson", 1_500_000_000, "The Lord of the Rings: The Return of the King"),
            (7,"Quentin Tarantino", 120_000_000, "Pulp Fiction"),
            (8,"Peter Jackson", 1_500_000_000, "The Lord of the Rings: The Fellowship of the Ring"),
            (9,"Sergio Leone", 10_000_000,"The Good, The Bad and the Ugly"),
            (10,"Robert Zemeckis", 60_000_000, "Forrest Gump"),
            (11,"David Fincher", 100_000_000, "Fight Club"),
        ]

        self.cursor.executemany("INSERT INTO movies VALUES(?, ? , ?, ?)", data_for_movies)
        self.cursor.executemany("INSERT INTO actors VALUES(?, ?, ?)", data_for_actors)
        self.cursor.executemany("INSERT INTO directors VALUES(?, ? , ?, ?)", data_for_directors)
        self.connection.commit()

        #commit changes
        self.connection.commit()

        return "done"
    
    def update_database_entry(self, new_value, primary_key, column, table):
        
        self.cursor.execute(f"UPDATE {table} SET '{column}' = '{new_value}' WHERE primary_key = {primary_key}")
        self.connection.commit()
        return True

    def initialize_random_data_database(self):

        self.cursor.executescript("""
        BEGIN;
        CREATE TABLE numbers(primary_key, ints, floats);
        CREATE TABLE strings(primary_key, random_characters, random_everything);
        CREATE TABLE words(primary_key, random_words, single_word);
        COMMIT;
        """)

        data_for_numbers = []

        for i in range(30):
            
            num = random.random() 
            num = math.floor(num * 10**7)

            float = random.random() * 10

            data_for_numbers.append((i, num, float))

        data_for_strings = []

        for i in range(30):
            char_string = ""
            char_all_string = ""
            for j in range(15):
                char = chr(math.floor((random.random()*100)%25)+61)
                char_all = chr(math.floor((random.random()*100)%67)+58)
                if(j == 0):
                    char_all_string = char_all
                    char_string = char
                else: 
                    char_all_string += char_all 
                    char_string += char
            
            data_for_strings.append((i, char_string, char_all_string))

        data_for_words = []

        with open('./src/strings.txt') as f:
            lines = f.readlines()

        strings = []

        for i in range(100):
            if(i != 99):
                strings.append(lines[i][0:-1])
            else:
                strings.append(lines[i]) 

        for i in range(30):
            word = random.choice(strings)
            string = ""
            for j in range(8):
                word_for_string = random.choice(strings)
                if(j == 0):
                    string = word_for_string
                else:
                    string += f"-{word_for_string}"

            data_for_words.append((i, string, word))
            
        self.cursor.executemany("INSERT INTO numbers VALUES(?, ? , ?)", data_for_numbers)
        self.cursor.executemany("INSERT INTO strings VALUES(?, ?, ?)", data_for_strings)
        self.cursor.executemany("INSERT INTO words VALUES(?, ? , ?)", data_for_words)

        self.connection.commit()
            
        return None


        

def setup_premade_databases():

    movies = "movies.db"
    random_data = "random_data.db"

    current_directory = os.listdir("./src/") 

    if(movies not in current_directory):
        database = DataBase("./src/movies.db")
        database.initialize_movies_database()
        database = None
    if(random_data not in current_directory):
        database = DataBase("./src/random_data.db")
        database.initialize_random_data_database()
        database = None

    return None