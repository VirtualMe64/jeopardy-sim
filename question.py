class Question:
    def __init__(self, value, daily_double=False):
        self.value = value
        self.daily_double = daily_double
        self.answered = False
    
    def __str__(self):
        if self.daily_double:
            return '\033[1m' + str(self.value) + '\033[0m'
        
        return str(self.value)

    def __repr__(self):
        return self.__str__()