import main.googleAPI.util.TimeUtil as TimeUtil
from main.googleAPI.adaptor.Adaptor import Adaptor
from main.googleAPI.service.Gmail import Gmail


# send email if log absent
def send_mail(gmail, read_id, params):
    try:
        if 'Time Log' in params and 'Email' in params:
            message = gmail.create_message("2016123304@yonsei.ac.kr", params['Email'],
                                           "Log missing", f"google docs link-{params['URL']}")
            gmail.send_message("me", read_id, message)
            print(f"Messages sent to {params['Email']}")
    except Exception as error:
        print(f'send_email:{error}')
        raise error


class TimeLogAdaptor(Adaptor):

    def __init__(self, gmail_cred):
        self.columns = ['Student Name', 'Package', 'Course', 'Date', 'Tutor', 'Email', 'Time Log']
        self.gmail = Gmail(gmail_cred)

    def get_attr(self):
        return self.columns

    def supports(self, read_params):
        columns = self.columns
        # check if missing key columns
        for col in columns:
            if col not in read_params:
                return False
        return True

    def validates(self, read_params):
        columns = self.columns
        for col in columns:
            if not read_params[col]:
                return False
        return True

    def handle(self, read_id, read_file, read_params):
        gmail = self.gmail
        link = read_file.get('webViewLink')
        time = TimeUtil.time_regex(read_file.get('modifiedTime'), time_format='api')
        read_params['Last Modified Time'] = str(time[0]) + ':' + str(time[1])
        read_params['URL'] = link
        # if not read_params['Time Log'] and not gmail.message_sent(read_id):
        #     send_mail(gmail, read_id, read_params)
