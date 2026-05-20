import typing as t

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

    class BrokenStringException(Exception):
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

        self.broken_string_count = 0

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
    ) -> Note:   
        def _check_for_broken_string():
            if self.debug:
                print(f"Broken string count: {str(self.broken_string_count)}")

            if self.broken_string_count > 1:
                raise self.BrokenStringException()

        note = self.get_note(name)

        if (note is None):
            self.broken_string_count += 1
            _check_for_broken_string()
            raise self.NoSuchNoteException()
        
        if note.count < 1:
            self.broken_string_count += 1
            _check_for_broken_string()
            raise self.NoteDepletedException()

        note.count -= 1
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