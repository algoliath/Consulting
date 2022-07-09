from main.googleAPI.adaptor.Adaptor import Adaptor


class PaymentAdaptor(Adaptor):

    def __init__(self):
        self.columns = ['Student', 'Date', 'Package', 'Time Log']
