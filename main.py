import collections

import fire
from chess import engine as chess_engine, pgn

LIMIT = chess_engine.Limit(time=0.1)


class Solver:
    def __init__(self, cp, d, n, e):
        self.n = n
        self.d = d
        self.cp = cp
        self.engine = chess_engine.SimpleEngine.popen_uci(e)


    def get_output(self, board, moves):
        return [board.fen()]

    def meets_conditions(self, best_move, second_best_move):
        # Moves are sorted starting by the best
        score1 = best_move['score'].white().score()
        score2 = second_best_move['score'].white().score()
        return score1 - score2 >= self.cp

    def handle_game(self, game):
        positions = []
        board = game.board()

        for move in game.mainline_moves():
            evaluated_moves = self.engine.analyse(board, LIMIT, multipv=self.n)
            best_move, second_best_move = evaluated_moves[:2]
            if self.meets_conditions(best_move, second_best_move):
                node_output = self.get_output(evaluated_moves)
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
    solver = Solver(cp, d, n, e)

    with open(input_path, 'r') as input_, open(output_path, 'w') as output:
        game = pgn.read_game(input_)
        # while game:
        for _ in range(10):
            try:
                positions = solver.handle_game(game)
                for position in positions:
                    output.write(position + '\n')
            except Exception as ex:
                print(ex)
            finally:
                game = pgn.read_game(input_)

    solver.engine.quit()


if __name__ == '__main__':
    fire.Fire(entrypoint)
