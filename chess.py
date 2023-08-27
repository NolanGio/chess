'''Chess engine'''

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

board = [0]*64
'''The chess board using a single array representation'''
turn = piece.white # piece.white = 8 and piece.black = 16
'''Whose turn is it currently: piece.white / piece.black'''
moves = []
'''Array of possible moves'''
last_move = []
'''Last move taken by previous player:[source, destination, piece]'''
must_promote = []
'''Array used as boolean to indicate if promote() function must be called to promote a pawn on said square'''

def startBoardFromFen(fen_string:str, first_turn:int):
    '''Starts the board array using FEN notation'''
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

def play(move:list[int]):
    '''Plays a move on the board array'''
    # Is there a promotion to be made?
    global must_promote
    if must_promote:
        print("Must promote on square:", must_promote)
    else:
        board[move[1]] = board[move[0]]
        board[move[0]] = 0
        last_move = [move[0], move[1], board[move[1]]]
        if len(move) == 3:
            board[move[2]] = 0
        if last_move[2] & piece.pawn and (last_move[1] // 8 == 0 or last_move[1] // 8 == 7):
            promote = [last_move[1]]
    return

def _play(move:list[int], board:list[int]):
    '''Same as play but for legal moves generation'''
    board[move[1]] = board[move[0]]
    board[move[0]] = 0
    if len(move) == 3:
        board[move[2]] = 0
    return

def promote(piece:int):
    if piece in [2, 3, 4, 5]:
        board[must_promote] = piece
        must_promote = []
    else:
        raise ValueError("piece must be defined using valid pieces constants such as piece.queen")
    return

def generate_moves(): #TODO
    '''
    Generate moves (ex. [56, 40]) which indicate start, and arrival.
    This array will have a 3rd value for square capture (ex. enpassant).
    This function does not keep track of legal moves.
    This affects the moves array of the module
    '''
    add_moves = []
    if turn == piece.white:
        for i in range(len(board)):
            square = board[i]
            if square & piece.white:
                # Generate moves for each piece
                if square & piece.pawn:
                    add_moves = [[i, i-8]]
                    # Check for double step
                    if i//8 == 6:
                        add_moves = [[i, i-8], [i, i-16]]
                    # Check for enpassant if there was a previous move
                    if last_move:
                        # Check if double step was made by a pawn
                        if last_move[2] & piece.pawn:
                            if last_move[0] == i-17 and last_move[1] == i-1:
                                add_moves.append([i, i-9, i-1])
                            elif last_move[0] == i-15 and last_move[1] == i+1:
                                add_moves.append([i, i-7, i+1])
                    # Remove moves that would capture white pieces
                    j = 0
                    while j < len(add_moves):
                        if board[add_moves[j][1]] & piece.white:
                            add_moves.pop(j)
                        else:
                            j += 1
                    moves.extend(add_moves)
                    continue
                elif square & piece.bishop:
                    continue
                elif square & piece.knight:
                    add_moves = []
                    # Remove moves that would capture white pieces
                    j = 0
                    while j < len(add_moves):
                        if add_moves[j][1] & piece.white:
                            add_moves.pop(j)
                        else:
                            j += 1
                    moves.extend(add_moves)
                    continue
                elif square & piece.rook:
                    continue
                elif square & piece.queen:
                    continue
                elif square & piece.king:
                    add_moves = [[i, i-9],[i, i-8],[i, i-7],
                                  [i, i-1],         [i, i+1],
                                  [i, i+7],[i, i+8],[i, i+9]]
                    # Remove moves that would capture white pieces
                    j = 0
                    while j < len(add_moves):
                        if board[add_moves[j][1]] & piece.white:
                            add_moves.pop(j)
                        else:
                            j += 1
                    moves.extend(add_moves)
                    continue
    else:
        for i in range(len(board)):
            square = board[i]
            if square & piece.white:
                # Generate moves for each piece
                if square & piece.pawn:
                    add_moves = [[i, i-8]]
                    # Check for double step
                    if i//8 == 6:
                        add_moves.append([i, i-16])
                    # Check for enpassant
                    if last_move[2] & piece.pawn:
                        if last_move[0] == i-17 and last_move[1] == i-1:
                            add_moves.append([i, i-9, piece.white])
                        elif last_move[0] == i-15 and last_move[1] == i+1:
                            add_moves.append([i, i-7, piece.white])
                    # Remove moves that would capture white pieces
                    for j in range(len(add_moves)):
                        if add_moves[j][1] & piece.white:
                            add_moves.pop(j)
                    moves.extend(add_moves)
                    continue
                elif square & piece.knight:
                    add_moves = [[i, i-9],[i, i-8],[i, i-7],
                                  [i, i-1],         [i, i+1],
                                  [i, i+7],[i, i+8],[i, i+9]]
                    # Remove moves that would capture white pieces
                    for j in range(len(add_moves)):
                        if add_moves[j][1] & piece.white:
                            add_moves.pop(j)
                    moves.extend(add_moves)
                    continue
                elif square & piece.bishop:
                    add_moves = [[i, i-9],[i, i-8],[i, i-7],
                                  [i, i-1],         [i, i+1],
                                  [i, i+7],[i, i+8],[i, i+9]]
                    # Remove moves that would capture white pieces
                    for j in range(len(add_moves)):
                        if add_moves[j][1] & piece.white:
                            add_moves.pop(j)
                    moves.extend(add_moves)
                    continue
                elif square & piece.rook:
                    add_moves = [[i, i-9],[i, i-8],[i, i-7],
                                  [i, i-1],         [i, i+1],
                                  [i, i+7],[i, i+8],[i, i+9]]
                    # Remove moves that would capture white pieces
                    for j in range(len(add_moves)):
                        if add_moves[j][1] & piece.white:
                            add_moves.pop(j)
                    moves.extend(add_moves)
                    continue
                elif square & piece.queen:
                    add_moves = [[i, i-9],[i, i-8],[i, i-7],
                                  [i, i-1],         [i, i+1],
                                  [i, i+7],[i, i+8],[i, i+9]]
                    # Remove moves that would capture white pieces
                    for j in range(len(add_moves)):
                        if add_moves[j][1] & piece.white:
                            add_moves.pop(j)
                    moves.extend(add_moves)
                    continue
                elif square & piece.king:
                    add_moves = [[i, i-9],[i, i-8],[i, i-7],
                                  [i, i-1],         [i, i+1],
                                  [i, i+7],[i, i+8],[i, i+9]]
                    # Remove moves where king teleports
                    j = 0
                    for j in range(len(add_moves)):
                        if add_moves[j][1] < 0 or add_moves[j][1] > 63 or (add_moves[j][0] % 8 - add_moves[j][1] % 8)**2 != 1:
                            add_moves.pop(j)
                        else:
                            j += 1
                    # Remove moves that would capture white pieces
                    for j in range(len(add_moves)):
                        if add_moves[j][1] & piece.white:
                            add_moves.pop(j)
                    moves.extend(add_moves)
                    continue
    return

def _generate_moves(turn:int, board:list[int]): #TODO
    '''
    Same as generate_moves().
    Returns a list of possible moves.
    Used to check for non legal moves.
    '''
    new_moves = []
    return new_moves
    
def generate_legal_moves():
    '''Removes moves that result in possible capture of allied king'''
    generate_moves()
    for i in range(len(moves)):
        
        # Loop through possible moves and play them
        move = moves[i]
        new_board = board
        _play(move, new_board)
        
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
                    legal = False
            else:
                if new_board[new_move[1]] == piece.king | piece.black:
                    legal = False
        if not legal:
            moves.pop(i)

    return

def minimax(depth:int): #TODO
    '''Performs minimax selection of best move (AI)'''
    return