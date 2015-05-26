from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from schedulizer.models import course
from algorithm import schedule as schedulize, checkConflicts
from datetime import time

# Create your views here.

def home(request):
	return render(request, 'main.html')

def main(request):
	return render(request, 'main.html')

def about(request):
	return render(request, 'about.html')

def contact(request):
	return render(request, 'contact.html')

def service(request):
	all_courses = course.objects.all()
	subject_codes = []
	numbers_by_subject = {}
	for this_course in all_courses:
		subject_code = this_course.subject_code
		course_number = this_course.course_number
		if subject_code not in subject_codes:
			subject_codes.append(subject_code)
			numbers_by_subject[subject_code] = [course_number]
		else:
			if course_number not in numbers_by_subject[subject_code]:
				numbers_by_subject[subject_code].append(numbers_by_subject)

	return render(request, 'service.html', 
		{
			'subject_codes': subject_codes, 
			'numbers_by_subject': numbers_by_subject
		})

def staff(request):
	return render(request, 'staff.html')

 
#def css(request):
	# return render(request, 'main.css', content_type="text/css")

def make_schedule(request):
	schedule = []
	link = ""
	if request.method == "POST":
		required_course_names = []
		optional_course_names = []

		data = request.POST
		keys = request.POST.keys()

		for i in range(1, int(data['num_courses'])):
			department_selector = "department" + str(i)
			if department_selector in keys:
				dep_name = data[department_selector]
				c_num = data["number" + str(i)]
				full_name = course.objects.filter(subject_code=dep_name, course_number=c_num)[0].course_title
				
				optional = int(data["option"+str(i)])
				if (optional):
					optional_course_names.append(full_name)
				else:
					required_course_names.append(full_name)
			else:
				break

		start_time = time(0)
		end_time = time(23,59,59)
		days = ""
		if "start_time" in keys:
			split_time = data["start_time"].split(':')
			start_time = time(int(split_time[0]), int(split_time[1]), int(split_time[2]))
		if "end_time" in keys:
			split_time = data["start_time"].split(':')
			end_time = time(int(split_time[0]), int(split_time[1]), int(split_time[2]))
		if "no-mondays" in keys:
			days += "M"
		if "no-tuesdays" in keys:
			days += "T"
		if "no-wednesdays" in keys:
			days += "W"
		if "no-thursdays" in keys:
			days += "R"
		if "no-fridays" in keys:
			days += "F"

		schedule = schedulize(required_course_names, optional_course_names, days, start_time, end_time)
		print schedule

		link += "/recall/?courses="

		for course_obj in schedule:
			link += str(course_obj.id)
			link += ","

		link = link[:-1]
	return render(request, "schedule.html", {
		"courses": schedule,
		"link": link,
		})

def recall_schedule(request):
	courses = request.GET.get('courses')
	if courses:
		courses_to_display = []
		split_courses = courses.split(",")
		for course_id in split_courses:
			try:
				course_obj = course.objects.get(id=course_id)
			except course.DoesNotExist:
				pass
			else:
				courses_to_display.append(course_obj)
		return render(request, "recall.html", {"courses": courses_to_display})
	else:
		return HttpResponseRedirect('/')
