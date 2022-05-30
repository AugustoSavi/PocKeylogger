from dotenv import load_dotenv
import smtplib,os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email:

    def __init__(self):
        load_dotenv()
        # Configuração
        self.host = os.getenv('HOST_URL')
        self.port = os.getenv('PORT')
        self.user = os.getenv('USUARIO')
        self.password = os.getenv('SENHA')
        
        # Criando objeto
        print('Criando objeto servidor...')
        self.server = smtplib.SMTP(self.host, self.port)
        self.login()


    def login(self):
        # Login com servidor
        print('Login...')
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.user, self.password)

    def createMessage(self,message):
        # Criando mensagem
        self.message = 'Olá, mundo!'
        print('Criando mensagem...')
        self.email_msg = MIMEMultipart()
        self.email_msg['From'] = self.user
        self.email_msg['To'] = os.getenv('EMAIL_DE_DESTINO')
        self.email_msg['Subject'] = os.getlogin()
        print('Adicionando texto...')
        self.email_msg.attach(MIMEText(message, 'plain'))

    def sendMessage(self):
        # Enviando mensagem
        print('Enviando mensagem...')
        self.server.sendmail(self.email_msg['From'], self.email_msg['To'], self.email_msg.as_string())
        print('Mensagem enviada!')

    def closeServer(self):
        # fechando o server
        print('closing Server...')
        self.server.quit()