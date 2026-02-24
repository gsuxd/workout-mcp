from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from .models import Exercise, CustomExerciseType, MuscleGroup, EquipmentCategory

# Request Body Models for Creating/Updating Resources

class PostWorkoutsRequestBody(BaseModel):
    """Request body for creating a new workout"""
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    exercises: List[Exercise]
    routine_id: Optional[str] = None

class PutWorkoutsRequestBody(BaseModel):
    """Request body for updating an existing workout"""
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    exercises: Optional[List[Exercise]] = None
    routine_id: Optional[str] = None

class PostRoutinesRequestBody(BaseModel):
    """Request body for creating a new routine"""
    title: str
    folder_id: Optional[int] = None
    exercises: List[Exercise]

class PutRoutinesRequestBody(BaseModel):
    """Request body for updating an existing routine"""
    title: Optional[str] = None
    folder_id: Optional[int] = None
    exercises: Optional[List[Exercise]] = None

class PostRoutineFolderRequestBody(BaseModel):
    """Request body for creating a new routine folder"""
    title: str
    index: Optional[int] = None

class CreateCustomExerciseRequestBody(BaseModel):
    """Request body for creating a custom exercise template"""
    title: str
    type: CustomExerciseType
    primary_muscle_group: Optional[MuscleGroup] = None
    secondary_muscle_groups: Optional[List[MuscleGroup]] = None
    equipment_category: Optional[EquipmentCategory] = None
