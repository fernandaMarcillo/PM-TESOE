from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage

USERS_DB = {"admin": "admin123", "user": "user123"}
CURRENT_USER = {"username": "Invitado"}

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="¡Bienvenido a Tesoe Pop!", font_size=26, color=(0.3, 0.15, 0.05, 1), bold=True))
        
        self.username_input = TextInput(hint_text="Usuario", multiline=False)
        self.password_input = TextInput(hint_text="Contraseña", password=True, multiline=False)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        
        btn_login = Button(text="Iniciar Sesión", background_color=(0.9, 0.6, 0.7, 1), font_size=16)
        btn_login.bind(on_press=self.verify_login)
        layout.add_widget(btn_login)
        
        btn_go_register = Button(text="¿No tienes cuenta? Regístrate", background_color=(0.8, 0.7, 0.6, 1))
        btn_go_register.bind(on_press=self.go_to_register)
        layout.add_widget(btn_go_register)
        self.add_widget(layout)

    def verify_login(self, instance):
        user = self.username_input.text
        password = self.password_input.text
        if user in USERS_DB and USERS_DB[user] == password:
            CURRENT_USER["username"] = user
            self.manager.get_screen('profile').update_profile()
            if user == "admin":
                self.manager.current = 'admin_panel'
            else:
                self.manager.current = 'catalog'
        else:
            self.username_input.text = ""
            self.password_input.text = ""
            self.username_input.hint_text = "Datos Incorrectos. Reintente."

    def go_to_register(self, instance):
        self.manager.current = 'register'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="Registro de Usuario", font_size=24, color=(0.3, 0.15, 0.05, 1), bold=True))
        
        self.new_user = TextInput(hint_text="Nuevo Usuario", multiline=False)
        self.new_pass = TextInput(hint_text="Nueva Contraseña", password=True, multiline=False)
        layout.add_widget(self.new_user)
        layout.add_widget(self.new_pass)
        
        btn_register = Button(text="Crear Cuenta", background_color=(0.9, 0.6, 0.7, 1))
        btn_register.bind(on_press=self.save_user)
        layout.add_widget(btn_register)
        self.add_widget(layout)

    def save_user(self, instance):
        if self.new_user.text and self.new_pass.text:
            USERS_DB[self.new_user.text] = self.new_pass.text
            self.manager.current = 'login'

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.label_title = Label(text="Perfil de Usuario", font_size=24, color=(0.3, 0.15, 0.05, 1), bold=True)
        self.layout.add_widget(self.label_title)
        
        self.label_user = Label(text="", font_size=18, color=(0.4, 0.2, 0.1, 1))
        self.layout.add_widget(self.label_user)
        
        self.layout.add_widget(AsyncImage(source="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"))
        
        btn_logout = Button(text="Cerrar Sesión", background_color=(0.7, 0.2, 0.2, 1))
        btn_logout.bind(on_press=self.logout)
        self.layout.add_widget(btn_logout)
        
        btn_back = Button(text="Volver al Catálogo", background_color=(0.8, 0.7, 0.6, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        self.layout.add_widget(btn_back)
        self.add_widget(self.layout)

    def update_profile(self):
        self.label_user.text = f"Nombre: {CURRENT_USER['username']}\nEstado: Miembro Activo ✨"

    def logout(self, instance):
        CURRENT_USER["username"] = "Invitado"
        self.manager.current = 'login'
