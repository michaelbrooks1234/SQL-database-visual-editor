from sqlite3 import *
from sqlite3 import Error
import os



class DataBase:
    
    def __init__(self, path):
        
        connecty = None

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
    
    def get_formatted_table(self, table):
        result = self.cursor.execute(f"SELECT * FROM {table}").fetchall()

        return [result, self.cursor.description]
    
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
    
    def update_database_entry(self, data, table):
        primary_key = data[0]
        column = data[1]
        
        self.cursor.execute(f"SELECT {column} FROM {table} WHERE primary_key = {primary_key}").fetchone()

        return True

        


def setup_premade_databases():

    movies = "movies.db"
    random_data = "random_data.db"
    random_customer = "random_customer.db"

    current_directory = os.listdir("./src/") 

    if(movies not in current_directory):
        database = DataBase("./src/movies.db")
        database.initialize_movies_database()
        database = None
    if(random_data not in current_directory):
        database = DataBase("./src/random_data.db")

        database = None
    if(random_customer not in current_directory):
        database = DataBase("./src/random_customer.db")

        database = None

    return None