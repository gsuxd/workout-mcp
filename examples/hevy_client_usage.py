"""
Example usage of the Hevy API Client

This file demonstrates how to use the HevyClient to interact with the Hevy API.
"""

import asyncio
from datetime import datetime, timedelta
from services.hevy import HevyClient
from services.types import (
    PostWorkoutsRequestBody,
    CreateCustomExerciseRequestBody,
    SetType,
    CustomExerciseType,
    MuscleGroup,
    EquipmentCategory,
)


async def example_usage():
    """Example usage of the Hevy API client."""
    
    # Initialize client (uses HEVY_API_KEY from .env)
    async with HevyClient() as client:
        
        # ==================== User Info ====================
        print("=== User Info ===")
        user = await client.get_user_info()
        if user:
            print(f"User: {user.name} (ID: {user.id})")
            print(f"Profile: {user.url}\n")
        
        # ==================== Workouts ====================
        print("=== Workouts ===")
        
        # Get workout count
        count = await client.get_workout_count()
        print(f"Total workouts: {count}")
        
        # Get paginated workouts
        workouts = await client.get_workouts(page=1)
        if workouts:
            print(f"Page {workouts.page}/{workouts.page_count}")
            for workout in workouts.workouts[:3]:  # Show first 3
                print(f"  - {workout.title} ({workout.start_time.date()})")
        
        # Get specific workout
        if workouts and workouts.workouts:
            workout_id = workouts.workouts[0].id
            workout = await client.get_workout(workout_id)
            if workout:
                print(f"\nWorkout details: {workout.title}")
                print(f"  Exercises: {len(workout.exercises)}")
                for ex in workout.exercises[:2]:  # Show first 2
                    print(f"    - {ex.title}: {len(ex.sets)} sets")
        
        # Get workout events (for sync)
        since = datetime.now() - timedelta(days=7)
        events = await client.get_workout_events(since=since, page=1)
        if events:
            print(f"\nWorkout events in last 7 days: {len(events.events)}")
        
        # ==================== Create Workout ====================
        print("\n=== Create Workout Example ===")
        
        # Example: Create a simple workout
        new_workout = PostWorkoutsRequestBody(
            workout={
                "title": "Morning Push Workout",
                "description": "Chest and triceps focus",
                "start_time": datetime.now(),
                "end_time": datetime.now() + timedelta(hours=1),
                "exercises": [
                    {
                        "exercise_template_id": "bench-press-barbell",  # Use actual template ID
                        "sets": [
                            {"type": SetType.WARMUP, "weight_kg": 60, "reps": 10},
                            {"type": SetType.NORMAL, "weight_kg": 80, "reps": 8},
                            {"type": SetType.NORMAL, "weight_kg": 80, "reps": 8},
                            {"type": SetType.NORMAL, "weight_kg": 80, "reps": 7},
                        ],
                    },
                    {
                        "exercise_template_id": "tricep-dips",  # Use actual template ID
                        "sets": [
                            {"type": SetType.NORMAL, "reps": 12},
                            {"type": SetType.NORMAL, "reps": 10},
                            {"type": SetType.FAILURE, "reps": 8},
                        ],
                    },
                ],
            }
        )
        
        # Uncomment to actually create:
        # created = await client.create_workout(new_workout)
        # if created:
        #     print(f"Created workout: {created.id}")
        
        # ==================== Routines ====================
        print("\n=== Routines ===")
        
        routines = await client.get_routines(page=1)
        if routines:
            print(f"Total routines: {len(routines.routines)}")
            for routine in routines.routines[:3]:
                print(f"  - {routine.title} ({len(routine.exercises)} exercises)")
        
        # ==================== Exercise Templates ====================
        print("\n=== Exercise Templates ===")
        
        templates = await client.get_exercise_templates(page=1)
        if templates:
            print(f"Total templates: {len(templates.exercise_templates)}")
            for template in templates.exercise_templates[:5]:
                custom = "Custom" if template.is_custom else "Standard"
                print(f"  - {template.title} ({custom})")
        
        # Create custom exercise
        custom_exercise = CreateCustomExerciseRequestBody(
            exercise={
                "title": "My Custom Exercise",
                "exercise_type": CustomExerciseType.WEIGHT_REPS,
                "muscle_group": MuscleGroup.CHEST,
                "other_muscles": [MuscleGroup.TRICEPS, MuscleGroup.SHOULDERS],
                "equipment_category": EquipmentCategory.DUMBBELL,
            }
        )
        
        # Uncomment to actually create:
        # created_template = await client.create_custom_exercise(custom_exercise)
        # if created_template:
        #     print(f"\nCreated custom exercise: {created_template.id}")
        
        # ==================== Exercise History ====================
        print("\n=== Exercise History ===")
        
        if templates and templates.exercise_templates:
            template_id = templates.exercise_templates[0].id
            history = await client.get_exercise_history(template_id)
            if history:
                print(f"Total history entries: {len(history.exercise_history)}")
                for entry in history.exercise_history[:3]:
                    print(f"    - {entry.workout_title} ({entry.workout_start_time.date()}): reps={entry.reps} weight_kg={entry.weight_kg}")


if __name__ == "__main__":
    asyncio.run(example_usage())
