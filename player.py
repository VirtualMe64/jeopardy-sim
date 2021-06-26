import random

class Player:
    def __init__(self, p_know, p_correct, buzzer_skill, daily_double_strat, final_jeopardy_strat, pick_question_strat):
        '''
        param p_know: Probability of 'knowing' question - deciding to buzz in\n
        param p_correct: Probability of getting question correct after buzzing in\n
        param buzzer_skill: Skill at buzzer (weighting for buzz in random selection), positive float\n
        param daily_double_strat: Function to decide daily double wager based on game info\n
        param final_jeopardy_strat: Function to decide final jeopardy wager based on game info\n
        param pick_question_strat: Function to pick question from board based on game info\n
        '''
        self.p_know = p_know
        self.p_correct = p_correct
        self.buzzer_skill = buzzer_skill
        self.daily_double_strat = daily_double_strat
        self.final_jeopardy_strat = final_jeopardy_strat
        self.pick_question_strat = pick_question_strat
        self.money = 0

    def know_question(self):
        return random.random() <= self.p_know
    
    def is_correct(self):
        return random.random() <= self.p_correct

if __name__ == '__main__':
    player = Player(0.7, 0.95, 1, lambda x : x, lambda x : x, lambda x : x)
    n = 0
    for i in range(0, 10):
        if player.know_question():
            n += 1
    print(n)
