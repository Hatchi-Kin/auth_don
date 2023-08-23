import os
import datetime
import requests
from ics import Calendar
from dotenv import load_dotenv

load_dotenv()
ICS_URL = os.getenv('ICS_URL')

class MyIcs:
    def __init__(self):
        self.__location = ""
        self.__horaire = ""
        self.__intervenant = ""
        self.__descript = ""
        self.__date = ""

    def __str__(self):
        return f"Le {self.__date}, de {self.__horaire} salle(s) {self.__location}, avec {self.__intervenant}.\n{self.__descript}"
    
    def get_location(self):
        return self.__location
    
    def get_horaire(self):
        return self.__horaire
    
    def get_intervenant(self):
        return self.__intervenant
    
    def get_descript(self):
        return self.__descript
    
    def get_date(self):
        return self.__date
    

    def get_the_right_room(commande: str) -> list:
        response = requests.get(ICS_URL)
        calendar = Calendar(response.text)
        date = datetime.date.today()   ### - datetime.timedelta(days=6) ######## debug #########
        if commande == "matin":
            matin_aprem = 0
        elif commande == "aprem":
            matin_aprem = 1
        elif commande == "demain":
            date = date + datetime.timedelta(days=1)
            matin_aprem = 0 
        else:
            message = "Fichtre !"
            return message  
        events = [event for event in calendar.events if event.begin.date() == date]
        if events:
            events.sort(key=lambda x: x.begin.time())
            event = events[matin_aprem]
            description = event.description.encode('latin-1').decode('utf-8')
            location = event.location.encode('latin-1').decode('utf-8')
            horaire = event.begin.time().strftime("%H:%M")
            intervenant = ""
            descript = ""
            for line in description.splitlines():
                if line.startswith("- Intervenant(s) :"):
                    intervenant += line
                if line.startswith("- Description :"):
                    descript += line
            return [location, horaire, intervenant[2:], descript[2:], date.strftime("%A %d %B")]
    


    def set_all_myics(self, commande: str):
        event = MyIcs.get_the_right_room(commande)
        if event is not None:
            self.__location = event[0] if event[0] is not None else "Pas d'infos"
            self.__horaire = event[1] if event[1] is not None else "Peut-être un bug?"
            interv = event[2] if event[2] is not None else "T'es pas en télé-travail?"
            self.__intervenant = interv[17:] if len(interv) > 17 else "t'as des vacances?"
            desc = event[3] if event[3] is not None else "En tout cas..."
            self.__descript = desc[14:] if len(desc) > 14 else "Aucune idées..."
            self.__date = event[4] if event[4] is not None else "Moi j'ai pas tant que ça d'infos"
        else:
            self.__location = "Pas d'infos"
            self.__horaire = "Peut-être un bug?"
            self.__intervenant = "T'es pas en télé-travail?"
            self.__descript = "Aucune idées..."
            self.__date = "Moi j'ai pas tant que ça d'infos"

