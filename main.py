from kivy.app import App
from ui.ui_logic import build_screen_manager

class TesoePopApp(App):
    def build(self):
        self.title = "Tesoe Pop - Prototipo Oficial"
        return build_screen_manager()

if __name__ == '__main__':
    TesoePopApp().run()
