"""
Module: test_doctors


PyTest Unit Test cases for COMP120 PSA5 (Doctors Without Orders)
"""


import pytest


# the following is the module(s) we are testing
import doctors
from doctors import Doctor, Patient,can_schedule_all


def test_no_patients():
   """Test for the base case of when there is a doctor but are no patients to be seen."""


   d = Doctor("D1", 100)
   schedule = {d: set()} # schedule has doctor with no patients


   result = doctors.can_schedule_all([d], [], schedule)
   assert result == True




def test_no_doctors():
   """Test for the base case of when there isn't a doctor but there are patients."""


   p = Patient("P1", 1)
   result = doctors.can_schedule_all([], [p], {})


   assert result == False




def test_one_doctor_and_patient_ok():
   """Test for when there is one doctor and one patient and the doctor has
   enough hours to meet the patient."""


   d = Doctor("D1", 10)
   p = Patient("P1", 1)


   actual_schedule = {d: set()} # initial schedule is empty


   result = doctors.can_schedule_all([d], [p], actual_schedule)


   expected_patients_for_d = set([p]) # create a set with the patient


   # need to check that we returned the right value and that the schedule for
   # the doctor matches what we expected
   assert result == True
   assert actual_schedule[d] == expected_patients_for_d




# TODO: Complete all of the test functions below.
# DO NOT modify any of the test functions above here.




def test_one_doctor_and_patient_bad():
   """Test for when there is one doctor and one patient and the doctor does
   NOT have enough hours to meet the patient."""


   doctor = Doctor("Dr. Garcia",5) # information that I am sending to the doctor class
   patient = Patient('Donah Briggs',8)
   schedule = {doctor:set()} #create an empty dictionary
   assert can_schedule_all([doctor],[patient],schedule) == False # make sure its not True




def test_one_doctor_multiple_patient_ok():
   """Test for when there is one doctor and multiple patients, and that the
   doctor has enough time to meet with all patients."""
   doctor = Doctor("Dr. Garcia",5) # information that I am sending to the doctor class
   patient1 = Patient('Donah Briggs',2)
   patient2 = Patient('Bio Briggs',2)
   patient3 = Patient('Chloe Ogamba',1)
   schedule = {doctor:set()} #create an empty dictionary
   assert can_schedule_all([doctor],[patient1,patient2,patient3],schedule) == True
  




def test_one_doctor_multiple_patient_bad():
   """Test for when there is one doctor and multiple patients, and that the
   doctor does NOT have enough time to meet with all patients. Also, none of
   the patients should require more hours than the doctor has free."""


   doctor = Doctor("Dr. Garcia",5) # information that I am sending to the doctor class
   patient1 = Patient('Donah Briggs',3)
   patient2 = Patient('Bio Briggs',3)
   patient3 = Patient('Chloe Ogamba',4)
   schedule = {doctor:set()} #create an empty dictionary
   assert can_schedule_all([doctor],[patient1,patient2,patient3],schedule) == False
  


def test_two_doctors_multiple_patient_ok():
   """Test for when there are two doctor and multiple patients, and that
   (1) We can't schedule all the patients with a single doctor.
   (2) We can schedule all the patients across the two doctors.
   (3) Each doctor will be assigned at least two patients."""


   doctor1 = Doctor("Dr. Garcia",10) # information that I am sending to the doctor class
   doctor2 = Doctor("Dr.Johnson",10)


   patient1 = Patient('Donah Briggs',4)
   patient2 = Patient('Bio Briggs',6)
   patient3 = Patient('Chloe Ogamba',2)
   patient4 = Patient('Melissa Vargas',3)
   schedule = {doctor1:set(),doctor2:set()} #create an empty dictionary


   assert can_schedule_all([doctor1],[patient1,patient2,patient3,patient4],schedule) or can_schedule_all([doctor2],[patient1,patient2,patient3,patient4],schedule) == False #can't schedule all the patients with a single doctor #####
   assert can_schedule_all([doctor1,doctor2],[patient1,patient2,patient3,patient4],schedule) == True #can schedule all the patients across the two doctors


   assert len(schedule[doctor1]) >=2 #Each doctor will be assigned at least two patients.
   assert len(schedule[doctor2]) >=2
 


def test_two_doctors_multiple_patient_bad():
   """Test for when there are two doctor and multiple patients, and that
   (1) We can't schedule all the patients with the two doctors.
   (2) None of the patients by themselves require more hours than either of
   the doctors."""


   doctor1 = Doctor("Dr. Garcia",10) # information that I am sending to the doctor class
   doctor2 = Doctor("Dr.Johnson",10)


   patient1 = Patient('Donah Briggs',4)
   patient2 = Patient('Bio Briggs',6)
   patient3 = Patient('Chloe Ogamba',2)
   patient4 = Patient('Melissa Vargas',3)
   schedule = {doctor1:set(),doctor2:set()} #create an empty dictionary


 
   assert can_schedule_all([doctor1,doctor2],[patient1,patient2,patient3,patient4],schedule) == True
  
   assert patient1.needed_hours <= doctor1.max_hours


if __name__ == "__main__":
   pytest.main(['test_doctors.py'])


