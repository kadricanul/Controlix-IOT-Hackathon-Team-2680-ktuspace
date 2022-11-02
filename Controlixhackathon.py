
import random
import sys
import io
import string
import math
import serial
import pandas as pd
import numpy as np
import folium 
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5 import QtCore, QtWidgets
from paho.mqtt import client as mqtt_client
lat ="22"
longmqtt ="0"
message1 ="12"
lat1 ="0"
long ="2"
mesafe = ""


##your mqtt credentials here#########
broker = ''
port = 1883
topic = ""
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = ''
password = ''
#############################
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}`")
        
        """message1 = msg.payload.decode()
        message1 = message1.split(',')
        global lat 
        global longmqtt
        lat = message1[0] 
        longmqtt2 = message1[1] 
        print(lat)
        print(longmqtt)"""#
       

    
    client.subscribe(topic)
    client.on_message = on_message
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()



class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ktuspace')
        self.window_width, self.window_height = 1920, 1080
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QHBoxLayout()
        self.setLayout(layout)

        
        m = folium.Map(
            location=[40.98464843519320,29.053348730806200], tiles="OpenStreetMap", zoom_start=15
        	
        )
#mesafe = np.array[25]{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,}
        
        yol = pd.DataFrame({'lon':[29.03544533418240,
        29.036173388212900,
        29.037695692834600,
        29.038026687414000,
        29.038688640372400,
        29.038688327994100,
        29.039052435872100,
        29.039912988128400,
        29.040938955844600,
        29.042295698852700,
        29.044215180718000,
        29.046002228427800,
        29.048153119070200,
        29.050204918178800,
        29.053348730806200,
        29.057286525272200,
        29.057021764357800,
        29.061522525066400,
        29.064566710390600,
        29.067578306746100,
        29.069464651617100,
        29.072608501011500,
        29.077009813471400,
        29.079015820585000,
        29.082397627559300,
        29.084209534991800],
        'lat':[40.99324126384470,
        40.99354105416170,
        40.99429050083820,
        40.99364104719800,
        40.99259193470080,
        40.99266697745070,
        40.99196754398640,
        40.99076852550280,
        40.98991923173830,
        40.98887012733340,
        40.98787094016190,
        40.98704658930540,
        40.98587249407660,
        40.98509811171880,
        40.98464843519320,
        40.98434871214200,
        40.98452358058990,
        40.98347437252300,
        40.98279988109310,
        40.98207544050150,
        40.98147585273860,
        40.98077627116070,
        40.97935234879510,
        40.97715877529120,
        40.97325769804460,
        40.97010544624560],}, dtype=str)
        baz = pd.DataFrame({
        'lon':[29.066187158773500,
        29.070102473791500,
        29.071201193111200,
        29.074115819880900,
        29.077794316529700,
        29.079866779376400,
        29.083565751200400,
        29.081105320394800,
        29.087458373863600],
        'lat':[40.982681641602500,
        40.98006517164680,
        40.98246967728620,
        40.98015679950490,
        40.97886956502730,
        40.97550481105550,
        40.97537265292510,
        40.97123228227060,
        40.97175652243600],}, dtype=str)
                
        for i in range(0,len(baz)):
                    folium.Marker(
                        location=[baz.iloc[i]['lat'], baz.iloc[i]['lon']],
                        fill=False,).add_to(m)
                    folium.Circle (
                        radius = 130,
                        location=[baz.iloc[i]['lat'], baz.iloc[i]['lon']],
                        fill=False,
                        color ="red").add_to(m)
                   

        for i in range(0,len(yol)):
                    folium.Circle (
                        radius = 20,
                        location=[yol.iloc[i]['lat'], yol.iloc[i]['lon']],
                        fill=False,
                        color ="black").add_to(m)
                
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

            


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    run()
    myApp = MyApp()
    myApp.show()
    #myApp.repaint()
    
       
    
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')