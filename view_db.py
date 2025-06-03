import sqlite3
from tabulate import tabulate

def view_database():
    conn = sqlite3.connect('farm_data.db')
    c = conn.cursor()
    
    print("\n📊 DATABASE CONTENT:")
    c.execute('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 5')
    rows = c.fetchall()
    
    headers = ["ID", "Timestamp", "Soil", "Temp", "Wind", "Humidity", "Command"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    conn.close()

if __name__ == "__main__":
    view_database()

# أضف هذا إلى ملف view_db.py
import matplotlib.pyplot as plt
import pandas as pd

def plot_sensor_data():
    conn = sqlite3.connect('farm_data.db')
    df = pd.read_sql("SELECT * FROM sensor_data", conn)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    plt.figure(figsize=(12,6))
    plt.plot(df['timestamp'], df['soil'], label='رطوبة التربة')
    plt.plot(df['timestamp'], df['temp'], label='درجة الحرارة')
    plt.legend()
    plt.savefig('sensor_trends.png')
