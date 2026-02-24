from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

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
class Set(BaseModel):
    """Represents a single set in an exercise"""
    index: int
    type: SetType
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[float] = None
    duration_seconds: Optional[float] = None
    rpe: Optional[float] = None  # 0-10 scale
    custom_metric: Optional[float] = None

class Exercise(BaseModel):
    """Represents an exercise within a workout or routine"""
    index: int
    title: str
    notes: Optional[str] = None
    exercise_template_id: str
    supersets_id: Optional[int] = None
    sets: List[Set]

class Workout(BaseModel):
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

class Routine(BaseModel):
    """Represents a workout routine template"""
    id: str
    title: str
    folder_id: Optional[int] = None
    updated_at: datetime
    created_at: datetime
    exercises: List[Exercise]

class RoutineFolder(BaseModel):
    """Represents a folder for organizing routines"""
    id: int
    index: int
    title: str
    updated_at: datetime
    created_at: datetime

class ExerciseTemplate(BaseModel):
    """Represents an exercise template (standard or custom)"""
    id: str
    title: str
    type: str
    primary_muscle_group: Optional[MuscleGroup] = None
    secondary_muscle_groups: List[MuscleGroup] = []
    is_custom: bool
    equipment_category: Optional[EquipmentCategory] = None
