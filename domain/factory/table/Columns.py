# main tables

def time_table():
    return ['Docs Id', 'Student Id', 'Tutor Id', 'Consultant Id', 'Course', 'Course Date', 'Time Log']


def student_table():
    return ['Student Id', 'Name', 'Email', 'Phone Number', 'Current Package', 'Current Apps']


def tutor_table():
    return ['Tutor Id', 'Name', 'Email', 'Phone Number']


def consultant_table():
    return ['Consultant Id', 'Name', 'Email', 'Phone Number']


# derived tables
def payment_table():
    return ['Tutor Id', 'Tutor Name', 'Student Id', 'Student Name', 'SPENT HOURS']
