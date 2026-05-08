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
        return next((note for note in self.notes if note.name == name), None)
    
    def play_note(
        self,
        name: str,
    ):
        n = self.get_note(name)
        if n is None:
            raise self.NoSuchNoteException
        
        if n.count == 0:
            raise self.NoteDepletedException

        n.count -= 1

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

    def possible_sums(self, n: int) -> t.Set[int]:
        notes = []
        for note, count in self.notes.items():
            notes.extend([note] * count)

        totals = set()
        for combo in combinations(notes, n):
            totals.add(sum([note.val for note in combo]))

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
    global_id = 0

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

        self.eurydice_goal = Goal()
        self.state = self.LevelState.READY
      
    def __str__(self) -> str:
        res = str(self.lyre)
        res += "\n"
        res += "Orpheus  needs:  " + str(self.orpheus_goal)
        res += "\n"
        res += "Eurydice needs: " + str(self.eurydice_goal) + f" ({self.eurydice_lives} lives remaining)"
        return res
    
    def get_state(self) -> LevelState:
       return self.state       
    
    def play_note(self, note: str):
        self.lyre.play_note(note)

    def set_eurydice_goal(self):
        if self.state != self.LevelState.ORPHEUS_SUCCESS:
            raise Exception

        eligible_notes = [note for note in self.lyre.notes.keys() if self.lyre.notes[note] > 0]
        eurydice_goal_sum_len = len(eligible_notes) / 2
        curr_notes = 0
        note_counts = {}

        while (curr_notes < eurydice_goal_sum_len):
            idx = randint(0, len(eligible_notes) - 1)
            if eligible_notes[idx] in note_counts:
                if note_counts[eligible_notes[idx]] == self.lyre.notes[eligible_notes[idx]]:
                    continue
                note_counts[eligible_notes[idx]] += 1
            else:
                note_counts[eligible_notes[idx]] = 1
            curr_notes += 1
        
        flattened_notes = []
        for note, count in note_counts.items():
          flattened_notes.extend([note] * count)

        eurydice_note_count = len(flattened_notes)
        possible_totals = self.lyre.possible_sums(eurydice_note_count)
      
        self.eurydice_lives = len(possible_totals)
        self.eurydice_goal.val = sum([note.val for note in flattened_notes])

    def try_orpheus(
        self,
        notes: t.List[Note]
    ):
        total = sum([note.val for note in notes])

        if total == self.orpheus_goal.val:
            self.state = self.LevelState.ORPHEUS_SUCCESS
        else:
            self.state = self.LevelState.ORPHEUS_FATAL

    def try_eurydice(
        self,
        notes: t.List[Note],
        n: int,
    ):
        if self.eurydice_lives == 0:
            self.state = self.LevelState.EURYDICE_FATAL
            return
        
        solutions = self.lyre.n_sum(self.eurydice_goal.val, n)
        if len(solutions) == 0:
            self.state = self.LevelState.EURYDICE_THWARTED
        else:
            if sum([note.val for note in notes]) == self.eurydice_goal.val:
                self.state = self.LevelState.SUCCESS
            else:
                self.state = self.LevelState.EURYDICE_FAIL
                self.eurydice_lives -= 1
            


        
