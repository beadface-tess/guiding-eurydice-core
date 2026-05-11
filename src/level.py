import random
import typing as t

from enum import Enum
from itertools import combinations

class Note:
    def __init__(
      self,
      val: t.Optional[int]=-1,
      name: t.Optional[str]="Z",
      count: t.Optional[int]=1,
    ):
      self.val = val
      self.name = name
      self.count = count
        
    def __str__(self) -> str:
        return "{:<2}".format(self.name) + " (" + "{:02d}".format(self.val) + ") - " + "{:02d}".format(self.count) + " remaining"

class Lyre:
    class NoSuchNoteException(Exception):
        pass

    class NoteDepletedException(Exception):
        pass

    def __init__(
      self,
      notes: t.Optional[t.List[Note]]=None,
      debug: t.Optional[bool]=False,
    ):
        if notes is not None:
            self.notes = notes
        else:
            self.notes = []
        self.debug = debug

    def __str__(self) -> str:
        res = ""

        for note in self.notes:
            res += str(note) + "\n"
        
        return res
    
    def copy(self) -> Lyre:
        l = Lyre()
        l.debug = self.debug

        for note in self.notes:
            n = Note()
            n.name = note.name
            n.val = note.val
            n.count = note.count

            l.notes.append(n)
        
        return l
    
    def get_note(
        self,
        name: str,
    ) -> Note:
        note = next((note for note in self.notes if note.name == name), None)
        
        return note
    
    def play_note(
        self,
        name: str,
    ):
        note = self.get_note(name)

        if (note is None):
            raise self.NoSuchNoteException
        
        if note.count < 1:
            raise self.NoteDepletedException
        
        
        note.count -= 1

    def n_sum(self, target, n=None) -> t.List[t.Tuple]:
        notes = []
        for note in self.notes:
            notes.extend([note] * note.count)

        results = []

        if n is None:
            sizes = range(1, len(notes) + 1)
        else:
            sizes = [n]

        if self.debug:
            print("Eurydice size: ", [str(n) for n in sizes])

        for size in sizes:
            for combo in combinations(notes, size):
                if sum([note.val for note in combo]) == target:
                    if self.debug:
                        print("For size ", str(size), " found combination ", [[str(note) for note in tup] for tup in combinations(notes, size)], " that works.")

                    results.append(combo)

        return results

    def possible_sums(self, flattened_notes: t.List[int], n: int) -> t.Set[int]:
        totals = set()
        for combo in combinations(flattened_notes, n):
            totals.add(sum([val for val in combo]))

        return totals

class Goal:
    class NoGoalDefinedException(Exception):
        pass

    def __init__(
      self,
      val: t.Optional[int]=None,
    ):
        if val is None:
          self.val = -1
        else:
          self.val = val
          
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

    def _assign_id(self):
        self.id = self.global_id
        Level.global_id += 1

    def __init__(
      self,
      lyre: t.Optional[Lyre]=None,
      orpheus_goal: t.Optional[Goal]=None,
      debug: t.Optional[bool]=False,
      given_seed: t.Optional[int]=None,
    ):
        self._assign_id()
        self.eurydice_lives = -1

        if lyre is not None:
          self.lyre = lyre
        else:
          self.lyre = Lyre()

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
        self.backup_rng_state = None
      
    def __str__(self) -> str:
        res = str(self.lyre)
        res += "\n"
        res += "Orpheus needs:  " + str(self.orpheus_goal)

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

        if given_seed is not None:
            self.seed = given_seed
        else:
            self.seed = random.randint(0, 1000)
        
        self.rng = random.Random(self.seed)

    def set_eurydice_goal(self) -> int:
        print("HELLo")
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

        return eurydice_goal_sum_len

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
        eurydice_sum_length: int,
    ) -> bool:
        if self.debug:
            print("Checking Eurydice...")
        if (num_notes == eurydice_sum_length) and (total == self.eurydice_goal.val):
            self.state = self.LevelState.SUCCESS
            return True

        if self.eurydice_lives == 0:
            if self.debug:
                print("Eurydice is out of lives.")
            self.state = self.LevelState.EURYDICE_FATAL
            return False
        
        solutions = self.lyre.n_sum(self.eurydice_goal.val, eurydice_sum_length)

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
        return True
        


        
