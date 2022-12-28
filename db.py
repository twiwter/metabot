import sqlite3

class BotDB:
    def __init__(self, db_file):
        """Connection to database"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exist(self, user_id):
        """Is user exist"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Get id with user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]
    
    def get_user_information(self, user_id):
        """Get all user info wuth help of user_id in TG"""
        result = self.cursor.execute("SELECT * FROM `users` WHERE user_id = ?", (user_id,))
        return result.fetchall()[0]

    def get_all_users(self):
        result = self.cursor.execute("SELECT * FROM `users`").fetchall()
        return result

    def get_all_users_id(self):
        """Get all user_id in table `users`"""
        result = self.cursor.execute("SELECT * FROM `users`").fetchall()
        users_id = []

        for _id in result:
            users_id.append(_id[1])

        return users_id

    def get_all_users_team_info(self, team_name):
        """Getting count of score of team"""
        result = self.cursor.execute("SELECT * FROM `users` WHERE `team_name` = ?", (team_name,))

        return result.fetchall()

    def get_score_team(self, team_name):
        """Getting count of score of team"""
        result = self.cursor.execute("SELECT `score` FROM `users` WHERE `team_name` = ?", (team_name,))
        score = result.fetchall()

        numbers = []

        for i in range(len(score)):
            numbers.append(int(score[i][0]))
        
        return sum(numbers)    

    def get_clients_count_team(self, team_name):
        """Getting count of clients of team"""
        result = self.cursor.execute("SELECT `clients_count` FROM `users` WHERE `team_name` = (?)", (team_name,))
        score = result.fetchall()

        numbers = []

        for i in range(len(score)):
            numbers.append(int(score[i][0]))
        
        return sum(numbers)    

    def get_consults_count_team(self, team_name):
        """Getting count of clients of team"""
        result = self.cursor.execute("SELECT `consults_count` FROM `users` WHERE `team_name` = (?)", (team_name,))
        score = result.fetchall()

        numbers = []

        for i in range(len(score)):
            numbers.append(int(score[i][0]))

        return sum(numbers)     

    def add_operation(self, user_id, operation_name, score, c_name = "", amount = ""):
        """Add record to table `operations`"""
        self.cursor.execute("INSERT OR IGNORE INTO `operations` (`user_id`, `operation_name`, `c_name`, `amount`, `score`) VALUES (?, ?, ?, ?, ?)", (user_id, operation_name, c_name, amount, score,))
        return self.conn.commit()

    def get_information_about_operation(self, user_id, operation_name):
        result = self.cursor.execute("SELECT * FROM `operations` WHERE `user_id` = ? AND `operation_name` = ? AND `date` BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY `date`",
                (user_id,operation_name))
        return result.fetchall()

    def get_last_operation(self):
        """Get last operattion from table `operations`"""
        _id = self.cursor.execute("SELECT MAX(`id`) FROM `operations`")
        result = self.cursor.execute("SELECT * FROM `operations` WHERE `id` = (?)", (_id.fetchone()[0],))
        return result.fetchone()

    def update_score(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `score` = `score` + ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def update_clients_count(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `clients_count` = `clients_count` + ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def update_consults_count(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `consults_count` = `consults_count` + ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def do_sql(self, req):
        if "SELECT" in req:
            result = self.cursor.execute(req)
            return result.fetchall()
        else:
            self.cursor.execute(req)
            return self.conn.commit()

    def close(self):
        """Close connection to database"""
        self.conn.close()

# BotDB("database.db").get_all_user_id()