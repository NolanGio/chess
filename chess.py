'''Chess engine'''
import const

class piece:
    '''Constants related to pieces for gameboard and movement logic'''
    pawn = 1
    bishop = 2
    knight = 3
    rook = 4
    queen = 5
    king = 6
    white = 8
    black = 16
    draw = 7

board = [0]*64
'''The chess board using a single array representation'''
turn = piece.white # piece.white = 8 and piece.black = 16
'''Whose turn is it currently: piece.white / piece.black'''
moves = []
'''Array of possible moves'''
last_move = []
'''Last move taken by previous player:[source, destination, piece]'''
over = 0
'''Who won\nNone: 0\nWhite: piece.white\nBlack: piece.black\nDraw: piece.draw'''

# Variables used to check for castling
Km = False # White king has moved
Rrm = False # White rook right has moved
Rlm = False # White rook left has moved
km = False # Black king has moved
rrm = False # Black rook right has moved
rlm = False # Black rook left has moved

def startBoardFromFen(fen_string:str, first_turn:int, 
    hKm:bool = False, hRrm:bool = False, hRlm:bool = False,
    hkm:bool = False, hrrm:bool = False, hrlm:bool = False,):
    '''
    Starts the board array using FEN notation.
    You can specify if any of the pieces used 
    for castling has moved.\n
    hKm: has white king moved\n
    hRrm: has white rook on right moved\n
    hRlm: has white rook on left moved\n
    hrm: has black king moved\n
    hrrm: has black rook on right moved\n
    hrlm: has black king on left moved
    '''
    
    global Km, Rrm, Rlm, km, rrm, rlm
    # Assign castling booleans:
    Km, Rrm, Rlm, km, rrm, rlm = hKm, hRrm, hRlm, hkm, hrrm, hrlm

    # Check for valid first player
    if first_turn == piece.white or first_turn == piece.black:
        turn = first_turn
    else:
        raise ValueError("first turn must be defined using valid pieces constants such as piece.white or piece.black")

    x, y = 0, 0 # Position on the board
    for char in fen_string:

        if y > 7:
            break

        elif char == "/":
            x = 0
            y += 1

        elif char in "123456789":
            x += int(char)
            y += x//8
            x %= 8
        
        # UPPERCASE for white pieces and LOWERCASE for black pieces
        isWhite = True if char != char.lower() else False
        if char.lower() in "pbnrqk":
            # match with the corresponding piece and sets the array value
            if char.lower() == "p":
                if isWhite:
                    board[x + y * 8] = piece.pawn | piece.white
                else:
                    board[x + y * 8] = piece.pawn | piece.black

            elif char.lower() == "b":
                if isWhite:
                    board[x + y * 8] = piece.bishop | piece.white
                else:
                    board[x + y * 8] = piece.bishop | piece.black

            elif char.lower() == "n":
                if isWhite:
                    board[x + y * 8] = piece.knight | piece.white
                else:
                    board[x + y * 8] = piece.knight | piece.black

            elif char.lower() == "r":
                if isWhite:
                    board[x + y * 8] = piece.rook | piece.white
                else:
                    board[x + y * 8] = piece.rook | piece.black

            elif char.lower() == "q":
                if isWhite:
                    board[x + y * 8] = piece.queen | piece.white
                else:
                    board[x + y * 8] = piece.queen | piece.black

            elif char.lower() == "k":
                if isWhite:
                    board[x + y * 8] = piece.king | piece.white
                else:
                    board[x + y * 8] = piece.king | piece.black        
            x += 1
            y += x//8
            x %= 8
    
    # Change castling booleans
    if board[60] != piece.white | piece.king:
        Km = True
    if board[63] != piece.white | piece.rook:
        Rrm = True
    if board[56] != piece.white | piece.rook:
        Rlm = True
    if board[4] != piece.black | piece.king:
        km = True
    if board[7] != piece.black | piece.rook:
        rrm = True
    if board[0] != piece.black | piece.rook:
        rlm = True
    
    generate_legal_moves()
    return

def play(move:list[int]):
    '''Plays a move on the board array'''
    # Is there a promotion to be made?
    global moves, last_move, Km, Rrm, Rlm, km, rrm, rlm, turn, over
    if over:
        print("Game is already over")
    else:
        board[move[1]] = board[move[0]]
        board[move[0]] = 0
        last_move = [move[0], move[1], board[move[1]]]
        if len(move) == 3: # En passant
            board[move[2]] = 0
        if len(move) == 4: # Castling
            board[move[3]] = board[move[2]]
            board[move[2]] = 0
        if len(move) == 5: # Promotion
            color = piece.white if board[move[1]] & piece.white == piece.white else piece.black
            board[move[1]] = move[4] | color
        if not Km: # Update castling booleans for White
            if last_move[2] == piece.king | piece.white:
                Km = True
            if not Rrm:
                if last_move[2] == piece.rook | piece.white:
                    if last_move[0] == 63:
                        Rrm = True
            if not Rlm:
                if last_move[2] == piece.rook | piece.white:
                    if last_move[0] == 56:
                        Rlm = True
        if not km: # Update castling booleans for black
            if last_move[2] == piece.king | piece.black:
                km = True
            if not rrm:
                if last_move[2] == piece.rook | piece.black:
                    if last_move[0] == 7:
                        rrm = True
            if not rlm:
                if last_move[2] == piece.rook | piece.black:
                    if last_move[0] == 0:
                        rlm = True
        moves = []
        if turn == piece.white:
            turn = piece.black
        else:
            turn = piece.white
        generate_legal_moves()
    return

def _play(move:list[int], new_board:list[int]):
    '''Same as play but for legal moves generation'''
    new_board[move[1]] = new_board[move[0]]
    new_board[move[0]] = 0
    last_move = [move[0], move[1], new_board[move[1]]]
    if len(move) == 3: # En passant
        new_board[move[2]] = 0
    if len(move) == 4: # Castling
        new_board[move[3]] = new_board[move[2]]
        new_board[move[2]] = 0
    if len(move) == 5: # Promotion
            color = piece.white if new_board[move[1]] & piece.white == piece.white else piece.black
            new_board[move[1]] = move[4] | color
    return new_board

def generate_moves():
    '''
    Generate moves (ex. [56, 40]) which indicate start, and arrival.
    This array will have a 3rd value for square capture (ex. enpassant).
    This array will have a 4th value for second move (ex. castling).
    This function does not keep track of legal moves.
    This affects the moves array of the module
    '''
    global moves, Km, Rrm, Rlm, km, rrm, rlm, turn
    moves = []
    for i in range(len(board)):
        square = board[i]
        if square & turn == piece.white:
            # Generate moves for each piece
            if square % piece.white == piece.king:
                add_moves = [[i, i-9],[i, i-8],[i, i-7],
                              [i, i-1],         [i, i+1],
                              [i, i+7],[i, i+8],[i, i+9]]
                    
                # Remove moves where king teleports
                j = 0
                while j < len(add_moves):
                    if not(0 <= add_moves[j][1]//8 <= 7) or ((add_moves[j][1] % 8 - add_moves[j][0] % 8) not in [-1, 0, 1]):
                        add_moves.pop(j)
                    else:
                        j += 1
                # Check for castling
                if not Km:
                    if not Rrm and board[i+1] == 0 and board[i+2] == 0:
                        add_moves.append([i, i+2, i+3, i+1])
                    if not Rlm and board[i-1] == 0 and board[i-2] == 0 and board[i-3] == 0:
                        add_moves.append([i, i-2, i-4, i-1])
                # Remove moves that would capture white pieces
                j = 0
                while j < len(add_moves):
                    if board[add_moves[j][1]] & piece.white == piece.white:
                        add_moves.pop(j)
                    else:
                        j += 1
                moves.extend(add_moves)
                continue
            elif square % piece.white == piece.queen:
                add_moves = []
                x, y = i % 8, i // 8 
                j = 1
                while j < 8 - x: # right loop
                    if i+j > 63:
                        j = 8
                    elif board[i+j] & piece.white == piece.white:
                        j = 8
                    elif board[i+j] & piece.black == piece.black:
                        add_moves.append([i, i+j])
                        j = 8
                    else:
                        add_moves.append([i, i+j])
                        j += 1
                j = 1
                while j < x+1: # left loop
                    if i-j < 0:
                        j = 8
                    elif board[i-j] & piece.white == piece.white:
                        j = 8
                    elif board[i-j] & piece.black == piece.black:
                        add_moves.append([i, i-j])
                        j = 8
                    else:
                        add_moves.append([i, i-j])
                        j += 1
                j = 1
                while j < 8 - y: # down loop
                    if i+j*8 > 63:
                        j = 8
                    elif board[i+j*8] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*8] & piece.black == piece.black:
                        add_moves.append([i, i+j*8])
                        j = 8
                    else:
                        add_moves.append([i, i+j*8])
                        j += 1
                j = 1
                while j < y+1: # up loop
                    if i-j*8 < 0:
                        j = 8
                    elif board[i-j*8] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*8] & piece.black == piece.black:
                        add_moves.append([i, i-j*8])
                        j = 8
                    else:
                        add_moves.append([i, i-j*8])
                        j += 1
                j = 1
                while j < 8 - x and j < 8 - y: # down-right loop
                    if i+j*9 > 63:
                        j = 8
                    elif board[i+j*9] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*9] & piece.black == piece.black:
                        add_moves.append([i, i+j*9])
                        j = 8
                    else:
                        add_moves.append([i, i+j*9])
                        j += 1
                j = 1
                while j < x+1 and j < y+1: # up-left loop
                    if i-j*9 < 0:
                        j = 8
                    elif board[i-j*9] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*9] & piece.black == piece.black:
                        add_moves.append([i, i-j*9])
                        j = 8
                    else:
                        add_moves.append([i, i-j*9])
                        j += 1
                j = 1
                while j < 8 - y and j < x+1: # down-left loop
                    if i+j*7 > 63:
                        j = 8
                    elif board[i+j*7] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*7] & piece.black == piece.black:
                        add_moves.append([i, i+j*7])
                        j = 8
                    else:
                        add_moves.append([i, i+j*7])
                        j += 1
                j = 1
                while j < y+1 and j < 8 - x: # up-right loop
                    if i-j*7 < 0:
                        j = 8
                    elif board[i-j*7] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*7] & piece.black == piece.black:
                        add_moves.append([i, i-j*7])
                        j = 8
                    else:
                        add_moves.append([i, i-j*7])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square % piece.white == piece.rook:
                add_moves = []
                x, y = i % 8, i // 8
                j = 1
                while j < 8 - x: # right loop
                    if i+j > 63:
                        j = 8
                    elif board[i+j] & piece.white == piece.white:
                        j = 8
                    elif board[i+j] & piece.black == piece.black:
                        add_moves.append([i, i+j])
                        j = 8
                    else:
                        add_moves.append([i, i+j])
                        j += 1
                j = 1
                while j < x+1: # left loop
                    if i-j < 0:
                        j = 8
                    elif board[i-j] & piece.white == piece.white:
                        j = 8
                    elif board[i-j] & piece.black == piece.black:
                        add_moves.append([i, i-j])
                        j = 8
                    else:
                        add_moves.append([i, i-j])
                        j += 1
                j = 1
                while j < 8 - y: # down loop
                    if i+j*8 > 63:
                        j = 8
                    elif board[i+j*8] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*8] & piece.black == piece.black:
                        add_moves.append([i, i+j*8])
                        j = 8
                    else:
                        add_moves.append([i, i+j*8])
                        j += 1
                j = 1
                while j < y+1: # up loop
                    if i-j*8 < 0:
                        j = 8
                    elif board[i-j*8] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*8] & piece.black == piece.black:
                        add_moves.append([i, i-j*8])
                        j = 8
                    else:
                        add_moves.append([i, i-j*8])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square % piece.white == piece.knight:
                add_moves = [
                        [i, i-17],      [i, i-15],
                [i, i-10],                      [i, i-6],

                 [i, i+6],                       [i, i+10],
                        [i, i+15],      [i, i+17],
                ]
                # Remove moves where knight teleports
                j = 0
                while j < len(add_moves):
                    if not(0 <= add_moves[j][1]//8 <= 7) or ((add_moves[j][1] % 8 - add_moves[j][0] % 8) not in [-2, -1, 1, 2]):
                        add_moves.pop(j)
                    else:
                        j += 1
                # Remove moves that would capture white pieces
                j = 0
                while j < len(add_moves):
                    if board[add_moves[j][1]] & piece.white == piece.white:
                        add_moves.pop(j)
                    else:
                        j += 1
                moves.extend(add_moves)
                continue
            elif square % piece.white == piece.bishop:
                add_moves = []
                x, y = i % 8, i // 8
                j = 1
                while j < 8 - x and j < 8 - y: # down-right loop
                    if i+j*9 > 63:
                        j = 8
                    elif board[i+j*9] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*9] & piece.black == piece.black:
                        add_moves.append([i, i+j*9])
                        j = 8
                    else:
                        add_moves.append([i, i+j*9])
                        j += 1
                j = 1
                while j < x+1 and j < y+1: # up-left loop
                    if i-j*9 < 0:
                        j = 8
                    elif board[i-j*9] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*9] & piece.black == piece.black:
                        add_moves.append([i, i-j*9])
                        j = 8
                    else:
                        add_moves.append([i, i-j*9])
                        j += 1
                j = 1
                while j < 8 - y and j < x+1: # down-left loop
                    if i+j*7 > 63:
                        j = 8
                    elif board[i+j*7] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*7] & piece.black == piece.black:
                        add_moves.append([i, i+j*7])
                        j = 8
                    else:
                        add_moves.append([i, i+j*7])
                        j += 1
                j = 1
                while j < y+1 and j < 8 - x: # up-right loop
                    if i-j*7 < 0:
                        j = 8
                    elif board[i-j*7] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*7] & piece.black == piece.black:
                        add_moves.append([i, i-j*7])
                        j = 8
                    else:
                        add_moves.append([i, i-j*7])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square % piece.white == piece.pawn:
                if i // 8 != 0:
                    add_moves = []
                    # Non capture moves
                    if board[i-8] == 0:
                        add_moves.append([i, i-8])
                        if i//8 == 6 and board[i-16] == 0:
                            add_moves.append([i, i-16])
                    # Capture moves
                    if board[i-7] != 0:
                        add_moves.append([i, i-7])
                    if board[i-9] != 0:
                        add_moves.append([i, i-9])                    
                    # Check for enpassant if there was a previous move
                    if last_move:
                        # Check if double step was made by a pawn
                        if last_move[2] % piece.white == piece.pawn:
                            if last_move[0] == i-17 and last_move[1] == i-1:
                                add_moves.append([i, i-9, i-1])
                            elif last_move[0] == i-15 and last_move[1] == i+1:
                                add_moves.append([i, i-7, i+1])
                    # Add promotion moves
                    for j in range(len(add_moves)):
                        add_move = add_moves[0]
                        if add_move[1] // 8 == 0:
                            src = add_move[0]
                            dest = add_move[1]
                            add_moves.pop(0)
                            add_moves.extend([[src, dest, 0, 0, 2], [src, dest, 0, 0, 3], [src, dest, 0, 0, 4], [src, dest, 0, 0, 5]])
                    # Remove moves that would capture white pieces
                    j = 0
                    while j < len(add_moves):
                        if board[add_moves[j][1]] & piece.white == piece.white:
                            add_moves.pop(j)
                        else:
                            j += 1
                    moves.extend(add_moves)
                continue
        elif square & turn == piece.black:
            # Generate moves for each piece
            if square % piece.white == piece.king:
                add_moves = [[i, i-9],[i, i-8],[i, i-7],
                              [i, i-1],         [i, i+1],
                              [i, i+7],[i, i+8],[i, i+9]]
                    
                # Remove moves where king teleports
                j = 0
                while j < len(add_moves):
                    if not(0 <= add_moves[j][1]//8 <= 7) or ((add_moves[j][1] % 8 - add_moves[j][0] % 8) not in [-1, 0, 1]):
                        add_moves.pop(j)
                    else:
                        j += 1
                # Check for castling
                if not km:
                    if not rrm and board[i+1] == 0 and board[i+2] == 0:
                        add_moves.append([i, i+2, i+3, i+1])
                    if not rlm and board[i-1] == 0 and board[i-2] == 0 and board[i-3] == 0:
                        add_moves.append([i, i-2, i-4, i-1])
                # Remove moves that would capture black pieces
                j = 0
                while j < len(add_moves):
                    if board[add_moves[j][1]] & piece.black == piece.black:
                        add_moves.pop(j)
                    else:
                        j += 1
                moves.extend(add_moves)
                continue
            elif square % piece.white == piece.queen:
                add_moves = []
                x, y = i % 8, i // 8 
                j = 1
                while j < 8 - x: # right loop
                    if i+j > 63:
                        j = 8
                    elif board[i+j] & piece.black == piece.black:
                        j = 8
                    elif board[i+j] & piece.white == piece.white:
                        add_moves.append([i, i+j])
                        j = 8
                    else:
                        add_moves.append([i, i+j])
                        j += 1
                j = 1
                while j < x+1: # left loop
                    if i-j < 0:
                        j = 8
                    elif board[i-j] & piece.black == piece.black:
                        j = 8
                    elif board[i-j] & piece.white == piece.white:
                        add_moves.append([i, i-j])
                        j = 8
                    else:
                        add_moves.append([i, i-j])
                        j += 1
                j = 1
                while j < 8 - y: # down loop
                    if i+j*8 > 63:
                        j = 8
                    elif board[i+j*8] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*8] & piece.white == piece.white:
                        add_moves.append([i, i+j*8])
                        j = 8
                    else:
                        add_moves.append([i, i+j*8])
                        j += 1
                j = 1
                while j < y+1: # up loop
                    if i-j*8 < 0:
                        j = 8
                    elif board[i-j*8] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*8] & piece.white == piece.white:
                        add_moves.append([i, i-j*8])
                        j = 8
                    else:
                        add_moves.append([i, i-j*8])
                        j += 1
                j = 1
                while j < 8 - x and j < 8 - y: # down-right loop
                    if i+j*9 > 63:
                        j = 8
                    elif board[i+j*9] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*9] & piece.white == piece.white:
                        add_moves.append([i, i+j*9])
                        j = 8
                    else:
                        add_moves.append([i, i+j*9])
                        j += 1
                j = 1
                while j < x+1 and j < y+1: # up-left loop
                    if i-j*9 < 0:
                        j = 8
                    elif board[i-j*9] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*9] & piece.white == piece.white:
                        add_moves.append([i, i-j*9])
                        j = 8
                    else:
                        add_moves.append([i, i-j*9])
                        j += 1
                j = 1
                while j < 8 - y and j < x+1: # down-left loop
                    if i+j*7 > 63:
                        j = 8
                    elif board[i+j*7] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*7] & piece.white == piece.white:
                        add_moves.append([i, i+j*7])
                        j = 8
                    else:
                        add_moves.append([i, i+j*7])
                        j += 1
                j = 1
                while j < y+1 and j < 8 - x: # up-right loop
                    if i-j*7 < 0:
                        j = 8
                    elif board[i-j*7] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*7] & piece.white == piece.white:
                        add_moves.append([i, i-j*7])
                        j = 8
                    else:
                        add_moves.append([i, i-j*7])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square % piece.white == piece.rook:
                add_moves = []
                x, y = i % 8, i // 8
                j = 1
                while j < 8 - x: # right loop
                    if i+j > 63:
                        j = 8
                    elif board[i+j] & piece.black == piece.black:
                        j = 8
                    elif board[i+j] & piece.white == piece.white:
                        add_moves.append([i, i+j])
                        j = 8
                    else:
                        add_moves.append([i, i+j])
                        j += 1
                j = 1
                while j < x+1: # left loop
                    if i-j < 0:
                        j = 8
                    elif board[i-j] & piece.black == piece.black:
                        j = 8
                    elif board[i-j] & piece.white == piece.white:
                        add_moves.append([i, i-j])
                        j = 8
                    else:
                        add_moves.append([i, i-j])
                        j += 1
                j = 1
                while j < 8 - y: # down loop
                    if i+j*8 > 63:
                        j = 8
                    elif board[i+j*8] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*8] & piece.white == piece.white:
                        add_moves.append([i, i+j*8])
                        j = 8
                    else:
                        add_moves.append([i, i+j*8])
                        j += 1
                j = 1
                while j < y+1: # up loop
                    if i-j*8 < 0:
                        j = 8
                    elif board[i-j*8] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*8] & piece.white == piece.white:
                        add_moves.append([i, i-j*8])
                        j = 8
                    else:
                        add_moves.append([i, i-j*8])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square % piece.white == piece.knight:
                add_moves = [
                        [i, i-17],      [i, i-15],
                [i, i-10],                      [i, i-6],

                 [i, i+6],                       [i, i+10],
                        [i, i+15],      [i, i+17],
                ]
                # Remove moves where knight teleports
                j = 0
                while j < len(add_moves):
                    if not(0 <= add_moves[j][1]//8 <= 7) or ((add_moves[j][1] % 8 - add_moves[j][0] % 8) not in [-2, -1, 1, 2]):
                        add_moves.pop(j)
                    else:
                        j += 1
                # Remove moves that would capture black pieces
                j = 0
                while j < len(add_moves):
                    if board[add_moves[j][1]] & piece.black == piece.black:
                        add_moves.pop(j)
                    else:
                        j += 1
                moves.extend(add_moves)
                continue
            elif square % piece.white == piece.bishop:
                add_moves = []
                x, y = i % 8, i // 8
                j = 1
                while j < 8 - x and j < 8 - y: # down-right loop
                    if i+j*9 > 63:
                        j = 8
                    elif board[i+j*9] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*9] & piece.white == piece.white:
                        add_moves.append([i, i+j*9])
                        j = 8
                    else:
                        add_moves.append([i, i+j*9])
                        j += 1
                j = 1
                while j < x+1 and j < y+1: # up-left loop
                    if i-j*9 < 0:
                        j = 8
                    elif board[i-j*9] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*9] & piece.white == piece.white:
                        add_moves.append([i, i-j*9])
                        j = 8
                    else:
                        add_moves.append([i, i-j*9])
                        j += 1
                j = 1
                while j < 8 - y and j < x+1: # down-left loop
                    if i+j*7 > 63:
                        j = 8
                    elif board[i+j*7] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*7] & piece.white == piece.white:
                        add_moves.append([i, i+j*7])
                        j = 8
                    else:
                        add_moves.append([i, i+j*7])
                        j += 1
                j = 1
                while j < y+1 and j < 8 - x: # up-right loop
                    if i-j*7 < 0:
                        j = 8
                    elif board[i-j*7] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*7] & piece.white == piece.white:
                        add_moves.append([i, i-j*7])
                        j = 8
                    else:
                        add_moves.append([i, i-j*7])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square % piece.white == piece.pawn:
                if i // 8 != 7:
                    add_moves = []
                    # Non capture moves
                    if board[i+8] == 0:
                        add_moves.append([i, i+8])
                        if i//8 == 1 and board[i+16] == 0:
                            add_moves.append([i, i+16])
                    # Capture moves
                    if board[i+7] != 0:
                        add_moves.append([i, i+7])
                    if board[i+9] != 0:
                        add_moves.append([i, i+9])                    
                    # Check for enpassant if there was a previous move
                    if last_move:
                        # Check if double step was made by a pawn
                        if last_move[2] % piece.white == piece.pawn:
                            if last_move[0] == i+17 and last_move[1] == i+1:
                                add_moves.append([i, i+9, i+1])
                            elif last_move[0] == i+15 and last_move[1] == i-1:
                                add_moves.append([i, i+7, i-1])
                    # Add promotion moves
                    for j in range(len(add_moves)):
                        add_move = add_moves[0]
                        if add_move[1] // 8 == 7:
                            src = add_move[0]
                            dest = add_move[1]
                            add_moves.pop(0)
                            add_moves.extend([[src, dest, 0, 0, 2], [src, dest, 0, 0, 3], [src, dest, 0, 0, 4], [src, dest, 0, 0, 5]])
                    # Remove moves that would capture black pieces
                    j = 0
                    while j < len(add_moves):
                        if board[add_moves[j][1]] & piece.black == piece.black:
                            add_moves.pop(j)
                        else:
                            j += 1
                    moves.extend(add_moves)
                continue
    return

def _generate_moves(turn:int, board:list[int]): #TODO
    '''
    Same as generate_moves().
    Returns a list of possible moves.
    Used to check for non legal moves.
    '''
    moves = []
    for i in range(len(board)):
        square = board[i]
        if square & turn == piece.white:
            # Generate moves for each piece
            if square & piece.king == piece.king:
                add_moves = [[i, i-9],[i, i-8],[i, i-7],
                              [i, i-1],         [i, i+1],
                              [i, i+7],[i, i+8],[i, i+9]]
                    
                # Remove moves where king teleports
                j = 0
                while j < len(add_moves):
                    if not(0 <= add_moves[j][1]//8 <= 7) or ((add_moves[j][1] % 8 - add_moves[j][0] % 8) not in [-1, 0, 1]):
                        add_moves.pop(j)
                    else:
                        j += 1
                # Remove moves that would capture white pieces
                j = 0
                while j < len(add_moves):
                    if board[add_moves[j][1]] & piece.white == piece.white:
                        add_moves.pop(j)
                    else:
                        j += 1
                moves.extend(add_moves)
                continue
            elif square & piece.queen == piece.queen:
                add_moves = []
                x, y = i % 8, i // 8 
                j = 1
                while j < 8 - x: # right loop
                    if i+j > 63:
                        j = 8
                    elif board[i+j] & piece.white == piece.white:
                        j = 8
                    elif board[i+j] & piece.black == piece.black:
                        add_moves.append([i, i+j])
                        j = 8
                    else:
                        add_moves.append([i, i+j])
                        j += 1
                j = 1
                while j < x+1: # left loop
                    if i-j < 0:
                        j = 8
                    elif board[i-j] & piece.white == piece.white:
                        j = 8
                    elif board[i-j] & piece.black == piece.black:
                        add_moves.append([i, i-j])
                        j = 8
                    else:
                        add_moves.append([i, i-j])
                        j += 1
                j = 1
                while j < 8 - y: # down loop
                    if i+j*8 > 63:
                        j = 8
                    elif board[i+j*8] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*8] & piece.black == piece.black:
                        add_moves.append([i, i+j*8])
                        j = 8
                    else:
                        add_moves.append([i, i+j*8])
                        j += 1
                j = 1
                while j < y+1: # up loop
                    if i-j*8 < 0:
                        j = 8
                    elif board[i-j*8] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*8] & piece.black == piece.black:
                        add_moves.append([i, i-j*8])
                        j = 8
                    else:
                        add_moves.append([i, i-j*8])
                        j += 1
                j = 1
                while j < 8 - x and j < 8 - y: # down-right loop
                    if i+j*9 > 63:
                        j = 8
                    elif board[i+j*9] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*9] & piece.black == piece.black:
                        add_moves.append([i, i+j*9])
                        j = 8
                    else:
                        add_moves.append([i, i+j*9])
                        j += 1
                j = 1
                while j < x+1 and j < y+1: # up-left loop
                    if i-j*9 < 0:
                        j = 8
                    elif board[i-j*9] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*9] & piece.black == piece.black:
                        add_moves.append([i, i-j*9])
                        j = 8
                    else:
                        add_moves.append([i, i-j*9])
                        j += 1
                j = 1
                while j < 8 - y and j < x+1: # down-left loop
                    if i+j*7 > 63:
                        j = 8
                    elif board[i+j*7] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*7] & piece.black == piece.black:
                        add_moves.append([i, i+j*7])
                        j = 8
                    else:
                        add_moves.append([i, i+j*7])
                        j += 1
                j = 1
                while j < y+1 and j < 8 - x: # up-right loop
                    if i-j*7 < 0:
                        j = 8
                    elif board[i-j*7] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*7] & piece.black == piece.black:
                        add_moves.append([i, i-j*7])
                        j = 8
                    else:
                        add_moves.append([i, i-j*7])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square & piece.rook == piece.rook:
                add_moves = []
                x, y = i % 8, i // 8
                j = 1
                while j < 8 - x: # right loop
                    if i+j > 63:
                        j = 8
                    elif board[i+j] & piece.white == piece.white:
                        j = 8
                    elif board[i+j] & piece.black == piece.black:
                        add_moves.append([i, i+j])
                        j = 8
                    else:
                        add_moves.append([i, i+j])
                        j += 1
                j = 1
                while j < x+1: # left loop
                    if i-j < 0:
                        j = 8
                    elif board[i-j] & piece.white == piece.white:
                        j = 8
                    elif board[i-j] & piece.black == piece.black:
                        add_moves.append([i, i-j])
                        j = 8
                    else:
                        add_moves.append([i, i-j])
                        j += 1
                j = 1
                while j < 8 - y: # down loop
                    if i+j*8 > 63:
                        j = 8
                    elif board[i+j*8] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*8] & piece.black == piece.black:
                        add_moves.append([i, i+j*8])
                        j = 8
                    else:
                        add_moves.append([i, i+j*8])
                        j += 1
                j = 1
                while j < y+1: # up loop
                    if i-j*8 < 0:
                        j = 8
                    elif board[i-j*8] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*8] & piece.black == piece.black:
                        add_moves.append([i, i-j*8])
                        j = 8
                    else:
                        add_moves.append([i, i-j*8])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square & piece.knight == piece.knight:
                add_moves = [
                        [i, i-17],      [i, i-15],
                [i, i-10],                      [i, i-6],

                 [i, i+6],                       [i, i+10],
                        [i, i+15],      [i, i+17],
                ]
                # Remove moves where knight teleports
                j = 0
                while j < len(add_moves):
                    if not(0 <= add_moves[j][1]//8 <= 7) or ((add_moves[j][1] % 8 - add_moves[j][0] % 8) not in [-2, -1, 1, 2]):
                        add_moves.pop(j)
                    else:
                        j += 1
                # Remove moves that would capture white pieces
                j = 0
                while j < len(add_moves):
                    if board[add_moves[j][1]] & piece.white == piece.white:
                        add_moves.pop(j)
                    else:
                        j += 1
                moves.extend(add_moves)
                continue
            elif square & piece.bishop == piece.bishop:
                add_moves = []
                x, y = i % 8, i // 8
                j = 1
                while j < 8 - x and j < 8 - y: # down-right loop
                    if i+j*9 > 63:
                        j = 8
                    elif board[i+j*9] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*9] & piece.black == piece.black:
                        add_moves.append([i, i+j*9])
                        j = 8
                    else:
                        add_moves.append([i, i+j*9])
                        j += 1
                j = 1
                while j < x+1 and j < y+1: # up-left loop
                    if i-j*9 < 0:
                        j = 8
                    elif board[i-j*9] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*9] & piece.black == piece.black:
                        add_moves.append([i, i-j*9])
                        j = 8
                    else:
                        add_moves.append([i, i-j*9])
                        j += 1
                j = 1
                while j < 8 - y and j < x+1: # down-left loop
                    if i+j*7 > 63:
                        j = 8
                    elif board[i+j*7] & piece.white == piece.white:
                        j = 8
                    elif board[i+j*7] & piece.black == piece.black:
                        add_moves.append([i, i+j*7])
                        j = 8
                    else:
                        add_moves.append([i, i+j*7])
                        j += 1
                j = 1
                while j < y+1 and j < 8 - x: # up-right loop
                    if i-j*7 < 0:
                        j = 8
                    elif board[i-j*7] & piece.white == piece.white:
                        j = 8
                    elif board[i-j*7] & piece.black == piece.black:
                        add_moves.append([i, i-j*7])
                        j = 8
                    else:
                        add_moves.append([i, i-j*7])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square & piece.pawn == piece.pawn:
                if i // 8 != 0:
                    add_moves = []
                    # Capture moves
                    if board[i-7] != 0:
                        add_moves.append([i, i-7])
                    if board[i-9] != 0:
                        add_moves.append([i, i-9])
                    # Remove moves that would capture white pieces
                    j = 0
                    while j < len(add_moves):
                        if board[add_moves[j][1]] & piece.white == piece.white:
                            add_moves.pop(j)
                        else:
                            j += 1
                    moves.extend(add_moves)
                continue
        elif square & turn == piece.black:
            # Generate moves for each piece
            if square & piece.king == piece.king:
                add_moves = [[i, i-9],[i, i-8],[i, i-7],
                              [i, i-1],         [i, i+1],
                              [i, i+7],[i, i+8],[i, i+9]]
                    
                # Remove moves where king teleports
                j = 0
                while j < len(add_moves):
                    if not(0 <= add_moves[j][1]//8 <= 7) or ((add_moves[j][1] % 8 - add_moves[j][0] % 8) not in [-1, 0, 1]):
                        add_moves.pop(j)
                    else:
                        j += 1
                # Remove moves that would capture black pieces
                j = 0
                while j < len(add_moves):
                    if board[add_moves[j][1]] & piece.black == piece.black:
                        add_moves.pop(j)
                    else:
                        j += 1
                moves.extend(add_moves)
                continue
            elif square & piece.queen == piece.queen:
                add_moves = []
                x, y = i % 8, i // 8 
                j = 1
                while j < 8 - x: # right loop
                    if i+j > 63:
                        j = 8
                    elif board[i+j] & piece.black == piece.black:
                        j = 8
                    elif board[i+j] & piece.white == piece.white:
                        add_moves.append([i, i+j])
                        j = 8
                    else:
                        add_moves.append([i, i+j])
                        j += 1
                j = 1
                while j < x+1: # left loop
                    if i-j < 0:
                        j = 8
                    elif board[i-j] & piece.black == piece.black:
                        j = 8
                    elif board[i-j] & piece.white == piece.white:
                        add_moves.append([i, i-j])
                        j = 8
                    else:
                        add_moves.append([i, i-j])
                        j += 1
                j = 1
                while j < 8 - y: # down loop
                    if i+j*8 > 63:
                        j = 8
                    elif board[i+j*8] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*8] & piece.white == piece.white:
                        add_moves.append([i, i+j*8])
                        j = 8
                    else:
                        add_moves.append([i, i+j*8])
                        j += 1
                j = 1
                while j < y+1: # up loop
                    if i-j*8 < 0:
                        j = 8
                    elif board[i-j*8] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*8] & piece.white == piece.white:
                        add_moves.append([i, i-j*8])
                        j = 8
                    else:
                        add_moves.append([i, i-j*8])
                        j += 1
                j = 1
                while j < 8 - x and j < 8 - y: # down-right loop
                    if i+j*9 > 63:
                        j = 8
                    elif board[i+j*9] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*9] & piece.white == piece.white:
                        add_moves.append([i, i+j*9])
                        j = 8
                    else:
                        add_moves.append([i, i+j*9])
                        j += 1
                j = 1
                while j < x+1 and j < y+1: # up-left loop
                    if i-j*9 < 0:
                        j = 8
                    elif board[i-j*9] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*9] & piece.white == piece.white:
                        add_moves.append([i, i-j*9])
                        j = 8
                    else:
                        add_moves.append([i, i-j*9])
                        j += 1
                j = 1
                while j < 8 - y and j < x+1: # down-left loop
                    if i+j*7 > 63:
                        j = 8
                    elif board[i+j*7] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*7] & piece.white == piece.white:
                        add_moves.append([i, i+j*7])
                        j = 8
                    else:
                        add_moves.append([i, i+j*7])
                        j += 1
                j = 1
                while j < y+1 and j < 8 - x: # up-right loop
                    if i-j*7 < 0:
                        j = 8
                    elif board[i-j*7] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*7] & piece.white == piece.white:
                        add_moves.append([i, i-j*7])
                        j = 8
                    else:
                        add_moves.append([i, i-j*7])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square & piece.rook == piece.rook:
                add_moves = []
                x, y = i % 8, i // 8
                j = 1
                while j < 8 - x: # right loop
                    if i+j > 63:
                        j = 8
                    elif board[i+j] & piece.black == piece.black:
                        j = 8
                    elif board[i+j] & piece.white == piece.white:
                        add_moves.append([i, i+j])
                        j = 8
                    else:
                        add_moves.append([i, i+j])
                        j += 1
                j = 1
                while j < x+1: # left loop
                    if i-j < 0:
                        j = 8
                    elif board[i-j] & piece.black == piece.black:
                        j = 8
                    elif board[i-j] & piece.white == piece.white:
                        add_moves.append([i, i-j])
                        j = 8
                    else:
                        add_moves.append([i, i-j])
                        j += 1
                j = 1
                while j < 8 - y: # down loop
                    if i+j*8 > 63:
                        j = 8
                    elif board[i+j*8] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*8] & piece.white == piece.white:
                        add_moves.append([i, i+j*8])
                        j = 8
                    else:
                        add_moves.append([i, i+j*8])
                        j += 1
                j = 1
                while j < y+1: # up loop
                    if i-j*8 < 0:
                        j = 8
                    elif board[i-j*8] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*8] & piece.white == piece.white:
                        add_moves.append([i, i-j*8])
                        j = 8
                    else:
                        add_moves.append([i, i-j*8])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square & piece.knight == piece.knight:
                add_moves = [
                        [i, i-17],      [i, i-15],
                [i, i-10],                      [i, i-6],

                 [i, i+6],                       [i, i+10],
                        [i, i+15],      [i, i+17],
                ]
                # Remove moves where knight teleports
                j = 0
                while j < len(add_moves):
                    if not(0 <= add_moves[j][1]//8 <= 7) or ((add_moves[j][1] % 8 - add_moves[j][0] % 8) not in [-2, -1, 1, 2]):
                        add_moves.pop(j)
                    else:
                        j += 1
                # Remove moves that would capture black pieces
                j = 0
                while j < len(add_moves):
                    if board[add_moves[j][1]] & piece.black == piece.black:
                        add_moves.pop(j)
                    else:
                        j += 1
                moves.extend(add_moves)
                continue
            elif square & piece.bishop == piece.bishop:
                add_moves = []
                x, y = i % 8, i // 8
                j = 1
                while j < 8 - x and j < 8 - y: # down-right loop
                    if i+j*9 > 63:
                        j = 8
                    elif board[i+j*9] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*9] & piece.white == piece.white:
                        add_moves.append([i, i+j*9])
                        j = 8
                    else:
                        add_moves.append([i, i+j*9])
                        j += 1
                j = 1
                while j < x+1 and j < y+1: # up-left loop
                    if i-j*9 < 0:
                        j = 8
                    elif board[i-j*9] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*9] & piece.white == piece.white:
                        add_moves.append([i, i-j*9])
                        j = 8
                    else:
                        add_moves.append([i, i-j*9])
                        j += 1
                j = 1
                while j < 8 - y and j < x+1: # down-left loop
                    if i+j*7 > 63:
                        j = 8
                    elif board[i+j*7] & piece.black == piece.black:
                        j = 8
                    elif board[i+j*7] & piece.white == piece.white:
                        add_moves.append([i, i+j*7])
                        j = 8
                    else:
                        add_moves.append([i, i+j*7])
                        j += 1
                j = 1
                while j < y+1 and j < 8 - x: # up-right loop
                    if i-j*7 < 0:
                        j = 8
                    elif board[i-j*7] & piece.black == piece.black:
                        j = 8
                    elif board[i-j*7] & piece.white == piece.white:
                        add_moves.append([i, i-j*7])
                        j = 8
                    else:
                        add_moves.append([i, i-j*7])
                        j += 1
                moves.extend(add_moves)
                continue
            elif square & piece.pawn == piece.pawn:
                if i // 8 != 7:
                    add_moves = []
                    # Capture moves
                    if board[i+7] != 0:
                        add_moves.append([i, i+7])
                    if board[i+9] != 0:
                        add_moves.append([i, i+9])
                    # Remove moves that would capture black pieces
                    j = 0
                    while j < len(add_moves):
                        if board[add_moves[j][1]] & piece.black == piece.black:
                            add_moves.pop(j)
                        else:
                            j += 1
                    moves.extend(add_moves)
                continue
    return moves
    
def generate_legal_moves():
    '''Removes moves that result in possible capture of allied king'''
    global board, moves, turn, over

    # Generate moves 
    generate_moves()
    
    i = 0
    while i < len(moves):
        
        # Loop through possible moves and play them
        test_move = moves[i]
        new_board = board.copy()
        new_board = _play(test_move, new_board)
        
        # Generate moves for opponent
        if turn == piece.white:
            new_moves = _generate_moves(piece.black, new_board)
        else:
            new_moves = _generate_moves(piece.white, new_board)
        j, legal = 0, True

        # Loop for possible moves of opponent which end up in king's capture
        while legal and j < len(new_moves):
            new_move = new_moves[j]
            if turn == piece.white:
                if new_board[new_move[1]] == piece.king | piece.white:
                    # Pawn bug fix
                    if not ((new_board[new_move[0]] % piece.white == piece.pawn) and (new_move[0]+8 == new_move[1])):
                        legal = False
                if len(test_move) == 4 and new_move[1] == 60:
                    legal = False
            else:
                if new_board[new_move[1]] == piece.king | piece.black:
                    # Pawn bug fix
                    if not ((new_board[new_move[0]] % piece.white == piece.pawn) and (new_move[0]-8 == new_move[1])):
                        legal = False
                if len(test_move) == 4 and new_move[1] == 4:
                    legal = False
            if len(test_move) == 4:
                if new_move[1] == test_move[3]:
                    legal = False

            j += 1
        if not legal:
            moves.pop(i)
        else:
            i += 1
    if len(moves) == 0:
        if turn == piece.white:
            new_moves = _generate_moves(piece.black, board)
            draw = True
            for new_move in new_moves:
                if board[new_move[1]] == piece.white | piece.king:
                    draw = False
            if draw:
                over = piece.draw
            else:
                over = piece.black
        else:
            new_moves = _generate_moves(piece.white, board)
            draw = True
            for new_move in new_moves:
                if board[new_move[1]] == piece.black | piece.king:
                    draw = False
            if draw:
                over = piece.draw
            else:
                over = piece.white
    return

def score(turn:int, board:list[int]):
    '''Returns a score for the *turn* player on *board* state. Used for minimax AI.'''
    score = 0
    # Change according to who is being evaluated
    player = 1
    if turn == piece.black:
        player = -1
    
    # Loop through all squares
    for i in range(len(board)):
        square = board[i]
        p_value = square % piece.white
        p_score = 0
        if square & piece.white:
            if p_value == piece.king:
                p_score = const.king + const.kingEvalWhite[i]
            if p_value == piece.queen:
                p_score = const.queen + const.queenEval[i]
            if p_value == piece.rook:
                p_score = const.rook + const.rookEvalWhite[i]
            if p_value == piece.knight:
                p_score = const.knight + const.knightEval[i]
            if p_value == piece.bishop:
                p_score = const.bishop + const.bishopEvalWhite[i]
            if p_value == piece.pawn:
                p_score = const.pawn + const.pawnEvalWhite[i]
        elif square & piece.black:
            if p_value == piece.king:
                p_score = (const.king + const.kingEvalBlack[i]) * -1
            if p_value == piece.queen:
                p_score = (const.queen + const.queenEval[i]) * -1
            if p_value == piece.rook:
                p_score = (const.rook + const.rookEvalBlack[i]) * -1
            if p_value == piece.knight:
                p_score = (const.knight + const.knightEval[i]) * -1
            if p_value == piece.bishop:
                p_score = (const.bishop + const.bishopEvalBlack[i]) * -1
            if p_value == piece.pawn:
                p_score = (const.pawn + const.pawnEvalBlack[i]) * -1
        score += p_score * player
    
    return score

def minimax(depth:int): #TODO
    '''Performs minimax selection of best move over *depth* moves'''
    return