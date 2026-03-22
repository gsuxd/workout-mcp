from typing import List, Optional, Union
from datetime import datetime
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from enum import Enum


class HevyBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

# Enums
class SetType(str, Enum):
    NORMAL = "normal"
    WARMUP = "warmup"
    DROPSET = "dropset"
    FAILURE = "failure"

class CustomExerciseType(str, Enum):
    WEIGHT_REPS = "weight_reps"
    REPS_ONLY = "reps_only"
    BODYWEIGHT_REPS = "bodyweight_reps"
    BODYWEIGHT_ASSISTED_REPS = "bodyweight_assisted_reps"
    DURATION = "duration"
    WEIGHT_DURATION = "weight_duration"
    DISTANCE_DURATION = "distance_duration"
    SHORT_DISTANCE_WEIGHT = "short_distance_weight"

class MuscleGroup(str, Enum):
    ABDOMINALS = "abdominals"
    SHOULDERS = "shoulders"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    FOREARMS = "forearms"
    QUADRICEPS = "quadriceps"
    HAMSTRINGS = "hamstrings"
    CALVES = "calves"
    GLUTES = "glutes"
    LATS = "lats"
    CHEST = "chest"
    LOWER_BACK = "lower_back"
    UPPER_BACK = "upper_back"
    TRAPS = "traps"
    NECK = "neck"
    ABDUCTORS = "abductors"
    ADDUCTORS = "adductors"
    CARDIO = "cardio"
    FULL_BODY = "full_body"
    OTHER = "other"

class EquipmentCategory(str, Enum):
    NONE = "none"
    BARBELL = "barbell"
    DUMBBELL = "dumbbell"
    KETTLEBELL = "kettlebell"
    MACHINE = "machine"
    PLATE = "plate"
    RESISTANCE_BAND = "resistance_band"
    SUSPENSION = "suspension"
    OTHER = "other"

# Base Models
class RepRange(HevyBaseModel):
    """Rep range for set prescriptions (e.g. 8-12)."""
    start: int
    end: int


class Set(HevyBaseModel):
    """Represents a single set in an exercise"""
    index: int
    type: SetType
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[float] = None
    duration_seconds: Optional[float] = None
    rpe: Optional[float] = None  # 0-10 scale
    custom_metric: Optional[float] = None
    rep_range: Optional[RepRange] = None

class Exercise(HevyBaseModel):
    """Represents an exercise within a workout or routine"""
    index: int
    title: str
    notes: Optional[str] = None
    exercise_template_id: str
    superset_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("superset_id", "supersets_id")
    )
    sets: List[Set]

    @property
    def supersets_id(self) -> Optional[int]:
        """Backward compatibility alias used by older callers."""
        return self.superset_id

class Workout(HevyBaseModel):
    """Represents a completed workout"""
    id: str
    title: str
    routine_id: Optional[str] = None
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    updated_at: datetime
    created_at: datetime
    exercises: List[Exercise]

class Routine(HevyBaseModel):
    """Represents a workout routine template"""
    id: str
    title: str
    folder_id: Optional[int] = None
    updated_at: datetime
    created_at: datetime
    exercises: List[Exercise]

class RoutineFolder(HevyBaseModel):
    """Represents a folder for organizing routines"""
    id: int
    index: int
    title: str
    updated_at: datetime
    created_at: datetime

class ExerciseTemplate(HevyBaseModel):
    """Represents an exercise template (standard or custom)"""
    id: Union[str, int]
    title: str
    type: str
    primary_muscle_group: Optional[MuscleGroup] = None
    secondary_muscle_groups: List[MuscleGroup] = Field(default_factory=list)
    is_custom: bool
    equipment_category: Optional[EquipmentCategory] = None
