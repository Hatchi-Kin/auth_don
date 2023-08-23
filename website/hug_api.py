from hugchat import hugchat
from hugchat.login import Login
from dotenv import load_dotenv
import os

load_dotenv()

class Narrator():

    def __init__(self):
        self.__MAIL= os.getenv("HUGGING_MAIL")
        self.__PSWD= os.getenv("HUGGING_PSWD")
        
    def __get_mail(self):
        return self.__MAIL
    
    def __get_pswd(self):
        return self.__PSWD

    def get_hugging_answer(self, message):
        # login avec le compte Hugging Face
        mail = self.__get_mail()
        passwd = self.__get_pswd()
        sign = Login(mail, passwd)
        cookies = sign.login()
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        pre_prompt = "Answer to this in 60 words or less: "
        prompt = f"{pre_prompt}\n{message}"
        return chatbot.chat(prompt)
    
    