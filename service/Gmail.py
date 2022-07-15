from googleapiclient.discovery import build
from googleapiclient import errors
from email.message import EmailMessage
from auth.credentials import get_credentials
import base64

SCOPES = ['https://mail.google.com/']


def gmail_authenticate(cred):
    return build('gmail', 'v1', credentials=cred)


class Gmail:

    def __init__(self, cred):
        self.service = gmail_authenticate(cred)
        self.emailed = {}

    def create_message(self, sender, to, subject, message_text):
        message = EmailMessage()
        message["From"] = sender
        message["To"] = to.split(",")
        message["Subject"] = subject
        message.set_content(message_text)
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf8')}

    def send_message(self, user_id, docs_id, message):
        service = self.service
        try:
            if self.message_sent(docs_id):
                return
            message = service.users().messages().send(userId=user_id, body=message).execute()
            print('Message Id: %s' % message['id'])
            self.emailed[docs_id] = True
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def message_sent(self, docs_id):
        return docs_id in self.emailed


def main():
    service = Gmail(cred=get_credentials(SCOPES))
    message = service.create_message("2016123304@yonsei.ac.kr", "jungmu971@naver.com", "로그 시간 누락", "로그 시간을 남기지 않았습니다")
    service.send_message("me", message)


if __name__ == '__main__':
    main()
