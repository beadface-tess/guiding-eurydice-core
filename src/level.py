import typing as t

class Note:
    def __init__(self):
        self.val = 0
        self.name = "X"

    def __init__(
        self,
        val: int,
        name: str,
    ):
        self.val = val
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} (" + "{.02d}".format(self.val) + ")"

class Lyre:
    class NoSuchNoteException(Exception):
        pass

    class NoteDepletedException(Exception):
        pass

    def __init__(self):
        self.notes : t.Dict[t.Note, int] = {}
    
    def __init__(
        self,
        notes: t.List[str],
    ):
        for note in notes:
            self.notes[note.name] = 1
    
    def __init__(
        self,
        notes: t.Dict[t.Note, int],
    ):
        self.notes = notes

    def __str__(self) -> str:
        res = ""

        for note, count in self.notes.items():
            res += f"{note} - " + "{.02d}".format(count) + " remaining" + "\n"
        
        return res
    
    def play_note(
        self,
        note_name: str,
    ):
        if note_name not in self.notes.keys():
            raise self.NoSuchNoteException
        
        if self.notes[note_name] == 0:
            raise self.NoteDepletedException

        self[note_name] -= 1

class Goal:
    class NoGoalDefinedException(Exception):
        pass

    def __init__(self):
        self.val = -1
    
    def __init__(
        self,
        val: int
    ):
        self.val = val
    
    def __str__(self) -> str:
        return str(self.val)
    
class Level:
    global_id = 0

    def _assign_id(self):
        self.id = self.global_id
        self.global_id += 1

    def __init__(self):
        self._assign_id()
        self.lyre = Lyre()
        self.orpheus_goal = Goal()
        self.eurydice_goal = Goal()

    def __init__(
        self,
        lyre: Lyre,
        orpheus_goal: Goal,
        eurydice_goal: Goal,
    ):
        self.assign_id()
        self.lyre = lyre
        self.orpheus_goal = orpheus_goal
        self.eurydice_goal = eurydice_goal

    def __str__(self) -> str:
        res = ""
        res += f"LEVEL {str(self.id)}"
        res += "\n"
        res += str(self.lyre)
        res += "\n"
        res += "Orpheus needs:  " + str(self.orpheus_goal)
        res += "\n"
        res += "Eurydice needs: " + str(self.eurydice_goal)
        return res


        