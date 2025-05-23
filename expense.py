import csv

class Expense:
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = float(amount)
    
    def to_list(self):
        return [self.name, self.category, str(self.amount)]
    
    @staticmethod
    def from_list(data):
        name, category, amount = data
        return Expense(name, category, float(amount))