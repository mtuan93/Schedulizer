import unittest
from prototype import settings
from datetime import time
from schedulizer.models import course

from algorithm import *

course1 = course(course_CRN="93948", course_title="CS101", start_time=time(hour=10), end_time=time(hour=10,minute=50),dates_given="MWF", term_name="1")

course2 = course(course_CRN="90384", course_title="CS102", start_time=time(hour=12), end_time=time(hour=13,minute=50),dates_given="TR", term_name="2")

course3 = course(course_CRN="39948", course_title="CS103", start_time=time(hour=11), end_time=time(hour=12,minute=50),dates_given="MW", term_name="3")

course4 = course(course_CRN="10394", course_title="CS101", start_time=time(hour=18), end_time=time(hour=21), dates_given="T", term_name="4")

course5 = course(course_CRN="29302", course_title="CS101", start_time=time(hour=12),end_time=time(hour=13,minute=20), dates_given="WF", term_name="5")

all_courses = [course1,course2,course3,course4,course5]
programming1 = [course1, course4, course5]
programming1_dict = {
    'Programming 1': programming1,
}
all_courses_dict ={
    'Programming 1': programming1,
    'Programming 2': [course2],
    'Programming 3': [course3]
}

class testCheckDay(unittest.TestCase):
    def test(self):
        assert checkDay(course1, "T") == True
        assert checkDay(course1, "F") == False
        assert checkDay(course1, "TR") == True
        assert checkDay(course3, "F") == True
        assert checkDay(course2, "MWF") == True
        assert checkDay(course2, "F") == True

class testCheckTime(unittest.TestCase):
    def test(self):
        assert checkTime(course1, time(hour=9),time(hour=12)) == True
        assert checkTime(course1, time(hour=12), time(hour=17)) == False
        assert checkTime(course1, time(hour=9), time(hour=10)) == False

class testCheckConflicts(unittest.TestCase):
    def test(self):
        assert checkConflicts([course1,course2]) == True
        assert checkConflicts([course2, course3]) == True
        assert checkConflicts([course1, course1]) == False
        assert checkConflicts([course3, course2]) == True

class testRemoveConflicting(unittest.TestCase):
    def test(self):
        assert removeConflicting([course1, course2], [course3]) == [course1, course2]
        assert removeConflicting([course3],[course1, course2]) == [course3]
        assert removeConflicting([course3], [course3]) == []

class testCleanRestrictedDays(unittest.TestCase):
    def test(self):
        test = cleanRestrictedDays(all_courses_dict, "F") 
        assert test['Programming 1'] == [course4] and test['Programming 2'] == [course2] and test['Programming 3'] == [course3]
        test = cleanRestrictedDays(programming1_dict, "TR")
        assert test['Programming 1'] == [course1, course5]
        assert cleanRestrictedDays(all_courses_dict, "TR") == None

class testCleanRestrictedTimes(unittest.TestCase):
    def test(self):
        test = cleanRestrictedTimes(programming1_dict,time(15),time(23,59,59))
        assert test['Programming 1'] == [course4]
        test = cleanRestrictedTimes(programming1_dict, time(0), time(13))
        assert test['Programming 1'] == [course1]
        assert cleanRestrictedTimes(all_courses_dict, time(0), time(13,30)) == None

class testScheduleCleanedCourses(unittest.TestCase):
    def test(self):
        assert scheduleCleanedCourses(all_courses_dict) == [course2, course3, course1]

if __name__ == '__main__':
    unittest.main()