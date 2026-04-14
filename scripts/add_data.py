from datetime import datetime
import sqlite3
from sqlite3 import Cursor

def day_out(cur: Cursor, new_ticks: list, new_tick_id: int) -> list:
    print("Hell yeah, way to get after it, dawg!")
    print("Let's get those sweet, sweet sends in that there database.")

    date = return_date()

    more_ticks = True
    while more_ticks is True:
        new_ticks.append(new_tick(cur, date, new_tick_id))
        new_tick_id += 1
        more_ticks = y_n(f"Do you have another tick to make on {date}, ya crusher?")

    another_day = True
    while another_day is True:
        another_day = y_n("Do you have ticks from another date to make, you absolute madlad?")
        if another_day is True:
            return day_out(cur, new_ticks)
    
    return new_ticks

def new_tick(cur: Cursor, date: str, new_tick_id: int) -> tuple:
    climb_id = climb(cur)

    pitch_count = get_int("How many pitches, king?")

    height = get_int("How many feet did you climb?")

    style = style_func()

    success = success_func()

    notes = notes_func()

    input = y_n("Were you climbing for pleasure?")
    if input is True:
        partner = partner_func(cur)
        client= '-1'
    elif input is False:
        client = client_func(cur)
        partner = '-1'

    # print("=+=+=+=+=+=+=+=+ NEW TICK ENTRY =+=+=+=+=+=+=+=+")
    # print(f"ID: {id}")
    # print(f"Date: {date}")
    # print(f"Climb: {climb_id}")
    # print(f"Pitches: {pitch_count}")
    # print(f"Height: {height}")
    # print(f"Style: {style}")
    # print(f"Success: {success}")
    # print(f"Notes: {notes}")
    # print(f"Partner/s: {partner}")
    # print(f"Client/s: {client}")

    # id = 1180
    # date = '2026-01-26'
    # climb_id = 406
    # pitch_count = 1
    # height = 100
    # style = 'Lead'
    # success = 'Redpoint'
    # notes = "Ayy"
    # partner = 113
    # client = -1

    new_tick = (new_tick_id, date, climb_id, pitch_count, height, style, success, notes, partner, client)

    return new_tick

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
        return climb_search(cur)
    else: 
        return new_climb(cur)

def climb_search(cur: Cursor) -> int:
    res = cur.execute(f"SELECT id FROM climbs ORDER BY id DESC;")
    newest_climb = res.fetchone()
    newest_climb = newest_climb[0]

    search_term = input("What was the name of the climb? : ")
    climbs = cur.execute(f"SELECT climbs.id, name, areas.area_name FROM climbs INNER JOIN areas ON areas.id = climbs.area WHERE name LIKE '%{search_term}%';")

    for climb in climbs:
        print(climb)
    search_results = get_int("If your climb showed up, put the ID here. (If not, put '-1')")
    if search_results == -1:
        redo_search = y_n("Try another search?")
        if redo_search is True:
            return climb_search(cur)
        else:
            return climb()
    elif search_results <= newest_climb:
        return search_results
    else:
        print("You gotta play by the rules, dude!")
        return climb_search(cur)

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
    grade_id = get_int("Grade ID (-1 for new amalgam grade, or -2 to search again): ")

    if grade_id == -1:
        return(new_join_grade(cur, new_id, grade))
    elif grade_id == -2:
        return grade_func(cur)
    elif grade_id < new_id:
        if grade_id > 0:
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

def style_func() -> str:
    styles = ["Lead", "TR", "LRS", "TRS", "Solo", "Follow", "Send", "Attempt", "Flash"]

    style = input("In what style did you do the climb? (Lead, TR, Follow, etc. -1 for a list): ")

    if style in styles:
        return style
    elif style == '-1':
        input(f"{styles} Any key to continue.")
        return style_func()
    else:
        input("Looks like you made a typo! Try again :)")
        return style_func()

def success_func() -> str:
    successes = ["Fell/Hung", "Pinkpoint", "Redpoint", "Onsight", "Flash", "Clean", "Attempt"]

    success = input("How did you do? (Onsight, Redpoint, Fell/Hung, etc. -1 for a list): ")

    if success in successes:
        return success
    elif success == '-1':
        input(f"{successes} Any key to continue.")
        return success_func()
    else:
        input("Looks like you made a typo! Try again :)")
        return success_func()

def notes_func() -> str:
    notes = input("Any notes for this tick? : ")

    if notes == '':
        return "-1"
    else:
        return notes

def partner_func(cur: Cursor) -> int:
    res = cur.execute("SELECT id FROM climbed_partners ORDER BY id DESC;")
    last_partner_amalgam = res.fetchone()
    new_amalgam_id = last_partner_amalgam[0] + 1

    partner_search_param = input("Search for your partner here! If you haven't climbed with them before, enter -1 for new partner or new partner group: ")

    while partner_search_param == '':
        print("Oops, looks like you hit enter too soon! Try again :)")
        return partner_func(cur)
    if partner_search_param == '-1':
        return new_amalgam_func(cur, new_amalgam_id)
    else:
        return easy_partner_search(cur, partner_search_param, new_amalgam_id)
    
def new_amalgam_func(cur: Cursor, new_amalgam_id: int) -> int:
    ### Receives the user input to build the amalgam join tables ###

    complete = False
    first_search = True
    partners = []

    while complete is False:
        if first_search is True:
            search = input("Partner search (-1 for new partner): ")
            while search == '':
                print("Oops! Looks like you hit enter too soon. Try again :)")
                return new_amalgam_func(cur, new_amalgam_id)
            if search == "-1":
                partners.append(new_partner(cur))
            else:
                partners.append(partner_search(cur, search))
            first_search = False
        else:
            search = input("Partner search (-1 for new partner, -2 if you're done): ")
            while search == '':
                print("Oops! Looks like you hit enter too soon. Try again :)")
                return new_amalgam_func(cur, new_amalgam_id)
            if search == "-1":
                partners.append(new_partner(cur))
            elif search == "-2":
                new_amalgam(cur, new_amalgam_id, partners)
                complete = True
            else:
                partners.append(partner_search(cur, search))

    return new_amalgam_id

def new_amalgam(cur: Cursor, new_amalgam_id: int, partners: list) -> int:
    ### Creates the join tables for new partners or partner groups ###

    # Start with climbed_partners with the join_id and notes
    notes = ""
    first_item = True
    for partner in partners:
        if first_item is True:
            notes = f"{partner[1]} {partner[2]}"
            first_item = False
        else:
            notes += f", {partner[1]} {partner[2]}"
    cur.execute(f"""
        INSERT INTO climbed_partners VALUES
            ({new_amalgam_id}, "{notes}")
    """)

    # climbed_with next with as many rows as partners, linking the new_amalgam_id with each partner_id
    new_data = []
    for partner in partners:
        new_data.append((new_amalgam_id, partner[0]))    
    cur.executemany("INSERT INTO climbed_with VALUES(?, ?)", new_data)

    return new_amalgam_id
    
def new_partner(cur: Cursor) -> list:
    ### Creates a new partner entry in partners table and returns the partner_id, first, and last name ###
    res = cur.execute("SELECT id FROM partners ORDER BY id DESC;")
    last_partner_id = res.fetchone()
    new_id = last_partner_id[0] + 1

    fname = input("What's their first name? : ")

    lname = input("What's their last name? : ")

    notes = input("Any notes? : ")

    cur.execute(f"""
        INSERT INTO partners VALUES
            ({new_id}, "{fname}", "{lname}", "{notes}")
    """)

    new_partner = [new_id, fname, lname]

    return(new_partner)

def partner_search(cur: Cursor, search: str) -> list:
    res = cur.execute("SELECT id FROM partners ORDER BY id DESC;")
    last_partner_id = (res.fetchone())[0]

    res = cur.execute(f"SELECT id, fname, lname, notes FROM partners WHERE fname LIKE '%{search}%' or lname LIKE '%{search}%' ORDER BY fname ASC;")
    results = res.fetchall()

    for partner in results:
        print(partner)

    choice = get_int("Partner ID (-1 to search again, -2 to add new partner)")

    if choice == -1:
        search = input("Partner search: ")
        return partner_search(cur, search)
    elif choice == -2:
        return new_partner(cur)
    elif choice > 0:
        if choice <= last_partner_id:
            res = cur.execute(f"SELECT id, fname, lname FROM partners WHERE id = {choice};")
            partner = res.fetchall()
            return [(partner[0])[0], (partner[0])[1], (partner[0])[2]]
    else:
        print("Oops, it looks like you made a typo! Try again :)")
        return partner_search(cur, search)

def easy_partner_search(cur: Cursor, param: str, new_amalgam_id: int) -> int:
    ### Searches notes field of all amalgams & single partners and returns amalgam id for direct use in ticks partner_id field ###
    # res = cur.execute(f"SELECT * FROM climbed_partners WHERE notes LIKE '%{param}%';")
    # print(res.fetchall())

    partners = cur.execute(f"""SELECT climbing_id, GROUP_CONCAT(fname || ' ' || lname, ', ') AS 'Partner/s' FROM climbed_with INNER JOIN partners ON partners.id = climbed_with.partner_id GROUP BY climbing_id;""")

    for partner in partners:
        if param in partner[1]:
            print(partner)

    partner_id = get_int("Partner ID (-1 to search again, or -2 to create a new partner or amalgam): ")

    if partner_id == -1:
        return partner_func(cur)
    elif partner_id == -2:
        return new_amalgam_func(cur, new_amalgam_id)
    elif partner_id < new_amalgam_id:
        if partner_id > 0:
            return partner_id
    else:
        input("Looks like you made a typo! Try again :)")
        return partner_func(cur)

def client_func(cur: Cursor) -> int:
    res = cur.execute("SELECT id FROM guided ORDER BY id DESC;")
    last_client_amalgam = res.fetchone()
    new_amalgam_id = last_client_amalgam[0] + 1

    client_search_param = input("Enter your clients first name here! (If they're a returning client, enter -1) : ")

    while client_search_param == '':
        print("Oops, looks like you hit enter too soon! Try again :)")
        return client_func(cur)
    if client_search_param == '-1':
        return easy_client_search(cur)
    else:
        return new_client_func(cur, client_search_param)

def new_client_func(cur: Cursor, fname: str) -> int:
    res = cur.execute("SELECT id FROM clients ORDER BY id DESC;")
    new_client_id = (res.fetchone())[0] + 1

    lname = ''
    while lname == '':
        lname = input("Enter your clients last name here (-1 to go back and choose an existing client): ")
    if lname == '-1':
        return client_func(cur)

    client_notes = ''
    while client_notes == '':
        client_notes = input("Enter any notes about them here (-1 to go back and choose an existing client): ")
    if lname == '-1':
        return client_func(cur)

    new_clients = [(new_client_id, fname, lname, client_notes)]
    new_client_id += 1

    more_clients = True
    while more_clients is True:
        more_clients = y_n("Were there any more clients?")
        if more_clients is True:
            new_clients.append(new_client_simple(new_client_id, new_client_id))
            new_client_id += 1
        else:
            new_guided_id = new_guided_item(cur)
            for client in new_clients:
                cur.execute(f"""
                    INSERT INTO clients VALUES
                            ({client[0]}, "{client[1]}", "{client[2]}", "{client[3]}")
                """)

                cur.execute(f"""
                    INSERT INTO guided_client VALUES
                            ({new_guided_id}, {client[0]})
                """)

    return new_guided_id
            
def new_guided_item(cur: Cursor) -> int:
    res = cur.execute("SELECT id FROM guided ORDER BY id DESC;")
    new_guided_id = (res.fetchone())[0] + 1

    company = ''
    while company == '':
        company = input("What outfit abbreviation did you guide for? (ex: SRMG, ARR) : ")

    tip = get_int("How much did they tip?")

    notes = ''
    while notes == '':
        notes = input("How did the day go? What'd you guys get up to? : ")

    cur.execute(f"""
                INSERT INTO guided VALUES
                ({new_guided_id}, "{company}", {tip}, "{notes}")
    """)
    
    return new_guided_id    

def new_client_simple(cur: Cursor, new_client_id: int) -> tuple:
    fname = ''
    while fname == '':
        fname = input("What's this next client's first name? : ")
    
    lname = ''
    while lname == '':
        lname = input("What's their last name? : ")
    
    notes = ''
    while notes == '':
        notes = input("Any notes about them? : ")

    return (new_client_id, fname, lname, notes)

def easy_client_search(cur: Cursor) -> int:
    res = cur.execute("SELECT guided_id FROM guided_client ORDER BY guided_id DESC;")
    last_guided_id = (res.fetchone())[0]

    client_search = input("What was your client's name? : ")

    while client_search == '':
        print("Oops, looks like you hit enter too soon! Try again :)")
        return easy_client_search(cur)
    
    clients = cur.execute(f"""SELECT guided_id, GROUP_CONCAT(fname || ' ' || lname, ', ') AS 'Client/s' FROM guided_client INNER JOIN clients ON clients.id = guided_client.client_id GROUP BY guided_id;""")

    for client in clients:
        if client_search in client[1]:
            print(client)
    
    choice = get_int("Enter client ID (-1 to search again, -2 to add new client)")

    if choice == -1:
        return easy_client_search(cur)
    elif choice == -2:
        return None
    elif choice > 0:
        if choice <= last_guided_id:
            return choice
    else:
        print("Oops, looks like you made a typo! Try again :)")
        return easy_client_search(cur)

def dev() -> bool:
    print('(1) Did you do some RAD CLIMBING??')
    print('(2) Or are you updating the DB?')
    dev_env = input('(1 or 2) : ')
    if dev_env == '1':
        return False
    elif dev_env == '2':
        return True
    else:
        print('Oops, looks like you made a typo! Try again :)')
        return dev()

con = sqlite3.connect("ticks")
cur = con.cursor()
new_ticks = []

cur.execute("PRAGMA foreign_keys = ON;")

res = cur.execute("SELECT id FROM ticks ORDER BY id DESC;")
last_tick = res.fetchone()
new_tick_id = last_tick[0] + 1
dev = dev()

if dev is False:
    new_ticks = day_out(cur, new_ticks, new_tick_id)

    cur.executemany("INSERT INTO ticks VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", new_ticks)

    con.commit()

    print("Hell yeah dude!! Here's to another great day of climbing :)")
else:
    print("Let's update that there database!")