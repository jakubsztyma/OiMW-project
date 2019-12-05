import fire
from chess import engine as chess_engine, pgn


def handle_game(engine, game):
    print(game.headers['Event'])
    return 'Test'


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
        while True:
            try:
                game = pgn.read_game(input_)
                if game is None:
                    break

                result = handle_game(engine, game)
                output.write(result)
            except Exception as ex:
                print(ex)

    engine.quit()


if __name__ == '__main__':
    fire.Fire(entrypoint)
