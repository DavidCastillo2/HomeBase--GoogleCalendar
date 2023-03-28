from HomeBase.HomeBaseCalendar import CalendarGrabber
from HomeBase.Scraper import HomeBaseBrowser


class HomeBase:
    def __init__(self):
        self.weeks = []
        self.thisweek = []
        self.usefullWeeks = []
        self.HomeBaseBrowser = HomeBaseBrowser()
        self.PersonManager = None

    def scrapeNextWeek(self):
        # Click on the next button
        self.HomeBaseBrowser.nextWeek()

        # Scrape our results
        cg = CalendarGrabber(self.HomeBaseBrowser.driver)
        personManger = cg.getData()

        # Combine ;)
        self.PersonManager.combine(personManger)

    def scrapeWeek(self):
        cg = CalendarGrabber(self.HomeBaseBrowser.driver)
        self.PersonManager = cg.getData()

    def getNames(self):
        if self.PersonManager is None:
            return None
        else:
            return self.PersonManager.getNames()

    def exit(self):
        self.HomeBaseBrowser.driver.close()
