import requests
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr
import re

class covid_cases_data:
    def __init__(self):
        self.source_url = 'https://api.covid19india.org/data.json'
        self.data = requests.get(self.source_url).json()
        self.state_data = self.get_state_data()
        self.country_data = self.get_country_data()

    def get_state_data(self):
        return self.data['statewise'][1::]

    def get_country_data(self):
        return self.data['statewise'][0]

    def get_national_data(self,type_):
        if type_ == 'deaths':
            return int(self.country_data['deaths'])
        elif type_ == 'active_cases':
            return int(self.country_data['active'])
        elif type_ == 'cured':
            return int(self.country_data['recovered'])
        elif type_== 'total_confirmed':
            return int(self.country_data['confirmed'])
            


    def update_data(self):
        self.data = requests.get(self.source_url).json()
        self.state_data = self.get_state_data()
        self.country_data = self.get_country_data()

    def get_statewise_data(self, type_, required_state):
        current_state = None
        for state in self.state_data:
            if state['state'].lower() == required_state:
                current_state = state
        
        if type_=='active_cases':
            return int(current_state['active'])
        elif type_=='cured':
            return int(current_state['recovered'])
        elif type_=='deaths':
            return int(current_state['deaths'])
        elif type_=='total_confirmed':
            return int(current_state['confirmed'])
            
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait() 

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        #Using text = '' here because using text=None would be problematic as this function returns text.lower()
        text = ''
        try:
            text = r.recognize_google(audio)
        except:
            print('Sorry I am not really sure what you just said! Would you mind repeating it for me please')
    return text.lower()

def speak_answer(answer):
    if answer:
        print(answer)
        speak(str(answer))



def main():
    d = covid_cases_data()
    end_words = ['stop','quit','end']

    states = ['andaman and nicobar islands','andhra pradesh','arunachal pradesh','assam','bihar','chandigarh','chhattisgarh','dadar nagar haveli','delhi','goa','gujarat','haryana','himachal pradesh','jammu and kashmir','jharkhand','karnataka','kerala','ladakh','madhya pradesh','maharashtra','manipur','meghalaya','mizoram','nagaland','odisha','puducherry','punjab','rajasthan','sikkim','tamil nadu','telengana','tripura','uttarakhand','uttar pradesh','west bengal']
    
    nation_patterns = [
        {
            'pattern':re.compile('[\w\s]+ total [\w\s]+ cases'), 
            'type':'total_confirmed'
        },
		
        {
            'pattern':re.compile('[\w\s]+ active cases'), 
            'type':'active_cases'
        },
        
        {
            'pattern':re.compile('[\w\s]+ number [\w\s]+ deaths'), 
            'type':'deaths'
        },
        
        {
            'pattern':re.compile('[\w\s]+ discharged'),
            'type':'cured'
        }
    ]

    state_patterns = [
        {
            'pattern':re.compile('[\w\s]+ confirmed cases [\w\s]+state'),
            'type':'total_confirmed'
        },

        {
            'pattern':re.compile('[\w\s]+ deaths [\w\s]+state'),
            'type':'deaths'
        },

        {
            'pattern':re.compile('[\w\s]+ active cases [\w\s]+state'),
            'type':'active_cases'
        },

        {
            'pattern':re.compile('[\w\s]+ discharged [\w\s]+state'),
            'type':'cured'
        }
    ]

    while True:
        print("Welcome... Please speak now")
        text = speech_to_text()
        print(f'You just said: {text}')

        if text in end_words:
            print("Goodbye!")
            break
        
        if text == 'update':
            d.update_data()
            continue

        answer = None

        if 'state' not in text:
            for pattern in nation_patterns:
                if pattern['pattern'].match(text):
                    print('Nation specific command detected')
                    answer = d.get_national_data(pattern['type'])
                    speak_answer(answer)
                    break
        
            continue


        for pattern in state_patterns:
            if pattern['pattern'].match(text):
                for state in states:
                    if state in text:
                        print('State specific command detected')
                        answer = d.get_statewise_data(pattern['type'],state) 
                        speak_answer(answer)
                        break

        
        
        

if __name__ == '__main__':
    main()


