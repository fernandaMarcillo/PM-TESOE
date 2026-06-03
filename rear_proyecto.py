import os

# Estructura corregida con contraste de color (Café chocolate), Filtro de Categorías y Perfil Dinámico
estructura_proyecto = {
    # MÓDULO LOGIN
    "login/__init__.py": "",
    "login/login_logic.py": '''from kivy.uix.screenmanager import Screen
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
        self.label_user.text = f"Nombre: {CURRENT_USER['username']}\\nEstado: Miembro Activo ✨"

    def logout(self, instance):
        CURRENT_USER["username"] = "Invitado"
        self.manager.current = 'login'
''',

    # MÓDULO PRODUCTOS (CON CATEGORÍAS FILTRABLES)
    "products/__init__.py": "",
    "products/products_logic.py": '''from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage

PRODUCTS_LIST = [
    {"id": 1, "name": "Torta de Fresa", "price": 15.0, "category": "Tortas", "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400"},
    {"id": 2, "name": "Donas Glaseadas", "price": 2.5, "category": "Donas", "img": "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=400"},
    {"id": 3, "name": "Brownie con Nuez", "price": 3.0, "category": "Brownies", "img": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400"},
    {"id": 4, "name": "Cupcake Vainilla", "price": 2.0, "category": "Cupcakes", "img": "https://images.unsplash.com/photo-1576618148400-f54bed99fcfd?w=400"},
    {"id": 5, "name": "Galletas Chispas", "price": 1.5, "category": "Galletas", "img": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400"}
]

SELECTED_PRODUCT = {}
CATEGORIA_ACTUAL = "Todas"

class CatalogScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Barra Superior
        nav_bar = BoxLayout(size_hint_y=0.08, spacing=5)
        btn_profile = Button(text="👤 Mi Perfil", background_color=(0.8, 0.7, 0.6, 1))
        btn_profile.bind(on_press=lambda x: self.go_profile())
        btn_cart = Button(text="🛒 Ver Carrito", background_color=(0.9, 0.6, 0.7, 1))
        btn_cart.bind(on_press=lambda x: setattr(self.manager, 'current', 'cart'))
        nav_bar.add_widget(btn_profile)
        nav_bar.add_widget(btn_cart)
        main_layout.add_widget(nav_bar)
        
        # FILTRO DE CATEGORÍAS (Persona 2)
        categoria_layout = BoxLayout(size_hint_y=0.08, spacing=4)
        categorias = ["Todas", "Tortas", "Donas", "Brownies", "Cupcakes", "Galletas"]
        for cat in categorias:
            btn_cat = Button(text=cat, font_size=11, background_color=(0.85, 0.75, 0.7, 1))
            btn_cat.bind(on_press=lambda inst, c=cat: self.filtrar_por_categoria(c))
            categoria_layout.add_widget(btn_cat)
        main_layout.add_widget(categoria_layout)
        
        # ScrollView del Catálogo
        scroll = ScrollView()
        product_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        product_layout.bind(minimum_height=product_layout.setter('height'))
        
        global CATEGORIA_ACTUAL
        for prod in PRODUCTS_LIST:
            # Si no coincide con el filtro, saltar este producto
            if CATEGORIA_ACTUAL != "Todas" and prod["category"] != CATEGORIA_ACTUAL:
                continue
                
            item_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=120, spacing=10)
            img = AsyncImage(source=prod["img"], size_hint_x=0.35)
            
            details = BoxLayout(orientation='vertical', padding=5)
            details.add_widget(Label(text=prod["name"], font_size=18, color=(0.3, 0.15, 0.05, 1), bold=True))
            details.add_widget(Label(text=f"Precio: ${prod['price']}", font_size=14, color=(0.4, 0.2, 0.1, 1)))
            details.add_widget(Label(text=f"Cat: {prod['category']}", font_size=12, color=(0.6, 0.4, 0.3, 1)))
            
            btn_view = Button(text="Ver", size_hint_x=0.2, background_color=(0.9, 0.6, 0.7, 1))
            btn_view.bind(on_press=lambda instance, p=prod: self.view_details(p))
            
            item_box.add_widget(img)
            item_box.add_widget(details)
            item_box.add_widget(btn_view)
            product_layout.add_widget(item_box)
            
        scroll.add_widget(product_layout)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def filtrar_por_categoria(self, categoria):
        global CATEGORIA_ACTUAL
        CATEGORIA_ACTUAL = categoria
        self.on_enter()

    def view_details(self, product):
        global SELECTED_PRODUCT
        SELECTED_PRODUCT.update(product)
        self.manager.current = 'product_detail'
        
    def go_profile(self):
        self.manager.get_screen('profile').update_profile()
        self.manager.current = 'profile'

class ProductDetailScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        if SELECTED_PRODUCT:
            layout.add_widget(Label(text=SELECTED_PRODUCT["name"], font_size=26, color=(0.3, 0.15, 0.05, 1), bold=True))
            layout.add_widget(AsyncImage(source=SELECTED_PRODUCT["img"], size_hint_y=0.4))
            layout.add_widget(Label(text=f"Categoría: {SELECTED_PRODUCT['category']}", font_size=16, color=(0.4, 0.2, 0.1, 1)))
            layout.add_widget(Label(text=f"Precio Unitario: ${SELECTED_PRODUCT['price']}", font_size=20, color=(0.3, 0.15, 0.05, 1)))
            
            btn_add = Button(text="Agregar al Carrito", background_color=(0.4, 0.8, 0.4, 1), size_hint_y=0.15)
            btn_add.bind(on_press=self.add_to_cart)
            layout.add_widget(btn_add)
            
        btn_back = Button(text="Volver al catálogo", size_hint_y=0.1, background_color=(0.8, 0.7, 0.6, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def add_to_cart(self, instance):
        from cart.cart_logic import CART_ITEMS
        CART_ITEMS.append(SELECTED_PRODUCT.copy())
        self.manager.current = 'cart'
''',

    # MÓDULO CARRITO
    "cart/__init__.py": "",
    "cart/cart_logic.py": '''from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

CART_ITEMS = []
ORDERS_PREPARED = []

class CartScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self.main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        self.main_layout.add_widget(Label(text="Tu Carrito de Compras 🛒", font_size=22, color=(0.3, 0.15, 0.05, 1), size_hint_y=0.1, bold=True))
        
        scroll = ScrollView()
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        
        total_price = 0.0
        for idx, item in enumerate(CART_ITEMS):
            total_price += item['price']
            item_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            item_box.add_widget(Label(text=item['name'], color=(0.3, 0.15, 0.05, 1)))
            item_box.add_widget(Label(text=f"${item['price']}", color=(0.4, 0.2, 0.1, 1)))
            
            btn_delete = Button(text="❌", size_hint_x=0.2, background_color=(0.8, 0.3, 0.3, 1))
            btn_delete.bind(on_press=lambda instance, i=idx: self.remove_item(i))
            item_box.add_widget(btn_delete)
            self.list_layout.add_widget(item_box)
            
        scroll.add_widget(self.list_layout)
        self.main_layout.add_widget(scroll)
        
        self.label_total = Label(text=f"Total a Pagar: ${total_price:.2f}", font_size=18, color=(0.3, 0.15, 0.05, 1), size_hint_y=0.1, bold=True)
        self.main_layout.add_widget(self.label_total)
        
        actions = BoxLayout(size_hint_y=0.15, spacing=10)
        btn_back = Button(text="Seguir Comprando", background_color=(0.8, 0.7, 0.6, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        
        btn_checkout = Button(text="Realizar Pedido", background_color=(0.4, 0.7, 0.9, 1))
        btn_checkout.bind(on_press=lambda x: self.checkout(total_price))
        
        actions.add_widget(btn_back)
        if CART_ITEMS:
            actions.add_widget(btn_checkout)
            
        self.main_layout.add_widget(actions)
        self.add_widget(self.main_layout)

    def remove_item(self, index):
        CART_ITEMS.pop(index)
        self.on_enter()

    def checkout(self, total):
        global CART_ITEMS
        if CART_ITEMS:
            from login.login_logic import CURRENT_USER
            pedido = {
                "usuario": CURRENT_USER["username"],
                "productos": [item['name'] for item in CART_ITEMS],
                "total": total
            }
            ORDERS_PREPARED.append(pedido)
            CART_ITEMS.clear()
            self.manager.current = 'order_summary'

class OrderSummaryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="¡Pedido Realizado con Éxito! 🎉", font_size=24, color=(0.2, 0.6, 0.2, 1), bold=True))
        layout.add_widget(Label(text="Tu postre se está preparando en la cocina de Tesoe Pop.", font_size=16, color=(0.3, 0.15, 0.05, 1)))
        
        btn_finish = Button(text="Volver al Catálogo", background_color=(0.9, 0.6, 0.7, 1), size_hint_y=0.2)
        btn_finish.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        layout.add_widget(btn_finish)
        self.add_widget(layout)
''',

    # MÓDULO ADMINISTRADOR
    "admin/__init__.py": "",
    "admin/admin_logic.py": '''from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from products.products_logic import PRODUCTS_LIST
from cart.cart_logic import ORDERS_PREPARED

class AdminPanelScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout.add_widget(Label(text="Panel de Administración 🛠️", font_size=22, color=(0.3, 0.15, 0.05, 1), bold=True))
        
        layout.add_widget(Label(text="Agregar Nuevo Producto:", font_size=14, color=(0.4, 0.2, 0.1, 1)))
        self.name_in = TextInput(hint_text="Nombre del postre", multiline=False)
        self.price_in = TextInput(hint_text="Precio (Ej: 4.50)", multiline=False)
        layout.add_widget(self.name_in)
        layout.add_widget(self.price_in)
        
        btn_add = Button(text="Guardar Producto", background_color=(0.4, 0.7, 0.4, 1))
        btn_add.bind(on_press=self.add_product_admin)
        layout.add_widget(btn_add)
        
        layout.add_widget(Label(text="Pedidos Recibidos de Clientes:", font_size=16, color=(0.3, 0.15, 0.05, 1), bold=True))
        scroll = ScrollView()
        orders_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        orders_layout.bind(minimum_height=orders_layout.setter('height'))
        
        for order in ORDERS_PREPARED:
            txt = f"Cliente: {order['usuario']} | {', '.join(order['productos'])} | Total: ${order['total']}"
            orders_layout.add_widget(Label(text=txt, size_hint_y=None, height=30, color=(0.2, 0.2, 0.2, 1)))
            
        scroll.add_widget(orders_layout)
        layout.add_widget(scroll)
        
        btn_logout = Button(text="Salir de Admin", background_color=(0.7, 0.2, 0.2, 1))
        btn_logout.bind(on_press=self.logout)
        layout.add_widget(btn_logout)
        self.add_widget(layout)

    def add_product_admin(self, instance):
        if self.name_in.text and self.price_in.text:
            try:
                new_p = {
                    "id": len(PRODUCTS_LIST) + 1,
                    "name": self.name_in.text,
                    "price": float(self.price_in.text),
                    "category": "Reposteria",
                    "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400"
                }
                PRODUCTS_LIST.append(new_p)
                self.name_in.text = ""
                self.price_in.text = ""
                self.on_enter()
            except ValueError:
                self.price_in.text = "Precio Inválido"

    def logout(self, instance):
        from login.login_logic import CURRENT_USER
        CURRENT_USER["username"] = "Invitado"
        self.manager.current = 'login'
''',

    # MÓDULO UI / DISEÑO GENERAL
    "ui/__init__.py": "",
    "ui/ui_logic.py": '''from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from login.login_logic import LoginScreen, RegisterScreen, ProfileScreen
from products.products_logic import CatalogScreen, ProductDetailScreen
from cart.cart_logic import CartScreen, OrderSummaryScreen
from admin.admin_logic import AdminPanelScreen

def aplicar_estilos_pastel():
    Window.clearcolor = (0.98, 0.95, 0.92, 1)

def build_screen_manager():
    aplicar_estilos_pastel()
    sm = ScreenManager()
    
    sm.add_widget(LoginScreen(name='login'))
    sm.add_widget(RegisterScreen(name='register'))
    sm.add_widget(ProfileScreen(name='profile'))
    sm.add_widget(CatalogScreen(name='catalog'))
    sm.add_widget(ProductDetailScreen(name='product_detail'))
    sm.add_widget(CartScreen(name='cart'))
    sm.add_widget(OrderSummaryScreen(name='order_summary'))
    sm.add_widget(AdminPanelScreen(name='admin_panel'))
    
    return sm
''',

    # ARCHIVO MAIN
    "main.py": '''from kivy.app import App
from ui.ui_logic import build_screen_manager

class TesoePopApp(App):
    def build(self):
        self.title = "Tesoe Pop - Panadería & Postres"
        return build_screen_manager()

if __name__ == '__main__':
    TesoePopApp().run()
'''
}

print("🏗️ Re-estructurando proyecto Tesoe Pop con letras visibles y filtros...")
for ruta, contenido in estructura_proyecto.items():
    directorio = os.path.dirname(ruta)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
print("🎉 ¡Proyecto corregido! Borra este script e inicia con: python main.py")