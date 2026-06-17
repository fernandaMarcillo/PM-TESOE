from kivy.app import App
from ui.ui_logic import build_screen_manager

class TesoePopApp(App):
    def build(self):
        # Configuración de metadatos de la ventana principal
        self.title = "Tesoe Pop - Prototipo Oficial"
        
        # URL directa para el ícono de la aplicación (asíncrono por red)
        self.icon = "https://cdn-icons-png.flaticon.com/512/3014/3014481.png"
        
        # Retorna el ScreenManager completamente estilizado y unificado
        return build_screen_manager()

if __name__ == '__main__':
    TesoePopApp().run()