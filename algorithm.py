from schedulizer.models import course
from datetime import time

def checkDay(course, days):
    """
    Checks whether a course does not meet on supplied days

    @type course: course
    @param course: any course object
    @type days: str
    @param days: a string to indicate NOT allowed days of week
    @rtype: bool
    @return: whether the course DOES NOT MEET on days
    """
    for day in days:
        if day in course.dates_given:
            return False
    return True

def checkTime(course, start_time, end_time):
    """
    Checks whether a course meets in the window start_time to end_time

    @type course: course
    @param course: any course object
    @type start_time: datetime.time
    @param start_time: the earliest a class can begin
    @type end_time: datetime.time
    @param end_time: the latest a class can end 
    @rtype: bool
    @return: whether course meets inside window
    """
    print "Looking at course", course, course.end_time
    if start_time:
        if course.start_time < start_time:
            return False
    if end_time:
        if course.end_time > end_time:
            return False
    return True

def checkConflicts(courses):
    """
    Checks whether any courses supplied conflict

    @type courses: list of course
    @param courses: any course objects in a list
    @rtype: bool
    @return: true if no courses conflict
    """
    if len(courses) <= 1:
        return True
    for i in range(len(courses)):
        for j in range(i+1,len(courses)):
            print "Course1: ", courses[i], "Course2: ", courses[j]
            # do courses meet on the same days?
            if not checkDay(courses[i],courses[j].dates_given):
                # do the courses start at the same time?
                if courses[i].start_time == courses[j].start_time:
                    return False
                # figure out who starts first
                elif courses[i].start_time < courses[j].start_time:
                    # does course j start before course i ends?
                    if courses[j].start_time <= courses[i].end_time:
                        return False
                else:
                    # does course i start before course j ends?
                    if courses[i].start_time <= courses[j].end_time:
                        return False

    return True

def removeConflicting(courses_to_add, existing_schedule):
    """
    Removes from courses_to_add all courses that conflict with any courses in existing_schedule

    @type courses: list of course
    @param courses: any course objects
    @type schedule: list of course
    @param schedule: a list of non-conflicting courses to check the other list against
    @rtype: list of course
    @return: all courses in the list of courses that don't conflict with any in schedule
    """
    return_courses = []
    for course in courses_to_add:
        if checkConflicts(existing_schedule + [course]):
            return_courses.append(course)
    return return_courses

def cleanRestrictedDays(all_courses, restricted_days):
    """
    Returns a list of those sections that don't meet on restricted days. Returns None when all sections of any course overlap with restricted days.

    @type all_courses: dict[str, list of course]
    @param all_courses: a dictionary with course names as keys and lists of sections as values
    @rtype list of course
    @return all of the supplied courses minus those that meet on restricted days or None if all sections of a course have been removed
    """
    cleaned_courses = {}
    for course_name in all_courses.keys():
        allowed_sections = []

        for section in all_courses[course_name]:
            if checkDay(section, restricted_days):
                allowed_sections.append(section)

        if len(allowed_sections) == 0:
            return None
    
        cleaned_courses[course_name] = allowed_sections

    return cleaned_courses

def cleanRestrictedTimes(all_courses, start_time, end_time):
    """
    Returns a list of those sectios that begin at or after start_time and end at or before end_time. Returns None when doing so removes all sections of a course.

    @type all_courses: dict[str, list of course]
    @param all_courses: a dictionary with course names as keys and lists of sections as values
    @rtype list of course
    @return all of the supplied courses minus those that meet during restricted times or None if all sections of a course have been removed
    """
    cleaned_courses = {}
    for course_name in all_courses.keys():
        allowed_sections = []

        for section in all_courses[course_name]:
            if checkTime(section, start_time, end_time):
                allowed_sections.append(section)

        if len(allowed_sections) == 0:
            return None

        cleaned_courses[course_name] = allowed_sections

    return cleaned_courses

def scheduleCleanedCourses(all_courses):
    """
    Schedules courses by choose courses with 1 section, removing sections of other courses that conflict with the exisitng schedule, and repeating until no courses are unschedule. Returns None on all errors.

    @type all_courses: dict[str, list of course]
    @param all_courses: all of the sections of courses that have already been cleaned against schedule restrictions
    @rtype: list of course
    @return: a schedule of non-conflicting courses or None if there were issues.
    """
    # base case for recursion
    if len(all_courses) == 0:
        return []
    else:
        schedule = []
        courses_scheduled = []

        # add all single courses
        for course_name in all_courses.keys():
            sections = all_courses[course_name]
            if len(sections) == 1:
                schedule +=  sections
                courses_scheduled.append(course_name)

        remaining_keys = []

        for key in all_courses.keys():
            if key not in courses_scheduled:
                remaining_keys.append(key)
        if not schedule:
            key = remaining_keys[0]
            temp_courses = {}
            remaining_keys.remove(key)
            for key1 in remaining_keys:
                temp_courses[key1] = all_courses[key1]
            for section in all_courses[key]:
                temp_courses[key] = [section]
                schedule = scheduleCleanedCourses(temp_courses)
                if schedule: # a successful schedule was made, so keep it
                    return schedule
        else:
            if checkConflicts(schedule):
                remaining_courses ={}
                for course_name in remaining_keys:
                    remaining_sections = removeConflicting(all_courses[course_name],schedule)
                    if len(remaining_sections) == 0:
                        return None # the only section of some course conflicts with all sections of another course
                    remaining_courses[course_name] = remaining_sections
                remaining_schedule = scheduleCleanedCourses(remaining_courses)
                if remaining_schedule != None:
                    return schedule + remaining_schedule
                else:
                    return None # there was an issue making the rest of the schedule
            else:
                return schedule
                return None # courses with single sections conflict




def scheduleRequired(course_names, restricted_days="", schedule_start=time(0), schedule_end=time(23,59,59)):
    """
    Creates a schedule of all courses supplied. Return None for all errors in creation.

    @type course_names: list of str
    @param course_names: a list of strings used to query the database for courses
    @type restricted_days: str
    @param restricted_days: an optional, unordered string of days when not to have class.
    @type schedule_start: datetime.time
    @param schedule_start: an optional parameter for the earliest time a class can begin.
    @type schedule_end: datetime.time
    @param schedule_end: an optional parameter for the latest a class can end. 
    @rtype: list of course
    @return: a schedule containing exactly len(course_names) courses which do not conflict, or None for any errors
    """
    all_courses = {}

    # Get all the courses from DB
    for course_name in course_names:
        sections = course.objects.filter(course_title=course_name)
        if len(sections) == 0: 
            return None # no valid sections
        else:
            all_courses[course_name] = sections

    # remove bad days
    if (restricted_days):
        all_courses = cleanRestrictedDays(all_courses, restricted_days)

        if not all_courses:
            return None # restrictions on day removed all sections of a course

    # remove bad times
    if (schedule_start != time(0) or schedule_end != time(23,59,59)):
        all_courses = cleanRestrictedTimes(all_courses, schedule_start, schedule_end)

        if not all_courses:
            return None # restrictions on time removed all sections of a course

    # make the clean schedule
    return scheduleCleanedCourses(all_courses)


def schedule(required_course_names, optional_course_names, restricted_days="", schedule_start=time(0), schedule_end=time(23,59,59)):
    """
    Creates a schedule containing at least required courses, and any optional courses that fit after creating a schedule of required courses. Returns None for errors concerning scheduling required courses.

    @type required_course_names: list of str
    @param required_course_names: a list of strings used to query the database for courses. these will always be in the shedule, or create errors
    @type optional_course_names: list of str
    @param optional_course_names: a list of strings used to query the database for courses. these courses might be in the schedule. they will not create errors.
    @type restricted_days: str
    @param restricted_days: an optional, unordered string of days when not to have class. defaults to empty string.
    @type schedule_start: datetime.time
    @param schedule_start: an optional parameter for the earliest time a class can begin. defaults to 0:00:00.
    @type schedule_end: datetime.time
    @param schedule_end: an optional parameter for the latest a class can end. defaults to 23:59:59.
    @rtype: list of course
    @return: a schedule containing exactly len(course_names) courses which do not conflict, or None for any errors
    """
    schedule = scheduleRequired(required_course_names, restricted_days, schedule_start, schedule_end)
    print schedule

    optional_courses = {}

    # Get optional courses from DB
    for course_name in optional_course_names:
        sections = course.objects.filter(course_title=course_name)
        sections = removeConflicting(sections, schedule)
        if len(sections) != 0: 
            optional_courses[course_name] = sections

    optional_schedule = []
    optional_size = len(optional_courses)

    for key in optional_courses.keys():
        for section in optional_courses[key]:
            remaining_courses = {key:[section]}
            for key_1 in optional_courses.keys():
                if key_1 != key:
                    remaining_courses[key_1] = optional_courses[key_1]
            subschedule = scheduleRequired(remaining_courses, None, None, None)
            if len(subschedule) > len(optional_schedule):
                optional_schedule = subschedule
            if len(optional_schedule) == optional_size:
                break

    schedule += optional_schedule

    return schedule