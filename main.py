from datetime import datetime
from typing import Any, Optional
from fastmcp import FastMCP
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.responses import JSONResponse
import os

from services.hevy import HevyClient

API_KEY = os.environ["API_KEY"]

class AuthMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            auth = headers.get(b"authorization", b"").decode()
            if auth != f"Bearer {API_KEY}":
                response = JSONResponse({"error": "Unauthorized"}, status_code=401)
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)

mcp = FastMCP("HevyHealthServer")

# Shared client instance
_client: Optional[HevyClient] = None

def get_client() -> HevyClient:
    """Get or create the shared Hevy client instance."""
    global _client
    if _client is None:
        _client = HevyClient()
    return _client


def _jsonable(value: Any) -> Any:
    """Convert tool outputs into JSON-safe values."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json", exclude_none=True)
    return value


def _ok(data: Any) -> dict:
    return {
        "ok": True,
        "data": _jsonable(data),
        "error": None,
    }


def _error(code: str, message: str, details: Optional[dict] = None) -> dict:
    return {
        "ok": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
    }

# ==================== User Tools ====================

@mcp.tool()
async def get_user_info():
    """Get basic user profile information (id, name, url)."""
    client = get_client()
    result = await client.get_user_info()
    if result is None:
        return _error("upstream_error", "Failed to get user info")
    return _ok(result)

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
    if result is None:
        return _error("upstream_error", "Failed to get workouts", {"page": page})
    return _ok(result)

@mcp.tool()
async def get_workout(workout_id: str):
    """
    Get complete details for a single workout.

    Args:
        workout_id: Unique workout ID
    """
    client = get_client()
    result = await client.get_workout(workout_id)
    if result is None:
        return _error("not_found", f"Failed to get workout {workout_id}", {"workout_id": workout_id})
    return _ok(result)

@mcp.tool()
async def get_workout_count():
    """Get the total number of workouts on the account."""
    client = get_client()
    count = await client.get_workout_count()
    if count is None:
        return _error("upstream_error", "Failed to get workout count")
    return _ok({"count": count})

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
        if result is None:
            return _error(
                "upstream_error",
                "Failed to get workout events",
                {"since": since, "page": page},
            )
        return _ok(result)
    except ValueError as e:
        return _error("invalid_input", "Invalid date format", {"since": since, "reason": str(e)})

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
    from services.types import PostWorkoutsRequestBody

    client = get_client()
    try:
        workout_data = PostWorkoutsRequestBody(
            workout={
                "title": title,
                "description": description,
                "start_time": datetime.fromisoformat(start_time.replace('Z', '+00:00')),
                "end_time": datetime.fromisoformat(end_time.replace('Z', '+00:00')),
                "exercises": exercises,
                "routine_id": routine_id,
            }
        )
        result = await client.create_workout(workout_data)
        if result is None:
            return _error("upstream_error", "Failed to create workout")
        return _ok(result)
    except (ValueError, Exception) as e:
        return _error("invalid_input", "Failed to create workout", {"reason": str(e)})

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
    if result is None:
        return _error("upstream_error", "Failed to get routines", {"page": page})
    return _ok(result)

@mcp.tool()
async def get_routine(routine_id: str):
    """
    Get a routine by its unique ID.

    Args:
        routine_id: Unique routine ID
    """
    client = get_client()
    result = await client.get_routine(routine_id)
    if result is None:
        return _error("not_found", f"Failed to get routine {routine_id}", {"routine_id": routine_id})
    return _ok(result)

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
    from services.types import PostRoutinesRequestBody

    client = get_client()
    try:
        routine_data = PostRoutinesRequestBody(
            routine={
                "title": title,
                "folder_id": folder_id,
                "exercises": exercises,
            }
        )
        result = await client.create_routine(routine_data)
        if result is None:
            return _error("upstream_error", "Failed to create routine")
        return _ok(result)
    except (ValueError, Exception) as e:
        return _error("invalid_input", "Failed to create routine", {"reason": str(e)})

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
    from services.types import PutRoutinesRequestBody

    client = get_client()
    try:
        routine_data = PutRoutinesRequestBody(
            routine={
                "title": title,
                "folder_id": folder_id,
                "exercises": exercises,
            }
        )
        result = await client.update_routine(routine_id, routine_data)
        if result is None:
            return _error(
                "upstream_error",
                f"Failed to update routine {routine_id}",
                {"routine_id": routine_id},
            )
        return _ok(result)
    except (ValueError, Exception) as e:
        return _error("invalid_input", "Failed to update routine", {"reason": str(e)})

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
    if result is None:
        return _error("upstream_error", "Failed to get routine folders", {"page": page})
    return _ok(result)

@mcp.tool()
async def get_routine_folder(folder_id: int):
    """
    Get a single routine folder by ID.

    Args:
        folder_id: Unique folder ID
    """
    client = get_client()
    result = await client.get_routine_folder(folder_id)
    if result is None:
        return _error("not_found", f"Failed to get folder {folder_id}", {"folder_id": folder_id})
    return _ok(result)

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
        folder_data = PostRoutineFolderRequestBody(
            routine_folder={
                "title": title,
                "index": index,
            }
        )
        result = await client.create_routine_folder(folder_data)
        if result is None:
            return _error("upstream_error", "Failed to create folder")
        return _ok(result)
    except (ValueError, Exception) as e:
        return _error("invalid_input", "Failed to create folder", {"reason": str(e)})

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
    if result is None:
        return _error("upstream_error", "Failed to get exercise templates", {"page": page})
    return _ok(result)

@mcp.tool()
async def get_exercise_template(template_id: str):
    """
    Get details for a specific exercise template.

    Args:
        template_id: Unique template ID
    """
    client = get_client()
    result = await client.get_exercise_template(template_id)
    if result is None:
        return _error("not_found", f"Failed to get template {template_id}", {"template_id": template_id})
    return _ok(result)

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
            exercise={
                "title": title,
                "exercise_type": CustomExerciseType(exercise_type),
                "muscle_group": MuscleGroup(primary_muscle_group) if primary_muscle_group else None,
                "other_muscles": [MuscleGroup(mg) for mg in secondary_muscle_groups] if secondary_muscle_groups else [],
                "equipment_category": EquipmentCategory(equipment_category) if equipment_category else None,
            }
        )
        result = await client.create_custom_exercise(exercise_data)
        if result is None:
            return _error("upstream_error", "Failed to create custom exercise")
        return _ok(result)
    except (ValueError, Exception) as e:
        return _error("invalid_input", "Failed to create custom exercise", {"reason": str(e)})

@mcp.tool()
async def get_exercise_history(
    template_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """
    Get the history of a specific exercise across all workouts.

    Args:
        template_id: Unique exercise template ID
        start_date: Optional ISO 8601 start date filter
        end_date: Optional ISO 8601 end date filter
    """
    client = get_client()
    try:
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00')) if start_date else None
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00')) if end_date else None
        result = await client.get_exercise_history(template_id, start_date=start_dt, end_date=end_dt)
        if result is None:
            return _error(
                "upstream_error",
                f"Failed to get exercise history for {template_id}",
                {
                    "template_id": template_id,
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )
        return _ok(result)
    except ValueError as e:
        return _error(
            "invalid_input",
            "Invalid date format",
            {
                "template_id": template_id,
                "start_date": start_date,
                "end_date": end_date,
                "reason": str(e),
            },
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("MCP_PORT", "8001"))
    host = os.getenv("MCP_HOST", "0.0.0.0")
    
    app = mcp.http_app(path="/mcp")
    app.add_middleware(AuthMiddleware)  # Starlette nativo
    
    uvicorn.run(app, host=host, port=port)
