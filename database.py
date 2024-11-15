import sqlite3
from tabulate import tabulate

# Connect the database (or create it if it doesn't exist)
connection = sqlite3.connect("legally-blonde.db")

# Create the cursor
cursor = connection.cursor()

# Create tables if they don't already exist
cursor.execute("""
        CREATE TABLE IF NOT EXISTS
            characters (
            charId INTEGER PRIMARY KEY AUTOINCREMENT,
            fName TEXT,
            lName TEXT,
            title TEXT,
            suffix TEXT
            )""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS
            alias (
            aliasId INTEGER PRIMARY KEY AUTOINCREMENT,
            alias TEXT
            )""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS
            char_has_alias (
            charAliasId INTEGER PRIMARY KEY AUTOINCREMENT,
            charId INTEGER,
            aliasId INTEGER,
            FOREIGN KEY (charId) REFERENCES characters(charId),
            FOREIGN KEY (aliasId) REFERENCES alias(aliasId)
            )""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS
            actors (
            actorId INTEGER PRIMARY KEY AUTOINCREMENT,
            fName TEXT NOT NULL,
            lName TEXT NOT NULL
            )""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS
            actor_is_char (
            acId INTEGER PRIMARY KEY AUTOINCREMENT,
            actorId INTEGER,
            charId INTEGER,
            FOREIGN KEY (actorId) REFERENCES actors(actorId),
            FOREIGN KEY (charId) REFERENCES characters(charId)
            )""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS
            productions (
            prodId INTEGER PRIMARY KEY AUTOINCREMENT,
            prodName TEXT NOT NULL,
            prodStartYr INT NOT NULL,
            prodEndYr INT
            )""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS
            shows (
            showId INTEGER PRIMARY KEY AUTOINCREMENT,
            prodId INTEGER,
            date DATE,
            time TEXT,
            location TEXT,
            FOREIGN KEY (prodId) REFERENCES productions(prodId)
            )""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS
            cast_list (
            castListId INTEGER PRIMARY KEY AUTOINCREMENT,
            showId INTEGER,
            acId INTEGER,
            type TEXT,
            FOREIGN KEY (showId) REFERENCES shows(showId),
            FOREIGN KEY (acId) REFERENCES actor_is_char(acId)
            )""")


def get_qmarks(values):
    return ", ".join("?" for _ in values)


def view_table_option(table):
    """
    Request if the user would like to view the table to get IDs.
    """

    choice = input(f"\nShow the {table.upper()} table to get IDs (Y/N)? ").lower()

    if choice == "y":
        view_data(table)
    elif choice == "n":
        return


def continuous_data(table):
    """
    Create a loop for the user to continuously add large amounts of data.
    """
    cont = "y"

    while cont == "y":
        add_data(table)
        cont = input("Continue (Y/N)? ").lower()


def view_data(table):
    """
    Allow user to view the data.
    """
    if table == "characters":
        # View characters
        cursor.execute(f"SELECT * FROM {table}")
        headers = ["ID", "fName", "lName", "Title", "Suffix"]
    elif table == "alias":
        # View alias
        cursor.execute(f"SELECT * FROM {table}")
        headers = ["ID", "alias"]
    elif table == "char_has_alias":
        # View char/alias
        cursor.execute(f"SELECT * FROM {table}")
        headers = ["ID", "charId", "aliasId"]
    elif table == "actors":
        # View actors
        cursor.execute(f"SELECT * FROM {table}")
        headers = ["ID", "fName", "lName"]
    elif table == "actor_is_char":
        # View actor/char relationship
        cursor.execute(f"""
                    SELECT ac.acid, a.actorid, a.fname || ' ' || a.lname, 
                    c.charid, c.title || ' ' || c.fname || ' ' || c.lname || ' ' || c.suffix
                    FROM actor_is_char ac
                    INNER JOIN actors a
                    ON ac.actorId = a.actorId
                    INNER JOIN characters c
                    ON ac.charId = c.charId
                    """)
        headers = ["ID", "actorId", "actorName", "charId", "charName"]
    elif table == "productions":
        # View productions
        cursor.execute(f"SELECT * FROM {table}")
        headers = ["ID", "prodName", "prodStartYr", "prodEndYr"]
    elif table == "shows":
        # View shows
        cursor.execute(f"SELECT * FROM {table}")
        headers = ["ID", "prodId", "date", "time", "location"]
    elif table == "cast_list":
        # View cast list
        cursor.execute(f"SELECT * FROM {table}")
        headers = ["ID", "showId", "acId", "type"]
    records = cursor.fetchall()
    print(tabulate(records, headers, tablefmt="grid"))


def add_data(table):
    """
    Allow user to add data to the database.
    """
    if table == "characters":
        # Need to know first name, last name, and title
        fName = input("\nEnter the character's first name: ")
        if fName == "":
            fName = ""
        lName = input("Enter the character's last name: ")
        if lName == "":
            lName = ""
        title = input("Enter the character's title: ")
        if title == "":
            title = ""
        suffix = input("Enter the character's suffix: ")
        if suffix == "":
            suffix = ""

        values = [None, fName, lName, title, suffix]
    elif table == "alias":
        # Need to know the alias
        alias = input("\nEnter the alais: ")

        values = [None, alias]
    elif table == "char_has_alias":
        # Need to know the aliasId and charId
        # Ask the user if they'd like to see the data for IDs
        # Ask the user if they'd like to see the data for IDs
        view_table_option("characters")
        charId = input("\nEnter the character ID: ")

        view_table_option("alias")
        aliasId = input("\nEnter the alais ID: ")

        values = [None, charId, aliasId]
    elif table == "actors":
        # Need to know first name and last name
        fName = input("\nEnter the actor's first name: ")
        lName = input("Enter the actor's last name: ")

        values = [None, fName, lName]
    elif table == "actor_is_char":
        # Need to know the actorId, charId, prodId, type
        # Ask the user if they'd like to see the data for IDs
        view_table_option("actors")
        actorId = input("\nEnter the actorId: ")

        # Ask the user if they'd like to see the data for IDs
        view_table_option("characters")
        charId = input("\nEnter the charId: ")

        values = [None, actorId, charId]
    elif table == "productions":
        # Need to know the name, start year, and end year
        prodName = input("\nWhat is the name of the production? ")
        prodStartYr = input("What year did the production start? ")
        prodEndYr = input("What year did the production finish (press enter if not applicable)? ")

        values = [None, prodName, prodStartYr, prodEndYr]
    elif table == "shows":
        # Need to know the prodId, date, and location
        # Ask the user if they'd like to see the data for IDs
        view_table_option("productions")

        prodId = input("\nWhat production (ID) is the show part of? ")
        date = input("What date was the show (YYYY-MM-DD)? ")
        time = input("When was the show (M for matinee/E for evening)? ")
        location = input("Where was the show located? ")

        values = [None, prodId, date, time, location]
    elif table == "cast_list":
        # Need to know the showId, acId, and type
        # Ask the user if they'd like to see the data for IDs
        view_table_option("shows")
        showId = input("\nWhat show (ID) is related? ")

        # Ask the user if they'd like to see the data for IDs
        view_table_option("actor_is_char")
        acId = input("\nWhat actor/char (ID) is part of this show? ")

        type = input("What type was their role (actor/understudy/standby/emergency cover, etc)? ")

        values = [None, showId, acId, type]
    else:
        print("That table does not exist. Check your spelling or add it to the database.")
    
    # Get ?s for the length of the tuple
    qmarks = get_qmarks(values)
    # Add the data to the specified table
    cursor.execute(f"INSERT INTO {table} VALUES ({qmarks})", values)
    connection.commit()
    print(f"\nAdded data to the {table.upper()} table.")


def delete_data():
    """
    Allow user to delete data.
    """
    # Find out what table they would like to delete from
    table = input("\nWhat table would you like to delete data from? ")

    # Display all of the data that the user requests to better know what to update from
    view_data(table)

    if table == "characters":
        # Delete from characters
        charId = int(input("\nWhat is the ID of the character you would like to delete? "))

        values = [charId,]

        where = f"WHERE charId = {charId}"
    elif table == "alias":
        # Delete from alias
        aliasId = int(input("\nWhat is the ID of the alias you would like to delete? "))

        values = [aliasId,]

        where = f"WHERE aliasId = {aliasId}"
    elif table == "char_has_alias":
        # Delete from char_has_alias
        charAliasId = int(input("\nWhat is the ID of the character/alias you would like to delete? "))

        values = [charAliasId,]

        where = f"WHERE charAliasId = {charAliasId}"
    elif table == "actors":
        # Delete from actors
        actorId = int(input("\nWhat is the ID of the actor you would like to delete? "))

        values = [actorId,]

        where = f"WHERE actorId = {actorId}"
    elif table == "actor_is_char":
        # Delete from actor_is_char
        acId = int(input("\nWhat is the ID of the actor/character relationship you would like to delete? "))

        values = [acId,]

        where = f"WHERE acId = {acId}"
    elif table == "productions":
        # Delete from productions
        prodId = int(input("\nWhat is the ID of the production you would like to delete? "))

        values = [prodId,]

        where = f"WHERE prodId = {prodId}"
    elif table == "shows":
        # Delete from show
        showId = int(input("\nWhat is the ID of the show you would like to delete? "))

        values = [showId,]

        where = f"WHERE showId = {showId}"
    elif table == "cast_list":
        # Delete from show
        castListId = int(input("\nWhat is the ID of the cast listing you would like to delete? "))

        values = [castListId,]

        where = f"WHERE castListId = {castListId}"
    else:
        print("That table does not exist. Check your spelling or add it to the database.")
    
    # Get ?s for the length of the tuple
    qmarks = get_qmarks(values)
    # Remove data from specified table
    cursor.execute(f"DELETE FROM {table} {where} = ({qmarks})", values)
    connection.commit()
    print(f"\nRemoved data from the {table.upper()} table.")


def update_data():
    """
    Allow user to update data.
    """
    table = input("\nWhat table would you like to update data in? ")

    view_data(table)

    if table == "characters":
        # Update character
        charId = input("\nWhat is the ID of the character you would like to update? ")

        # Set the where statement
        where = f"WHERE charId = {charId}"

        cursor.execute(f"SELECT fname, lname, title, alias, suffix FROM {table} {where}")
        # Get the first line of data, that's all we need
        currentinfo = cursor.fetchone()

        print("\nPress enter on any prompt to keep original data.")
        fName = input("\nEnter the character's new first name: ")
        if fName == "":
            fName = currentinfo[0]
        
        lName = input("Enter the character's new last name: ")
        if lName == "":
            lName = currentinfo[1]
        
        title = input("Enter the character's new title: ")
        if title == "":
            title = currentinfo[2]

        suffix = input("Enter the character's new suffix: ")
        if suffix == "":
            suffix = currentinfo[3]

        # Set the tuple
        values = [fName, lName, title, suffix]

        # Set the query
        query = f"SET fName = ?, lName = ?, title = ?, suffix = ?"
    elif table == "alias":
        # Update alias
        aliasId = input("\nWhat is the ID of the alias you would like to update? ")

        # Set the where statement
        where = f"WHERE aliasId = {aliasId}"

        cursor.execute(f"SELECT alias FROM {table} {where}")
        # Get the first line of data, that's all we need
        currentinfo = cursor.fetchone()

        print("\nPress enter on any prompt to keep original data.")
        alias = input("\nEnter the new alias name: ")
        if alias == "":
            alias = currentinfo[0]

        # Set the tuple
        values = [alias,]

        # Set the query
        query = f"SET alias = ?"
    elif table == "char_has_alias":
        # Update char_has_alias
        charAliasId = input("\nWhat is the ID of the alias you would like to update? ")

        # Set the where statement
        where = f"WHERE charAliasId = {charAliasId}"

        cursor.execute(f"SELECT charId, aliasId FROM {table} {where}")
        # Get the first line of data, that's all we need
        currentinfo = cursor.fetchone()

        # Ask the user if they'd like to see the data for IDs
        view_table_option("characters")

        print("\nPress enter on any prompt to keep original data.")
        charId = input("\nEnter the new character ID: ")
        if charId == "":
            charId = currentinfo[0]

        # Ask the user if they'd like to see the data for IDs
        view_table_option("alias")

        aliasId = input("\nEnter the new alias ID: ")
        if aliasId == "":
            aliasId = currentinfo[0]

        # Set the tuple
        values = [charId, aliasId]

        # Set the query
        query = f"SET charId = ?, aliasId = ?"
    elif table == "actors":
        # Update actor
        actorId = input("\nWhat is the ID of the actor you would like to update? ")

        # Set the where statement
        where = f"WHERE actorId = {actorId}"

        cursor.execute(f"SELECT fname, lname FROM {table} {where}")
        # Get the first line of data, that's all we need
        currentinfo = cursor.fetchone()

        print("Press enter on any prompt to keep original data.")
        fName = input("\nEnter the actor's first name: ")
        if fName == "":
            fName = currentinfo[0]
        
        lName = input("Enter the actor's last name: ")
        if lName == "":
            lName = currentinfo[1]

        # Set the tuple
        values = [fName, lName]

        # Set the query
        query = f"SET fName = ?, lName = ?"
    elif table == "actor_is_char":
        # Update actor_is_char
        acId = input("\nWhat is the ID of the relationship you would like to update? ")

        # Set the where statement
        where = f"WHERE acId = {acId}"

        cursor.execute(f"SELECT actorId, charId FROM {table} {where}")
        # Get the first line of data, that's all we need
        currentinfo = cursor.fetchone()

        # Ask the user if they'd like to see the data for IDs
        view_table_option("actors")

        print("Press enter on any prompt to keep original data.")
        actorId = input("\nEnter the new actor ID: ")
        if actorId == "":
            actorId = currentinfo[0]
        
        # Ask the user if they'd like to see the data for IDs
        view_table_option("characters")

        charId = input("\nEnter the character ID: ")
        if charId == "":
            charId = currentinfo[1]

        # Set the tuple
        values = [actorId, charId]

        # Set the query
        query = f"SET actorId = ?, charId = ?"
    elif table == "productions":
        # Update productions
        prodId = input("\nWhat is the ID of the production you would like to update? ")

        # Set the where statement
        where = f"WHERE prodId = {prodId}"

        cursor.execute(f"SELECT prodName, prodStartYr, prodEndYr FROM {table} {where}")
        # Get the first line of data, that's all we need
        currentinfo = cursor.fetchone()

        print("Press enter on any prompt to keep original data.")
        prodName = input("\nEnter the new production name: ")
        if prodName == "":
            prodName = currentinfo[0]
    
        prodStartYr = input("Enter the new start year: ")
        if prodStartYr == "":
            prodStartYr = currentinfo[1]

        prodEndYr = input("Enter the new end year: ")
        if prodEndYr == "":
            prodEndYr = currentinfo[2]

        # Set the tuple
        values = [prodName, prodStartYr, prodEndYr]

        # Set the query
        query = f"SET prodName = ?, prodStartYr = ?, prodEndYr = ?"
    elif table == "shows":
        # Update show
        showId = input("\nWhat is the ID of the show you would like to update? ")

        # Set the where statement
        where = f"WHERE showId = {showId}"

        cursor.execute(f"SELECT prodId, date, time, location FROM {table} {where}")
        # Get the first line of data, that's all we need
        currentinfo = cursor.fetchone()

        # Ask the user if they'd like to see the data for IDs
        view_table_option("productions")

        print("Press enter on any prompt to keep original data.")
        prodId = input("\nEnter the new production ID: ")
        if prodId == "":
            prodId = currentinfo[0]

        date = input("Enter the new date (YYYY-MM-DD): ")
        if date == "":
            date = currentinfo[1]

        time = input("Enter the new time (M for matinee, E for evening): ")
        if time == "":
            time = currentinfo[2]

        location = input("Enter the new location: ")
        if location == "":
            location = currentinfo[3]

        # Set the tuple
        values = [prodId, date, time, location]

        # Set the query
        query = f"SET prodId = ?, date = ?, time = ?, location = ?"
    elif table == "cast_list":
        # Update cast list
        castListId = input("\nWhat is the ID of the cast listing you would like to update? ")

        # Set the where statement
        where = f"WHERE castListId = {castListId}"

        cursor.execute(f"SELECT showId, acId, type FROM {table} {where}")
        # Get the first line of data, that's all we need
        currentinfo = cursor.fetchone()

        # Ask the user if they'd like to see the data for IDs
        view_table_option("shows")

        print("Press enter on any prompt to keep original data.")
        showId = input("\nEnter the new show ID: ")
        if showId == "":
            showId = currentinfo[0]

        # Ask the user if they'd like to see the data for IDs
        view_table_option("actor_is_char")

        acId = input("Enter the new actor/character relationship: ")
        if acId == "":
            acId = currentinfo[1]

        type = input("Enter the new type/cover status (understudy, swing, standby, etc.): ")
        if type == "":
            type = currentinfo[2]

        # Set the tuple
        values = [showId, acId, type]

        # Set the query
        query = f"SET showId = ?, acId = ?, type = ?"
    else:
        print("That table dos not exist. Check your spelling or add it to the database.")

    # Update data from specified table
    cursor.execute(f"UPDATE {table} {query} {where}", values)
    connection.commit()
    print(f"\nUpdated data in the {table.upper()} table.")


def query_data():
    """
    Allow user to query data.
    """
    # As a base let's pull up the cast_list for a show

    # Ask the user if they'd like to see the data for IDs
    view_table_option("shows")
    showId = input("\nWhat is the show ID you would like to see the cast list for? ")

    cursor.execute(f"""
                SELECT c.fname || ' ' || c.lname, a.fname || ' ' || a.lname, cl.type
                FROM cast_list cl
                INNER JOIN actor_is_char ac
                ON cl.acId = ac.acId
                INNER JOIN characters c
                ON ac.charId = c.charId
                INNER JOIN actors a
                ON ac.actorId = a.actorId
                WHERE showID = {showId}
                """)
    headers = ["Character", "Actor", "Cover Status"]
    records = cursor.fetchall()
    print(tabulate(records, headers, tablefmt="grid"))


def main():
    """
    The main function of the program
    """
    choice = None
    while choice != -1:
        print("\nWhat would you like to do?")
        print("     1. View data")
        print("     2. Add data")
        print("     3. Query data")
        print("     4. Delete data")
        print("     5. Update data")
        print("     6. Exit")
        choice = int(input("> "))

        if choice == 1:
            table = input(("\nWhat table would you like to view? ")).lower()
            view_data(table)
        elif choice == 2:
            table = input("\nWhat table do you want to add to? ").lower()
            cont = input("Will you be adding more than one item (Y/N)? ").lower()
            if cont == "y":
                continuous_data(table)
            elif cont == "n":
                add_data(table)
            else:
                print("Invalid option.")
        elif choice == 3:
            query_data()
        elif choice == 4:
            delete_data()
        elif choice == 5:
            update_data()
        elif choice == 6:
            break
        else:
            print("Not a valid option.")

if __name__ == "__main__":
    main()