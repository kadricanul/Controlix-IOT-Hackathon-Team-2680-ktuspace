#include "EspMQTTClient.h"

EspMQTTClient client(
  "wifissid",
  "wifipass",
  "" ,//mqtt broker  
  "username",   
  "pass",    
  "TestClient",    
  1883              
);


float gpslat[27] = {
41.476126,
41.476576,
41.476841,
41.477170,
41.477628,
41.477917,
41.478054,
41.478271,
41.478223,
41.478207,
41.478352,
41.480024,
41.479405,
41.480233,
41.479895,
41.479155,
41.478054,
41.477154,
41.477082,
41.475949,
41.475314,
41.474349,
41.473433,
41.472854,
41.472058,
41.473031
};
float gpslong[27] = {
28.287878,
28.288350,
28.288640,
28.289194,
28.289999,
28.290439,
28.291051,
28.291716,
28.292317,
28.292982,
28.293433,
28.295032,
28.296834,
28.297757,
28.299956,
28.300503,
28.298636,
28.298293,
28.296823,
28.297027,
28.297714,
28.298637,
28.299270,
28.300118,
28.298981,
28.293863
};
float bazlat[10] = {
41.479909,
41.476800,
41.480216,
41.479438,
41.481190,
41.478296,
41.476102,
41.473634,
41.471375
};
float bazlong[10] = {
28.290419,
28.291446,
28.294600,
28.298834,
28.296506,
28.298738,
28.298727,
28.297579,
28.295948
};
float bazistasyonu_mesafe[10];
float enkucuk = 999999.99;

void onConnectionEstablished()
{
  // Subscribe to "mytopic/test" and display received message to Serial
  client.subscribe("teams/1000", [](const String & payload) {
    Serial.println(payload);
  });

 

  // Publish a message to "mytopic/test"
  client.publish("teams/1000", "busonmus"); // You can activate the retain flag by setting the third parameter to true

  // Execute delayed instructions
 
}

void setup() {
  Serial.begin(115200);
  client.enableDebuggingMessages(); 
  client.enableHTTPWebUpdater(); 
  client.enableOTA(); 
  client.enableLastWillMessage("TestClient/lastwill", "");  

}
int b;
void loop() {
  client.loop();
   Serial.println(b);
   String telem1 = telemetri(b);
   client.publish("teams/1000", telem1); 
 Serial.println(telem1);
 
  b++;
  delay(1000);
  if(b == 26){while(1);}
}
int bazistasyonu(int sayac,float gpslat,float gpslong){
    for(int i;i < 9;i++){
       bazistasyonu_mesafe[i] = distanceBetween(gpslat,gpslong,bazlat[i],bazlong[i]); 
       Serial.print(bazistasyonu_mesafe[i]);
       Serial.print( "    ");
      
      }
      Serial.println();
      
      int enkucukno;
     for(int a;a<9;a++){
        if(bazistasyonu_mesafe[a] < enkucuk ){
            
            enkucuk = bazistasyonu_mesafe[a];
            Serial.print(enkucuk);
            Serial.print("    ");
            enkucukno = a;
          }
      }
      Serial.print("numarası");
      Serial.println(enkucukno);
      enkucuk = 999999;
      return enkucukno; 
  }
String telemetri(int sayac){

    int mesafe = bazistasyonu(sayac,gpslat[sayac],gpslong[sayac]);
    //if (sayac < 0 )sayac = 0;
    //int mesafe;
    String telemarray[5];
    
    if(sayac < 10){
         telemarray[0] = String(gpslat[sayac],6);
         telemarray[1] = String(gpslong[sayac],6);
         telemarray[2] = String(gpslat[sayac],6);
         telemarray[3] = String(gpslong[sayac],6);
         telemarray[4] = String(mesafe);
          
        
      }
      else{
         telemarray[0] = "0.000000";
         telemarray[1] = "0.000000";
         telemarray[2] = String(gpslat[sayac],6);
         telemarray[3] = String(gpslong[sayac],6);
         telemarray[4] = String(mesafe);
        }
        String telem = telemarray[0]+","+telemarray[1]+","+telemarray[2]+","+telemarray[3]+","+telemarray[4];
        return telem;
  }

double distanceBetween(double lat1, double long1, double lat2, double long2)
{
 
  double delta = radians(long1-long2);
  double sdlong = sin(delta);
  double cdlong = cos(delta);
  lat1 = radians(lat1);
  lat2 = radians(lat2);
  double slat1 = sin(lat1);
  double clat1 = cos(lat1);
  double slat2 = sin(lat2);
  double clat2 = cos(lat2);
  delta = (clat1 * slat2) - (slat1 * clat2 * cdlong);
  delta = sq(delta);
  delta += sq(clat2 * sdlong);
  delta = sqrt(delta);
  double denom = (slat1 * slat2) + (clat1 * clat2 * cdlong);
  delta = atan2(delta, denom);
 double zort = abs(delta * 6372795);
  return zort;
}
