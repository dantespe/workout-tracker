#! /usr/bin/env python
from todoist.api import TodoistAPI
from datetime import timedelta as td
from datetime import datetime
import os

API_KEY = os.environ.get("TODOIST_API_KEY")
PROJECT_ID = os.environ.get("TODOIST_WORKOUT_PROJECT_ID")

DRY_RUN = False

REGIME = [
    'Run',
    'Phase 1: Chest & Delts',
    'Phase 1: Legs',
    'Phase 1: Back & Traps',
    'Phase 1: Arms',
    'OFF',
    'Run',
    'Phase 2: Chest & Delts',
    'Phase 2: Legs',
    'Phase 2: Back & Traps',
    'Phase 2: Arms',
    'OFF',
    'OFF'
]

BREAK = [
    'BREAK 1',
    'BREAK 2',
    'BREAK 3'
]
CYCLES_TIL_BREAK = 5
STARTING_PUSH_UPS = 20
YEAR = 2019


def send_to_todoist(assignment, day, time=""):
    print(day)
    date_string = "{d} at {t}".format(d=day.strftime("%m/%d/%Y"), t=time) if time else "{d}".format(d=day.strftime("%m/%d/%Y"))
    if DRY_RUN:
        print(assignment + ' on '+ date_string)
    else:
        api = TodoistAPI(API_KEY)
        api.sync()
        api.items.add(assignment, PROJECT_ID, date_string=date_string)
        api.commit()

def daily_assignment(day):
    assignment = "Do {number} push ups".format(number=STARTING_PUSH_UPS + 5 * day.month)
    send_to_todoist(assignment, day, time="7am")
    send_to_todoist(assignment, day, time="10pm")

def set_workouts_for_year(day, shift=1):
    day_count = 0
    cycles = 0
    rest = False

    while day.year == YEAR:
        daily_assignment(day)

        # Determine if rest is needed
        if not rest and cycles == CYCLES_TIL_BREAK:
            rest = True
            cycles = 0
            day_count = 0

        if rest:
            send_to_todoist(BREAK[day_count], day)

            if day_count + 1 == len(BREAK):
                rest = False
                day_count = -1

        else:
            if day_count % len(REGIME) + 1 == len(REGIME):
                cycles += 1
            send_to_todoist(REGIME[day_count % len(REGIME)], day)

        day += td(days=shift)
        day_count += 1


def main():
    day = datetime(month=1, day=1, year=YEAR)
    set_workouts_for_year(day)

if __name__ == "__main__":
    main()
