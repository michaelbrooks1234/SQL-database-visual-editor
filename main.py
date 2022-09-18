from src.tkinter import *
from src.database import *



def main():

    setup_premade_databases()

    width = 1000
    height = 800
    window = Window(width, height)
    window.setup_landing()

    return None

main()