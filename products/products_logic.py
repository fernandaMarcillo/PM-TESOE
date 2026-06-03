from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from cart.cart_logic import ORDERS_PREPARED
from login.login_logic import CURRENT_USER

PRODUCTS_LIST = [
    {"id": 1, "name": "Torta de Fresa", "price": 15.0, "category": "Tortas", "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400"},
    {"id": 2, "name": "Torta de Chocolate", "price": 16.5, "category": "Tortas", "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400"},
    {"id": 6, "name": "Donas Glaseadas", "price": 2.5, "category": "Donas", "img": "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=400"},
    {"id": 7, "name": "Dona de Nutella", "price": 3.0, "category": "Donas", "img": "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=400"},
    {"id": 11, "name": "Brownie con Nuez", "price": 3.0, "category": "Brownies", "img": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400"},
    {"id": 16, "name": "Cupcake Vainilla", "price": 2.0, "category": "Cupcakes", "img": "https://images.unsplash.com/photo-1576618148400-f54bed99fcfd?w=400"},
    {"id": 17, "name": "Cupcake Oreo", "price": 2.5, "category": "Cupcakes", "img": "https://images.unsplash.com/photo-1576618148400-f54bed99fcfd?w=400"},
    {"id": 21, "name": "Galletas Chispas", "price": 1.5, "category": "Galletas", "img": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400"}
]

SELECTED_PRODUCT = {}
CATEGORIA_ACTUAL = "Todas"
TEXTO_BUSQUEDA = ""

class CatalogScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        nav_bar = BoxLayout(size_hint_y=0.08, spacing=5)
        btn_profile = Button(text="👤 Mi Perfil", background_color=(0.8, 0.7, 0.6, 1))
        btn_profile.bind(on_press=lambda x: self.go_profile())
        btn_cart = Button(text="🛒 Ver Carrito", background_color=(0.9, 0.6, 0.7, 1))
        btn_cart.bind(on_press=lambda x: setattr(self.manager, 'current', 'cart'))
        nav_bar.add_widget(btn_profile)
        nav_bar.add_widget(btn_cart)
        main_layout.add_widget(nav_bar)

        search_box = BoxLayout(size_hint_y=0.08, spacing=5)
        self.search_input = TextInput(hint_text="🔍 Buscar postre...", multiline=False)
        self.search_input.bind(text=self.actualizar_busqueda)
        search_box.add_widget(self.search_input)
        main_layout.add_widget(search_box)
        
        categoria_layout = BoxLayout(size_hint_y=0.08, spacing=4)
        categorias = ["Todas", "Tortas", "Donas", "Brownies", "Cupcakes", "Galletas"]
        for cat in categorias:
            btn_cat = Button(text=cat, font_size=11, background_color=(0.85, 0.75, 0.7, 1))
            btn_cat.bind(on_press=lambda inst, c=cat: self.filtrar_por_categoria(c))
            categoria_layout.add_widget(btn_cat)
        main_layout.add_widget(categoria_layout)
        
        scroll = ScrollView()
        product_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        product_layout.bind(minimum_height=product_layout.setter('height'))
        
        global CATEGORIA_ACTUAL, TEXTO_BUSQUEDA
        for prod in PRODUCTS_LIST:
            if CATEGORIA_ACTUAL != "Todas" and prod["category"] != CATEGORIA_ACTUAL:
                continue
            if TEXTO_BUSQUEDA.lower() not in prod["name"].lower():
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

    def actualizar_busqueda(self, instance, text):
        global TEXTO_BUSQUEDA
        TEXTO_BUSQUEDA = text
        self.on_enter()

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
        
        encontrado = False
        for item in CART_ITEMS:
            if item["id"] == SELECTED_PRODUCT["id"]:
                item["qty"] += 1
                encontrado = True
                break
        if not encontrado:
            nuevo_item = SELECTED_PRODUCT.copy()
            nuevo_item["qty"] = 1
            CART_ITEMS.append(nuevo_item)
            
        self.manager.current = 'cart'

class ClientOrdersScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout.add_widget(Label(text="📦 Mis Pedidos", font_size=24, bold=True, color=(0.3, 0.15, 0.05, 1), size_hint_y=0.1))

        scroll = ScrollView()
        orders_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        orders_layout.bind(minimum_height=orders_layout.setter('height'))
        
        mis_pedidos = [o for o in ORDERS_PREPARED if o['usuario'] == CURRENT_USER['username']]

        if not mis_pedidos:
            orders_layout.add_widget(Label(text="Aún no tienes pedidos registrados.", color=(0.5, 0.5, 0.5, 1)))
        else:
            for pedido in reversed(mis_pedidos):
                box = BoxLayout(orientation='vertical', size_hint_y=None, height=90, padding=5)
                # Detalle en string de una sola línea corregido
                detalles = f"Pedido #{pedido.get('id', 'N/A')} | Total: ${pedido['total']:.2f}\nMétodo: {pedido.get('metodo', 'N/A')}\nEstado: {pedido['status']}"
                box.add_widget(Label(text=detalles, color=(0.2, 0.2, 0.2, 1), halign='center'))
                box.add_widget(Button(background_color=(0.8, 0.7, 0.6, 1), size_hint_y=None, height=2, disabled=True))
                orders_layout.add_widget(box)

        scroll.add_widget(orders_layout)
        layout.add_widget(scroll)

        btn_back = Button(text="Volver al Perfil", size_hint_y=0.1, background_color=(0.8, 0.7, 0.6, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        layout.add_widget(btn_back)
        self.add_widget(layout)
