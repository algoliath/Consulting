from main.googleAPI.domain.entity.Person import Person


class Consultant(Person):

    def __init__(self, pin, name, email, contact, payroll):
        super.__init__(pin, name, email)
        self.contact = contact
        self.payroll = payroll
