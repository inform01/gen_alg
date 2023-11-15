from __future__ import annotations

import random


class Subject:
    def __init__(self, name: str) -> None:
        self.name = name


class Teacher:
    def __init__(self, name: str) -> None:
        self.name = name


class Group:
    def __init__(self, name: str, num_students: int) -> None:
        self.name = name
        self.num_students = num_students


class Room:
    def __init__(self, name: str, capacity: int) -> None:
        self.name = name
        self.capacity = capacity


class Class:
    def __init__(
        self,
        subject: Subject,
        teachers: list[Teacher] | Teacher,
        groups: list[Group] | Group,
        is_lecture: bool,
        room: Room,
        weekday: int,
        time_slot: int,
    ):
        self.subject = subject
        self.teachers = teachers
        self.groups = groups
        self.is_lecture = is_lecture
        self.room = room
        self.weekday = weekday
        self.time_slot = time_slot


class Schedule:
    def __init__(self, classes: list[Class]):
        self.classes = classes


def evaluate_the_schedule(schedule: Schedule) -> float:
    score = 0

    teacher_conflicts = sum(
        1
        for c1 in schedule.classes
        for c2 in schedule.classes
        if set(
            [c1.teachers] if isinstance(c1.teachers, Teacher) else c1.teachers
        ).intersection(
            [c2.teachers] if isinstance(c2.teachers, Teacher) else c2.teachers
        )
        and c1 != c2
        and c1.weekday == c2.weekday
        and c1.time_slot == c2.time_slot
    )
    score -= teacher_conflicts

    room_capacity_conflicts = sum(
        1
        for cls in schedule.classes
        if sum(group.num_students for group in cls.groups) > cls.room.capacity
    )
    score -= room_capacity_conflicts

    teacher_time_conflicts = sum(
        1
        for c1 in schedule.classes
        for c2 in schedule.classes
        if set(
            [c1.teachers] if isinstance(c1.teachers, Teacher) else c1.teachers
        ).intersection(
            [c2.teachers] if isinstance(c2.teachers, Teacher) else c2.teachers
        )
        and c1.weekday == c2.weekday
        and c1.time_slot == c2.time_slot
        and c1 != c2
    )
    score -= teacher_time_conflicts

    group_time_conflicts = sum(
        1
        for c1 in schedule.classes
        for c2 in schedule.classes
        if set([c1.groups] if isinstance(c1.groups, Group) else c1.groups).intersection(
            [c2.groups] if isinstance(c2.groups, Group) else c2.groups
        )
        and c1.weekday == c2.weekday
        and c1.time_slot == c2.time_slot
        and c1 != c2
    )
    score -= group_time_conflicts

    room_time_conflicts = sum(
        1
        for c1 in schedule.classes
        for c2 in schedule.classes
        if c1.room == c2.room
        and c1.weekday == c2.weekday
        and c1.time_slot == c2.time_slot
        and c1 != c2
    )
    score -= room_time_conflicts

    return score


def mutate(schedule: Schedule) -> Schedule:
    mutated_classes = schedule.classes.copy()
    index = random.randrange(len(mutated_classes))
    mutated_classes[index] = Class(
        mutated_classes[index].subject,
        random.choice(teachers),
        mutated_classes[index].groups,
        mutated_classes[index].is_lecture,
        mutated_classes[index].room,
        mutated_classes[index].weekday,
        mutated_classes[index].time_slot,
    )
    return Schedule(mutated_classes)


def crossover(
    first_schedule: Schedule, second_schedule: Schedule
) -> (Schedule, Schedule):
    crossover_point = random.randrange(len(first_schedule.classes))
    child_classes1 = (
        first_schedule.classes[:crossover_point]
        + second_schedule.classes[crossover_point:]
    )
    child_classes2 = (
        second_schedule.classes[:crossover_point]
        + first_schedule.classes[crossover_point:]
    )
    return Schedule(child_classes1), Schedule(child_classes2)


def genetic_algorithm(
    population, evaluate_the_schedule, mutate, crossover, generations=100
):
    for _ in range(generations):
        population = sorted(population, key=evaluate_the_schedule, reverse=True)
        new_population = population[:10]
        while len(new_population) < len(population):
            parent1, parent2 = random.sample(population[:10], 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1), mutate(child2)])
        population = new_population
    return sorted(population, key=evaluate_the_schedule, reverse=True)[0]


def convert_for_printing(items):
    if type(items) == list:
        return ", ".join(item.name for item in items)
    return items.name


if __name__ == "__main__":
    teachers = [
        Teacher(name)
        for name in (
            "0 Koval",
            "1 Burlaka",
            "2 Sumonenko",
            "3 Ivashuk",
            "4 Zuiko",
            "5 Bondar",
            "6 Petrenko",
            "7 Oliynik",
            "8 Babenko",
            "9 Marchenko",
            "10 Lytvynenko",
            "11 Zaytsev",
            "12 Petrov",
            "13 Zabuiko",
            "14 Arestovich",
        )
    ]

    subjects = [
        Subject(name)
        for name in (
            "0 Introduction to Computer Science",
            "1 Data Structures and Algorithms",
            "2 Operating Systems",
            "3 Computer Networks",
            "4 Database Systems",
            "5 Software Engineering",
            "6 Artificial Intelligence",
            "7 Machine Learning",
            "8 Computer Graphics",
            "9 Web Development",
            "10 Cybersecurity",
            "11 Human-Computer Interaction",
            "12 English",
            "13 Parallel and Distributed Computing",
            "14 Physical education",
        )
    ]

    groups = [
        Group("MI", 15),
        Group("TTP-41", 25),
        Group("TTP-42", 24),
        Group("TK-1", 30),
        Group("TK-2", 20),
    ]

    rooms = (
        [Room(f"Room_{i}", 50) for i in range(4)]
        + [Room(f"Room_{i + 4}", 20) for i in range(10)]
        + [Room(f"Room_{i + 14}", 15) for i in range(6)]
    )

    weekdays = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday"}
    times = {1: "8:40-10:15", 2: "10:35-12:10", 3: "12:20-13:55"}

    population = []
    for _ in range(100):
        classes = [
            Class(
                random.choice(subjects),
                random.sample(teachers, 1)
                if random.choice([True, False])
                else random.sample(teachers, 2),
                [random.choice(groups)]
                if random.choice([True, False])
                else random.sample(groups, 2),
                random.choice([True, False]),
                random.choice(rooms),
                random.choice(list(weekdays.keys())),
                random.choice(list(times.keys())),
            )
            for _ in range(30)
        ]
        population.append(Schedule(classes))

    best_schedule = genetic_algorithm(
        population, evaluate_the_schedule, mutate, crossover
    )

    best_schedule.classes.sort(key=lambda cls: (cls.weekday, cls.time_slot))

    print(
        f"{'День':<10} {'Час':<15} {'Предмет':<40} {'Викладач':<30} {'Група':<15} {'Лекція'}"
    )
    print("-" * 115)

    for cls in best_schedule.classes:
        print(
            f"{weekdays[cls.weekday]:<10} {times[cls.time_slot]:<15} {cls.subject.name:<40} "
            f"{convert_for_printing(cls.teachers):<30} {convert_for_printing(cls.groups):<15} {cls.is_lecture}"
        )
