from time import time

import fire
import filters as ff
from chess import engine as chess_engine, pgn, Move

from uci_http_client import UCIHttpClient

#python3 -m pipenv run main.py --depth=4


class Solver:
    CONCISE_HEADERS = {"White", "Black", "Site", "Date"}

    def __init__(self, h, cp, depth, alt, cpu_cores, **kwargs):
        self.h = h
        # self.cpu_cores = cpu_cores
        self.cp = cp
        self.depth = depth
        # self.limit = chess_engine.Limit(depth=depth)
        self.alternatives = alt
<<<<<<< HEAD
        self.limit = chess_engine.Limit(depth=d) # not to be used
        self.engine = UCIHttpClient()
=======
        self.engine = UCIHttpClient(alt, cpu_cores)
>>>>>>> f096c9d16c1b9a8c7da5e361157ab40ed5dbd91e

    def __del__(self):
        pass
        # self.engine.quit()

    def get_desired_headers(self, game_headers):
        if self.h == "minimal":
            return {}
        elif self.h == "concise":
            result = {
                key: val
                for key, val in game_headers.items()
                if key in self.CONCISE_HEADERS
            }
            return result
        elif self.h == "all":
            return game_headers
        else:
            raise Exception("Invalid h parameter")

    def get_comment(self, move, real_move_uci):
        cp = move.get("cp", "")
        was_played = move["pv"] == real_move_uci
        if was_played:
            return f"{cp} G"
        return cp

<<<<<<< HEAD
        evaluated_moves2 = self.engine.analyse(
                board.fen(), self.maxdepth, cores=self.cpu_cores, levels=self.alternatives
            )
        second_best_moves = [evaluated_moves2[(self.maxdepth - 1) * self.alternatives + 1 + i] for i in range(self.alternatives-1)]
        second_best_moves = [(board_num, second_best["pv"][0], second_best["cp"], real_move == second_best["pv"][0]) for second_best in second_best_moves]
=======
    def get_output(self, headers, board, real_move_uci, moves):
        output_headers = {"FEN": board.fen(), **headers}
        game = pgn.Game(headers=output_headers)
>>>>>>> f096c9d16c1b9a8c7da5e361157ab40ed5dbd91e

        best_move = moves[0]
        game.add_main_variation(Move.from_uci(best_move["pv"]), comment=self.get_comment(best_move, real_move_uci))

        for move in moves[1:]:
            game.add_variation(Move.from_uci(move["pv"]), comment=self.get_comment(move, real_move_uci))
        return str(game)

    def handle_game(self, game):
        positions = []
        board = game.board()
        headers = self.get_desired_headers(game.headers)

        for move in game.mainline_moves():
<<<<<<< HEAD
            evaluated_moves = self.engine.analyse(
                board.fen(), self.maxdepth, cores=self.cpu_cores
            )
=======
            print(move)
            all_evaluated = self.engine.analyse(board.fen(), self.depth)
>>>>>>> f096c9d16c1b9a8c7da5e361157ab40ed5dbd91e

            depth = self.depth
            if depth not in all_evaluated:
                print("moves for selected depth were not generated")
                board.push(move)
                continue

            evaluated_moves = all_evaluated[depth]
            best_move = evaluated_moves[0]["pv"]

            if all([
                ff.not_only_move(evaluated_moves),
                ff.not_losing(evaluated_moves),
                ff.not_a_starting_move(board, n_ignore=8),
                ff.not_check(board, best_move=best_move),
                ff.better_than_second(evaluated_moves, min_diff=self.cp),
                ff.not_strong_in_given_depth(all_evaluated, depth=4, best_move=best_move),
                ff.is_not_best_material_gain(board, best_move)
            ]):
                print(f"Move found {best_move}")
                node_output = self.get_output(headers, board, move.uci(), evaluated_moves)
                positions.append(node_output)

            board.push(move)
        return positions


def entrypoint(
<<<<<<< HEAD
    input_path="test_pgn.pgn",
    output_path="out.test",
    h="minimal",
    cp=20,  
    d=20,
    alt = 4, 
    cpu_cores=2,
    **kwargs,
=======
        input_path="test_pgn.pgn",
        output_path="out.test",
        h="minimal",
        cp=50,  # this arg should probably be placed with filters only
        depth=7,
        alt=3,
        cpu_cores=2,
        **kwargs
>>>>>>> f096c9d16c1b9a8c7da5e361157ab40ed5dbd91e
):
    print(input_path, output_path, h, cp, depth, alt, cpu_cores)  # Show selected params
    solver = Solver(h, cp, depth, alt, cpu_cores, **kwargs)

    with open(input_path, "r") as input_, open(output_path, "w") as output:
        start = time()
<<<<<<< HEAD
  
        positions = solver.handle_game(game)
        for _ in range(5): #does nothing atm?
            try:
                for p in positions:
                    output.write("\n[FEN '{}'] \n".format(p[0]))
                    to_print = "{}. {} {{{}}}{} ".format(p[1][0], p[1][1], p[1][2], "{G}" if p[1][3] else "")
                    for k in p[2]:
                        to_print += "({}. {} {{{}}}{}) ".format(k[0], k[1], k[2], "{G}" if k[3] else "")
                    print("[FEN {}]".format(p[0]) + "\n" + to_print)
                    output.write(to_print)
            except Exception as ex:
                print(ex)
            finally:
                game = pgn.read_game(input_)
=======

        while True:
            game = pgn.read_game(input_)
            if game is None:
                break
            for p in solver.handle_game(game):
                output.write(str(p))
                output.write("\n\n")

>>>>>>> f096c9d16c1b9a8c7da5e361157ab40ed5dbd91e
        print(time() - start)


if __name__ == "__main__":
    fire.Fire(entrypoint)
