import chess

def draw():
    for y in range(8):
        row = []
        for x in range(8):
            row.append(chess.board[x + y * 8])
        print(row)

def main():
    chess.startBoardFromFen(
    "rnbqkbnrpppppppp////PPPPPPPPRNBQKBNR",
    chess.piece.white)
    print("Moves:", chess.moves, "\n")
    run = True
    while run:
        draw()
        command = input("Enter command: ")
        if command == "q":
            run = False
        elif command:
            command = [int(word.strip()) for word in command.split()]
            print("\n\n")
            if len(command) == 1:
                chess.promote(command[0])
            else:
                chess.play(command)
                chess.generate_legal_moves()
                print("Moves:", chess.moves)
                print("Winner:", chess.over, "\n")

    return



if __name__ == "__main__":
    main()