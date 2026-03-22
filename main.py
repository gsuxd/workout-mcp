from datetime import datetime
from typing import Optional
from fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from services.hevy import HevyClient

API_KEY = "76598381b462d9a0991cfa3d6012418b66d774b400ad555d94e80238ce42eb26"

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        api_key = request.headers.get("Authorization")
        if api_key != f"Bearer {API_KEY}":
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
        return await call_next(request)

mcp = FastMCP("HevyHealthServer")
mcp.add_middleware(AuthMiddleware)

# Shared client instance
_client: Optional[HevyClient] = None

def get_client() -> HevyClient:
    """Get or create the shared Hevy client instance."""
    global _client
    if _client is None:
        _client = HevyClient()
    return _client

# ==================== User Tools ====================

@mcp.tool()
async def get_user_info():
    """Get basic user profile information (id, name, url)."""
    client = get_client()
    result = await client.get_user_info()
    return result.model_dump() if result else {"error": "Failed to get user info"}

# ==================== Workout Tools ====================

@mcp.tool()
async def get_workouts(page: int = 1):
    """
    Get a paginated list of workouts.

    Args:
        page: Page number (default: 1)
    """
    client = get_client()
    result = await client.get_workouts(page=page)
    return result.model_dump() if result else {"error": "Failed to get workouts"}

@mcp.tool()
async def get_workout(workout_id: str):
    """
    Get complete details for a single workout.

    Args:
        workout_id: Unique workout ID
    """
    client = get_client()
    result = await client.get_workout(workout_id)
    return result.model_dump() if result else {"error": f"Failed to get workout {workout_id}"}

@mcp.tool()
async def get_workout_count():
    """Get the total number of workouts on the account."""
    client = get_client()
    count = await client.get_workout_count()
    return {"count": count} if count is not None else {"error": "Failed to get workout count"}

@mcp.tool()
async def get_workout_events(since: str, page: int = 1):
    """
    Get workout events (updates or deletes) since a given date for synchronization.

    Args:
        since: ISO 8601 datetime string (e.g., "2024-01-01T00:00:00")
        page: Page number (default: 1)
    """
    client = get_client()
    try:
        since_dt = datetime.fromisoformat(since.replace('Z', '+00:00'))
        result = await client.get_workout_events(since=since_dt, page=page)
        return result.model_dump() if result else {"error": "Failed to get workout events"}
    except ValueError as e:
        return {"error": f"Invalid date format: {e}"}

@mcp.tool()
async def create_workout(
    title: str,
    start_time: str,
    end_time: str,
    exercises: list,
    description: Optional[str] = None,
    routine_id: Optional[str] = None
):
    """
    Create a new workout.

    Args:
        title: Workout title
        start_time: ISO 8601 datetime string
        end_time: ISO 8601 datetime string
        exercises: List of exercises with sets
        description: Optional workout description
        routine_id: Optional routine ID this workout is based on
    """
    from services.types import PostWorkoutsRequestBody, Exercise

    client = get_client()
    try:
        workout_data = PostWorkoutsRequestBody(
            title=title,
            description=description,
            start_time=datetime.fromisoformat(start_time.replace('Z', '+00:00')),
            end_time=datetime.fromisoformat(end_time.replace('Z', '+00:00')),
            exercises=[Exercise(**ex) for ex in exercises],
            routine_id=routine_id
        )
        result = await client.create_workout(workout_data)
        return result.model_dump() if result else {"error": "Failed to create workout"}
    except (ValueError, Exception) as e:
        return {"error": f"Failed to create workout: {e}"}

# ==================== Routine Tools ====================

@mcp.tool()
async def get_routines(page: int = 1):
    """
    Get a paginated list of routines.

    Args:
        page: Page number (default: 1)
    """
    client = get_client()
    result = await client.get_routines(page=page)
    return result.model_dump() if result else {"error": "Failed to get routines"}

@mcp.tool()
async def get_routine(routine_id: str):
    """
    Get a routine by its unique ID.

    Args:
        routine_id: Unique routine ID
    """
    client = get_client()
    result = await client.get_routine(routine_id)
    return result.model_dump() if result else {"error": f"Failed to get routine {routine_id}"}

@mcp.tool()
async def create_routine(
    title: str,
    exercises: list,
    folder_id: Optional[int] = None
):
    """
    Create a new routine.

    Args:
        title: Routine title
        exercises: List of exercises with sets
        folder_id: Optional folder ID to organize the routine
    """
    from services.types import PostRoutinesRequestBody, Exercise

    client = get_client()
    try:
        routine_data = PostRoutinesRequestBody(
            title=title,
            folder_id=folder_id,
            exercises=[Exercise(**ex) for ex in exercises]
        )
        result = await client.create_routine(routine_data)
        return result.model_dump() if result else {"error": "Failed to create routine"}
    except (ValueError, Exception) as e:
        return {"error": f"Failed to create routine: {e}"}

@mcp.tool()
async def update_routine(
    routine_id: str,
    title: Optional[str] = None,
    exercises: Optional[list] = None,
    folder_id: Optional[int] = None
):
    """
    Update an existing routine.

    Args:
        routine_id: Unique routine ID
        title: Optional new title
        exercises: Optional new list of exercises
        folder_id: Optional new folder ID
    """
    from services.types import PutRoutinesRequestBody, Exercise

    client = get_client()
    try:
        routine_data = PutRoutinesRequestBody(
            title=title,
            folder_id=folder_id,
            exercises=[Exercise(**ex) for ex in exercises] if exercises else None
        )
        result = await client.update_routine(routine_id, routine_data)
        return result.model_dump() if result else {"error": f"Failed to update routine {routine_id}"}
    except (ValueError, Exception) as e:
        return {"error": f"Failed to update routine: {e}"}

# ==================== Routine Folder Tools ====================

@mcp.tool()
async def get_routine_folders(page: int = 1):
    """
    Get a paginated list of routine folders.

    Args:
        page: Page number (default: 1)
    """
    client = get_client()
    result = await client.get_routine_folders(page=page)
    return result.model_dump() if result else {"error": "Failed to get routine folders"}

@mcp.tool()
async def get_routine_folder(folder_id: int):
    """
    Get a single routine folder by ID.

    Args:
        folder_id: Unique folder ID
    """
    client = get_client()
    result = await client.get_routine_folder(folder_id)
    return result.model_dump() if result else {"error": f"Failed to get folder {folder_id}"}

@mcp.tool()
async def create_routine_folder(title: str, index: Optional[int] = None):
    """
    Create a new routine folder.

    Args:
        title: Folder title
        index: Optional display order index
    """
    from services.types import PostRoutineFolderRequestBody

    client = get_client()
    try:
        folder_data = PostRoutineFolderRequestBody(title=title, index=index)
        result = await client.create_routine_folder(folder_data)
        return result.model_dump() if result else {"error": "Failed to create folder"}
    except (ValueError, Exception) as e:
        return {"error": f"Failed to create folder: {e}"}

# ==================== Exercise Template Tools ====================

@mcp.tool()
async def get_exercise_templates(page: int = 1):
    """
    Get all available exercise templates (standard and custom).

    Args:
        page: Page number (default: 1)
    """
    client = get_client()
    result = await client.get_exercise_templates(page=page)
    return result.model_dump() if result else {"error": "Failed to get exercise templates"}

@mcp.tool()
async def get_exercise_template(template_id: str):
    """
    Get details for a specific exercise template.

    Args:
        template_id: Unique template ID
    """
    client = get_client()
    result = await client.get_exercise_template(template_id)
    return result.model_dump() if result else {"error": f"Failed to get template {template_id}"}

@mcp.tool()
async def create_custom_exercise(
    title: str,
    exercise_type: str,
    primary_muscle_group: Optional[str] = None,
    secondary_muscle_groups: Optional[list[str]] = None,
    equipment_category: Optional[str] = None
):
    """
    Create a new custom exercise template.

    Args:
        title: Exercise title
        exercise_type: Type of exercise (weight_reps, reps_only, bodyweight_reps, etc.)
        primary_muscle_group: Primary muscle group targeted
        secondary_muscle_groups: List of secondary muscle groups
        equipment_category: Equipment category (barbell, dumbbell, machine, etc.)
    """
    from services.types import CreateCustomExerciseRequestBody, CustomExerciseType, MuscleGroup, EquipmentCategory

    client = get_client()
    try:
        exercise_data = CreateCustomExerciseRequestBody(
            title=title,
            type=CustomExerciseType(exercise_type),
            primary_muscle_group=MuscleGroup(primary_muscle_group) if primary_muscle_group else None,
            secondary_muscle_groups=[MuscleGroup(mg) for mg in secondary_muscle_groups] if secondary_muscle_groups else None,
            equipment_category=EquipmentCategory(equipment_category) if equipment_category else None
        )
        result = await client.create_custom_exercise(exercise_data)
        return result.model_dump() if result else {"error": "Failed to create custom exercise"}
    except (ValueError, Exception) as e:
        return {"error": f"Failed to create custom exercise: {e}"}

@mcp.tool()
async def get_exercise_history(template_id: str):
    """
    Get the history of a specific exercise across all workouts.

    Args:
        template_id: Unique exercise template ID
    """
    client = get_client()
    result = await client.get_exercise_history(template_id)
    return result.model_dump() if result else {"error": f"Failed to get exercise history for {template_id}"}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001)
