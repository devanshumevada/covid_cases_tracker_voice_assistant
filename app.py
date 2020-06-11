import requests
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr
import re

class covid_cases_data:
    def __init__(self):
        self.source_url = 'https://www.mohfw.gov.in'
        self.response = requests.get(self.source_url)
        self.soup = BeautifulSoup(self.response.content, 'lxml')
        self.state_data = self.get_state_data()
        self.country_data = self.get_country_data()

    def get_state_data(self):
        op_rows = []
        for row in self.soup.find_all('tr'):
            current_row = []
            for col in row.find_all('td'):
                current_row.append(col)
            op_rows.append(current_row)
        return op_rows

    def get_country_data(self):
        return self.soup.find('div', class_='site-stats-count').find_all('li')

    def get_national_data(self,type_):
        if type_ == 'deaths':
            return int(self.country_data[2].strong.text)
        elif type_ == 'active_cases':
            return int(self.country_data[0].strong.text)
        elif type_ == 'cured':
            return int(self.country_data[1].strong.text)
        elif type_== 'total_confirmed':
            return int(self.state_data[38][5].text)


    def update_data(self):
        self.response = requests.get(self.source_url)
        self.soup = BeautifulSoup(self.response.content, 'lxml')
        self.state_data = self.get_state_data()
        self.country_data = self.get_country_data()

    def get_statewise_data(self, type_, required_state):
        current_state = None
        for state in self.state_data[1:36]:
            if state[1].text.lower() == required_state:
                current_state = state
        
        if type_=='active_cases':
            return int(current_state[2].text)
        elif type_=='cured':
            return int(current_state[3].text)
        elif type_=='deaths':
            return int(current_state[4].text)
        elif type_=='total_confirmed':
            return int(current_state[5].text)

            
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait() 

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
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
                    print('National Pattern matched')
                    answer = d.get_national_data(pattern['type'])
                    speak_answer(answer)
                    break
        
            continue


        for pattern in state_patterns:
            if pattern['pattern'].match(text):
                for state in states:
                    if state in text:
                        answer = d.get_statewise_data(pattern['type'],state) 
                        speak_answer(answer)
                        break

        
        
        

if __name__ == '__main__':
    main()


