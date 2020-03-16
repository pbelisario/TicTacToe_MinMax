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
        # if the computer wins with the current board state
        # the score is 1
        score = +1
    elif wins(state, HUMAN):
        # if the human wins with the current board state
        # the score is -1
        score = -1
    else:
        # if no one wins with the current board state
        # the score is 0
        score = 0
    return score


def wins(state, player):
    '''
        Given the board state, checks if the player won the game
        @{param} state: current board state
        @{param} player: which player is
        @{return} True (has the victory) or False (Does not have the victory yet) 
    
    '''
    # How should be the board state to have an winner
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
    '''
        Checks if the game is over
        @{param} state: current board state
        @{return} True if either the player or computer won the game, False otherwise
    '''
    return wins(state, HUMAN) or wins(state, COMPUTER)

def empty_cells(state):
    '''
        return a list of empty cells within the current board state
    '''
    cells =[]
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x,y])
    return cells


def is_valid(x,y):
    '''
        Given an coordinate checks if the movement if valid or not
    '''
    if [x,y] in empty_cells(board):
        return True
    else:
        return False

def set_move(x,y, player):
    '''
        Set the board coordinate as choosen by the player
    '''
    if is_valid(x,y):
        board[x][y] = player
        return True
    else:
        return False

def minmax(state, depth, player):
    '''
        @{param} state: current board State
        @{param} depth: how many empty cells currently exists
        @{param} player: who is playing with minmax
        @{return} vector [X, Y, position Score]
    '''
    # if the player is the computer
    # the best position is at
    # X, Y -1, -1 with score -Infity
    if player == COMPUTER:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, +inf]
    
    # if there isn't an empty space or the game is over
    # return positions -1, -1 and evaluated score
    # only the evaluation will be used in this case
    # Guarantee the recursion ends
    if depth == 0 or you_lost(state):
        score = evaluate(state)
        return [-1, -1, score]
    
    # Recursively open the board empty cells tree
    for cell in empty_cells(state):
        
        # select the first empty cell available
        x, y = cell[0], cell[1]
        
        # temporary set the current player
        # at the selected cell
        state[x][y] = player

        # do the Minmax again, 
        # with the new temporary board, and the other player
        score = minmax(state, depth - 1, -player)
        
        # set the state as unused again
        state[x][y] = 0

        # update the score postions' to the correct one
        # it is up to this point -1, -1
        score[0], score[1] = x, y
        
        if player == COMPUTER:
            # if the player is the computer do the max strategy
            if score[2] > best[2]:
                best = score # Max value
        else:
            if score[2] < best[2]:
                # if the player other player do the min strategy
                best = score # Min value
    return best

def clean():
    system('clear')

def render(state, computer_choice, human_choice):
    '''
        print current board State
    '''
    chars = {
        -1: human_choice,
         1: computer_choice,
         0: ' ' 
    }

    line = '--------------------------------'

    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end ='')
        print('\n'+line)

def computer_turn(computer_choice, human_choice):
    
    # how many empty cells exists in the board
    depth = len(empty_cells(board))
    
    # if there is no empty cells or someone won the game
    # the computer does not take his turn
    if depth == 0 or you_lost(board):
        return
    
    clean()
    print(f'Computer turn [{computer_choice}]')
    render(board, computer_choice, human_choice)

    # if the board is empty
    # start placing the maker at an random position
    if depth == 9:
        x = choice([0,1,2])
        y = choice([0,1,2])
    else:
        # otherwise do the minmax algorithm
        # and place the marker at X Y board coordinate
        move = minmax(board, depth, COMPUTER)
        x, y = move[0], move[1]
    
    set_move(x,y,COMPUTER)
    time.sleep(1)

def human_turn(computer_choice, human_choice):
    
    # how many empty cells exists in the board
    depth = len(empty_cells(board))
    
    # if there is no empty cells or someone won the game
    # the computer does not take his turn
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
            # Set the players choice
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
    
    # Game loop
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