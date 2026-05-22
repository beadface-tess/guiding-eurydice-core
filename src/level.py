import random
import typing as t

from enum import Enum

from .difficulty import Difficulty
from .lyre import Lyre

class Goal:
    class NoGoalDefinedException(Exception):
        pass

    def __init__(
      self,
      val: t.Optional[int]=None,
    ):
        self.val = val or -1
        self.sum_len = -1
          
    def __str__(self) -> str:
        return str(self.val)
    
class Level:
    global_id = 1

    class LevelState(Enum):
        READY = 0
        ORPHEUS_FATAL = 1
        ORPHEUS_SUCCESS = 2
        EURYDICE_THWARTED = 3
        EURYDICE_FAIL = 4
        EURYDICE_FATAL = 5
        SUCCESS = 6

    def _get_next_id(self) -> int:
        Level.global_id += 1
        return Level.global_id - 1

    def __init__(
      self,
      id: t.Optional[int] = None,
      lyre: t.Optional[Lyre]=None,
      difficulty: t.Optional[Difficulty]=None,
      orpheus_goal: t.Optional[Goal]=None,
      debug: t.Optional[bool]=False,
      given_seed: t.Optional[int]=None,
    ):
        print("received id", id)
        self.id = id or self._get_next_id()
        self.eurydice_lives = -1

        self.difficulty = difficulty or Difficulty()

        self.lyre = lyre or Lyre()

        self.original_lyre = self.lyre.copy()
        self.backup_lyre = None

        if orpheus_goal is not None:
          self.orpheus_goal = orpheus_goal
        else:
          self.orpheus_goal = Goal()

        if given_seed is not None:
            self.seed = given_seed
        else:
            self.seed = random.randint(0, 1000)

        self.debug = debug
        self.lyre.debug = debug

        self.eurydice_goal = Goal()
        self.state = self.LevelState.READY
        self.rng = random.Random(self.seed)
        self.lyre.rng = self.rng
        self.lyre.difficulty = self.difficulty
        self.backup_rng_state = None
      
    def __str__(self) -> str:
        res = str(self.lyre)

        if (self.debug):
            res += "\n"
            res += "Eurydice needs: " + str(self.eurydice_goal) + f" ({self.eurydice_lives} lives remaining)"
        
        return res

    def get_state(self) -> LevelState:
       return self.state       
    
    def play_note(self, note: str):
        self.lyre.play_note(note)

    def back_up_lyre(self):
        self.backup_lyre = self.lyre.copy()    

    def back_up_rng(self):
        self.backup_rng_state = self.rng.getstate()

    def thwart_rollback(self):
        self.lyre = self.backup_lyre
        self.rng.setstate(self.backup_rng_state)

    def resolve_thwart(self):
        self.eurydice_lives -= 1
        self.thwart_rollback()
        self.state = Level.LevelState.ORPHEUS_SUCCESS

    def reset(
        self,
        given_seed: t.Optional[int] = None,
    ):
        self.state = Level.LevelState.READY
        self.eurydice_goal = Goal()
        self.lyre = self.original_lyre

        if given_seed is not None:
            self.seed = given_seed
        else:
            self.seed = random.randint(0, 1000)
        
        self.rng = random.Random(self.seed)

    def set_eurydice_goal(self):
        if self.state != self.LevelState.ORPHEUS_SUCCESS:
            raise Exception

        eligible_notes = [note for note in self.lyre.notes if note.count > 0]
        
        flattened_notes : t.List[int] = []
        for note in eligible_notes:
          flattened_notes.extend([note.val] * note.count)

        if self.debug:
            print("LEVEL ID:", self.id)
            print("SEED:", self.seed)
            print("RNG STATE:", self.rng.getstate()[1][:5])
            print("LYRE:", [(n.name, n.val, n.count) for n in self.lyre.notes])
            print("ELIGIBLE LEN:", len(eligible_notes))

        eurydice_goal_sum_len = self.rng.randint(int(len(eligible_notes) / 2), len(eligible_notes))

        if self.debug:
            print("GOAL LEN: ", str(eurydice_goal_sum_len))

        possible_totals = sorted(self.lyre.possible_sums(flattened_notes, eurydice_goal_sum_len))
      
        self.eurydice_lives = len(possible_totals)
        self.eurydice_goal.val = possible_totals[self.rng.randint(0, len(possible_totals) - 1)]
        self.eurydice_goal.sum_len = eurydice_goal_sum_len

    def try_orpheus(
        self,
        total: int,
    ):
        if total == self.orpheus_goal.val:
            self.state = self.LevelState.ORPHEUS_SUCCESS
        else:
            self.state = self.LevelState.ORPHEUS_FATAL

    def check_eurydice(
        self,
        num_notes: int,
        total: int,
    ) -> bool:
        if self.debug:
            print("Checking Eurydice...")
        if (num_notes == self.eurydice_goal.sum_len):
            if (total == self.eurydice_goal.val):
                if self.debug:
                    print("Eurydice has met her goal. Returning True.")

                self.state = self.LevelState.SUCCESS
                return True
        else:
            if self.debug:
                print("Sum length is incorrect.")
                
            self.state = self.LevelState.EURYDICE_FATAL
            return False

        if self.eurydice_lives == 0:
            if self.debug:
                print("Eurydice is out of lives.")
            self.state = self.LevelState.EURYDICE_FATAL
            return False
        
        solutions = self.lyre.n_sum(self.eurydice_goal.val, self.eurydice_goal.sum_len)

        if self.debug:
            print(f"Found {str(len(solutions))} solutions for Eurydice: {[[str(note) for note in soln] for soln in solutions]}")
        if len(solutions) == 0:
            if self.debug:
                print("No solutions possible for Eurydice. Thwarting...")
            self.state = self.LevelState.EURYDICE_THWARTED
            return False
        
        else:
            self.state = self.LevelState.EURYDICE_FAIL
            self.eurydice_lives -= 1

            if self.debug:
                print(f"Eurydice has failed. {self.eurydice_lives} lives remaining.")

        return True
        


        
