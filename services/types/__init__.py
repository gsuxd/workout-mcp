"""
Hevy API Type Definitions

This package contains Pydantic models for the Hevy API.

Organization:
- models.py: Base models and enums (Set, Exercise, Workout, Routine, etc.)
- responses.py: API response models (Paginated*, Events, Counts, etc.)
- requests.py: Request body models for creating/updating resources
"""

# Base models and enums
from .models import (
    # Enums
    SetType,
    CustomExerciseType,
    MuscleGroup,
    EquipmentCategory,
    # Base models
    Set,
    Exercise,
    Workout,
    Routine,
    RoutineFolder,
    ExerciseTemplate,
)

# Response models
from .responses import (
    # Pagination
    PaginatedWorkouts,
    PaginatedRoutines,
    PaginatedRoutineFolders,
    PaginatedExerciseTemplates,
    # Events
    UpdatedWorkout,
    DeletedWorkout,
    PaginatedWorkoutEvents,
    # Other responses
    WorkoutCount,
    ExerciseHistoryEntry,
    ExerciseHistory,
    UserInfo,
    UserInfoResponse,
    CreatedCustomExerciseResponse,
)

# Request models
from .requests import (
    PostWorkoutsRequestBody,
    PutWorkoutsRequestBody,
    PostRoutinesRequestBody,
    PutRoutinesRequestBody,
    PostRoutineFolderRequestBody,
    CreateCustomExerciseRequestBody,
)

__all__ = [
    # Enums
    "SetType",
    "CustomExerciseType",
    "MuscleGroup",
    "EquipmentCategory",
    # Base models
    "Set",
    "Exercise",
    "Workout",
    "Routine",
    "RoutineFolder",
    "ExerciseTemplate",
    # Response models
    "PaginatedWorkouts",
    "PaginatedRoutines",
    "PaginatedRoutineFolders",
    "PaginatedExerciseTemplates",
    "UpdatedWorkout",
    "DeletedWorkout",
    "PaginatedWorkoutEvents",
    "WorkoutCount",
    "ExerciseHistoryEntry",
    "ExerciseHistory",
    "UserInfo",
    "UserInfoResponse",
    "CreatedCustomExerciseResponse",
    # Request models
    "PostWorkoutsRequestBody",
    "PutWorkoutsRequestBody",
    "PostRoutinesRequestBody",
    "PutRoutinesRequestBody",
    "PostRoutineFolderRequestBody",
    "CreateCustomExerciseRequestBody",
]
