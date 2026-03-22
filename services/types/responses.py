from typing import List, Literal, Optional, Union
from datetime import datetime
from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from .models import Workout, Routine, RoutineFolder, ExerciseTemplate, Set


class ResponseBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

# Pagination Models
class PaginatedWorkouts(ResponseBaseModel):
    page: int
    page_count: int
    workouts: List[Workout]

class PaginatedRoutines(ResponseBaseModel):
    page: int
    page_count: int
    routines: List[Routine]

class PaginatedRoutineFolders(ResponseBaseModel):
    page: int
    page_count: int
    routine_folders: List[RoutineFolder]

class PaginatedExerciseTemplates(ResponseBaseModel):
    page: int
    page_count: int
    exercise_templates: List[ExerciseTemplate]

# Workout Events (for sync)
class UpdatedWorkout(ResponseBaseModel):
    type: Literal["updated"]
    workout: Workout

class DeletedWorkout(ResponseBaseModel):
    type: Literal["deleted"]
    id: str
    deleted_at: datetime

class PaginatedWorkoutEvents(ResponseBaseModel):
    page: int
    page_count: int
    events: List[Union[UpdatedWorkout, DeletedWorkout]]

# Count Response
class WorkoutCount(ResponseBaseModel):
    workout_count: int = Field(validation_alias=AliasChoices("workout_count", "count"))

    @property
    def count(self) -> int:
        """Backward compatibility alias for old callers."""
        return self.workout_count

# Exercise History
class ExerciseHistoryEntry(ResponseBaseModel):
    workout_id: Union[str, int]
    workout_title: str
    workout_start_time: datetime
    workout_end_time: Optional[datetime] = None
    exercise_template_id: Union[str, int]
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[float] = None
    duration_seconds: Optional[float] = None
    rpe: Optional[float] = None
    custom_metric: Optional[float] = None
    set_type: Optional[str] = None

class ExerciseHistory(ResponseBaseModel):
    exercise_history: List[ExerciseHistoryEntry] = Field(
        default_factory=list,
        validation_alias=AliasChoices("exercise_history", "history")
    )


# User Models
class UserInfo(ResponseBaseModel):
    id: str
    name: str
    url: str


class UserInfoResponse(ResponseBaseModel):
    data: UserInfo


class CreatedCustomExerciseResponse(ResponseBaseModel):
    id: Union[str, int] = Field(validation_alias=AliasChoices("id", "exercise_template_id"))