import sqlite3

try:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Create operation
    cursor.execute("INSERT INTO `operations` (`user_id`, `operation_name`, `c_name`, `score`) VALUES (?, ?, ?, ?)", (1000, "client", "deep_ua", 30))

    # Count all users
    operations = cursor.execute("SELECT * FROM `operations`")
    print(operations.fetchall())

    # Commit all changes 
    conn.commit()

except sqlite3.Error as error:
    print("Error:", error)

finally:
    if(conn):
        conn.close()