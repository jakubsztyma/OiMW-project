import fire
from chess import engine as chess_engine, pgn

LIMIT = chess_engine.Limit(time=0.1)

def get_output(move1, move2):
    return [board.fen()]

def meets_conditions(move1, move2):
    # Moves are sorted starting by the best
    score1 = move1['score'].white().score()
    score2 = move2['score'].white().score()
    return max(score1, score2) > 100 + min(score1, score2)

def handle_game(engine, game):
    print(game.headers['Event'])
    positions = []
    board = game.board()

    for move in game.mainline_moves():
        move1, move2 = engine.analyse(board, LIMIT, multipv=2)
        if meets_conditions(move1, move2):
            node_output = get_output(move1, move2)
            positions.extend(node_output)
        board.push(move)
    return positions[:2]


def entrypoint(
        input_path,
        output_path,
        h='minimal',
        cp=50,
        d=30,
        n=2,
        e='stockfish-10/Linux/stockfish_10_x64',
        # TODO chess engine params
):
    print(input_path, output_path, h, cp, d, n, e)  # Show selected params

    engine = chess_engine.SimpleEngine.popen_uci(e)

    with open(input_path, 'r') as input_, open(output_path, 'w') as output:
        game = pgn.read_game(input_)
        # while game:
        for _ in range(10):
            try:
                positions = handle_game(engine, game)
                for position in positions:
                    output.write(position + '\n')
            except Exception as ex:
                print(ex)
            finally:
                game = pgn.read_game(input_)

    engine.quit()


if __name__ == '__main__':
    fire.Fire(entrypoint)
