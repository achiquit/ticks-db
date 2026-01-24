from datetime import datetime
import sqlite3
from sqlite3 import Cursor

### REMEMBER TO ADD CON.COMMIT TO THE END OF THE SCRIPT ###

### To Do: Style script for new_tick() ###

def new_tick(cur: Cursor) -> None:
    res = cur.execute("SELECT id FROM ticks ORDER BY id DESC;")
    last_tick = res.fetchone()
    id = last_tick[0] + 1

    tick_date = return_date()

    climb_id = climb(cur)

    pitch_count = get_int("How many pitches, king?")

    height = input("How many feet did you climb? : ")



    print(f"ID: {id}")
    print(f"Date: {tick_date}")
    print(f"Climb: {climb_id}")
    print(f"Pitches: {pitch_count}")
    print(f"Height: {height}")

def y_n(text: str) -> bool:
    choice = input(f"{text} (y/n): ")
    if choice == "y":
        return True
    elif choice == "n":
        return False
    else:
        input("Come on man, you gotta play by the rules!")
        y_n(text)

def get_int(text: str) -> int:
    number_as_integer = None
    while number_as_integer is None:
        try:
            number_as_integer = int(input(f"{text}: "))
            return number_as_integer
        except ValueError:
            print("Dude, you gotta enter a number!")

def return_date() -> str:
    """Returns a date with the choice to default to todays date, or enter a custom date."""
    when_q = input("Was this tick today? (y/n): ")
    if when_q == "y":
        tick_date = datetime.today().strftime('%Y-%m-%d')
    elif when_q == "n":
        tick_date = input("Date of tick (YYYY-MM-DD): ")
    else:
        input("You gotta pick an actual choice, dude")
        tick_date = return_date()
    return(tick_date)

def climb(cur: Cursor) -> int:

    repeat = y_n("Have you done this climb before?")

    if repeat is True:
        return climb_search()
    else: 
        return new_climb(cur)

def climb_search() -> int:
    con = sqlite3.connect("ticks-test")
    cur = con.cursor()

    res = cur.execute(f"SELECT id FROM climbs ORDER BY id DESC;")
    newest_climb = res.fetchone()
    newest_climb = newest_climb[0]

    search_term = input("What was the name of the climb? : ")
    res = cur.execute(f"SELECT name, id FROM climbs WHERE name LIKE '%{search_term}%';")
    print(res.fetchall())
    search_results = get_int("If your climb showed up, put the ID here. If not, put '-1' : ")
    if search_results == -1:
        redo_search = y_n("Try another search?")
        if redo_search is True:
            return climb_search()
        else:
            return climb()
    elif search_results <= newest_climb:
        return search_results
    else:
        print("You gotta play by the rules, dude!")
        return climb_search()

def new_climb(cur: Cursor) -> int:
    """Adding a new climb to the DB"""

    res = cur.execute("SELECT id FROM climbs ORDER BY id DESC;")
    last_climb = res.fetchone()
    id = last_climb[0] + 1

    name = input("Climb Name: ")

    grade = grade_func(cur)

    danger = danger_func()

    type = type_func(cur)

    commitment = commitment_func()

    gps = input("GPS: ")

    area_id = area(cur)

    notes = input("Climb notes: ")

    cur.execute(f"""
        INSERT INTO climbs VALUES
            ({id}, "{name}", {grade}, '{danger}', {type}, '{commitment}', '{gps}', {area_id}, "{notes}")
    """)

    return(id)

def area(cur: Cursor) -> int:

    res = cur.execute("SELECT id FROM areas ORDER BY id DESC;")
    last_area = res.fetchone()
    area_id = last_area[0] + 1

    area_search = input("Search for area (if it's new put -1): ")

    if area_search == "-1":
        area_name = input("Area Name: ")

        country = input("Country: ")

        state = input("State: ")

        notes = input("Area notes: ")

        cur.execute(f"""
        INSERT INTO areas VALUES
            ({area_id}, "{area_name}", '{country}', '{state}', "{notes}")
        """)

        return(area_id)

    else:
        res = cur.execute("SELECT area_name, state, id FROM areas WHERE area_name LIKE '%" + area_search + "%';")
        print(res.fetchall())

        area_id = get_int("Area ID (if you want to search again, enter -1)")
        
        if area_id is -1:
            return(area(cur))
        elif area_id <= last_area[0]:
            return(area_id)
        else:
            input("Oops, looks like you made a typo! Try again :)")
            return(area(cur))

def danger_func() -> str:
    danger = input("Danger Rating (G, PG, PG-13, R, X, or -1): ")
    if danger in ['G', 'PG', 'PG-13', 'R', 'X', '-1']:
        return danger
    else:
        print("Looks like you made a typo! Try again :)")
        return danger_func()

def type_func(cur: Cursor) -> int:
    choice = get_int("Climb Type (1: Trad | 2: Sport | 3: TR | 4: Boulder | -1: More)")
    if choice == -1:
        res = cur.execute("SELECT * FROM climb_type;")
        print(res.fetchall())
        choice = get_int("Climb Type")
        return choice
    elif choice == 1:
        return 5
    elif choice == 2:
        return 4
    elif choice == 3:
        return 3
    elif choice == 4:
        return 2
    else:
        print(f"{choice} is of type {type(choice)}")
        return type_func(cur)

def commitment_func() -> str:
    commitment = input("Commitment (I, II, etc, -1 for nothing): ")
    if commitment in ['-1', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII']:
        return commitment
    else:
        input("You probably made a typo! Try again :)")
        return commitment_func()

def grade_func(cur: Cursor) -> int:
    res = cur.execute("SELECT id FROM join_grades ORDER BY id DESC;")
    last_grade = res.fetchone()
    new_id = last_grade[0] + 1

    grade = input("Grade: ")

    res = cur.execute("SELECT * FROM join_grades WHERE notes LIKE '%" + grade + "%';")
    print(res.fetchall())
    grade_id = get_int("Grade ID (-1 for new amalgam grade)")

    if grade_id == -1:
        return(new_join_grade(cur, new_id, grade))
    elif grade_id < new_id:
        return grade_id
    else:
        input("Looks like you made a typo! Try again :)")
        return grade_func(cur)

def new_join_grade(cur: Cursor, new_id: int, grade: str) -> int:
    complete = False
    new_amalgam = []
    insert_amalgam = []
    grade_names = []
    grade_num = 1

    grade_id = get_int(f"Grade {grade_num} ID")
    new_amalgam.append((grade_id, grade))
    grade_num += 1

    while complete is False:
        grade_id = get_grade_id(cur, grade_num, new_id)
        if grade_id[0] is -1:
            complete = True
        else:
            new_amalgam.append(grade_id)
        grade_num += 1

    for item in new_amalgam:
        insert_amalgam.append((new_id, item[0]))

    cur.executemany("INSERT INTO which_grades VALUES(?, ?)", insert_amalgam)

    insert_amalgam = [new_id]
    for item in new_amalgam:
        grade_names.append(item[1])
    first_item = True
    for item in grade_names:
        if first_item is True:
            insert_grade_notes = item
            first_item = False
        else:
            insert_grade_notes = insert_grade_notes + f", {item}"
    insert_amalgam.append(insert_grade_notes)
    insert_amalgam = tuple(insert_amalgam)

    cur.execute(f"""
    INSERT INTO join_grades VALUES 
        ({insert_amalgam[0]}, "{insert_amalgam[1]}")
    """)

    return new_id

def get_grade_id(cur: Cursor, grade_num: int, new_id: int) -> tuple:
    if grade_num <= 2:
        grade = input(f"Grade {grade_num} Search: ")
    else:
        grade = input(f"Grade {grade_num} Search (if done, enter -1): ")

    if grade == "-1":
        return [-1]

    res = cur.execute("SELECT * FROM join_grades WHERE notes LIKE '" + grade + "';")
    print(res.fetchall())
    grade_id = get_int(f"Grade {grade_num} ID: ")

    if grade_id < new_id:
        grade_return = (grade_id, grade)
        return grade_return
    else:
        input("Oops, looks like you made a typo! Try again :)")
        return get_grade_id(cur, grade_num, new_id)

print("Hell yeah, way to get after it, dawg!")
print("Let's get those sweet, sweet sends in that there database.")

con = sqlite3.connect("ticks-test")
cur = con.cursor()

new_tick(cur)

# con.commit()