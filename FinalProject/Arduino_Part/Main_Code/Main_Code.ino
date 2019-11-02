
 
#include <SPI.h>
#include <MFRC522.h>
 
#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.


String code_1 = "42 26 20 10";
String incoming_code ;
int pages_of_code_1 = 2;
int incoming_pages ;
int def_pages ;

 
void setup() 
{
  Serial.begin(9600);   // Initiate a serial communication
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522 

}
void loop() 
{  while (Serial.available())    
{   digitalWrite(7,LOW);



  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) return;
 
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) return;
 
  //Show UID on serial monitor
  
  String content= "";
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {  content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX)); }
     content.toUpperCase();
     incoming_code = content.substring(1);


// read the rfid code
incoming_pages = Serial.read(); 
if (incoming_code == code_1 )
 { def_pages = pages_of_code_1 - incoming_pages ;
  if ( def_pages >= 0 )
    { pages_of_code_1 = pages_of_code_1 - incoming_pages ;
      Serial.println("P") ;
    }
  else 
  { pages_of_code_1 = 0 ;
    Serial.println("NP") ;
    }
   
 }} 

 }


