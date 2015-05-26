import os
import datetime
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prototype.settings')
import django
django.setup()
from schedulizer.models import course

def populate():

	start = datetime.time(12,0,0)
	end = datetime.time(15,20,0)
	add_course("Fall 2014", "000001", "CS", "171",\
	 					"001", "Introduction to Programming 1", "Professor A",\
	 					start, end, "TR")

	start = datetime.time(9,0,0)
	end = datetime.time(9,50,0)
	add_course("Fall 2014", "000002", "CHEM", "101",\
	 					"001", "Principles of Chemistry", "Professor B",\
	 					start, end, "MWF")

	start = datetime.time(10,0,0)
	end = datetime.time(10,50,0)
	add_course("Fall 2014", "000003", "PHYS", "111",\
	 					"001", "Introduction to Physics 1", "Professor C",\
	 					start, end, "MWF")

	start = datetime.time(13,0,0)
	end = datetime.time(13,50,0)
	add_course("Fall 2014", "000004", "MATH", "200",\
	 					"001", "Discrete Math", "Professor D",\
	 					start, end, "MTWR")

	start = datetime.time(15,0,0)
	end = datetime.time(16,50,0)
	add_course("Fall 2014", "000005", "ENG", "101",\
	 					"001", "Basic English", "Professor E",\
	 					start, end, "MF")

	start = datetime.time(10,30,0)
	end = datetime.time(12,20,0)
	add_course("Fall 2014", "000006", "CS", "171",\
	 					"002", "Introduction to Programming 1", "Professor F",\
	 					start, end, "TR")

	start = datetime.time(12,30,0)
	end = datetime.time(13,50,0)
	add_course("Fall 2014", "000007", "MATH", "200",\
	 					"002", "Theory and Computation 1", "Professor G",\
	 					start, end, "TRF")

	start = datetime.time(17,0,0)
	end = datetime.time(20,50,0)
	add_course("Fall 2014", "000008", "PHYS", "111",\
	 					"002", "Introduction to Physics 1", "Professor H",\
	 					start, end, "M")

	start = datetime.time(12,0,0)
	end = datetime.time(12,50,0)
	add_course("Fall 2014", "000009", "CHEM", "101",\
	 					"002", "Principles of Chemistry 1", "Professor T",\
	 					start, end, "MTWR")

	start = datetime.time(10,30,0)
	end = datetime.time(11,50,0)
	add_course("Fall 2014", "000010", "ENG", "101",\
	 					"002", "Basic English", "Professor Z",\
	 					start, end, "MTF")

def add_course(termName, courseCRN, subjectCode, courseNumber, courseSection, courseTitle, instrucTor, startTime, endTime, datesGiven):
    course_data = course(term_name=termName, course_CRN=courseCRN, subject_code=subjectCode, course_number=courseNumber, course_section=courseSection, course_title=courseTitle, instructor=instrucTor, start_time=startTime, end_time=endTime, dates_given=datesGiven)
    course_data.save()

# Start execution here!
if __name__ == '__main__':
    print ("Starting population script...")
    populate()
    print ("Completed")