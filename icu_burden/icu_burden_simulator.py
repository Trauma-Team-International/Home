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

import simpy


class ICU_Types(Enum):
    standard_icu = 1
    ventilated_icu = 2


def hospital_manager(env, icu_type, hospital, hours_in_day):
    """A hospital_manager tries to place each patient while there exists free
    space.
    """

    with hospital.counter.request() as my_turn:
        # Wait until its our turn
        result = yield my_turn

        max_capacity = hospital.departments_capacity[icu_type]['max_capacity']
        new_cases = len(
            hospital.departments_capacity[icu_type]['icu_date_arriving_list'])

        place_available = max_capacity - new_cases

        # Check if it's our turn or if icu_type is filled in
        if place_available <= 0:
            hospital.daily_refused_total[icu_type] += 1

        else:
            # Hold a place
            hospital.daily_accepted_total[icu_type] += 1
            hospital.departments_capacity[icu_type]['icu_date_arriving_list']\
                .append(env.now)

        yield env.exit()


def update_icu_departments(
        env, hospital, standard_icu_stay_duration,
        ventilated_icu_stay_duration, standard_icu_fatality_rate,
        ventilated_icu_fatality_rate, hours_in_day):
    """Update statistic every 24 hours"""

    nearest_hour = round(env.now)
    day_number = int(nearest_hour / hours_in_day)

    if ((nearest_hour != 0) and
            (nearest_hour % hours_in_day == 0) and
            (day_number not in hospital.statistic)):

        # update standard icu
        standard_icu_list = hospital.departments_capacity[
            ICU_Types.standard_icu.name]['icu_date_arriving_list']
        total_died_standard_icu = round(len(standard_icu_list)*standard_icu_fatality_rate)
        standard_icu_length = len(standard_icu_list)
        hospital.departments_capacity[
            ICU_Types.standard_icu.name]['icu_date_arriving_list'] = random.sample(
                standard_icu_list,
                standard_icu_length - total_died_standard_icu)

        # update ventilated icu
        ventilated_icu_list = hospital.departments_capacity[
            ICU_Types.ventilated_icu.name]['icu_date_arriving_list']
        total_died_ventilated_icu = round(len(ventilated_icu_list)*ventilated_icu_fatality_rate)
        ventilated_icu_length = len(ventilated_icu_list)
        hospital.departments_capacity[
            ICU_Types.ventilated_icu.name]['icu_date_arriving_list'] = random.sample(
                ventilated_icu_list,
                ventilated_icu_length - total_died_ventilated_icu)

        # release standard icu
        standard_icu_list = hospital.departments_capacity[
            ICU_Types.standard_icu.name]['icu_date_arriving_list']
        standard_icu_before_release_length = len(standard_icu_list)
        standard_icu_list = list(
            filter(
                lambda arrival_date: (arrival_date + standard_icu_stay_duration) > env.now,
                standard_icu_list))
        standard_icu_released_count = standard_icu_before_release_length - len(standard_icu_list)
        hospital.departments_capacity[
            ICU_Types.standard_icu.name]['icu_date_arriving_list'] = standard_icu_list

        # release ventilated icu
        ventilated_icu_list = hospital.departments_capacity[
            ICU_Types.ventilated_icu.name]['icu_date_arriving_list']
        ventilated_icu_before_release_length = len(ventilated_icu_list)
        ventilated_icu_list = list(
            filter(
                lambda arrival_date: (arrival_date + ventilated_icu_stay_duration) > env.now,
                ventilated_icu_list))
        ventilated_icu_released_count = ventilated_icu_before_release_length - len(ventilated_icu_list)
        hospital.departments_capacity[
            ICU_Types.ventilated_icu.name]['icu_date_arriving_list'] = ventilated_icu_list

        total_died_refused_ventilated_icu = hospital.daily_refused_total[
            ICU_Types.ventilated_icu.name]
        total_demand = {
            icu_type: (hospital.daily_refused_total[icu_type] + hospital.daily_accepted_total[icu_type]) for icu_type in hospital.departments}
        total_released = {
            ICU_Types.standard_icu.name: standard_icu_released_count,
            ICU_Types.ventilated_icu.name: ventilated_icu_released_count}
        total_refused = {
            icu_type: hospital.daily_refused_total[icu_type] for icu_type in hospital.departments}
        total_died = {
            ICU_Types.standard_icu.name: total_died_standard_icu,
            ICU_Types.ventilated_icu.name: (total_died_ventilated_icu + total_died_refused_ventilated_icu)}

        hospital.statistic.update({day_number: {
            'total_demand': total_demand,
            'total_released': total_released,
            'total_refused': total_refused,
            'total_died': total_died
        }})

        # cleanup count for next the day
        hospital.daily_refused_total.update({
            icu_type: 0 for icu_type in hospital.departments})

    yield env.exit()


def patients_arrivals(
        env, hospital, hours_in_day,
        patients_amount, doubles_in_days,
        standard_icu_stay_duration, ventilated_icu_stay_duration,
        standard_icu_fatality_rate, ventilated_icu_fatality_rate):
    """Emulating patient arriving"""
    growth_rate = 0
    while True:
        # growth_rate should be growth_rate+1 for being always bigger then env.now
        if env.now > 0 and (env.now > round(doubles_in_days*hours_in_day)*(growth_rate+1)):
            growth_rate += 1

        total_population = get_population_by_day(patients_amount, growth_rate)
        yield env.timeout(
            get_daily_incoming_rate(hours_in_day, total_population))

        icu_type = random.choice(hospital.departments)
        env.process(
            hospital_manager(env, icu_type, hospital, hours_in_day))
        env.process(
            update_icu_departments(
                env, hospital,
                standard_icu_stay_duration, ventilated_icu_stay_duration,
                standard_icu_fatality_rate, ventilated_icu_fatality_rate,
                hours_in_day))


def is_there_difference_between_max_and_current(departments_capacity):
    return departments_capacity['max_capacity'] - len(departments_capacity['icu_date_arriving_list'])


def get_nearest_day(time_now, hours_in_day):
    return math.ceil(time_now / hours_in_day)


def get_population_by_day(patients_amount, growth_rate):
    return ((growth_rate * patients_amount) + patients_amount)


def get_daily_incoming_rate(hours_in_day, population):
    return hours_in_day / population


def simulate(params_dictionary: dict = {
             'patients_amount':  120,
             'days_to_simulate':  20,
             'doubles_in_days': 4.1,
             'starting_standard_icu_count': 100,
             'starting_ventilated_icu_count':  30,
             'standard_icu_capacity': 100,
             'ventilated_icu_capacity': 30,
             'standard_icu_fatality_rate': 0.1,
             'ventilated_icu_fatality_rate': 0.1,
             'standard_icu_stay_duration': 5,
             'ventilated_icu_stay_duration': 5}):

    patients_amount = params_dictionary['patients_amount']
    days_to_simulate = params_dictionary['days_to_simulate']
    doubles_in_days = params_dictionary['doubles_in_days']
    starting_standard_icu_count = params_dictionary['starting_standard_icu_count']
    starting_ventilated_icu_count = params_dictionary['starting_ventilated_icu_count']
    standard_icu_capacity = params_dictionary['standard_icu_capacity']
    ventilated_icu_capacity = params_dictionary['ventilated_icu_capacity']
    standard_icu_fatality_rate = params_dictionary['standard_icu_fatality_rate']
    ventilated_icu_fatality_rate = params_dictionary['ventilated_icu_fatality_rate']
    standard_icu_stay_duration = params_dictionary['standard_icu_stay_duration']
    ventilated_icu_stay_duration = params_dictionary['ventilated_icu_stay_duration']

    hospital = collections.namedtuple(
        'Hospital',
        'counter, departments, departments_capacity, '
        'daily_refused_total, daily_accepted_total, statistic')
    # Setup and start the simulation
    random_seed = 42
    hours_in_day = 24
    days_to_simulate = days_to_simulate*hours_in_day
    standard_icu_stay_duration = standard_icu_stay_duration*hours_in_day
    ventilated_icu_stay_duration = ventilated_icu_stay_duration*hours_in_day

    random.seed(random_seed)
    env = simpy.Environment()

    # Create icu_type hospital
    counter = simpy.Resource(env, capacity=1)
    statistic = {}
    departments = [ICU_Types.standard_icu.name, ICU_Types.ventilated_icu.name]
    departments_capacity = {
        ICU_Types.standard_icu.name: {
            'max_capacity': standard_icu_capacity,
            'icu_date_arriving_list': [0] * starting_standard_icu_count},
        ICU_Types.ventilated_icu.name: {
            'max_capacity': ventilated_icu_capacity,
            'icu_date_arriving_list': [0] * starting_ventilated_icu_count}}

    daily_refused_total = {icu_type: 0 for icu_type in departments}
    daily_accepted_total = {icu_type: 0 for icu_type in departments}
    hospital = hospital(counter, departments,
                        departments_capacity, daily_refused_total,
                        daily_accepted_total, statistic)

    # Start process and run
    env.process(patients_arrivals(env, hospital,
                                  hours_in_day, patients_amount,
                                  doubles_in_days, standard_icu_stay_duration,
                                  ventilated_icu_stay_duration,
                                  standard_icu_fatality_rate,
                                  ventilated_icu_fatality_rate))
    env.run(until=days_to_simulate)

    return hospital.statistic


simulate()
