from datetime import datetime

from selenium.common.exceptions import NoSuchElementException

from People.Person import Person, PersonManager


class CalendarGrabber:
    calendarID = 'schedule-builder'

    def __init__(self, d):
        self.driver = d
        # Get today's date
        datetime.utcnow()
        self.todayDate = -1

    def waitLoad(self, pathToDiv, textOfDiv=None):
        stopBool = False
        while not stopBool:
            try:
                div = self.driver.find_element_by_xpath(pathToDiv)
                if textOfDiv == div.text or textOfDiv is None:
                    stopBool = True
            except NoSuchElementException:
                continue
        return

    def getData(self):
        weekDates = self.getWeekDates()
        staffDivs = self.driver.find_elements_by_class_name('user-body')
        people = []
        for staffWeek in staffDivs:
            people.append(Person(staffWeek, weekDates))
        return PersonManager(people)

    # Returns dictionary of retVal[Weekday] = DayNumber
    def getWeekDates(self):
        retVal = {}
        calendarDiv = self.loadCalendar()  # Fully load calendar

        # Get calendar Data
        weekDatesXpath = '/html/body/div[1]/div/div[6]/div[1]/div/div/div[2]/div[2]/table[2]/thead/tr'
        for i in range(1, 9):
            try:
                # Get Div with Date and DayNum
                divXPath = weekDatesXpath + "/th[" + str(i) + ']'
                dateDiv = self.driver.find_element_by_xpath(divXPath)

                weekDay = dateDiv.find_element_by_xpath(divXPath + '/a/div[1]').text

                numDay = dateDiv.find_element_by_xpath(divXPath + '/a/div[2]').text
                retVal[weekDay] = numDay
            except NoSuchElementException:
                # This is for the divs in this row that don't have dates
                continue

        return retVal

    def loadCalendar(self):
        weekDatesXpath = '/html/body/div[1]/div/div[6]/div[1]/div/div/div[2]/div[2]/table[2]/thead/tr'

        # load calendar
        self.waitLoad(weekDatesXpath)
        # Load all of calendar - Probably want to clean this part up
        self.waitLoad('/html/body/div[1]/div/div[6]/div[1]/div/div/div[2]/div[2]/table[2]/tbody[2]/tr/td[6]')

        return self.driver.find_element_by_xpath(weekDatesXpath)





