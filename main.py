from time import time

import fire
import filters as ff
from chess import engine as chess_engine, pgn

from uci_http_client import UCIHttpClient



class Solver:
    CONCISE_HEADERS = {'White', 'Black', 'Site', 'Date'}

    def __init__(self, h, cp, d, cpu_cores, **kwargs):
        self.h = h
        self.cpu_cores = cpu_cores
        self.cp = cp
        self.limit = chess_engine.Limit(depth=d)
        self.engine = UCIHttpClient()

    def __del__(self):
        pass
        # self.engine.quit()

    def get_desired_headers(self, game_headers):
        if self.h == 'minimal':
            return {}
        elif self.h == 'concise':
            result = {key: val for key, val in game_headers.items() if key in self.CONCISE_HEADERS}
            return result
        elif self.h == 'all':
            return game_headers
        else:
            raise Exception('Invalid h parameter')

    def get_output(self, headers, board, moves):
        # TODO format output accordingly to specification
        result = []
        for move in moves:
            uci_move = move['pv'][0]
            board.push(uci_move)
            output_headers = {'fen':board.fen(), **headers}
            game = pgn.Game(headers=output_headers)
            result.append(str(game))
            board.pop()
        return result

    def meets_conditions(self, best_move, second_best_move):
        # TODO add other constraints
        # Moves are sorted starting by the best
        score1 = best_move['score'].white().score()
        score2 = second_best_move['score'].white().score()
        return score1 - score2 >= self.cp

    def handle_game(self, game):
        positions = []
        board = game.board()
        headers = self.get_desired_headers(game.headers)

        for move in game.mainline_moves():
            evaluated_moves = self.engine.analyse(board.fen(), self.limit, cores=self.cpu_cores)
            #ff.not_a_starting_move(game, move, evaluated_moves)
            best_move, second_best_move = evaluated_moves[:2]
            if self.meets_conditions(best_move, second_best_move):
                print(f'Move found {best_move["pv"][0]}')
                node_output = self.get_output(headers, board, evaluated_moves)
                positions.extend(node_output)
            board.push(move)
        return positions


def entrypoint(
        input_path = "test_pgn.pgn",
        output_path = "out.test",
        h='minimal',
        cp=50,
        d=10,
        cpu_cores=2,
        **kwargs
):

    print(input_path, output_path, h, cp, d, cpu_cores)  # Show selected params
    solver = Solver(h, cp, d, cpu_cores, **kwargs)

    with open(input_path, 'r') as input_, open(output_path, 'w') as output:
        game = pgn.read_game(input_)
        # while game:
        start = time()
        for _ in range(5):
            try:
                positions = solver.handle_game(game)
                for position in positions:
                    output.write(position + '\n')
            except Exception as ex:
                print(ex)
            finally:
                game = pgn.read_game(input_)
        print(time() - start)


if __name__ == '__main__':
    fire.Fire(entrypoint)
