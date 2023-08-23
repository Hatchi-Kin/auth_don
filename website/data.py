from .connection import Connection
# from connection import Connection

class Data:

    def get_all_data():
        # get all the data in order from higest value in pledges_euro to lowest
        cursor = Connection.connect()
        cursor.execute("SELECT * FROM jackpot")
        jackpot = []
        for row in cursor:
            jackpot.append(row)
        Connection.disconnect()
        return jackpot
    

    def get_top_ten():
        # get the top 10 pledges
        cursor = Connection.connect()
        cursor.execute("SELECT * FROM jackpot ORDER BY pledges_euro DESC LIMIT 10")
        jackpot10 = []
        for row in cursor:
            jackpot10.append(row)
        Connection.disconnect()
        return jackpot10
    

    def get_total_pledges():
        cursor = Connection.connect()
        cursor.execute("SELECT SUM(pledges_euro) FROM jackpot")
        total_pledges = round( cursor.fetchone()[0] , 2 )
        Connection.disconnect()
        return total_pledges


    def save_entry(name, last_name, email, pledges_euro):
        cursor = Connection.connect()
        query = f"INSERT INTO jackpot(name, last_name, email, pledges_euro) VALUES('{name}', '{last_name}', '{email}', {pledges_euro})"
        cursor.execute(query)
        Connection.disconnect()
        return True
    

    def get_msg():
        cursor = Connection.connect()
        cursor.execute("SELECT * FROM fight_chat ORDER BY time ASC LIMIT 10")
        name_message = []
        for row in cursor:
            name = row[1]
            msg = row[2]
            name_message.append([name, msg])
        Connection.disconnect()
        return name_message
    

    def save_msg(name, msg):
        cursor = Connection.connect()
        query = f"INSERT INTO fight_chat(avatar, message) VALUES('{name}', '{msg}')"
        cursor.execute(query)
        Connection.disconnect()
        return True


    