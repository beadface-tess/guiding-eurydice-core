import typing as t

from enum import Enum
from itertools import combinations
from random import randint

class Note:
    def __init__(
      self,
      val: t.Optional[int],
      name: t.Optional[str],
    ):
      if val is None:
        self.val = -1
      else:
        self.val = val

      if name is None:
        self.name = "X"
      else:
        self.name = name
        
    def __str__(self) -> str:
        return f"{self.name} (" + "{.02d}".format(self.val) + ")"

class Lyre:
    class NoSuchNoteException(Exception):
        pass

    class NoteDepletedException(Exception):
        pass

    def __init__(
      self,
      notes: t.Optional[t.Union[t.List[str], t.Dict[Note, int]]],
    ):
        self.notes = {}
        if notes is not None:
          if isinstance(notes, list):
            for note in notes:
              self.notes[note] = 1
          elif isinstance(notes, dict):
            self.notes = notes
          else:
            raise Exception

    def __str__(self) -> str:
        res = ""

        for note, count in self.notes.items():
            res += f"{note} - " + "{.02d}".format(count) + " remaining" + "\n"
        
        return res
    
    def play_note(
        self,
        note: Note,
    ):
        if note not in self.notes:
            raise self.NoSuchNoteException
        
        if self.notes[note] == 0:
            raise self.NoteDepletedException

        self.notes[note] -= 1

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
      val: t.Optional[int],
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
      lyre: t.Optional[Lyre],
      orpheus_goal: t.Optional[Goal],
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
        res = ""
        res += f"LEVEL {str(self.id)}: {str(self.state)}"
        res += "\n"
        res += str(self.lyre)
        res += "\n"
        res += "Orpheus needs:  " + str(self.orpheus_goal)
        res += "\n"
        res += "Eurydice needs: " + str(self.eurydice_goal) + f" ({self.eurydice_lives} lives remaining)"
        return res
    
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
        total = 0

        for note in notes:
            self.lyre.play_note(note)
            total += note.val

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
            


        
