from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from OldMain import scrapeItTime


class MainApp(App):
    def build(self):
        return AppLayout()


class AppLayout(GridLayout):
    def __init__(self, **kwargs):
        super(AppLayout, self).__init__(**kwargs)
        self.rows = 3

        # Title bar
        self.title = Label(text="HomeBase -> Google Calendar")
        self.add_widget(self.title)

        # Button
        self.doIt = False
        self.inside = None
        self.start = None
        self.buttonObject()

        # Bottom text
        self.text = Label(text=" ")
        self.add_widget(self.text)

    def buttonObject(self):
        self.inside = GridLayout()
        self.inside.cols = 3
        self.inside.add_widget(Label(text=''))
        self.start = Button(text="Begin")
        self.start.bind(on_press=self.pressed)
        self.inside.add_widget(self.start)
        self.inside.add_widget(Label(text=''))
        self.add_widget(self.inside)

    def pressed(self, instance):
        # Update our text Accordingly
        self.text.text = "Finished!"

        # Scrape Bool
        scrapeItTime()


if __name__ == "__main__":
    MainApp().run()

