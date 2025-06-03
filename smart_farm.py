import paho.mqtt.client as mqtt
import json
import sqlite3
from datetime import datetime

# 1. Setup Database
conn = sqlite3.connect('farm_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sensor_data 
            (id INTEGER PRIMARY KEY, 
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
             soil REAL, temp REAL, wind REAL, humidity REAL,
             command TEXT)''')
conn.commit()
conn.close()

# 2. MQTT Callback Function
def on_message(client, userdata, msg):
    try:
        # Parse incoming data
        data = json.loads(msg.payload.decode())
        
        # Print received data
        print("\n" + "="*50)
        print(f"📡 DATA RECEIVED [{datetime.now().strftime('%H:%M:%S')}]:")
        print(f"  - Soil Moisture: {data['soil']}%")
        print(f"  - Temperature: {data['temp']}°C")
        print(f"  - Wind Speed: {data['wind']}%")
        print(f"  - Air Humidity: {data['humidity']}%")
        
        # Make decision
        if data['soil'] < 30: 
            command = "PUMP_ON"
            print("  ⚠️ DECISION: Pump ON (Dry soil)")
        elif data['temp'] > 35 and data['humidity'] < 40: 
            command = "PUMP_ON"
            print("  ⚠️ DECISION: Pump ON (High temperature)")
        else: 
            command = "PUMP_OFF"
            print("  ✅ DECISION: Pump OFF (Normal conditions)")
        
        # Save to database
        conn = sqlite3.connect('farm_data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO sensor_data 
                    (soil, temp, wind, humidity, command) 
                    VALUES (?, ?, ?, ?, ?)''',
                    (data['soil'], data['temp'], data['wind'], 
                     data['humidity'], command))
        conn.commit()
        conn.close()
        
        # Send command back to device
        client.publish("farm/commands", command)
        print(f"  📤 COMMAND SENT: {command}")
        print("="*50)
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

# 3. Main Execution
if __name__ == "__main__":
    # Create MQTT client
    client = mqtt.Client()
    client.connect("broker.hivemq.com", 1883)
    client.subscribe("farm/sensors")
    client.on_message = on_message
    
    print("🚀 Smart Farm System ACTIVE")
    print("⏳ Waiting for device data...")
    client.loop_forever()