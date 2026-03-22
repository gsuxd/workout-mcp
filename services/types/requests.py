from typing import List, Optional, Union
from datetime import datetime
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator

from .models import (
    CustomExerciseType,
    EquipmentCategory,
    MuscleGroup,
    RepRange,
    SetType,
)

# Request Body Models for Creating/Updating Resources


class RequestBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class SetRequestBody(RequestBaseModel):
    index: Optional[int] = None
    type: SetType
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[float] = None
    duration_seconds: Optional[float] = None
    rpe: Optional[float] = None
    custom_metric: Optional[float] = None
    rep_range: Optional[RepRange] = None
    rest_seconds: Optional[int] = None


class ExerciseRequestBody(RequestBaseModel):
    index: Optional[int] = None
    title: Optional[str] = None
    notes: Optional[str] = None
    exercise_template_id: Union[str, int]
    superset_id: Optional[int] = None
    rest_seconds: Optional[int] = None
    sets: List[SetRequestBody] = Field(default_factory=list)


class WorkoutCreateBody(RequestBaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_private: Optional[bool] = None
    exercises: List[ExerciseRequestBody] = Field(default_factory=list)
    routine_id: Optional[Union[str, int]] = None


class WorkoutUpdateBody(RequestBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_private: Optional[bool] = None
    exercises: Optional[List[ExerciseRequestBody]] = None
    routine_id: Optional[Union[str, int]] = None


class RoutineCreateBody(RequestBaseModel):
    title: str
    folder_id: Optional[int] = None
    notes: Optional[str] = None
    exercises: List[ExerciseRequestBody] = Field(default_factory=list)


class RoutineUpdateBody(RequestBaseModel):
    title: Optional[str] = None
    folder_id: Optional[int] = None
    notes: Optional[str] = None
    exercises: Optional[List[ExerciseRequestBody]] = None


class RoutineFolderCreateBody(RequestBaseModel):
    title: str
    index: Optional[int] = None


class CustomExerciseCreateBody(RequestBaseModel):
    title: str
    exercise_type: CustomExerciseType = Field(
        validation_alias=AliasChoices("exercise_type", "type"),
        serialization_alias="exercise_type",
    )
    muscle_group: Optional[MuscleGroup] = Field(
        default=None,
        validation_alias=AliasChoices("muscle_group", "primary_muscle_group"),
        serialization_alias="muscle_group",
    )
    other_muscles: List[MuscleGroup] = Field(
        default_factory=list,
        validation_alias=AliasChoices("other_muscles", "secondary_muscle_groups"),
        serialization_alias="other_muscles",
    )
    equipment_category: Optional[EquipmentCategory] = None

class PostWorkoutsRequestBody(RequestBaseModel):
    """Request body for creating a new workout"""
    workout: WorkoutCreateBody

    @model_validator(mode="before")
    @classmethod
    def wrap_legacy_payload(cls, data):
        if isinstance(data, dict) and "workout" not in data:
            return {"workout": data}
        return data

class PutWorkoutsRequestBody(RequestBaseModel):
    """Request body for updating an existing workout"""
    workout: WorkoutUpdateBody

    @model_validator(mode="before")
    @classmethod
    def wrap_legacy_payload(cls, data):
        if isinstance(data, dict) and "workout" not in data:
            return {"workout": data}
        return data

class PostRoutinesRequestBody(RequestBaseModel):
    """Request body for creating a new routine"""
    routine: RoutineCreateBody

    @model_validator(mode="before")
    @classmethod
    def wrap_legacy_payload(cls, data):
        if isinstance(data, dict) and "routine" not in data:
            return {"routine": data}
        return data

class PutRoutinesRequestBody(RequestBaseModel):
    """Request body for updating an existing routine"""
    routine: RoutineUpdateBody

    @model_validator(mode="before")
    @classmethod
    def wrap_legacy_payload(cls, data):
        if isinstance(data, dict) and "routine" not in data:
            return {"routine": data}
        return data

class PostRoutineFolderRequestBody(RequestBaseModel):
    """Request body for creating a new routine folder"""
    routine_folder: RoutineFolderCreateBody

    @model_validator(mode="before")
    @classmethod
    def wrap_legacy_payload(cls, data):
        if isinstance(data, dict) and "routine_folder" not in data:
            return {"routine_folder": data}
        return data

class CreateCustomExerciseRequestBody(RequestBaseModel):
    """Request body for creating a custom exercise template"""
    exercise: CustomExerciseCreateBody

    @model_validator(mode="before")
    @classmethod
    def wrap_legacy_payload(cls, data):
        if isinstance(data, dict) and "exercise" not in data:
            return {"exercise": data}
        return data
