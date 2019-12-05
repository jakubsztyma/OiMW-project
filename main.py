import chess
import fire

def entrypoint():
    board = chess.Board()
    print(board.legal_moves)


if __name__ == '__main__':
    fire.Fire(entrypoint)