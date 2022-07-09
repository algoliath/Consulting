class Person:
    def __init__(self, pin, name, email):
        self.pin = pin
        self.name = name
        self.email = email

    def get_pin(self):
        return self.pin

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name
