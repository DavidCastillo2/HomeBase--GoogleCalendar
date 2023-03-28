from GoogleCalendar.CalendarManager import CalendarManager
from HomeBase.HomeBase import HomeBase


'''
This was made to be super modular, easy to extend the classes I already made. This can be used to easily
make this work for a host of users and be run and auto check for updates to HomeBase and google calendar and such

Main sticking points: 
    A method in the Person.py file called convertTime(time, day) is also used to see if an event is too far
    away from the current day (14 days away = doesn't add).
    
    Month is never scrapped. This is also a possible solution to the above problem.
'''


def scrapeItTime():
    # Logs in and sends chrome to calendar page
    homeDriver = HomeBase()

    # Scout 3 weeks worth of the homeBase calendar
    homeDriver.scrapeWeek()
    print("Page 1 Done")
    homeDriver.scrapeNextWeek()
    print("Page 2 Done")
    homeDriver.scrapeNextWeek()  # Probably useless since the calendar doesn't go that far
    print("Page 3 Done\n")

    # Yeet these work days to Google Calendar
    cm = CalendarManager()
    cm.updateCalendar(homeDriver, "David C.")

    # Exit and cleanup
    homeDriver.exit()
    print("End reached!")

