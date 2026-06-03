from kivy.uix.screenmanager import Screen
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
