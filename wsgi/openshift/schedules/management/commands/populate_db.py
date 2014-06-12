from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import NoArgsCommand
import math
import pytz
from schedules.models import Faculty, Event
import urllib2
import re
import os
import sys
import codecs

file = "response.html"

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
COMMAND_DIR = os.path.join(BASE_DIR, 'commands')

termCode = '201403'

#subjectCode = ['CS', 'AS']
subjectCode = ['ACTG', 'AEC', 'AED', 'AG', 'AHE', 'ALS', 'ANS', 'ANTH', 'AREC', 'ART', 'AS', 'ASL', 'ATS', 'BA', 'BB',
               'BEE', 'BI', 'BIOE', 'BOT', 'BRR', 'CBEE', 'CCE', 'CE', 'CEM', 'CH', 'CHE', 'CHN', 'COMM', 'CROP', 'CS',
               'CSS', 'DHE', 'ECE', 'ECON', 'EECS', 'ENG', 'ENGR', 'ENSC', 'ENT', 'ENVE', 'ES', 'EXSS', 'FE', 'FES',
               'FILM', 'FIN', 'FLL', 'FOR', 'FR', 'FS', 'FST', 'FW', 'GD', 'GEO', 'GER', 'GPH', 'GRAD', 'GS', 'H', 'HC',
               'HDFS', 'HHS', 'HORT', 'HST', 'HSTS', 'IE', 'IEPA', 'IEPG', 'IEPH', 'INTL', 'IST', 'IT', 'JCHS', 'JPN',
               'LS', 'MATS', 'MB', 'MCB', 'ME', 'MFGE', 'MGMT', 'MP', 'MPP', 'MRM', 'MRKT', 'MS', 'MTH', 'MUED', 'MUP',
               'MUS', 'NE', 'NMC', 'NR', 'NS', 'NUTR', 'OC', 'PAC', 'PAX', 'PBG', 'PH', 'PHAR', 'PHL', 'PPOL', 'PS',
               'PSM', 'PSY', 'QS', 'RHP', 'RNG', 'RS', 'SED', 'SOC', 'SOIL', 'SPAN', 'ST', 'SUS', 'TA', 'TCE', 'TOX',
               'VMB', 'VMC', 'WGSS', 'WLC', 'WR', 'WRE', 'WRP', 'WRS', 'WSE', 'Z']

levels = ['lower', 'upper', 'grad', 'pro', 'inservice']
pacific = pytz.timezone('US/Pacific')
fmt = '%Y-%m-%d %H:%M:%S %Z%z'
utc = pytz.utc

#alphabet = ['M']
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']


def getFilePath(fileName):
    return os.path.join(COMMAND_DIR, fileName)


def get_instructor(first_initial, last_name):
    try:
        return Faculty.objects.get(first_initial=first_initial, last_name=last_name)
    except ObjectDoesNotExist:
        print 'CANNOT FIND: ' + first_initial + ' ' + last_name
    except MultipleObjectsReturned:
        print 'CANNOT ADD: ' + first_initial + ' ' + last_name + ', found multiple user objects...'


def runSoup(subject, self):
    with open(getFilePath(file), 'r') as f:
        soup = BeautifulSoup(f, 'html5lib')
    table = soup.find("table")

    for row in table.findAll('tr')[3:]:
        cells = row.findAll('td')
        if len(cells) == 10:
            fullName = cells[9].text.strip()
            location = cells[6].text.strip()
            credits = cells[4].text.strip()
            crn = cells[3].text.strip()
            section = cells[2].text.strip()
            courseNumber = cells[1].text.strip()
            title = cells[0].text.strip()

            course_dt_line = cells[5].text.strip()
            course_dt_line = course_dt_line.replace(" ", "").replace("?", " ")
            course_dt = course_dt_line.split()
            lastName = "".join(fullName.split(",")[:1]).strip()
            firstInitial = "".join(fullName.split(",")[1:2]).strip()
            course_days = "".join(course_dt[:1])
            course_times = "".join(course_dt[1:2]).replace(" ", "")
            course_dates = "".join(course_dt[2:3]).replace(" ", "")

            if fullName != "TBA" and course_days != "TBA" and len(course_times) >= 9 and len(course_dates) >= 13:
                instructor = get_instructor(firstInitial, lastName)
                if instructor:
                    myTime = course_times.split("-")
                    startTimeHrs = int("".join(myTime[:1])[:1])
                    startTimeMin = int("".join(myTime[:1])[1:])
                    endTimeHrs = int("".join(myTime[1:])[:1])
                    endTimeMin = int("".join(myTime[1:])[1:])

                    myDate = course_dates.split("-")
                    startDatePST = pacific.localize(datetime.strptime("".join(myDate[:1]), "%m/%d/%y"))
                    endDatePST = pacific.localize(datetime.strptime("".join(myDate[1:]), "%m/%d/%y"))
                    startDate = utc.normalize(startDatePST.astimezone(utc))
                    endDate = utc.normalize(endDatePST.astimezone(utc))

                    dtDelta = endDate - startDate
                    course_weeks = dtDelta.total_seconds() / 60 / 60 / 24 / 7
                    course_weeks = math.trunc(math.ceil(course_weeks))

                    for d in course_days:
                        if d == "T":
                            daysOff = 1
                        elif d == "W":
                            daysOff = 2
                        elif d == "R":
                            daysOff = 3
                        elif d == "F":
                            daysOff = 4
                        else:
                            daysOff = 0

                        for w in range(course_weeks):
                            startOffset = timedelta(days=daysOff, minutes=startTimeMin, hours=startTimeHrs, weeks=w)
                            endOffset = timedelta(days=daysOff, minutes=endTimeMin, hours=endTimeHrs, weeks=w)

                            busyDayStart = startDate + startOffset
                            busyDayEnd = startDate + endOffset

                            event, created = Event.objects.get_or_create(faculty_user=instructor,
                                                                         start_time=pacific.normalize(busyDayStart),
                                                                         end_time=pacific.normalize(busyDayEnd),
                                                                         description=title)

                            if created:
                                print 'ADDED COURSE: ' + title + ' - INSTRUCTOR: ' + instructor.first_name + ' ' + instructor.last_name


def populate_course_events(self):
    for i in range(0, len(subjectCode)):
        print ("Subject = %s " % subjectCode[i])
        for j in range(0, len(levels)):
            response = urllib2.urlopen('http://catalog.oregonstate.edu/MySocList.aspx?termcode=' + termCode +
                                       '&campus=corvallis&subjectcode=' + subjectCode[i] + '&level=' + levels[j])
            fh = open(getFilePath(file), "w+")
            fh.write(response.read())
            fh.close()
            runSoup(subjectCode[i], self)


def populate_faculty(self):
    for i in range(0, len(alphabet)):
        try:
            response = urllib2.urlopen("http://catalog.oregonstate.edu/FacultyList.aspx?type=1&ch=" + alphabet[i])
            fh = open(getFilePath(file), "w+")
            fh.write(response.read())
            fh.close()
        except urllib2.URLError, e:
            print 'could not connection to remote server for scraping ' + e.reason

        print ("--------------------- %s ------------------------" % alphabet[i])

        with open(getFilePath(file), 'r') as f:
            soup = BeautifulSoup(f, 'html5lib')

        for t in soup.find_all('table'):
            #Gets name and title
            name_line = t.find('span', attrs={'id': re.compile('_Label5$')})
            title_line = t.find('span', attrs={'id': re.compile('_Label6$')})

            if name_line is not None:
                full_name = name_line.get_text().strip(u'\xa0').encode('ascii', 'replace').replace(",", "").split()
                full_title = title_line.get_text().strip(u'\xa0').encode('ascii', 'replace').split(",")

                last_name = "".join(full_name[:1])
                first_name = "".join(full_name[1:2])
                first_initial = first_name[0] + '.'
                title = " ".join(full_title[1:2]).strip()
                department = " ".join(full_title[2:]).strip()

                django_username = last_name + '_' + first_name

                django_user = User.objects.get_or_create(username=django_username, first_name=first_name,
                                                           last_name=last_name, email=None,
                                                           password=set_unusable_password())
                faculty, created = \
                    Faculty.objects.get_or_create(django_user_id=django_user.id, title=title,
                                                  department=department, first_initial=first_initial)

                if created:
                    print 'ADDED: ' + first_initial + last_name + ' (linked)'



class Command(NoArgsCommand):
    help = 'Closes the specified poll for voting'
    requires_model_validation = True

    def handle_noargs(self, **options):
        # the order of this matters since courses depend on instructors being populated
        populate_faculty(self)
        populate_course_events(self)