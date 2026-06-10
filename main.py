WORKOUTS_FILE = "workouts.txt"
SEPARATOR = "=" * 50


def print_header():
    """Display the application header."""
    print("\n" + SEPARATOR)
    print("💪 GYM PROGRESS TRACKER 💪")
    print(SEPARATOR + "\n")

def print_menu():
    """Display the main menu."""
    print("\nWhat would you like to do?")
    print("  1. Add a new workout")
    print("  2. View all workouts")
    print("  3. Add a set to an existing exercise")
    print("  4. Delete an exercise (and its sets)")
    print("  5. Delete entire workout")
    print("  6. Exit")
    print()


def get_input(prompt, input_type=str):
    """Get validated input from user."""
    while True:
        try:
            value = input(prompt)
            if input_type == int:
                return int(value)
            return value
        except ValueError:
            print("❌ Invalid input. Please try again.")


def read_file():
    """Read all lines from workouts file."""
    try:
        file = open(WORKOUTS_FILE, "r")
        lines = file.readlines()
        file.close()
        return lines
    except FileNotFoundError:
        return []


def write_file(lines):
    """Write lines to workouts file."""
    file = open(WORKOUTS_FILE, "w")
    file.writelines(lines)
    file.close()


def view_workouts():
    """Display all workouts in a formatted way."""
    lines = read_file()
    if not lines:
        print("📝 No workouts recorded yet.\n")
        return

    print("\n" + SEPARATOR)
    print("YOUR WORKOUTS")
    print(SEPARATOR)
    for line in lines:
        print(line.rstrip())
    print(SEPARATOR + "\n")


def add_workout():
    """Add a new workout entry with sets and reps."""
    print("\n" + "-" * 50)
    print("ADD NEW WORKOUT")
    print("-" * 50)

    date = get_input("📅 Enter date (e.g., 05/07/2026): ").strip()
    exercise = get_input("🏋️ Enter exercise name (e.g., Bench Press): ").strip()

    if not date or not exercise:
        print("❌ Date and exercise cannot be empty.\n")
        return

    file = open(WORKOUTS_FILE, "a")
    file.write(f"\n📅 Date: {date}\n🏋️ Exercise: {exercise}\n")
    file.close()

    add_sets_for_workout()


def add_sets_for_workout():
    """Allow user to add multiple sets for a workout."""
    set_count = 1

    while True:
        print(f"\n--- SET #{set_count} ---")
        reps = get_input("  Reps: ").strip()
        weight = get_input("  Weight (lbs): ").strip()

        if not reps or not weight:
            print("❌ Reps and weight cannot be empty.\n")
            continue

        file = open(WORKOUTS_FILE, "a")
        file.write(f"  Set {set_count}: {reps} reps @ {weight} lbs\n")
        file.close()

        choice = get_input("\nAdd another set? (1 = Yes, 2 = No): ", int)
        if choice != 1:
            print("✅ Workout saved!\n")
            break
        set_count += 1


def delete_workout():
    """Delete a complete workout (date, exercise, and all sets)."""
    print("\n" + "-" * 50)
    print("DELETE WORKOUT")
    print("-" * 50)

    lines = read_file()
    if not lines:
        print("📝 No workouts to delete.\n")
        return

    # Display workouts with numbers
    print("\nAvailable workouts:\n")
    workout_entries = []
    current_entry = []

    for i, line in enumerate(lines):
        current_entry.append((i, line))
        # Each workout starts with "📅 Date:" so we know when a new one begins
        if line.startswith("📅 Date:"):
            # Check if we have a previous entry to save
            if len(current_entry) > 1:
                workout_entries.append(current_entry[:-1])
            current_entry = [(i, line)]

    # Don't forget the last entry
    if current_entry:
        workout_entries.append(current_entry)

    # Display for user selection
    for idx, entry in enumerate(workout_entries, 1):
        print(f"{idx}. {entry[0][1].strip()}")
        for line_idx, line in entry[1:]:
            print(f"   {line.rstrip()}")

    choice = get_input("\nEnter the workout number to delete (or 0 to cancel): ", int)

    if choice == 0:
        print("❌ Cancelled.\n")
        return

    if 1 <= choice <= len(workout_entries):
        # Get the indices to delete
        indices_to_delete = {idx for idx, _ in workout_entries[choice - 1]}

        # Remove the selected workout
        new_lines = [line for i, line in enumerate(lines) if i not in indices_to_delete]
        write_file(new_lines)
        print("✅ Workout deleted successfully!\n")
    else:
        print("❌ Invalid choice.\n")


def add_set_to_exercise():
    """Add a set to an already existing exercise."""
    print("\n" + "-" * 50)
    print("ADD SET TO EXISTING EXERCISE")
    print("-" * 50)

    lines = read_file()
    if not lines:
        print("📝 No exercises found. Please add a workout first.\n")
        return

    # Find all exercises with their line indices
    exercises = []
    for i, line in enumerate(lines):
        if line.startswith("🏋️ Exercise:"):
            exercises.append((i, line.strip()))

    if not exercises:
        print("📝 No exercises found.\n")
        return

    # Display exercises
    print("\nAvailable exercises:\n")
    for idx, (line_idx, exercise_line) in enumerate(exercises, 1):
        print(f"{idx}. {exercise_line}")

    choice = get_input("\nEnter the exercise number to add a set to (or 0 to cancel): ", int)

    if choice == 0:
        print("❌ Cancelled.\n")
        return

    if 1 <= choice <= len(exercises):
        exercise_line_idx, exercise_line = exercises[choice - 1]

        # Find the highest set number for this exercise
        highest_set = 0
        i = exercise_line_idx + 1

        while i < len(lines):
            if lines[i].startswith("🏋️ Exercise:") or lines[i].startswith("📅 Date:"):
                # We've reached the next exercise/workout
                break
            if lines[i].strip().startswith("Set"):
                try:
                    set_num = int(lines[i].split("Set")[1].split(":")[0].strip())
                    highest_set = max(highest_set, set_num)
                except (ValueError, IndexError):
                    pass
            i += 1

        next_set_num = highest_set + 1

        print(f"\n--- SET #{next_set_num} ---")
        reps = get_input("  Reps: ").strip()
        weight = get_input("  Weight (lbs): ").strip()

        if not reps or not weight:
            print("❌ Reps and weight cannot be empty.\n")
            return

        # Insert the new set after the exercise line
        new_set_line = f"  Set {next_set_num}: {reps} reps @ {weight} lbs\n"
        
        # Find the correct position to insert (after the last set of this exercise)
        insert_pos = exercise_line_idx + 1
        while insert_pos < len(lines):
            if lines[insert_pos].startswith("🏋️ Exercise:") or lines[insert_pos].startswith("📅 Date:"):
                break
            insert_pos += 1

        lines.insert(insert_pos, new_set_line)
        write_file(lines)
        print("✅ Set added successfully!\n")
    else:
        print("❌ Invalid choice.\n")


def delete_exercise():
    """Delete a specific exercise and all its sets."""
    print("\n" + "-" * 50)
    print("DELETE EXERCISE")
    print("-" * 50)

    lines = read_file()
    if not lines:
        print("📝 No exercises found.\n")
        return

    # Find all exercises
    exercises = []
    for i, line in enumerate(lines):
        if line.startswith("🏋️ Exercise:"):
            exercises.append((i, line.strip()))

    if not exercises:
        print("📝 No exercises found.\n")
        return

    # Display exercises
    print("\nAvailable exercises:\n")
    for idx, (line_idx, exercise_line) in enumerate(exercises, 1):
        print(f"{idx}. {exercise_line}")

    choice = get_input("\nEnter the exercise number to delete (or 0 to cancel): ", int)

    if choice == 0:
        print("❌ Cancelled.\n")
        return

    if 1 <= choice <= len(exercises):
        exercise_idx, _ = exercises[choice - 1]

        # Find all lines belonging to this exercise
        start_idx = exercise_idx
        end_idx = exercise_idx + 1

        # Find where this exercise ends (next exercise or date line)
        while end_idx < len(lines):
            if lines[end_idx].startswith("🏋️ Exercise:") or lines[end_idx].startswith("📅 Date:"):
                break
            end_idx += 1

        # Remove the exercise and its sets
        new_lines = lines[:start_idx] + lines[end_idx:]
        write_file(new_lines)
        print("✅ Exercise deleted successfully!\n")
    else:
        print("❌ Invalid choice.\n")


def main_menu():
    """Main menu loop."""
    print_header()

    while True:
        print_menu()
        choice = get_input("Enter your choice (1-6): ", int)

        if choice == 1:
            add_workout()
        elif choice == 2:
            view_workouts()
        elif choice == 3:
            add_set_to_exercise()
        elif choice == 4:
            delete_exercise()
        elif choice == 5:
            delete_workout()
        elif choice == 6:
            print("👋 Thanks for using Gym Tracker! Keep grinding!\n")
            break
        else:
            print("❌ Invalid choice. Please enter 1-6.\n")


if __name__ == "__main__":
    main_menu()




