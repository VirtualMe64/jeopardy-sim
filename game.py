from player import Player
from pprint import pprint
import random

def gen_board(double):
    '''
    param double: Boolean, true if board should be double jeopardy
    '''
    return [[(400 if double else 200) * p for p in range(1, 6)] for i in range(6)]

def round_over(board):
    for col in board:
        for q in col:
            if q != -1:
                return False
    
    return True

def bet_function(money):
    return money

def pick_q(board):
    for c in range(len(board)):
        for r in range(len(board[c])):
            if board[c][r] != -1:
                return c, r

def sim():
    p1 = Player(0.7, 0.9, 1, bet_function, bet_function, pick_q)
    p2 = Player(0.7, 0.9, 1, bet_function, bet_function, pick_q)
    p3 = Player(0.7, 0.9, 1, bet_function, bet_function, pick_q)

    players = [p1, p2, p3]
    in_control = 0

    board = gen_board(False)
    while not round_over(board):
        c, r = players[in_control].pick_question_strat(board)
        participants = []
        for player in players:
            if player.know_question():
                participants.append(player)
        
        while len(participants) > 0:
            buzz_index = random.choices(range(len(participants)), [p.buzzer_skill for p in participants])[0]
            curr = participants[buzz_index]

            if curr.is_correct():
                curr.money += board[c][r]
                break
            else:
                curr.money -= board[c][r]
                participants.pop(buzz_index)

        board[c][r] = -1
    
    #print(f"Player 1: {p1.money}\nPlayer 2: {p2.money}\nPlayer 3: {p3.money}")
    return p1.money, p2.money, p3.money

p1Money, p2Money, p3Money = 0, 0, 0

n = 1000
for i in range(n):
    vals = sim()
    p1Money += vals[0]
    p2Money += vals[1]
    p3Money += vals[2]

print(p1Money / n)
print(p2Money / n)
print(p3Money / n)