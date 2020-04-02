"""
Scenario:
- there is a certain number of patients at start day_total_cases
- each day there are more new patients based on doubles_in_days
- each day some patients will die based on case_fatality_rate
- each day some patients are released based on mean_duration
    - all patients that meet mean_duration and did not die are released
- some patients can be admitted based on current available capacity
    - such patients will be added to day_total_cases
- some patients may not be admittable due to lack of current capacity
    - such patients will die
"""
import collections
import random
import math
from enum import Enum
from functools import reduce

import simpy

PATIENTS_AMOUNT = 300
HOURS_IN_DAY = 24
RANDOM_SEED = 42
HOSPITAL_CAPACITY = 100  # Capacity of hospital per icu_type
SIMULATE_TIME = 20*HOURS_IN_DAY  # Simulate until
DAILY_GROWTH_RATE = 0.178
DAILY_VENTILATED_ICU_DIE_RATE = 0.1
DAILY_DIE_VENTILATED_ICU_REJECTED_RATE = 0.1
STANDARD_ICU_MEAN_DURATION_PERIOD = 5*HOURS_IN_DAY
VENTILATED_ICU_MEAN_DURATION_PERIOD = 5*HOURS_IN_DAY


class ICU_Types(Enum):
    STANDARD_ICU = 1
    VENTILATED_ICU = 2


def hospital_manager(env, icu_type, hospital, hours_in_day):
    """A hospital_manager tries to place each patient while there exists free space."""

    with hospital.counter.request() as my_turn:
        # Wait until its our turn
        result = yield my_turn

        place_available = (hospital.departments_capacity[icu_type]['max_length'] - len(
            hospital.departments_capacity[icu_type]['icu_date_arriving_list']))

        # Check if it's our turn or if icu_type is filled in
        if place_available == 0:
            print(f'avail: {place_available} type: {icu_type}')
            print('refused')
            hospital.daily_refused_total[icu_type] += 1

        else:
            print(f'avail: {place_available} type: {icu_type}')
            print('not refused')
            # Hold a place
            hospital.daily_accepted_total[icu_type] += 1
            hospital.departments_capacity[icu_type]['icu_date_arriving_list'].append(
                env.now)

        yield env.exit()


def update_icu_departments(
        env, hospital, standard_icu_mean_duration,
        ventilated_icu_mean_duration, daily_ventilated_icu_die_rate, hours_in_day):
    """Update statistic every 24 hours"""

    nearest_hour = round(env.now)
    day_number = nearest_hour / hours_in_day

    if (nearest_hour != 0) and (nearest_hour % hours_in_day == 0) and (day_number not in hospital.statistic):

        # update ventilated icu
        ventilated_icu_list = hospital.departments_capacity[
            ICU_Types.VENTILATED_ICU.name]['icu_date_arriving_list']
        count_died_people = round(
            len(ventilated_icu_list)*daily_ventilated_icu_die_rate)
        ventilated_icu_length = len(ventilated_icu_list)
        hospital.departments_capacity[
            ICU_Types.VENTILATED_ICU.name]['icu_date_arriving_list'] = random.sample(ventilated_icu_list,
                                                                                     ventilated_icu_length - count_died_people)

        # release standard icu
        standard_icu_list = hospital.departments_capacity[
            ICU_Types.STANDARD_ICU.name]['icu_date_arriving_list']
        standard_icu_before_release_length = len(standard_icu_list)
        standard_icu_list = list(filter(lambda arrival_date: (arrival_date+standard_icu_mean_duration) > env.now,
                                        standard_icu_list))
        standard_icu_released_count = standard_icu_before_release_length - \
            len(standard_icu_list)

        # release ventilated icu
        ventilated_icu_list = hospital.departments_capacity[
            ICU_Types.VENTILATED_ICU.name]['icu_date_arriving_list']
        ventilated_icu_before_release_length = len(ventilated_icu_list)
        ventilated_icu_list = list(filter(lambda arrival_date: (arrival_date+ventilated_icu_mean_duration) > env.now,
                                          ventilated_icu_list))
        ventilated_icu_released_count = ventilated_icu_before_release_length - \
            len(ventilated_icu_list)

        # update statistic
        hospital.statistic.update({day_number: {
            'total_demand': {icu_type: (hospital.daily_refused_total[icu_type] + hospital.daily_accepted_total[icu_type]) for icu_type in hospital.departments},
            'total_released': {ICU_Types.STANDARD_ICU.name: standard_icu_released_count, ICU_Types.VENTILATED_ICU.name: ventilated_icu_released_count},
            'total_refused': {icu_type: hospital.daily_refused_total[icu_type] for icu_type in hospital.departments},
            'total_died': {ICU_Types.STANDARD_ICU.name: 0, ICU_Types.VENTILATED_ICU.name: count_died_people},
        }})

        # cleanup count for next the day
        hospital.daily_refused_total.update({
            icu_type: 0 for icu_type in hospital.departments})

    yield env.exit()


def patients_arrivals(env, hospital):
    """Emulating patient arriving"""
    while True:
        total_population = get_population_by_day(
            env.now, HOURS_IN_DAY, PATIENTS_AMOUNT, DAILY_GROWTH_RATE)
        yield env.timeout(get_daily_incoming_rate(HOURS_IN_DAY, total_population))

        icu_type = random.choice(hospital.departments)
        env.process(hospital_manager(
            env, icu_type, hospital, HOURS_IN_DAY))
        env.process(update_icu_departments(
            env, hospital,
            STANDARD_ICU_MEAN_DURATION_PERIOD, VENTILATED_ICU_MEAN_DURATION_PERIOD,
            DAILY_VENTILATED_ICU_DIE_RATE, HOURS_IN_DAY))


def is_there_difference_between_max_and_current(departments_capacity):
    return departments_capacity['max_length'] - len(departments_capacity['icu_date_arriving_list'])


def get_nearest_day(time_now, hours_in_day):
    return math.ceil(time_now / hours_in_day)


def get_population_by_day(time_now, hours_in_day, patients_amount, daily_growth_rate):
    return (get_nearest_day(time_now, hours_in_day)*daily_growth_rate*patients_amount) + patients_amount


def get_daily_incoming_rate(hours_in_day, population):
    return hours_in_day / population


hospital = collections.namedtuple('Hospital', 'counter, departments, departments_capacity, '
                                  'filled_in, daily_refused_total, daily_accepted_total, statistic')


# Setup and start the simulation
print('icu_type renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Create icu_type hospital
counter = simpy.Resource(env, capacity=1)
statistic = {}
departments = [ICU_Types.STANDARD_ICU.name, ICU_Types.VENTILATED_ICU.name]
departments_capacity = {
    ICU_Types.STANDARD_ICU.name: {'max_length': HOSPITAL_CAPACITY * 0.8, 'icu_date_arriving_list': []},
    ICU_Types.VENTILATED_ICU.name: {'max_length': HOSPITAL_CAPACITY * 0.2, 'icu_date_arriving_list': []}}
filled_in = {icu_type: env.event() for icu_type in departments}
daily_refused_total = {icu_type: 0 for icu_type in departments}
daily_accepted_total = {icu_type: 0 for icu_type in departments}
hospital = hospital(counter, departments,
                    departments_capacity, filled_in, daily_refused_total, daily_accepted_total, statistic)


# Start process and run
env.process(patients_arrivals(env, hospital))
env.run(until=SIMULATE_TIME)

# Analysis/results
for icu_type in departments:
    if hospital.departments[icu_type]:
        pass
