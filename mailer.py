from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
import threading
import smtplib
Register_mail = '''
MDTextFieldRound:
    icon_left: 'email'
    hint_text: 'Enter the mail here.'
    size_hint_x:None
    pos_hint:{'center_x':.5,'center_y':.6}
    required:True
    width:230
'''
Register_pass = '''
MDTextFieldRound:
    icon_left: 'key-variant'
    hint_text: 'Enter the password here.'
    size_hint_x:None
    pos_hint:{'center_x':.5,'center_y':.5}
    required:True
    width:230
'''
mail_content = '''
MDTextField:
    hint_text: 'Enter the mail here.'
    size_hint_x:None
    pos_hint:{'center_x':.5,'center_y':.43}
    required:True
    helper_text_mode:'on_focus'
    helper_text:"Enter content"
    width:230
'''
mail_reciever = '''
MDTextField:
    hint_text: 'Enter the reciever mail.'
    size_hint_x:None
    pos_hint:{'center_x':.5,'center_y':.35}
    required:True
    helper_text:"Enter mail"
    helper_text_mode:'on_focus'
    width:230
'''
class Mailer(MDApp):
    def build(self):
        self.screen = Screen()
        Window.size = (384, 640)
        self.header = MDLabel(text = "Login Page!",
                                pos_hint = {'center_x':.68,'center_y':.8},
                                font_style = "H3")
        self.status = MDLabel(pos_hint = {'center_x':.95,'center_y':.1},
                                text = "status")
        self.submit_btn = MDRoundFlatButton(text = "start",
                                                pos_hint = {'center_x':.5,'center_y':.2},
                                                size_hint_x = None,
                                                size_hint = (.35,.059),
                                                width = 300,
                                                on_press = self.login_finish)
        self.mail_reciever = Builder.load_string(mail_reciever)
        self.mail_content  = Builder.load_string(mail_content)
        self.mail = Builder.load_string(Register_mail)
        self.screen.add_widget(self.submit_btn)
        self.passw = Builder.load_string(Register_pass)
        self.screen.add_widget(self.header)
        self.screen.add_widget(self.mail_reciever)
        self.screen.add_widget(self.mail_content)
        self.screen.add_widget(self.status)
        self.screen.add_widget(self.mail)
        self.screen.add_widget(self.passw)
        return self.screen
    def login_finish(self,*args):
        start_thread = threading.Thread(target = self.automatic_email)
        start_thread.start()
        if not start_thread.isDaemon():
            self.status.text = "Success"

    def automatic_email(self):
        mail = self.mail.text
        passw = self.passw.text
        self.s = smtplib.SMTP('smtp.gmail.com', 587)
        self.s.starttls()
        try:
            self.s.login(mail, passw)
        except Exception as error:
            with open("errors.txt","a",encoding="utf-8") as errors:
                errors.write("{}\n".format(error))
            self.status.text = "failed"
        email = self.mail_reciever.text
        message = self.mail_content.text
        self.s.sendmail(mail, email, message)
Mailer().run()