
class Tutor(Person):

    def __init__(self, pin, name, email, contact, payroll):
        super.__init__(pin, name, email)
        self.contact = contact
        self.payroll = payroll
