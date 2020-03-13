from random import choice
import time
from os import system

inf = float('inf')

HUMAN = -1
COMPUTER = 1
board = [
    [0, 0 ,0],
    [0, 0 ,0],
    [0, 0 ,0],
]

def evaluate(state):
    '''
        Do the evaluation of the board current state
        @{param} state: current board state
        @{return} 1 if computer wins, -1 if human wins. 0 if draw
    '''
    if wins(state, COMPUTER):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0
    return score

def wins(state, player):
    win_state =[
        [state[0][0], state[0][1], state[0][2]], # Win row 1
        [state[1][0], state[1][1], state[1][2]], # Win row 2
        [state[2][0], state[2][1], state[2][2]], # Win row 3
        [state[0][0], state[1][0], state[2][0]], # Win column 1
        [state[0][1], state[1][1], state[2][1]], # Win column 2
        [state[0][2], state[1][2], state[2][2]], # Win column 3
        [state[0][0], state[1][1], state[2][2]], # Win diagonal left-right
        [state[0][2], state[1][1], state[2][0]], # Win diagonal right-left
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def you_lost(state):
    return wins(state, HUMAN) or wins(state, COMPUTER)

def empty_cells(state):
    cells =[]
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x,y])
    return cells

def is_valid(x,y):
    if [x,y] in empty_cells(board):
        return True
    else:
        return False

def set_move(x,y, player):
    if is_valid(x,y):
        board[x][y] = player
        return True
    else:
        return False

def minmax(state, depth, player):
    if player == COMPUTER:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, +inf]
    
    if depth == 0 or you_lost(state):
        score = evaluate(state)
        return [-1, -1, score]
    
    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minmax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y
        
        if player == COMPUTER:
            if score[2] > best[2]:
                best = score # Max value
        else:
            if score[2] < best[2]:
                best = score # Min value
    return best

def clean():
    system('clear')

def render(state, computer_choice, human_choice):
    chars = {
        -1: human_choice,
         1: computer_choice,
         0: ' '
    }

    line = '--------------------------------'

    print('\n' + line)

    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end ='')
        print('\n'+line)

def computer_turn(computer_choice, human_choice):
    depth = len(empty_cells(board))
    if depth == 0 or you_lost(board):
        return
    
    clean()
    print(f'Computer turn [{computer_choice}]')
    render(board, computer_choice, human_choice)

    if depth == 9:
        x = choice([0,1,2])
        y = choice([0,1,2])
    else:
        move = minmax(board, depth, COMPUTER)
        x, y = move[0], move[1]
    
    set_move(x,y,COMPUTER)
    time.sleep(1)

def human_turn(computer_choice, human_choice):
    depth = len(empty_cells(board))
    if depth == 0 or you_lost(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{human_choice}]')
    render(board, computer_choice, human_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Digite de 1 ate 9: '))
            position = moves[move]
            movable = set_move(position[0], position[1], HUMAN)

            if not movable:
                print('Wrong move')
                move = -1
        
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('You are brillinat!, Next time try a correct value')

def main():
    clean()
    human_choice = '' # X or O
    computer_choice = '' # X or O
    first = ''

    # Humans choose
    while human_choice != 'O' and human_choice != 'X':
        try:
            print('')
            human_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('You need to read the instruction next time')
    
    # computer choose
    if human_choice == 'X':
        computer_choice = 'O'
    else:
        computer_choice = 'X'

        # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('You should know how to read instructions by now')
    
    while len(empty_cells(board)) > 0 and not you_lost(board):
        if first == 'N':
            computer_turn(computer_choice, human_choice)
            first = ''

        human_turn(computer_choice, human_choice)
        computer_turn(computer_choice, human_choice)
    
    # Game over message
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{human_choice}]')
        render(board, computer_choice, human_choice)
        print('YOU WIN!')
    elif wins(board, COMPUTER):
        clean()
        print(f'Computer turn [{computer_choice}]')
        render(board, computer_choice, human_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, computer_choice, human_choice)
        print('DRAW!')

    exit()

if __name__ == '__main__':
    main()