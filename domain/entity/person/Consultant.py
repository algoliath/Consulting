from domain.entity.person.Person import Person


class Consultant(Person):

    def __init__(self, id, name, email, contact, payroll):
        super.__init__(id, name, email)
        self.contact = contact
        self.payroll = payroll
