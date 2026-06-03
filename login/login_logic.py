import ssl
# Parche automático para evitar errores de certificados SSL al descargar imágenes de internet
ssl._create_default_https_context = ssl._create_unverified_context

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.clock import Clock

USERS_DB = {
    "admin": {"pass": "admin123", "email": "admin@tesoepop.com", "name": "Administrador General", "phone": "5512345678", "date": "01/06/2026", "level": "Staff"},
    "user": {"pass": "user123", "email": "cliente@gmail.com", "name": "Juan Pérez Alumno", "phone": "5587654321", "date": "02/06/2026", "level": "Cliente VIP ✨"}
}
CURRENT_USER = {"username": "Invitado", "email": "Invitado@mail.com", "name": "Invitado", "phone": "N/A", "date": "N/A", "level": "N/A"}

class SplashScreen(Screen):
    def on_enter(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(text="🧁 TESOE POP 🧁", font_size=36, color=(0.3, 0.15, 0.05, 1), bold=True))
        layout.add_widget(AsyncImage(source="https://cdn-icons-png.flaticon.com/512/3014/3014481.png", size_hint_y=0.5))
        self.loading_label = Label(text="Iniciando aplicación... 0%", font_size=16, color=(0.5, 0.3, 0.2, 1))
        layout.add_widget(self.loading_label)
        self.add_widget(layout)
        
        self.progress = 0
        Clock.schedule_interval(self.update_progress, 0.03)

    def update_progress(self, dt):
        self.progress += 2
        self.loading_label.text = f"Cargando módulos del sistema... {self.progress}%"
        if self.progress >= 100:
            Clock.unschedule(self.update_progress)
            self.manager.current = 'login'

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="¡Bienvenido a Tesoe Pop!", font_size=26, color=(0.3, 0.15, 0.05, 1), bold=True))
        
        self.username_input = TextInput(hint_text="Usuario o Correo Electrónico", multiline=False)
        self.password_input = TextInput(hint_text="Contraseña", password=True, multiline=False)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        
        btn_login = Button(text="Iniciar Sesión", background_color=(0.9, 0.6, 0.7, 1), font_size=16)
        btn_login.bind(on_press=self.verify_login)
        layout.add_widget(btn_login)
        
        btn_go_register = Button(text="¿No tienes cuenta? Regístrate aquí", background_color=(0.8, 0.7, 0.6, 1))
        btn_go_register.bind(on_press=self.go_to_register)
        layout.add_widget(btn_go_register)
        self.add_widget(layout)

    def verify_login(self, instance):
        input_data = self.username_input.text
        password = self.password_input.text
        
        found_user = None
        username_key = ""
        
        for u_key, u_data in USERS_DB.items():
            if input_data == u_key or input_data == u_data["email"]:
                if u_data["pass"] == password:
                    found_user = u_data
                    username_key = u_key
                    break
                    
        if found_user:
            CURRENT_USER.update({
                "username": username_key,
                "email": found_user["email"],
                "name": found_user["name"],
                "phone": found_user["phone"],
                "date": found_user["date"],
                "level": found_user["level"]
            })
            self.manager.get_screen('profile').update_profile()
            self.username_input.text = ""
            self.password_input.text = ""
            if username_key == "admin":
                self.manager.current = 'admin_panel'
            else:
                self.manager.current = 'catalog'
        else:
            self.password_input.text = ""
            self.username_input.hint_text = "Credenciales incorrectas. Reintente."

    def go_to_register(self, instance):
        self.manager.current = 'register'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=8)
        layout.add_widget(Label(text="Formulario de Registro", font_size=24, color=(0.3, 0.15, 0.05, 1), bold=True))
        
        self.reg_name = TextInput(hint_text="Nombre Completo", multiline=False)
        self.reg_email = TextInput(hint_text="Correo Electrónico", multiline=False)
        self.reg_phone = TextInput(hint_text="Teléfono Celular", multiline=False)
        self.reg_user = TextInput(hint_text="Nombre de Usuario", multiline=False)
        self.reg_pass = TextInput(hint_text="Contraseña", password=True, multiline=False)
        
        layout.add_widget(self.reg_name)
        layout.add_widget(self.reg_email)
        layout.add_widget(self.reg_phone)
        layout.add_widget(self.reg_user)
        layout.add_widget(self.reg_pass)
        
        btn_register = Button(text="Crear Nueva Cuenta", background_color=(0.4, 0.7, 0.4, 1))
        btn_register.bind(on_press=self.save_user)
        layout.add_widget(btn_register)
        
        btn_back = Button(text="Volver al Login", background_color=(0.6, 0.6, 0.6, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def save_user(self, instance):
        if self.reg_user.text and self.reg_pass.text and self.reg_email.text:
            USERS_DB[self.reg_user.text] = {
                "pass": self.reg_pass.text,
                "email": self.reg_email.text,
                "name": self.reg_name.text if self.reg_name.text else self.reg_user.text,
                "phone": self.reg_phone.text if self.reg_phone.text else "N/A",
                "date": "02/06/2026",
                "level": "Cliente Regular"
            }
            self.manager.current = 'login'

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=5)
        
        self.layout.add_widget(Label(text="Perfil de Usuario", font_size=24, color=(0.3, 0.15, 0.05, 1), bold=True))
        self.layout.add_widget(AsyncImage(source="https://cdn-icons-png.flaticon.com/512/3135/3135715.png", size_hint_y=0.25))
        
        self.lbl_name = Label(text="", font_size=16, color=(0.3, 0.15, 0.05, 1))
        self.lbl_user = Label(text="", font_size=14, color=(0.4, 0.2, 0.1, 1))
        self.lbl_email = Label(text="", font_size=14, color=(0.4, 0.2, 0.1, 1))
        self.lbl_phone = Label(text="", font_size=14, color=(0.4, 0.2, 0.1, 1))
        self.lbl_date = Label(text="", font_size=12, color=(0.5, 0.4, 0.3, 1))
        self.lbl_level = Label(text="", font_size=14, color=(0.2, 0.5, 0.2, 1), bold=True)
        
        self.layout.add_widget(self.lbl_name)
        self.layout.add_widget(self.lbl_user)
        self.layout.add_widget(self.lbl_email)
        self.layout.add_widget(self.lbl_phone)
        self.layout.add_widget(self.lbl_date)
        self.layout.add_widget(self.lbl_level)
        
        btn_orders = Button(text="📦 Ver Mis Pedidos", background_color=(0.3, 0.6, 0.9, 1), size_hint_y=0.15)
        btn_orders.bind(on_press=self.go_to_orders)
        self.layout.add_widget(btn_orders)
        
        btn_logout = Button(text="Cerrar Sesión", background_color=(0.7, 0.2, 0.2, 1), size_hint_y=0.1)
        btn_logout.bind(on_press=self.logout)
        self.layout.add_widget(btn_logout)
        
        btn_back = Button(text="Volver al Catálogo", background_color=(0.8, 0.7, 0.6, 1), size_hint_y=0.1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        self.layout.add_widget(btn_back)
        self.add_widget(self.layout)

    def update_profile(self):
        self.lbl_name.text = f"Nombre: {CURRENT_USER['name']}"
        self.lbl_user.text = f"Usuario: @{CURRENT_USER['username']}"
        self.lbl_email.text = f"Correo: {CURRENT_USER['email']}"
        self.lbl_phone.text = f"Teléfono: {CURRENT_USER['phone']}"
        self.lbl_date.text = f"Miembro desde: {CURRENT_USER['date']}"
        self.lbl_level.text = f"Rango: {CURRENT_USER['level']}"

    def go_to_orders(self, instance):
        self.manager.get_screen('client_orders').on_enter()
        self.manager.current = 'client_orders'

    def logout(self, instance):
        CURRENT_USER.update({"username": "Invitado"})
        self.manager.current = 'login'
