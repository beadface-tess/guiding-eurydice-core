import typing as t

from enum import Enum
from itertools import combinations
from random import randint

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
      notes: t.Optional[t.List[Note]]={},
    ):
        self.notes = notes

    def __str__(self) -> str:
        res = ""

        for note in self.notes:
            res += str(note) + "\n"
        
        return res
    
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

        if note is None:
            raise self.NoSuchNoteException
        
        if note.count < 1:
            raise self.NoteDepletedException
        
        note.count -= 1

    def n_sum(self, target, n=None) -> t.List[t.Tuple]:
        notes = []
        for note, count in self.notes.items():
            notes.extend([note] * count)

        results = []

        if n is None:
            sizes = range(1, len(notes) + 1)
        else:
            sizes = [n]

        for size in sizes:
            for combo in combinations(notes, size):
                if sum([note.val for note in combo]) == target:
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
    ):
        self._assign_id()
        self.eurydice_lives = -1

        if lyre is not None:
          self.lyre = lyre
        else:
          self.lyre = Lyre()

        if orpheus_goal is not None:
          self.orpheus_goal = orpheus_goal
        else:
          self.orpheus_goal = Goal()

        self.debug = debug

        self.eurydice_goal = Goal()
        self.state = self.LevelState.READY
      
    def __str__(self) -> str:
        res = str(self.lyre)
        res += "\n"
        res += "Orpheus  needs:  " + str(self.orpheus_goal)

        if (self.debug):
            res += "\n"
            res += "Eurydice needs: " + str(self.eurydice_goal) + f" ({self.eurydice_lives} lives remaining)"
        
        return res
    
    def get_state(self) -> LevelState:
       return self.state       
    
    def play_note(self, note: str):
        self.lyre.play_note(note)

    def reset(self):
        self.state = Level.LevelState.READY
        self.eurydice_goal = Goal()

    def set_eurydice_goal(self) -> int:
        if self.state != self.LevelState.ORPHEUS_SUCCESS:
            raise Exception

        eligible_notes = [note for note in self.lyre.notes if note.count > 0]
        
        flattened_notes : t.List[int] = []
        for note in eligible_notes:
          flattened_notes.extend([note.val] * note.count)

        eurydice_goal_sum_len = randint(int(len(eligible_notes) / 2), len(eligible_notes))

        possible_totals = list(self.lyre.possible_sums(flattened_notes, eurydice_goal_sum_len))
        print("Goal length: ", eurydice_goal_sum_len)
        print("POSSIBLE TOTALS: ", possible_totals)
      
        self.eurydice_lives = len(possible_totals)
        self.eurydice_goal.val = possible_totals[randint(0, len(possible_totals) - 1)]

        return eurydice_goal_sum_len

    def try_orpheus(
        self,
        total: int,
    ):
        if total == self.orpheus_goal.val:
            self.state = self.LevelState.ORPHEUS_SUCCESS
        else:
            self.state = self.LevelState.ORPHEUS_FATAL

    def try_eurydice(
        self,
        total: int,
        eurydice_sum_length: int,
    ):
        if self.eurydice_lives == 0:
            self.state = self.LevelState.EURYDICE_FATAL
            return
        
        solutions = self.lyre.n_sum(self.eurydice_goal.val, eurydice_sum_length)
        if len(solutions) == 0:
            self.state = self.LevelState.EURYDICE_THWARTED
        else:
            if total == self.eurydice_goal.val:
                self.state = self.LevelState.SUCCESS
            else:
                self.state = self.LevelState.EURYDICE_FAIL
                self.eurydice_lives -= 1
            


        
