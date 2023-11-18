import game_functions
from window import Window

class Game:
    def __init__(self):
        self.curr_round = '0-0'
        self.window = Window(0, 0, 2560, 1440)
        self.place = 1
        self.arrow_pos = 0
        self.timer_state = "transition_1"
        self.timer = 1
        self.game_loop()


    def game_loop(self):
        photo_taken = False
        while True:
            new_round = game_functions.get_round(self.window)
            if new_round and new_round != self.curr_round:
                print(new_round)
                self.timer_state = "transition_2"
                print("new round, setting state to transition_2")
                self.curr_round = new_round
                photo_taken = False
            # if new_round == self.round:
            #     continue
            if new_round in ["0-0", "1-1", "1-2", "2-4", "3-4", "4-4", "5-4", "6-4",
                                  "7-4"]:
                # In a carosell, or a starting round where you can't buy
                continue
            # In a normal round, and the round has updated
            timer = game_functions.get_timer(self.window)

            if timer != -1:
                if self.timer == 0 and photo_taken == False and self.timer_state == "transition_1":
                    game_functions.grab_enemy_board(self.window)
                    photo_taken = True
                if self.timer < 2  and timer >= 2:
                    self.timer_state = game_functions.next_timer_state(self.timer_state)
                    print("New state:", self.timer_state)
    
                self.timer = timer
            new_place = game_functions.get_place(self.window)
            if new_place:
                if new_place != self.place:
                    print("Now in", new_place, "Place")
                self.place = new_place
            
            arrow_pos = game_functions.get_arrow(self.window)
            if arrow_pos:
                if arrow_pos != self.arrow_pos:
                    print("Now spectating", arrow_pos, "position")
                    self.arrow_pos = arrow_pos
                    if self.timer_state == "preparation":
                        game_functions.grab_enemy_board(self.window)
            else:
                if self.arrow_pos:
                    print("No longer spectating anyone")
                    self.arrow_pos = 0
            
            

                
def main():
    Game()

if __name__ == "__main__":
    main()