from player import Player
from pprint import pprint
import random
from question import Question

def gen_board(double_jeopardy):
    '''
    param double_jeopardy: Boolean, true if board should be double jeopardy
    '''
    board = [[Question((400 if double_jeopardy else 200) * p) for p in range(1, 6)] for i in range(6)]
    add_daily_double(board, double_jeopardy)
    return board

# https://preview.redd.it/tzssic6y6ad11.png?width=2283&format=png&auto=webp&s=79d794d04d27a7465701877c5273a01bc4e430e1
DAILY_DOUBLE_DISTR = [
    [0.04, 2.23, 6.06, 7.71, 4.72], # category 1
    [0.03, 1.24, 3.77, 5.09, 2.69], # category 2
    [0.04, 1.80, 5.22, 7.26, 4.35], # category 3
    [0.03, 1.59, 5.01, 6.48, 4.21], # category 4
    [0.03, 1.17, 4.89, 6.95, 3.93], # category 5
    [0.03, 1.26, 3.65, 4.75, 3.20], # category 6
]

def add_daily_double(board, double_jeopardy):
    probs = [q for category in DAILY_DOUBLE_DISTR for q in category]
    indices = range(0, 30)
    dd1 = random.choices(indices, probs)[0]
    category = dd1 // 5
    question = dd1 % 5
    board[category][question].daily_double = True

    if double_jeopardy:
        probs[dd1] = 0
        dd2 = random.choices(indices, probs)[0]
        category = dd2 // 5
        question = dd2 % 5
        board[category][question].daily_double = True

def round_over(board):
    for col in board:
        for q in col:
            if not q.answered:
                return False
    
    return True

def bet_function_1(money):
    return money

def bet_function_2(money):
    return money // 2

def pick_q(board):
    for col in board:
        for q in col:
            if not q.answered:
                return q

def do_round(board, in_control, players):
    while not round_over(board):
        question = players[in_control].pick_question_strat(board)
        participants = []
        for player in players:
            if player.know_question():
                participants.append(player)
        
        while len(participants) > 0:
            buzz_index = random.choices(range(len(participants)), [p.buzzer_skill for p in participants])[0]
            curr = participants[buzz_index]
            
            if not question.daily_double:
                if curr.is_correct():
                    curr.money += question.value
                    in_control = participants.index(curr)
                    break
                else:
                    curr.money -= question.value
                    participants.pop(buzz_index)
            
            else: # Daily Double
                bet = curr.daily_double_strat(curr.money)
                if curr.is_correct():
                    curr.money += bet
                else:
                    curr.money -= bet
                break
                
        question.answered = True
    

def sim():
    p1 = Player(0.7, 0.9, 1, bet_function_1, bet_function_1, pick_q)
    p2 = Player(0.7, 0.9, 1, bet_function_2, bet_function_1, pick_q)
    p3 = Player(0.7, 0.9, 1, bet_function_2, bet_function_1, pick_q)

    players = [p1, p2, p3]
    in_control = 0

    board = gen_board(False)
    do_round(board, in_control, players) # Normal jeopardy

    board = gen_board(True)
    do_round(board, in_control, players) # Double jeopardy

    return p1.money, p2.money, p3.money

p1Money = 0
p2Money = 0
p3Money = 0

n = 1000
for i in range(n):
    vals = sim()
    p1Money += vals[0]
    p2Money += vals[1]
    p3Money += vals[2]

print(p1Money / n)
print(p2Money / n)
print(p3Money / n)