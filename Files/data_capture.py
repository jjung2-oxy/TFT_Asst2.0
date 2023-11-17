import game_functions
from window import Window

class Game:
    def __init__(self):
        self.curr_round = '0-0'
        self.window = Window(0, 0, 2560, 1440)
        self.place = 1
    

    def game_loop(self):

        while True:
            new_round = game_functions.get_round(self.window)
            # if new_round == self.round:
            #     continue
            if new_round in ["0-0", "1-1", "1-2", "2-4", "3-4", "4-4", "5-4", "6-4",
                                  "7-4"]:
                # In a carosell, or a starting round where you can't buy
                continue
            # In a normal round, and the round has updated
            self.place = game_functions.get_place(self.window)
                

