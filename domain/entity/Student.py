from main.googleAPI.domain.entity.Person import Person


class Student(Person):

    def __init__(self, pin, name, email, contact, package, grade):
        super.__init__(pin, name, email)
        self.contact = contact
        self.package = package
        self.grade = grade

    def get_contact(self):
        return self.contact

    def get_package(self):
        return self.package

    def get_grade(self):
        return self.grade
