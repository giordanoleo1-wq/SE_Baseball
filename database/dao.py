from database.DB_connect import DBConnect
from model.appearence import Appearence
from model.salary import Salary
from model.team import Team


class DAO:
    @staticmethod
    def read_all_teams():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM team """

        cursor.execute(query)

        for row in cursor:
            result.append(Team(row['id'],
                               row['year'],
                               row['team_code'],
                               row['name']))


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_all_salaries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM salary """

        cursor.execute(query)

        for row in cursor:
            result.append(Salary(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def read_all_appearences():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM appearance """

        cursor.execute(query)

        for row in cursor:
            result.append(Appearence(row['id'],
                                     row['year'],
                                     row['team_code'],
                                     row['team_id'],
                                     row['player_id']))


        cursor.close()
        conn.close()
        return result