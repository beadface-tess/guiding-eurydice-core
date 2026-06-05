import random
import typing as t

from itertools import combinations

from .difficulty import Difficulty

from src.utils import TextUtility

class Note:    
    def __init__(
      self,
      id: t.Optional[int]=None,
      val: t.Optional[int]=-1,
      name: t.Optional[str]="Z",
      count: t.Optional[int]=1,
      text_utility: t.Optional[TextUtility] = TextUtility(),
    ):
        self.id = None

        self.val = val
        self.val_hidden = False
        self.name = name
        self.name_hidden = False
        self.count = count
        self.count_hidden = False
        self.stress_count = 0

        self.text_utility = text_utility

        self.eliminated = False
        self.questioned = False
        self.checked = False
        
    def __str__(self) -> str:
        val_str = "??" if self.val_hidden else "{:02d}".format(self.val)
        name_str = "??" if self.name_hidden else "{:<2}".format(self.name)
        count_str = "??" if self.count_hidden else "{:02d}".format(self.count)

        scratchpad_str = " "
        if self.eliminated:
            if self.questioned or self.checked:
                raise ValueError("Note has multiple scratchpad states!")
            scratchpad_str = self.text_utility.red("✗")
        elif self.questioned:
            if self.eliminated or self.checked:
                raise ValueError("Note has multiple scratchpad states!")
            scratchpad_str = self.text_utility.yellow("?")
        elif self.checked:
            if self.eliminated or self.questioned:
                raise ValueError("Note has multiple scratchpad states!")
            scratchpad_str = self.text_utility.green("✓")

        return "{:2d}".format(self.id) + " | " + scratchpad_str + " | " + name_str + " (" + val_str + ") - " + count_str + " remaining"
    
    def eliminate(self) -> None:
        if self.eliminated:
            self.eliminated = False
        else:
            self.questioned = False
            self.checked = False
            self.eliminated = True
    
    def question(self) -> None:
        if self.questioned:
            self.questioned = False
        else:
            self.eliminated = False
            self.checked = False
            self.questioned = True
    
    def check(self) -> None:
        if self.checked:
            self.checked = False
        else:
            self.eliminated = False
            self.questioned = False
            self.checked = True

class Lyre:
    class NoSuchNoteException(Exception):
        pass

    class NoteDepletedException(Exception):
        pass

    class BrokenStringException(Exception):
        pass

    def __init__(
      self,
      notes: t.Optional[t.List[Note]]=None,
      debug: t.Optional[bool]=False,
      difficulty: t.Optional[Difficulty]=None,
      rng: t.Optional[random.Random]=None,
    ):        
        self.notes = notes or []

        for i, note in enumerate(self.notes):
            note.id = i + 1       

        self.debug = debug
        self.difficulty = difficulty or Difficulty(2, "")
        self.rng = rng or random.Random()

        self.no_such_note_count = 0
        self.notes_played_count = 0

        self.hide_note_names = False
        self.hide_note_values = False
        self.hide_remaining_notes = False

        self.next_hidden_note_name_it = 0
        self.next_hidden_note_value_it = 0
        self.next_hidden_remaining_it = 0

        if (self.difficulty.lyre_difficulty.note_names_difficulty.min_plays_per_it >= 0) and \
            (self.difficulty.lyre_difficulty.note_names_difficulty.max_plays_per_it >= 0) and \
            (self.difficulty.lyre_difficulty.note_names_difficulty.min_hidden_per_it >= 0) and \
            (self.difficulty.lyre_difficulty.note_names_difficulty.max_hidden_per_it >= 0):
            self.hide_note_names = True

        if (self.difficulty.lyre_difficulty.note_values_difficulty.min_plays_per_it >= 0) and \
            (self.difficulty.lyre_difficulty.note_values_difficulty.max_plays_per_it >= 0) and \
            (self.difficulty.lyre_difficulty.note_values_difficulty.min_hidden_per_it >= 0) and \
            (self.difficulty.lyre_difficulty.note_values_difficulty.max_hidden_per_it >= 0):
            self.hide_note_values = True

        if (self.difficulty.lyre_difficulty.remaining_notes_difficulty.min_plays_per_it >= 0) and \
            (self.difficulty.lyre_difficulty.remaining_notes_difficulty.max_plays_per_it >= 0) and \
            (self.difficulty.lyre_difficulty.remaining_notes_difficulty.min_hidden_per_it >= 0) and \
            (self.difficulty.lyre_difficulty.remaining_notes_difficulty.max_hidden_per_it >= 0):
            self.hide_remaining_notes = True


        if self.hide_note_names:
            self.next_hidden_note_name_it = self.rng.randint(
                self.difficulty.lyre_difficulty.note_names_difficulty.min_plays_per_it,
                self.difficulty.lyre_difficulty.note_names_difficulty.max_plays_per_it
            )

        if self.hide_remaining_notes:
            self.next_hidden_remaining_it = self.rng.randint(
                self.difficulty.lyre_difficulty.remaining_notes_difficulty.min_plays_per_it,
                self.difficulty.lyre_difficulty.remaining_notes_difficulty.max_plays_per_it
            )

        if self.hide_note_values:
            self.next_hidden_note_value_it = self.rng.randint(
                self.difficulty.lyre_difficulty.note_values_difficulty.min_plays_per_it,
                self.difficulty.lyre_difficulty.note_values_difficulty.max_plays_per_it
            )

    def reset_hidden_note_names(self):
        if self.hide_note_names:
            self.next_hidden_note_name_it = self.rng.randint(
                self.difficulty.lyre_difficulty.note_names_difficulty.min_plays_per_it + self.notes_played_count,
                self.difficulty.lyre_difficulty.note_names_difficulty.max_plays_per_it + self.notes_played_count
            )
    
    def reset_hidden_remaining_notes(self):
        if self.hide_remaining_notes:
            self.next_hidden_remaining_it = self.rng.randint(
                self.difficulty.lyre_difficulty.remaining_notes_difficulty.min_plays_per_it + self.notes_played_count,
                self.difficulty.lyre_difficulty.remaining_notes_difficulty.max_plays_per_it + self.notes_played_count
            )        

    def reset_hidden_note_values(self):
        if self.hide_note_values:
            self.next_hidden_value_it = self.rng.randint(
                self.difficulty.lyre_difficulty.remaining_notes_difficulty.min_plays_per_it + self.notes_played_count,
                self.difficulty.lyre_difficulty.note_values_difficulty.max_plays_per_it + self.notes_played_count
            )

    def hide_notes(self):
        def _get_indices_to_hide(difficulty: Difficulty.LyreDifficulty.NotesDifficulty) -> t.List[int]:
            num_note_names_to_hide = self.rng.randint(
                difficulty.min_hidden_per_it,
                difficulty.max_hidden_per_it
            )
            indices_to_choose_from = [i for i in range(0, len(self.notes))]
            indices_to_hide = []

            for _ in range(0, num_note_names_to_hide):
                chosen = self.rng.choice(indices_to_choose_from)
                indices_to_hide.append(chosen)
                indices_to_choose_from.pop(indices_to_choose_from.index(chosen))
            
            return indices_to_hide
        
        hide_note_names = self.hide_note_names and (self.notes_played_count == self.next_hidden_note_name_it)
        hide_note_values = self.hide_note_values and (self.notes_played_count == self.next_hidden_note_value_it)
        hide_remaining_notes = self.hide_remaining_notes and (self.notes_played_count == self.next_hidden_remaining_it)
        
        note_names_idxs = _get_indices_to_hide(self.difficulty.lyre_difficulty.note_names_difficulty) if hide_note_names else []
        note_values_idxs = _get_indices_to_hide(self.difficulty.lyre_difficulty.note_values_difficulty) if hide_note_values else []
        notes_remaining_idxs = _get_indices_to_hide(self.difficulty.lyre_difficulty.remaining_notes_difficulty) if hide_remaining_notes else []

        for idx, note in enumerate(self.notes):
            if hide_note_names and (idx in note_names_idxs):
                note.name_hidden = True
        
            if hide_note_values and (idx in note_values_idxs):
                note.val_hidden = True
            
            if hide_remaining_notes and (idx in notes_remaining_idxs):
                note.count_hidden = True

    def __str__(self) -> str:
        res = ""
        for note in self.notes:
            res += str(note) + "\n"
        return res  
    
    def copy(self) -> Lyre:
        l = Lyre()
        l.debug = self.debug
        l.difficulty = self.difficulty
        l.no_such_note_count = self.no_such_note_count
        l.notes_played_count = self.notes_played_count

        for note in self.notes:
            n = Note()
            n.name = note.name
            n.val = note.val
            n.count = note.count
            n.name_hidden = note.name_hidden
            n.val_hidden = note.val_hidden
            n.count_hidden = note.count_hidden

            l.notes.append(n)
        
        return l
    
    def get_note_by_name(
        self,
        name: str,
    ) -> Note:
        note = next((note for note in self.notes if note.name == name), None)
        
        return note
    
    def get_note_by_id(
        self,
        id: int,
    ) -> Note:
        note = next((note for note in self.notes if note.id == id), None)
        
        return note
    
    def play_note(
        self,
        name: str,
    ) -> Note:   
        def _check_for_broken_string(note: t.Optional[Note]=None):
            if self.debug:
                print(
                    "DEBUG depleted:",
                    note.name,
                    "count=", note.count,
                    "stress_count=", note.stress_count,
                    "max_notes_depleted=",
                    self.difficulty.lyre_difficulty.broken_strings_difficulty.max_notes_depleted,
                )

            if note:
                if note.count < 1:
                    note.stress_count += 1
                    if note.stress_count > self.difficulty.lyre_difficulty.broken_strings_difficulty.max_notes_depleted:
                        raise self.BrokenStringException()
                    raise self.NoteDepletedException()
            else:
                if self.no_such_note_count > self.difficulty.lyre_difficulty.broken_strings_difficulty.max_no_such_note:
                    raise self.BrokenStringException()
                self.no_such_note_count += 1
                raise self.NoSuchNoteException()

        note = self.get_note_by_name(name)
        _check_for_broken_string(note)
        note.count -= 1

        if (note.count < 0):
            note.count = 0

        self.hide_notes()
        if self.debug:
            print(f"no broken string; note {note.name} count s {str(note.count)}")


        if self.debug:
            print(f"note {note.name} count decreased to {str(note.count)}")
        self.notes_played_count += 1
        return note

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