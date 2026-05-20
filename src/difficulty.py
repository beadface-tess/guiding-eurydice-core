import json
import pathlib
import typing as t

class Difficulty():
    class LyreDifficulty():
        class NotesDifficulty():
            """Used for both remaining notes hidden config and note names hidden config."""
            def __init__(
                self,
                min_hidden_per_it: t.Optional[int] = 0,
                max_hidden_per_it: t.Optional[int] = -1,
                min_plays_per_it: t.Optional[int] = 0,
                max_plays_per_it: t.Optional[int] = -1
            ):
                self.min_hidden_per_it = min_hidden_per_it
                self.max_hidden_per_it = max_hidden_per_it
                self.min_plays_per_it = min_plays_per_it
                self.max_plays_per_it = max_plays_per_it

            @staticmethod
            def from_json(
                data: t.Dict[str, t.Any]
            ) -> NotesDifficulty:
                min_hidden_per_it = None
                max_hidden_per_it = None
                min_plays_per_it = None
                max_plays_per_it = None

                if ("min_hidden_per_it" in data.keys()) and (isinstance(data["min_hidden_per_it"], int)):
                    min_hidden_per_it = data["min_hidden_per_it"]
                
                if ("max_hidden_per_it" in data.keys()) and (isinstance(data["max_hidden_per_it"], int)):
                    max_hidden_per_it = data["max_hidden_per_it"]
                
                if ("min_plays_per_it" in data.keys()) and (isinstance(data["min_plays_per_it"], int)):
                    min_plays_per_it = data["min_plays_per_it"]
                
                if ("max_plays_per_it" in data.keys()) and (isinstance(data["max_plays_per_it"], int)):
                    max_plays_per_it = data["max_plays_per_it"]

                return NotesDifficulty(
                    min_hidden_per_it=min_hidden_per_it,
                    max_hidden_per_it=max_hidden_per_it,
                    min_plays_per_it=min_plays_per_it,
                    max_plays_per_it=max_plays_per_it,
                )

        class BrokenStringDifficulty():
            def __init__(
                self,
                max_notes_depleted: t.Optional[int] = -1,
                max_no_such_note: t.Optional[int] = -1
            ):
                self.max_notes_depleted = max_notes_depleted
                self.max_no_such_note = max_no_such_note

            @staticmethod
            def from_json(
                data: t.Dict[str, t.Any]
            ) -> BrokenStringDifficulty:
                max_notes_depleted = None
                max_no_such_note = None

                if ("max_notes_depleted" in data.keys()) and (isinstance(data["max_notes_depleted"], int)):
                    max_notes_depleted = data["max_notes_depleted"]
                
                if ("max_no_such_note" in data.keys()) and (isinstance(data["max_no_such_note"], int)):
                    max_no_such_note = data["max_no_such_note"]
                
                return BrokenStringDifficulty(
                    max_notes_depleted=max_notes_depleted,
                    max_no_such_note=max_no_such_note,
                )

        def __init__(
            self,
            remaining_notes_difficulty: t.Optional[NotesDifficulty] = None,
            note_names_difficulty: t.Optional[NotesDifficulty] = None,
            note_values_difficulty: t.Optional[NotesDifficulty] = None,
            broken_strings_difficulty: t.Optional[BrokenStringDifficulty] = None,
        ):
            self.remaining_notes_difficulty = remaining_notes_difficulty or self.NotesDifficulty()
            self.note_names_difficulty = note_names_difficulty or self.NotesDifficulty()
            self.note_values_difficulty = note_values_difficulty or self.NotesDifficulty()
            self.broken_strings_difficulty = broken_strings_difficulty or self.BrokenStringDifficulty()

        def from_json(
            self,
            data: t.Dict[str, t.Any]
        ) -> LyreDifficulty:
            remaining_notes_difficulty = None
            note_names_difficulty = None
            note_values_difficulty = None
            broken_string_difficulty = None

            if ("remaining_notes_hidden_config" in data.keys()) and (isinstance(data["remaining_notes_hidden_config"], dict)):
                remaining_notes_difficulty = self.NotesDifficulty.from_json(data["remaining_notes_hidden_config"])
            
            if ("note_names_hidden_config" in data.keys()) and (isinstance(data["note_names_hidden_config"], dict)):
                note_names_difficulty = self.NotesDifficulty.from_json(data["note_names_hidden_config"])

            if ("note_values_hidden_config" in data.keys()) and (isinstance(data["note_values_hidden_config"], dict)):
                note_values_difficulty = self.NotesDifficulty.from_json(data["note_values_hidden_config"])
            
            if ("broken_string_config" in data.keys()) and (isinstance(data["broken_string_config"], dict)):
                broken_string_difficulty = data["broken_string_config"]
            
            return LyreDifficulty(
                remaining_notes_difficulty=remaining_notes_difficulty,
                note_names_difficulty=note_names_difficulty,
                note_values_difficulty=note_values_difficulty,
                broken_string_difficulty=broken_string_difficulty,
            )

    class SumDifficulty():
        def __init__(
            self,
            min_turns_before_hiding_sum: t.Optional[int] = 0,
            max_turns_before_hiding_sum: t.Optional[int] = -1,
            min_hidden_addends_per_it: t.Optional[int] = 0,
            max_hidden_addends_per_it: t.Optional[int] = -1,
            min_plays_per_it: t.Optional[int] = 0,
            max_plays_per_it: t.Optional[int] = -1
        ):
            self.min_turns_before_hiding_sum = min_turns_before_hiding_sum
            self.max_turns_before_hiding_sum = max_turns_before_hiding_sum
            self.min_hidden_addends_per_it = min_hidden_addends_per_it
            self.max_hidden_addends_per_it = max_hidden_addends_per_it
            self.min_plays_per_it = min_plays_per_it
            self.max_plays_per_it = max_plays_per_it

        @staticmethod
        def from_json(
            data: t.Dict[str, t.Any]
        ) -> SumDifficulty:
            min_turns_before_hiding_sum = None
            max_turns_before_hiding_sum = None
            min_hidden_addends_per_it = None
            max_hidden_addends_per_it = None
            min_plays_per_it = None
            max_plays_per_it = None

            if ("min_turns_before_hiding_sum" in data.keys()) and (isinstance(data["min_turns_before_hiding_sum"], int)):
                min_turns_before_hiding_sum = data["min_turns_before_hiding_sum"]
            
            if ("max_turns_before_hiding_sum" in data.keys()) and (isinstance(data["max_turns_before_hiding_sum"], int)):
                max_turns_before_hiding_sum = data["max_turns_before_hiding_sum"]
            
            if ("min_hidden_addends_per_it" in data.keys()) and (isinstance(data["min_hidden_addends_per_it"], int)):
                min_hidden_addends_per_it = data["min_hidden_addends_per_it"]
            
            if ("max_hidden_addends_per_it" in data.keys()) and (isinstance(data["max_hidden_addends_per_it"], int)):
                max_hidden_addends_per_it = data["max_hidden_addends_per_it"]
            
            if ("min_plays_per_it" in data.keys()) and (isinstance(data["min_plays_per_it"], int)):
                min_plays_per_it = data["min_plays_per_it"]
            
            if ("max_plays_per_it" in data.keys()) and (isinstance(data["max_plays_per_it"], int)):
                max_plays_per_it = data["max_plays_per_it"]
            
            return SumDifficulty(
                min_turns_before_hiding_sum=min_turns_before_hiding_sum,
                max_turns_before_hiding_sum=max_turns_before_hiding_sum,
                min_hidden_addends_per_it=min_hidden_addends_per_it,
                max_hidden_addends_per_it=max_hidden_addends_per_it,
                min_plays_per_it=min_plays_per_it,
                max_plays_per_it=max_plays_per_it,
            )

    class NoSuchLevelException(Exception):
        pass

    class MissingLevelNameException(Exception):
        pass

    def __init__(
        self,
        num: int,
        name: str,
        lyre_difficulty: t.Optional[LyreDifficulty],
        sum_difficulty: t.Optional[SumDifficulty],
        tutorial: t.Optional[bool] = False,
        orpheus_lives: t.Optional[int] = 1,
        eurydice_lives: t.Optional[int] = 0,
    ):
        self.num = num
        self.name = name
        self.tutorial = tutorial
        self.orpheus_lives = orpheus_lives
        self.eurydice_lives = eurydice_lives
        self.lyre_difficulty = lyre_difficulty or self.LyreDifficulty()
        self.sum_difficulty = sum_difficulty or self.SumDifficulty()

    
    def from_json(
        self,
        num: int,
        json_file_path: pathlib.Path
    ) -> Difficulty:
        name = ""
        tutorial = None
        orpheus_lives = None
        eurydice_lives = None
        lyre_difficulty = None
        sum_difficulty = None

        with open(json_file_path, "r") as f:
            data = json.load(f)

            if str(num) not in data.keys():
                raise self.NoSuchLevelException()
            
            level_cfg = data[str(num)]

            if ("tutorial" in level_cfg.keys()) and (isinstance(level_cfg["tutorial"], bool)):
                tutorial = level_cfg["tutorial"]
            
            if ("orpheus_lives" in level_cfg.keys()) and (isinstance(level_cfg["orpheus_lives"], int)):
                orpheus_lives = level_cfg["orpheus_lives"]
            
            if ("eurydice_lives" in level_cfg.keys()) and (isinstance(level_cfg["eurydice_lives"], int)):
                eurydice_lives = level_cfg["eurydice_lives"]

            if ("lyre_difficulty_config" in level_cfg.keys()) and (isinstance(level_cfg["lyre_difficulty_cfg"], dict)):
                lyre_difficulty = self.LyreDifficulty.from_json(level_cfg["lyre_difficulty_config"])
            
            if ("sum_hidden_config" in level_cfg.keys()) and (isinstance(level_cfg["sum_hidden_config"], dict)):
                sum_difficulty = self.SumDifficulty.from_json(level_cfg["sum_hidden_config"])
            
            return Difficulty(
                num=num,
                name=name,
                tutorial=tutorial,
                orpheus_lives=orpheus_lives,
                eurydice_lives=eurydice_lives,
                lyre_difficulty=lyre_difficulty,
                sum_difficulty=sum_difficulty,
            )
            
        