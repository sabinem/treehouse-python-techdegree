import threading
from django.core.mail import send_mail

class EmailThread(threading.Thread):
    def __init__(self, subject, content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.content = content
        threading.Thread.__init__(self)

    def run (self):
        send_mail(
            self.subject,
            self.content,
            'info@teambuilder.com',
            self.recipient_list,
            fail_silently=False,
        )

def send_email(subject, content, recipient_list):
    EmailThread(subject, content, recipient_list).start()