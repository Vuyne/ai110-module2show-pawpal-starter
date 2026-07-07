from pawpal_system import Pet, Task


def test_mark_complete_updates_task_status():
    task = Task(title="Morning walk", duration_minutes=20)

    assert task.status == "pending"

    task.mark_complete()

    assert task.status == "complete"


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi")
    initial_count = pet.task_count

    pet.add_task(Task(title="Feeding", duration_minutes=10))

    assert pet.task_count == initial_count + 1
