import os
from typing import Optional
from datetime import datetime
import httpx
from dotenv import load_dotenv
from httpx import URL

from services.types import (
    # Base models
    Workout,
    Routine,
    RoutineFolder,
    ExerciseTemplate,
    # Response models
    PaginatedWorkouts,
    PaginatedRoutines,
    PaginatedRoutineFolders,
    PaginatedExerciseTemplates,
    PaginatedWorkoutEvents,
    WorkoutCount,
    ExerciseHistory,
    UserInfo,
    # Request models
    PostWorkoutsRequestBody,
    PutWorkoutsRequestBody,
    PostRoutinesRequestBody,
    PutRoutinesRequestBody,
    PostRoutineFolderRequestBody,
    CreateCustomExerciseRequestBody,
)

load_dotenv()


class HevyClient:
    """
    Async client for the Hevy API.

    Documentation: https://api.hevyapp.com/docs/
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Hevy API client.

        Args:
            api_key: Hevy API key. If not provided, will use HEVY_API_KEY from environment.
        """
        self.client = httpx.AsyncClient()
        self.client.base_url = URL("https://api.hevyapp.com/v1/")
        self.client.headers.update({
            "api-key": api_key or os.getenv("HEVY_API_KEY", "")
        })

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    # ==================== User Endpoints ====================

    async def get_user_info(self) -> Optional[UserInfo]:
        """
        Get basic user profile information.

        Returns:
            UserInfo object with id, name, and url, or None on error.
        """
        try:
            response = await self.client.get("user/info")
            response.raise_for_status()
            return UserInfo(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting user info: {e}")
            return None

    # ==================== Workout Endpoints ====================

    async def get_workouts(self, page: int = 1) -> Optional[PaginatedWorkouts]:
        """
        Get a paginated list of workouts.

        Args:
            page: Page number (default: 1)

        Returns:
            PaginatedWorkouts object or None on error.
        """
        try:
            response = await self.client.get("workouts", params={"page": page})
            response.raise_for_status()
            return PaginatedWorkouts(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting workouts: {e}")
            return None

    async def get_workout(self, workout_id: str) -> Optional[Workout]:
        """
        Get complete details for a single workout.

        Args:
            workout_id: Unique workout ID

        Returns:
            Workout object or None on error.
        """
        try:
            response = await self.client.get(f"workouts/{workout_id}")
            response.raise_for_status()
            return Workout(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting workout {workout_id}: {e}")
            return None

    async def create_workout(self, workout: PostWorkoutsRequestBody) -> Optional[Workout]:
        """
        Create a new workout.

        Args:
            workout: Workout data to create

        Returns:
            Created Workout object or None on error.
        """
        try:
            response = await self.client.post(
                "workouts",
                json=workout.model_dump(mode="json")
            )
            response.raise_for_status()
            return Workout(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error creating workout: {e}")
            return None

    async def update_workout(
        self,
        workout_id: str,
        workout: PutWorkoutsRequestBody
    ) -> Optional[Workout]:
        """
        Update an existing workout.

        Args:
            workout_id: Unique workout ID
            workout: Updated workout data

        Returns:
            Updated Workout object or None on error.
        """
        try:
            response = await self.client.put(
                f"workouts/{workout_id}",
                json=workout.model_dump(mode="json", exclude_none=True)
            )
            response.raise_for_status()
            return Workout(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error updating workout {workout_id}: {e}")
            return None

    async def get_workout_count(self) -> Optional[int]:
        """
        Get the total number of workouts on the account.

        Returns:
            Total workout count or None on error.
        """
        try:
            response = await self.client.get("workouts/count")
            response.raise_for_status()
            data = response.json()
            return data.get("count")
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting workout count: {e}")
            return None

    async def get_workout_events(
        self,
        since: datetime,
        page: int = 1
    ) -> Optional[PaginatedWorkoutEvents]:
        """
        Get a paged list of workout events (updates or deletes) since a given date.
        Useful for synchronization.

        Args:
            since: ISO 8601 datetime to get events since
            page: Page number (default: 1)

        Returns:
            PaginatedWorkoutEvents object or None on error.
        """
        try:
            response = await self.client.get(
                "workouts/events",
                params={
                    "since": since.isoformat(),
                    "page": page
                }
            )
            response.raise_for_status()
            return PaginatedWorkoutEvents(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting workout events: {e}")
            return None

    # ==================== Routine Endpoints ====================

    async def get_routines(self, page: int = 1) -> Optional[PaginatedRoutines]:
        """
        Get a paginated list of routines.

        Args:
            page: Page number (default: 1)

        Returns:
            PaginatedRoutines object or None on error.
        """
        try:
            response = await self.client.get("routines", params={"page": page})
            response.raise_for_status()
            return PaginatedRoutines(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting routines: {e}")
            return None

    async def get_routine(self, routine_id: str) -> Optional[Routine]:
        """
        Get a routine by its unique ID.

        Args:
            routine_id: Unique routine ID

        Returns:
            Routine object or None on error.
        """
        try:
            response = await self.client.get(f"routines/{routine_id}")
            response.raise_for_status()
            return Routine(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting routine {routine_id}: {e}")
            return None

    async def create_routine(self, routine: PostRoutinesRequestBody) -> Optional[Routine]:
        """
        Create a new routine.

        Args:
            routine: Routine data to create

        Returns:
            Created Routine object or None on error.
        """
        try:
            response = await self.client.post(
                "routines",
                json=routine.model_dump(mode="json")
            )
            response.raise_for_status()
            return Routine(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error creating routine: {e}")
            return None

    async def update_routine(
        self,
        routine_id: str,
        routine: PutRoutinesRequestBody
    ) -> Optional[Routine]:
        """
        Update an existing routine.

        Args:
            routine_id: Unique routine ID
            routine: Updated routine data

        Returns:
            Updated Routine object or None on error.
        """
        try:
            response = await self.client.put(
                f"routines/{routine_id}",
                json=routine.model_dump(mode="json", exclude_none=True)
            )
            response.raise_for_status()
            return Routine(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error updating routine {routine_id}: {e}")
            return None

    # ==================== Routine Folder Endpoints ====================

    async def get_routine_folders(self, page: int = 1) -> Optional[PaginatedRoutineFolders]:
        """
        Get a paginated list of routine folders.

        Args:
            page: Page number (default: 1)

        Returns:
            PaginatedRoutineFolders object or None on error.
        """
        try:
            response = await self.client.get("routine_folders", params={"page": page})
            response.raise_for_status()
            return PaginatedRoutineFolders(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting routine folders: {e}")
            return None

    async def get_routine_folder(self, folder_id: int) -> Optional[RoutineFolder]:
        """
        Get a single routine folder by ID.

        Args:
            folder_id: Unique folder ID

        Returns:
            RoutineFolder object or None on error.
        """
        try:
            response = await self.client.get(f"routine_folders/{folder_id}")
            response.raise_for_status()
            return RoutineFolder(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting routine folder {folder_id}: {e}")
            return None

    async def create_routine_folder(
        self,
        folder: PostRoutineFolderRequestBody
    ) -> Optional[RoutineFolder]:
        """
        Create a new routine folder.

        Args:
            folder: Folder data to create

        Returns:
            Created RoutineFolder object or None on error.
        """
        try:
            response = await self.client.post(
                "routine_folders",
                json=folder.model_dump(mode="json", exclude_none=True)
            )
            response.raise_for_status()
            return RoutineFolder(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error creating routine folder: {e}")
            return None

    # ==================== Exercise Template Endpoints ====================

    async def get_exercise_templates(self, page: int = 1) -> Optional[PaginatedExerciseTemplates]:
        """
        Get all available exercise templates (standard and custom).

        Args:
            page: Page number (default: 1)

        Returns:
            PaginatedExerciseTemplates object or None on error.
        """
        try:
            response = await self.client.get("exercise_templates", params={"page": page})
            response.raise_for_status()
            return PaginatedExerciseTemplates(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting exercise templates: {e}")
            return None

    async def get_exercise_template(self, template_id: str) -> Optional[ExerciseTemplate]:
        """
        Get details for a specific exercise template.

        Args:
            template_id: Unique template ID

        Returns:
            ExerciseTemplate object or None on error.
        """
        try:
            response = await self.client.get(f"exercise_templates/{template_id}")
            response.raise_for_status()
            return ExerciseTemplate(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting exercise template {template_id}: {e}")
            return None

    async def create_custom_exercise(
        self,
        exercise: CreateCustomExerciseRequestBody
    ) -> Optional[ExerciseTemplate]:
        """
        Create a new custom exercise template.

        Args:
            exercise: Custom exercise data to create

        Returns:
            Created ExerciseTemplate object or None on error.
        """
        try:
            response = await self.client.post(
                "exercise_templates",
                json=exercise.model_dump(mode="json", exclude_none=True)
            )
            response.raise_for_status()
            return ExerciseTemplate(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error creating custom exercise: {e}")
            return None

    async def get_exercise_history(self, template_id: str) -> Optional[ExerciseHistory]:
        """
        Get the history of a specific exercise across all workouts.

        Args:
            template_id: Unique exercise template ID

        Returns:
            ExerciseHistory object or None on error.
        """
        try:
            response = await self.client.get(f"exercise_history/{template_id}")
            response.raise_for_status()
            return ExerciseHistory(**response.json())
        except (httpx.HTTPError, ValueError) as e:
            print(f"Error getting exercise history for {template_id}: {e}")
            return None