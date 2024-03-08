# RoTTSana 

### What is this?
RoTTSana is a real-time speech translator from Spanish to Quechua and viceversa.
It contains more than 20 different Quechua region dialects 

### How does it work
1. Records the voice of the person talking
2. Makes a Speech-to-Text recognition in the desired language 
3. Translates the resultant text with Cloud translate 
4. The translated text is passed through a Text-to-Speech recognition
5. The generated audio is played automatically

### Tools and services
- Cloud Translate API
- Facebook MMS Models (STT: 1b-all)
- Facebook MMS Models (TTS: Diffferent Quechua dialects)
- Facebook MMS Models (TTS: Spanish)



### Regions Supported
- Ayacucho
- Cajamarca
- Canar
- Cuzco
- Eastern Apurimac
- Huallaga
- Huamelies
- Huaylas
- Huaylla Wanca
- Lambayeque
- Margos Lauricocha
- Napo
- North Bolivia
- North Junin
- Northern Conchucos
- Northern Pastaza
- Panao
- Salasaca Highland
- San Martin
- South Bolivia
- Southern Conchucos
- Tena Lowland
        

Note: When the program asks you to enter the Quechua region dialect. Type the region supported in minor cases and with dashes in case its double worded.

Ex: 

    Enter the Quechua region dialect you wanna use: san-martin

### Usage
1. Install all the dependencies


        pip install -r requirements.txt
    
    
2. Create a Service Account Permission credential of Cloud Translate API, downloading the json file and placing the path inside the `backend/functions.py` file: 
    
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jose/Downloads/massive-catfish-411714-89ecb4eed938.json"
    
    Get it following: https://cloud.google.com/translate/docs/authentication
    
    
3. Run the endpoints inside the backend folder

        cd backend
        python endpoints.py
    
    
4. In another terminal run the prototype.py inside the project root

        python prototype.py
    