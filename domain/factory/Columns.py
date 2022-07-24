# original tables
def docs_table():
    return ['DOCS ID', 'STUDENT ID', 'TUTOR ID', 'CONSULTANT ID', 'COURSE', 'COURSE DATE', 'TIME LOG',
            'TIME LAST MODIFIED', 'URL', 'SPENT HOURS']


def student_table():
    return ['STUDENT ID', 'NAME', 'EMAIL', 'PHONE NUMBER', 'CURRENT PACKAGE', 'CURRENT APPS']


def tutor_table():
    return ['TUTOR ID', 'NAME', 'EMAIL', 'PHONE NUMBER']


def consultant_table():
    return ['CONSULTANT ID', 'NAME', 'EMAIL', 'PHONE NUMBER']


# derived tables
def payment_table():
    return ['CONSULTANT ID', 'CONSULTANT NAME', 'STUDENT ID', 'STUDENT NAME', 'SPENT HOURS']
