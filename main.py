def main():
    import pygame, chess
    pygame.init()

    # Variables
    active_squares = [[], [], []] # Last played move and current selected piece
    available_moves = [] # All of the moves of the selected pieces
    active_moves = [] # Non capture moves (for graphics)
    active_captures = [] # Capture moves (for graphics)
    size = 66 # Size of board squares
    timer = pygame.time.get_ticks() # Used for dragging
    start_pos = pygame.mouse.get_pos() # Used for dragging
    promote = [] # src and dest of selected promoting move
    width, height =  530, 530

    # Booleans
    ai_white = False # Is white an AI
    ai_black = False # Is black an AI
    dragging = False # Used for dragging pieces and graphics
    playing = False # Is there a game being played
    promoting = False # If the player must promote

    # SETUP SURFACES --------------------------------------------------------------------------
    piece_size = 69 # size of piece images for scaling
    board = pygame.image.load("assets/board.png")
    Pimg = pygame.transform.scale(pygame.image.load("assets/wp.png"), (piece_size, piece_size))
    pimg = pygame.transform.scale(pygame.image.load("assets/bp.png"), (piece_size, piece_size))
    Bimg = pygame.transform.scale(pygame.image.load("assets/wb.png"), (piece_size, piece_size))
    bimg = pygame.transform.scale(pygame.image.load("assets/bb.png"), (piece_size, piece_size))
    Nimg = pygame.transform.scale(pygame.image.load("assets/wn.png"), (piece_size, piece_size))
    nimg = pygame.transform.scale(pygame.image.load("assets/bn.png"), (piece_size, piece_size))
    Rimg = pygame.transform.scale(pygame.image.load("assets/wr.png"), (piece_size, piece_size))
    rimg = pygame.transform.scale(pygame.image.load("assets/br.png"), (piece_size, piece_size))
    Qimg = pygame.transform.scale(pygame.image.load("assets/wq.png"), (piece_size, piece_size))
    qimg = pygame.transform.scale(pygame.image.load("assets/bq.png"), (piece_size, piece_size))
    Kimg = pygame.transform.scale(pygame.image.load("assets/wk.png"), (piece_size, piece_size))
    kimg = pygame.transform.scale(pygame.image.load("assets/bk.png"), (piece_size, piece_size))

    # Fonts
    promotion_font = pygame.font.Font("assets/arial.ttf", 24)
    game_font = pygame.font.Font("assets/arial.ttf", 50)
    title_font = pygame.font.Font("assets/arial.ttf", 75)

    # Stuff used for promoting
    Brect = bimg.get_rect(topleft = (width/2 - piece_size*2, height/2-piece_size/2))
    Nrect = nimg.get_rect(topleft = (width/2 - piece_size, height/2-piece_size/2))
    Rrect = rimg.get_rect(topleft = (width/2, height/2-piece_size/2))
    Qrect = qimg.get_rect(topleft = (width/2 + piece_size, height/2-piece_size/2))
    GRAY = (180, 180, 180)
    
    # Cancel buttons
    cancel_surf = promotion_font.render("X", False, GRAY)
    cancel_rect = cancel_surf.get_rect(center=(width/2+piece_size*2.2, height/2))
    home_surf = title_font.render("X", False, (0, 0, 0))
    home_rect = home_surf.get_rect(topright=(width, -5))
    
    # Yellow squares
    active_surf = pygame.Surface((67, 67))
    active_surf.fill((255, 255, 0))
    active_surf.set_alpha(128)

    # Black dots
    move_surf = pygame.Surface((67, 67), pygame.SRCALPHA)
    pygame.draw.circle(move_surf, (0, 0, 0), (33, 33), 10, width=0)
    move_surf.set_alpha(64)

    # Black circles
    capture_surf = pygame.Surface((67, 67), pygame.SRCALPHA)
    pygame.draw.circle(capture_surf, (0, 0, 0), (33, 33), 30, width=4)
    capture_surf.set_alpha(64)

    

    chess.startBoardFromFen(
        "rnbqkbnrpppppppp////PPPPPPPPRNBQKBNR",
        chess.piece.white)

    def Draw_pieces(screen):
        '''Draws the pieces of the board array'''
        for i in range(len(chess.board)):
            square = chess.board[i]
            if square == chess.piece.white | chess.piece.pawn:
                screen.blit(Pimg, (i%8*66, i//8*66))
            if square == chess.piece.white | chess.piece.bishop:
                screen.blit(Bimg, (i%8*66, i//8*66))
            if square == chess.piece.white | chess.piece.knight:
                screen.blit(Nimg, (i%8*66, i//8*66))
            if square == chess.piece.white | chess.piece.rook:
                screen.blit(Rimg, (i%8*66, i//8*66))
            if square == chess.piece.white | chess.piece.queen:
                screen.blit(Qimg, (i%8*66, i//8*66))
            if square == chess.piece.white | chess.piece.king:
                screen.blit(Kimg, (i%8*66, i//8*66))
            if square == chess.piece.black | chess.piece.pawn:
                screen.blit(pimg, (i%8*66, i//8*66))
            if square == chess.piece.black | chess.piece.bishop:
                screen.blit(bimg, (i%8*66, i//8*66))
            if square == chess.piece.black | chess.piece.knight:
                screen.blit(nimg, (i%8*66, i//8*66))
            if square == chess.piece.black | chess.piece.rook:
                screen.blit(rimg, (i%8*66, i//8*66))
            if square == chess.piece.black | chess.piece.queen:
                screen.blit(qimg, (i%8*66, i//8*66))
            if square == chess.piece.black | chess.piece.king:
                screen.blit(kimg, (i%8*66, i//8*66))

    def Draw_on_mouse(screen, active_squares):
        '''Draws a piece on the mouse if it is being dragged'''
        square = chess.board[active_squares[2][0]+active_squares[2][1]*8]
        if square == chess.piece.white | chess.piece.pawn:
            screen.blit(Pimg, Pimg.get_rect(center=pygame.mouse.get_pos()))
        if square == chess.piece.white | chess.piece.bishop:
            screen.blit(Bimg, Bimg.get_rect(center=pygame.mouse.get_pos()))
        if square == chess.piece.white | chess.piece.knight:
            screen.blit(Nimg, Nimg.get_rect(center=pygame.mouse.get_pos()))
        if square == chess.piece.white | chess.piece.rook:
            screen.blit(Rimg, Rimg.get_rect(center=pygame.mouse.get_pos()))
        if square == chess.piece.white | chess.piece.queen:
            screen.blit(Qimg, Qimg.get_rect(center=pygame.mouse.get_pos()))
        if square == chess.piece.white | chess.piece.king:
            screen.blit(Kimg, Kimg.get_rect(center=pygame.mouse.get_pos()))
        if square == chess.piece.black | chess.piece.pawn:
            screen.blit(pimg, pimg.get_rect(center=pygame.mouse.get_pos()))
        if square == chess.piece.black | chess.piece.bishop:
            screen.blit(bimg, bimg.get_rect(center=pygame.mouse.get_pos()))
        if square == chess.piece.black | chess.piece.knight:
            screen.blit(nimg, nimg.get_rect(center=pygame.mouse.get_pos()))
        if square == chess.piece.black | chess.piece.rook:
            screen.blit(rimg, rimg.get_rect(center=pygame.mouse.get_pos()))
        if square == chess.piece.black | chess.piece.queen:
            screen.blit(qimg, qimg.get_rect(center=pygame.mouse.get_pos()))
        if square == chess.piece.black | chess.piece.king:
            screen.blit(kimg, kimg.get_rect(center=pygame.mouse.get_pos()))

    def distance(point1, point2):
        # Used for dragging
        return ((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)**0.5

    # set up the window
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess")

    # main loop
    run = True
    while run:
        # EVENTS ----------------------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x_pos, y_pos = pos
                if not playing:
                    if play2_rect.collidepoint(*pygame.mouse.get_pos()):
                        ai_white = False
                        ai_black = False
                        playing = True
                    if playw_rect.collidepoint(*pygame.mouse.get_pos()):
                        ai_white = False
                        ai_black = True
                        playing = True
                    if playb_rect.collidepoint(*pygame.mouse.get_pos()):
                        ai_white = True
                        ai_black = False
                        playing = True
                if chess.over:
                    if home_rect.collidepoint(*pygame.mouse.get_pos()):
                        chess.startBoardFromFen(
                        "rnbqkbnrpppppppp////PPPPPPPPRNBQKBNR",
                        chess.piece.white)
                        playing = False
                        active_squares = [[], [], []]
                if not chess.over and playing and not promoting and (not (ai_white and chess.turn == chess.piece.white)) and (not (ai_black and chess.turn == chess.piece.black)):
                    x = x_pos // size
                    y = y_pos // size
                    # Check if the clicked square can be played from the selected square
                    if x+y*8 in available_moves:
                        src = active_squares[2][0]+active_squares[2][1]*8
                        dest = x+y*8
                        for move in chess.moves:
                            if move[0] == src and move[1] == dest:
                                if len(move) == 5:
                                    promoting = True
                                    promote = [src, dest]
                                else:
                                    chess.play(move)
                                    active_squares[0] = [src%8, src//8]
                                    active_squares[1] = [dest%8, dest//8]
                                    active_squares[2] = []
                    
                    # Clear all effects
                    available_moves = []
                    active_moves = []
                    active_captures = []

                    # Add effects and available moves
                    if x+y*8 < 64:
                        if chess.board[x+y*8] & chess.turn == chess.turn:
                            active_squares[2] = [x, y]
                            for move in chess.moves:
                                if move[0] == x+y*8:
                                    if chess.board[move[1]] == 0:
                                        active_moves.append(move[1])
                                        if len(move) == 3:
                                            active_captures.append(move[1])
                                    else:
                                        active_captures.append(move[1])
                            dragging, timer, start_pos = True, pygame.time.get_ticks() + 100, pygame.mouse.get_pos()
                    available_moves.extend(active_moves)
                    available_moves.extend(active_captures)
                if promoting:
                    if cancel_rect.collidepoint(x_pos, y_pos):
                        promoting, promote = False, []
                    elif Brect.collidepoint(x_pos, y_pos):
                        promoting = False
                        chess.play([promote[0], promote[1], 0, 0, 2])
                        promote = []
                    elif Nrect.collidepoint(x_pos, y_pos):
                        promoting = False
                        chess.play([promote[0], promote[1], 0, 0, 3])
                        promote = []
                    elif Rrect.collidepoint(x_pos, y_pos):
                        promoting = False
                        chess.play([promote[0], promote[1], 0, 0, 4])
                        promote = []
                    elif Qrect.collidepoint(x_pos, y_pos):
                        promoting = False
                        chess.play([promote[0], promote[1], 0, 0, 5])
                        promote = []
            if event.type == pygame.MOUSEBUTTONUP:
                # Try to play dragging move if there was a time delay since dragging start and the piece was moved on dragging
                if dragging and timer < pygame.time.get_ticks() and distance(start_pos, pygame.mouse.get_pos()) > 10:
                    pos = pygame.mouse.get_pos()
                    x_pos, y_pos = pos
                    if not chess.over and playing and not promoting:
                        x = x_pos // size
                        y = y_pos // size
                        if x+y*8 in available_moves:
                            src = active_squares[2][0]+active_squares[2][1]*8
                            dest = x+y*8
                            for move in chess.moves:
                                if move[0] == src and move[1] == dest:
                                    if len(move) == 5:
                                        promoting = True
                                        promote = [src, dest]
                                    else:
                                        chess.play(move)
                                        active_squares[0] = [src%8, src//8]
                                        active_squares[1] = [dest%8, dest//8]
                                        active_squares[2] = []
                        available_moves = []
                        active_moves = []
                        active_captures = []
                dragging = False
        
        # DRAW ----------------------------------------------------------------------------------

        # Draw the board and square effects
        screen.fill("#5F5F5F")
        screen.blit(board, (0, 0))
        for active in active_squares:
            if active:
                x, y = active[0], active[1]
                screen.blit(active_surf, (x*size+1, y*size+1))
        for active in active_moves:
            x, y = active%8, active//8
            screen.blit(move_surf, (x*size+1, y*size+1))
        for active in active_captures:
            x, y = active%8, active//8
            screen.blit(capture_surf, (x*size+1, y*size+1))
        
        # Draw pieces
        Draw_pieces(screen)
        
        # Draw piece on mouse if dragging
        if dragging and timer < pygame.time.get_ticks() and distance(start_pos, pygame.mouse.get_pos()) > 10:
            x, y = active_squares[2][0], active_squares[2][1]
            screen.blit(active_surf, (x*size+1, y*size+1))
            Draw_on_mouse(screen, active_squares)
        
        # Draw game over
        if chess.over:
            ai_white = False
            ai_black = False
            if chess.over == chess.piece.white:
                text = game_font.render("White wins", False, (0, 0, 0))
            elif chess.over == chess.piece.black:
                text = game_font.render("Black wins", False, (0, 0, 0))
            else:
                text = game_font.render("Stalemate", False, (0, 0, 0))
            text_rect = text.get_rect(center=(width/2,height/2))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(width/2-text_rect.width/2-5, height/2-text_rect.height/2-5, text_rect.width+10, text_rect.height+10), 0, 20)
            screen.blit(text, text_rect)
            screen.blit(home_surf, home_rect)
        if promoting:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(width/2-piece_size*2, height/2-piece_size/2, piece_size*4+40, piece_size), 0, 20)
            screen.blit(cancel_surf, cancel_rect)

            if chess.turn == chess.piece.white:
                screen.blit(Bimg, Brect)
                screen.blit(Nimg, Nrect)
                screen.blit(Rimg, Rrect)
                screen.blit(Qimg, Qrect)
            else:
                screen.blit(bimg, Brect)
                screen.blit(nimg, Nrect)
                screen.blit(rimg, Rrect)
                screen.blit(qimg, Qrect)
        if not playing:
            title = title_font.render("Chess", False, (0, 0, 0))
            title_rect = title.get_rect(midtop=(width/2,size/2))
            play2 = game_font.render("2 Players", False, (0, 0, 0))
            play2_rect = play2.get_rect(midtop=(width/2,height/2))
            playw_rect = Bimg.get_rect(midbottom=(width/2-size*0.55,height/2))
            playb_rect = Bimg.get_rect(midbottom=(width/2+size*0.55,height/2))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(title_rect.x - 5, title_rect.y - 5, title_rect.width + 5, title_rect.height + 5), 0, 20)
            screen.blit(title, title_rect)
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(size*2, size*3-5, size*4, size*2+5), 0, 20)

            # Hover effect on buttons
            if play2_rect.collidepoint(*pygame.mouse.get_pos()):
                pygame.draw.rect(screen, GRAY, play2_rect)
            if playw_rect.collidepoint(*pygame.mouse.get_pos()):
                pygame.draw.rect(screen, GRAY, playw_rect)
            if playb_rect.collidepoint(*pygame.mouse.get_pos()):
                pygame.draw.rect(screen, GRAY, playb_rect)
            
            # Draw buttons
            screen.blit(play2, play2_rect)
            screen.blit(Kimg, playw_rect)
            screen.blit(kimg, playb_rect)

        # Show
        pygame.display.flip()

        # AI play -------------------------------------------------------------------------------

        if ai_white and chess.turn == chess.piece.white:
            chess.ai_play(chess.piece.white)
            active_squares = [[chess.last_move[0]%8, chess.last_move[0]//8], [chess.last_move[1]%8, chess.last_move[1]//8], []]
        if ai_black and chess.turn == chess.piece.black:
            chess.ai_play(chess.piece.black)
            active_squares = [[chess.last_move[0]%8, chess.last_move[0]//8], [chess.last_move[1]%8, chess.last_move[1]//8], []]

    # Exit
    pygame.quit()

if __name__ == "__main__":
    main()