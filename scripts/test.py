import sqlite3
from sqlite3 import Cursor

con = sqlite3.connect("ticks")
cur = con.cursor()