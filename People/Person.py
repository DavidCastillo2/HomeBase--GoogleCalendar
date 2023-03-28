from datetime import datetime, timedelta

from selenium.common.exceptions import NoSuchElementException


# This takes in a dictionary of dates and outputs an array of just dayNums
from Event import Event


# Takes in Dictionary of: "DayName: dayNum"
def sendDatesToArray(weekDates):
    retVal = []
    for key, value in weekDates.items():
        retVal.append(value)
    return retVal


class Person:
    def __init__(self, weekDiv, weekDates):
        # Dictionary, Key=string(dayNum) : Val=Day object
        self.days = {}
        self.name = None
        self.scrape(weekDiv, weekDates)

    def combine(self, person):
        for key, value in person.days.items():
            self.days[key] = value

    def getDay(self, dayNum):
        return self.days[str(dayNum)]

    def getDays(self):
        return self.days

    def scrape(self, weekDiv, weekDates):
        # Get all cells in a row
        cells = weekDiv.find_elements_by_tag_name('td')
        name = weekDiv.find_element_by_class_name('name').text

        # Prepare array of dates
        weekDates = sendDatesToArray(weekDates)

        # iterate over Week Days for a week
        for cell in cells:
            if cell.get_attribute('class') != 'control-cell':
                # Get the cell's weekDay Number
                dayNum = int(cell.get_attribute('data-wday'))
                dayNum = weekDates[dayNum]

                # Get the workday shift times and role
                try:
                    time = cell.find_element_by_class_name('time').text
                    role = cell.find_element_by_class_name('label-role').text
                except NoSuchElementException:
                    time = "No Time"
                    role = "Relax"

                # Add/replace this person's days dictionary with a Day object
                self.days[dayNum] = Day(dayNum, time, role)

        # Set name :)
        self.name = name
        return

    def __repr__(self):
        retVal = self.name + "\n"
        for key, value in self.days.items():
            retVal += "Key: " + str(key)
            retVal += "\t\t " + str(value) + "\n"
        return retVal


class Day:
    def __init__(self, dayNum, time, role):
        self.start = None
        self.end = None
        self.day = dayNum
        self.time = time
        self.role = role
        if role.find('UNIFIX2') != -1:
            self.title = "Winter Park"
            self.location = "501 N Orlando Ave #237, Winter Park, FL 32789"
        else:
            self.title = "Orlando"
            self.location = "5695 Vineland Rd, Orlando, FL 32819"
        self.splitTime()

    def splitTime(self):
        if self.time != "No Time":
            times = self.time.split(' - ')
            self.start = times[0]
            self.end = times[1]
        else:
            self.start = None
            self.end = None

    def __repr__(self):
        return "Day: " + str(self.day) + "\tTime: " + self.time + "\tRole: " + self.role


def sendTo24Hr(time):
    hour = ''
    mins = ''
    setHour = True
    for char in time:
        if char == 'A':
            if mins == '':
                return hour, str(0)
            else:
                return hour, mins
        elif char == 'P':
            if mins == '':
                return str(int(hour)+12), str(0)
            else:
                return str(int(hour)+12), mins
        if char == ':':
            setHour = False
        else:
            if setHour:
                hour += char
            else:
                mins += char
    return None


def convertTime(time, day):
    curTime = datetime.utcnow() + timedelta(hours=-4)
    day = int(day.day)
    time = sendTo24Hr(time)

    # Account for the week containing days from 2 months
    if curTime.day > day:
        if day+14 < curTime.day:  # Month ahead
            retVal = datetime(curTime.year, curTime.month + 1, day, int(time[0]), int(time[1]), 0)
        else:
            retVal = None  # This day has already passed
    else:
        if curTime.day > day - 14:
            retVal = datetime(curTime.year, curTime.month, day, int(time[0]), int(time[1]), 0)
        else:  # Day that has already passed
            retVal = None
    return retVal


class PersonManager:
    def __init__(self, people):
        self.people = {}
        for p in people:
            self.people[p.name] = p

        # Get today's date
        date = datetime.utcnow() + timedelta(hours=-4)
        self.todayDate = date.day

    def combine(self, personManager):
        for key, value in self.people.items():
            # Value = Person object
            value.combine(personManager.people[key])

    def getEventsByName(self, name):
        return self._getEventsByName(self.people[name])

    def getNames(self):
        retVal = []
        for key, val in self.people.items():
            retVal.append(key)
        return retVal

    # This method creates a Google Event!
    def _getEventsByName(self, person):
        days = person.days
        retVal = []
        for key, value in days.items():
            # These are the days I have off
            if value.start is None:
                continue

            start = convertTime(value.start, value)

            # This means we won't update old days that have already passed
            if start is None:
                continue

            end = convertTime(value.end, value)

            retVal.append(Event(value.title + " ~ Unifix", start, end, value.location))
        return retVal

    def __repr__(self):
        retVal = ''
        for key, value in self.people.items():
            p = self.people[key]
            retVal += str(p) + "\n"
        return retVal
