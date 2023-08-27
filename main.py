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
    run = True
    while run:
        draw()
        command = input("Enter command: ")
        if command == "q":
            run = False
        elif command:
            command = [int(word.strip()) for word in command.split()]
            print("\n\n")
            chess.play(command)
            chess.generate_moves()
            print("Moves: ", chess.moves, "\n")
    return



if __name__ == "__main__":
    main()