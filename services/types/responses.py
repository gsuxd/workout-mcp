from typing import List, Union, Literal
from datetime import datetime
from pydantic import BaseModel

from .models import Workout, Routine, RoutineFolder, ExerciseTemplate, Set

# Pagination Models
class PaginatedWorkouts(BaseModel):
    page: int
    page_count: int
    workouts: List[Workout]

class PaginatedRoutines(BaseModel):
    page: int
    page_count: int
    routines: List[Routine]

class PaginatedRoutineFolders(BaseModel):
    page: int
    page_count: int
    routine_folders: List[RoutineFolder]

class PaginatedExerciseTemplates(BaseModel):
    page: int
    page_count: int
    exercise_templates: List[ExerciseTemplate]

# Workout Events (for sync)
class UpdatedWorkout(BaseModel):
    type: Literal["updated"]
    workout: Workout

class DeletedWorkout(BaseModel):
    type: Literal["deleted"]
    id: str
    deleted_at: datetime

class PaginatedWorkoutEvents(BaseModel):
    page: int
    page_count: int
    events: List[Union[UpdatedWorkout, DeletedWorkout]]

# Count Response
class WorkoutCount(BaseModel):
    count: int

# Exercise History
class ExerciseHistoryEntry(BaseModel):
    workout_id: str
    workout_title: str
    workout_start_time: datetime
    sets: List[Set]

class ExerciseHistory(BaseModel):
    exercise_template_id: str
    exercise_title: str
    history: List[ExerciseHistoryEntry]

# User Models
class UserInfo(BaseModel):
    id: str
    name: str
    url: str