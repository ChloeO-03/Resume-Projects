"""
Module: doctors

An application to solve the Doctors Without Orders problem.

Authors:
1. Chloe Ogamba
2. Melissa Vargas
"""

from sys import argv, exit
from dataclasses import dataclass

def hour_or_hours(num_hours: int) -> str:
    """Helper function to get correct pluralization."""
    assert num_hours >= 0
    return "hour" if num_hours == 1 else "hours"


@dataclass(frozen=True)
class Doctor:
    """A representation of a Doctor, including their name and the maximum
    available hours for scheduling (max_hours).

    Doctors are immutable (i.e. can't change any of their two attributes).

    DO NOT MODIFY THIS CLASS IN ANY WAY!!!

    >>> dr_sat = Doctor("Sat Garcia", 7)
    >>> dr_sat.name
    'Sat Garcia'
    >>> dr_sat.max_hours
    7
    >>> dr_sat.max_hours = 11
    Traceback (most recent call last):
        ...
    dataclasses.FrozenInstanceError: cannot assign to field 'max_hours'
    """
    name: str
    max_hours: int

    def __str__(self) -> str:
        h = hour_or_hours(self.max_hours)
        return f"Doctor {self.name} ({self.max_hours} {h})"


@dataclass(frozen=True)
class Patient:
    """A representation of a Patient, including their name and the number of
    hours they need to be seen for (needed_hours).

    Patients are immutable (i.e. can't change any of their two attributes).

    DO NOT MODIFY THIS CLASS IN ANY WAY!!!

    >>> ouchy = Patient("Ben Hurt", 3)
    >>> ouchy.name
    'Ben Hurt'
    >>> ouchy.needed_hours
    3
    >>> ouchy.needed_hours = 1
    Traceback (most recent call last):
        ...
    dataclasses.FrozenInstanceError: cannot assign to field 'needed_hours'
    """
    name: str
    needed_hours: int

    def __str__(self) -> str:
        h = hour_or_hours(self.needed_hours)
        return f"Patient {self.name} ({self.needed_hours} {h})"


def parse_scheduling_data(filename: str) -> tuple[list[Doctor], list[Patient]]:
    """
    Reads the doctor and patient data from <filename>, returning a list of
    Doctors and and a list of Patients.

    DO NOT MODIFY THIS FUNCTION IN ANY WAY!!!

    Parameters:
        filename (str): Name of the file containing doctor and patient info.

    Returns:
        (tuple[list[Doctor], list[Patient]]): Two lists: the first of doctors
            and the second of patients, gathered from the specified file.
    """
    docs = []
    patients = []

    with open(filename, 'r') as f:
        all_lines = f.readlines()

        i = 0
        while i < len(all_lines) and (all_lines[i][0] == '#' or
                                      all_lines[i].strip() == ""):
            i += 1

        for line_num in range(i, len(all_lines)):
            line = all_lines[line_num]
            person_info, hours = line.split(':')
            person_split = person_info.split()
            title = person_split[0]
            name = " ".join(person_split[1:])

            if title == "Doctor":
                docs.append(Doctor(name, int(hours)))
            else:
                patients.append(Patient(name, int(hours)))

    return docs, patients


def can_schedule_all(doctors: list[Doctor], patients: list[Patient], schedule: dict[Doctor, set[Patient]]) -> bool:
    """
    Deciding which patient gos to which doctor based on the doctor's max hours 
    that they can work and the amount of hours the patient needs.

    Parameters:
        doctors (list): contains all of the information from the doctor's class
        patients (list): contains all of the information from the patient's class
        schedule (dictionary): contains the doctor's information and the patient/patients that the doctor can attend to

    Returns:
        (bool): True if the doctor and patient match and False if they don't
    """
    if len(patients)==0: #if we don't have any patients
        return True # the doctor can still work the the max amout of hours
    for doctor in doctors: # looping through our doctors list
        doctorz = doctor.max_hours # get the doctors maz hours
        patientz = patients[0].needed_hours # get patients needed hours
        
        untouched = schedule[doctor]
        for touching in untouched:
             
            doctorz -= touching.needed_hours #figure out the amount of hours the doctor has left ####

        if doctorz >= patientz:
            schedule[doctor].add(patients[0]) # adds the first patient to the schedule

            recurs_doctz =can_schedule_all(doctors,patients[1:],schedule) #recursive case
            if recurs_doctz == True:
                return True
            elif recurs_doctz == False: #remove the patient's informationfrom the list, if we are already matched
                    schedule[doctor].remove(patients[0]) ####

        elif doctorz > patientz: # if doctor hours is greater than the patient needed hours
            pass


    return False
       


if __name__ == "__main__":
    if len(argv) != 2:
        print("Error: wrong number of command line parameters")
        exit(1)

    docs, patients = parse_scheduling_data(argv[1])

    # create initial schedule, with each doctor assigned to no one!
    proposed_schedule: dict[Doctor, set[Patient]] = {d: set() for d in docs}

    if can_schedule_all(docs, patients, proposed_schedule):
        print("Proposed schedule:")
        for doc, docs_patients in proposed_schedule.items():
            patient_names = ", ".join([str(p) for p in docs_patients])
            print(f"\t{doc} -> {patient_names}")
    else:
        print("No valid schedule possible!")