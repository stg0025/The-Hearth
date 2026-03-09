from db import get_connection
import pandas as pd

def export_user_data():
    conn = get_connection()
    query = "SELECT id, name, addiction_type FROM users"
    df = pd.read_sql_query(query, conn)
    df.to_csv("users.csv", index=False)
    conn.close()

def export_session_data():
    conn = get_connection()
    query = "SELECT users.name, sessions.emotion, sessions.unmet_need, sessions.relapsed, sessions.notes FROM sessions INNER JOIN users ON sessions.user_id = users.id"
    df = pd.read_sql_query(query, conn)
    df.to_csv("sessions.csv", index=False)
    conn.close()

def export_intensity_log():
    conn = get_connection()
    query = "SELECT sessions.emotion, sessions.timestamp, intensity_log.minute, intensity_log.intensity FROM intensity_log INNER JOIN sessions ON intensity_log.session_id = sessions.id"
    df = pd.read_sql_query(query, conn)
    df.to_csv("intensity_log.csv", index=False)
    conn.close()

if __name__ == "__main__":
    export_user_data()
    print("User data exported to users.csv")
    export_session_data()
    print("Session data exported to sessions.csv")
    export_intensity_log()  
    print("Intensity log data exported to intensity_log.csv")
    print("Data exported to CSV files.")