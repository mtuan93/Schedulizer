# Schedulizer

### Introduction

This app is intended to allow students to easily visualize possible class schedules and to restrict their schedule based on various criteria. Upon visiting the site, the user will choose the classes they want in the schedule, and then select any optional restrictions on that schedule. After clicking on a “submit" button, they will be able to see their schedule on an example week.

The primary users will be students at Drexel. They will already have chosen their required classes and their optional classes when they come to our product, and will simply be looking for a schedule for all of those classes. We will refer to this user type as “the student". Some other use cases may be by other people who want to see whether certain class offerings conflict. For example, an academic advisor and/or faculty members may look up whether some higher-level classes conflict, in order to see whether additional sections of one of the classes should be offered. However, we are not designing our product for these use cases at the moment.

### Requirements
* Python 2.7
* [Django](https://www.djangoproject.com)

Quick command to install Django if you have `pip` is:

```bash
pip install Django==1.8.2
```

Or you can get the latest development version by this shell command:

```bash
git clone https://github.com/django/django.git
```

For more information on setting up the working environment with Django, see [here](https://docs.djangoproject.com/en/1.8/intro/install/).

### Features
* Schedulizer will provide the user with a friendly interface to select and submit desired courses to take next term.

* Schedulizer can produce all possible combinations of selected courses.

* Based on the results, user can clearly see what is the best combination of courses.

### Development Tools

* Repository: Github
* Frontend Service: HTML5, CSS3, Javascript
* Backend Service: Python
* Libraries: JQuery, BootStrap
* Database: SQLite
* Framework: Django

### App Structure

![alt structure](http://s1.postimg.org/dh52ro7r3/appstructure.png)


