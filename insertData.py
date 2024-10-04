import pandas as pd
import sqlite3

conn = sqlite3.connect('data.db')

def insert_data(df):
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""INSERT INTO hlaup (vidburdur, nafn, upphaf, endir, fjoldi) VALUES (?, ?, ?, ?, ?)""", (row['vidburdur'], row['nafn'], row['upphaf'], row['endir'], row['fjoldi']))

    conn.commit()

def read_csv():
    return pd.read_csv('hlaup.csv')

def main():
    df = read_csv()
    insert_data(df)

if __name__ == "__main__":
    main()