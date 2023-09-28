from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

class BatteryWidget(BoxLayout):
    def __init__(self, number, capacity, comment, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.number = number
        self.capacity = capacity
        self.comment = comment
        self.add_widget(Label(text=self.number))
        self.add_widget(Button(text=">", on_press=self.move_right))
        self.add_widget(Button(text="<", on_press=self.move_left))
        self.add_widget(Button(text="Podgląd", on_press=self.show_details))

    def move_right(self, instance):
        current_tab = self.parent
        next_tab = current_tab.next
        if next_tab:
            current_tab.remove_widget(self)
            next_tab.content.add_widget(self)

    def move_left(self, instance):
        current_tab = self.parent
        prev_tab = current_tab.prev
        if prev_tab:
            current_tab.remove_widget(self)
            prev_tab.content.add_widget(self)

    def show_details(self, instance):
        details = f"Numer: {self.number}\nPojemność: {self.capacity}\nKomentarz: {self.comment}"
        popup = Popup(title="Szczegóły akumulatora", content=Label(text=details), size_hint=(0.7, 0.7))
        popup.open()

class BatteryApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        tabs = TabbedPanel(do_default_tab=False)
        
        # Zakładki
        self.charged_tab = TabbedPanelItem(text="Naładowane", content=BoxLayout())
        self.discharged_tab = TabbedPanelItem(text="Rozładowane", content=BoxLayout())
        self.to_charge_tab = TabbedPanelItem(text="Do naładowania", content=BoxLayout())
        self.working_tab = TabbedPanelItem(text="Na robocie", content=BoxLayout())
        
        # Ustawienie kolejności zakładek
        self.tab_order = [self.charged_tab, self.discharged_tab, self.to_charge_tab, self.working_tab]
        
        for tab in self.tab_order:
            tabs.add_widget(tab)
        
        # Pasek narzędzi z przyciskiem "Dodaj akumulator"
        toolbar = BoxLayout(size_hint=(1, 0.1))
        add_button = Button(text="Dodaj akumulator")
        add_button.bind(on_press=self.show_popup)
        toolbar.add_widget(add_button)
        
        layout.add_widget(tabs)
        layout.add_widget(toolbar)
        
        return layout

    def show_popup(self, instance):
        # Okno popup do dodawania akumulatora
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(Label(text="Numer akumulatora:"))
        battery_number = TextInput()
        popup_layout.add_widget(battery_number)
        
        popup_layout.add_widget(Label(text="Pojemność:"))
        capacity = Spinner(text="Wybierz pojemność", values=('100', '200', '220', '150'))
        popup_layout.add_widget(capacity)
        
        popup_layout.add_widget(Label(text="Komentarz:"))
        comment = TextInput()
        popup_layout.add_widget(comment)
        
        submit_button = Button(text="Dodaj")
        submit_button.bind(on_press=lambda x: self.add_battery(battery_number.text, capacity.text, comment.text))
        popup_layout.add_widget(submit_button)
        
        popup = Popup(title="Dodaj akumulator", content=popup_layout, size_hint=(0.7, 0.7))
        popup.open()

    def add_battery(self, battery_number, capacity, comment):
        battery = BatteryWidget(battery_number, capacity, comment, app=self)
        self.to_charge_tab.content.add_widget(battery)

class BatteryWidget(BoxLayout):
    def __init__(self, number, capacity, comment, app, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.number = number
        self.capacity = capacity
        self.comment = comment
        self.app = app
        self.add_widget(Label(text=self.number))
        self.add_widget(Button(text=">", on_press=self.move_right))
        self.add_widget(Button(text="<", on_press=self.move_left))
        self.add_widget(Button(text="Podgląd", on_press=self.show_details))

    def move_right(self, instance):
        current_tab = self.parent.parent
        idx = self.app.tab_order.index(current_tab)
        if idx < len(self.app.tab_order) - 1:
            next_tab = self.app.tab_order[idx + 1]
            current_tab.content.remove_widget(self)
            next_tab.content.add_widget(self)

    def move_left(self, instance):
        current_tab = self.parent.parent
        idx = self.app.tab_order.index(current_tab)
        if idx > 0:
            prev_tab = self.app.tab_order[idx - 1]
            current_tab.content.remove_widget(self)
            prev_tab.content.add_widget(self)

    def show_details(self, instance):
        details = f"Numer: {self.number}\nPojemność: {self.capacity}\nKomentarz: {self.comment}"
        popup = Popup(title="Szczegóły akumulatora", content=Label(text=details), size_hint=(0.8, 0.8))
        popup.open()

if __name__ == "__main__":
    BatteryApp().run()
