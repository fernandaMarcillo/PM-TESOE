import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle, RoundedRectangle
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

# --- COMPONENTES VISUALES MODERNOS CON ICONOS REALES ---

class CatalogButton(Button):
    """Botón base plano con bordes redondeados regulables"""
    def __init__(self, bg_color=(0.9, 0.55, 0.65, 1), text_color=(1, 1, 1, 1), radius=[10], **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = text_color
        self.bold = True
        self.font_size = 13
        self.font_name = "Roboto"
        self.custom_bg = bg_color
        self.radius = radius
        
        with self.canvas.before:
            Color(*self.custom_bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


class PremiumIconButton(BoxLayout):
    """Botón que fusiona un ícono real transparente con texto opcional"""
    def __init__(self, text="", icon_url="", bg_color=(0.4, 0.25, 0.15, 1), text_color=(1, 1, 1, 1), radius=[10], on_press_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = (12, 6, 12, 6)
        self.spacing = 6
        
        # Base clicable transparente
        self.btn = Button(background_normal='', background_color=(0,0,0,0))
        if on_press_callback:
            self.btn.bind(on_press=on_press_callback)
            
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Imagen real del icono
        self.icon_img = AsyncImage(source=icon_url, size_hint_x=0.3 if text else 1, allow_stretch=True, keep_ratio=True)
        self.add_widget(self.icon_img)
        
        if text:
            self.lbl = Label(text=text, color=text_color, font_name="Roboto", bold=True, font_size=13, size_hint_x=0.7)
            self.add_widget(self.lbl)
            
        self.add_widget(self.btn)
        self.btn.bind(pos=self.sync_trigger, size=self.sync_trigger)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def sync_trigger(self, instance, value):
        # Mantiene el área del botón mapeada exactamente al contenedor
        self.btn.pos = self.pos
        self.btn.size = self.size


class CardContainer(BoxLayout):
    """Contenedor de tarjeta blanca suave para albergar elementos del catálogo"""
    def __init__(self, bg_color=(1, 1, 1, 1), radius=[10], **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ModernTextInput(TextInput):
    """Caja de texto moderna con esquinas redondeadas en su renderizado"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0, 0, 0, 0)
        self.font_name = "Roboto"
        self.cursor_color = (0.4, 0.25, 0.15, 1)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


# --- PANTALLAS ---

class CatalogScreen(Screen):
    def on_enter(self):
        global CATEGORIA_ACTUAL, TEXTO_BUSQUEDA
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.98, 0.96, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        main_layout = BoxLayout(orientation='vertical', padding=14, spacing=10)
        
        # Navbar Superior utilizando iconos reales
        nav_bar = BoxLayout(size_hint_y=0.07, spacing=10)
        
        btn_profile = PremiumIconButton(
            text="Mi Perfil", 
            icon_url="https://cdn-icons-png.flaticon.com/512/1077/1077114.png",
            bg_color=(0.4, 0.25, 0.15, 1),
            on_press_callback=lambda x: self.go_profile()
        )
        
        btn_cart = PremiumIconButton(
            text="Ver Carrito", 
            icon_url="https://cdn-icons-png.flaticon.com/512/1170/1170678.png",
            bg_color=(0.9, 0.55, 0.65, 1),
            on_press_callback=lambda x: setattr(self.manager, 'current', 'cart')
        )
        
        nav_bar.add_widget(btn_profile)
        nav_bar.add_widget(btn_cart)
        main_layout.add_widget(nav_bar)

        # Buscador moderno estilizado sin emojis directos en texto
        search_box = BoxLayout(size_hint_y=0.07)
        self.search_input = ModernTextInput(hint_text="Buscar postre...", multiline=False, padding=(14, 10))
        self.search_input.bind(text=self.actualizar_busqueda)
        search_box.add_widget(self.search_input)
        main_layout.add_widget(search_box)
        
        # Carrusel de Categorías con botones redondeados
        categoria_layout = BoxLayout(size_hint_y=0.06, spacing=5)
        categorias = ["Todas", "Tortas", "Donas", "Brownies", "Cupcakes", "Galletas"]
        for cat in categorias:
            is_active = (cat == CATEGORIA_ACTUAL)
            b_color = (0.4, 0.25, 0.15, 1) if is_active else (0.88, 0.82, 0.78, 1)
            t_color = (1, 1, 1, 1) if is_active else (0.3, 0.15, 0.05, 1)
            
            btn_cat = CatalogButton(text=cat, font_size=11, bg_color=b_color, text_color=t_color, radius=[8])
            btn_cat.bold = is_active
            btn_cat.bind(on_press=lambda inst, c=cat: self.filtrar_por_categoria(c))
            categoria_layout.add_widget(btn_cat)
        main_layout.add_widget(categoria_layout)
        
        # ScrollView del catálogo de productos
        scroll = ScrollView(size_hint_y=0.8)
        product_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=12, padding=(2, 4))
        product_layout.bind(minimum_height=product_layout.setter('height'))
        
        for prod in PRODUCTS_LIST:
            if CATEGORIA_ACTUAL != "Todas" and prod["category"] != CATEGORIA_ACTUAL:
                continue
            if TEXTO_BUSQUEDA.lower() not in prod["name"].lower():
                continue
                
            # Tarjeta de producto individual usando CardContainer
            item_box = CardContainer(orientation='horizontal', size_hint_y=None, height=105, spacing=10, padding=8, radius=[12])
            
            # Imagen real del postre
            img = AsyncImage(source=prod["img"], size_hint_x=0.28, allow_stretch=True, keep_ratio=True)
            
            details = BoxLayout(orientation='vertical', padding=(4, 2), spacing=2)
            details.add_widget(Label(text=prod["name"], font_size=15, font_name="Roboto", color=(0.3, 0.15, 0.05, 1), bold=True, halign="left"))
            details.add_widget(Label(text=f"${prod['price']:.2f}", font_size=14, font_name="Roboto", color=(0.15, 0.45, 0.25, 1), bold=True, halign="left"))
            details.add_widget(Label(text=f"{prod['category']}", font_size=11, font_name="Roboto", color=(0.6, 0.5, 0.4, 1), halign="left"))
            
            # Botón "Ver" interactivo e icono gráfico real integrado
            btn_view = PremiumIconButton(
                text="Ver",
                icon_url="https://cdn-icons-png.flaticon.com/512/4218/4218381.png",
                size_hint_x=0.26,
                bg_color=(0.9, 0.55, 0.65, 1),
                radius=[8],
                on_press_callback=lambda instance, p=prod: self.view_details(p)
            )
            
            item_box.add_widget(img)
            item_box.add_widget(details)
            item_box.add_widget(btn_view)
            product_layout.add_widget(item_box)
            
        scroll.add_widget(product_layout)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

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
        
        with self.canvas.before:
            Color(0.98, 0.96, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=14)
        
        if SELECTED_PRODUCT:
            layout.add_widget(Label(text=SELECTED_PRODUCT["name"], font_size=24, font_name="Roboto", color=(0.3, 0.15, 0.05, 1), bold=True, size_hint_y=0.1))
            layout.add_widget(AsyncImage(source=SELECTED_PRODUCT["img"], size_hint_y=0.45, allow_stretch=True, keep_ratio=True))
            
            # Bloque informativo blanco usando CardContainer
            info_box = CardContainer(orientation='vertical', padding=12, size_hint_y=0.25, spacing=4, radius=[12])
            info_box.add_widget(Label(text=f"Categoría: {SELECTED_PRODUCT['category']}", font_size=15, font_name="Roboto", color=(0.5, 0.4, 0.3, 1)))
            info_box.add_widget(Label(text=f"Precio Exclusivo: ${SELECTED_PRODUCT['price']:.2f}", font_size=22, font_name="Roboto", color=(0.15, 0.45, 0.25, 1), bold=True))
            layout.add_widget(info_box)
            
            # Botones de Acción estilizados con iconos gráficos vectoriales reales
            btn_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.2)
            
            btn_add = PremiumIconButton(
                text="Añadir al Carrito",
                icon_url="https://cdn-icons-png.flaticon.com/512/3514/3514491.png",
                bg_color=(0.35, 0.6, 0.4, 1),
                radius=[10],
                on_press_callback=self.add_to_cart
            )
            
            btn_back = CatalogButton(text="Volver al Catálogo", bg_color=(0.6, 0.55, 0.55, 1), radius=[10])
            btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
            
            btn_box.add_widget(btn_add)
            btn_box.add_widget(btn_back)
            layout.add_widget(btn_box)
            
        self.add_widget(layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

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
        
        with self.canvas.before:
            Color(0.98, 0.96, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        layout = BoxLayout(orientation='vertical', padding=15, spacing=12)
        layout.add_widget(Label(text="Mis Pedidos Solicitados", font_size=22, font_name="Roboto", bold=True, color=(0.3, 0.15, 0.05, 1), size_hint_y=0.08))

        scroll = ScrollView(size_hint_y=0.82)
        orders_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        orders_layout.bind(minimum_height=orders_layout.setter('height'))
        
        mis_pedidos = [o for o in ORDERS_PREPARED if o['usuario'] == CURRENT_USER['username']]

        if not mis_pedidos:
            orders_layout.add_widget(Label(text="Aún no tienes pedidos registrados en tu historial.", font_name="Roboto", color=(0.5, 0.5, 0.5, 1), font_size=14))
        else:
            for pedido in reversed(mis_pedidos):
                box = CardContainer(orientation='vertical', size_hint_y=None, height=85, padding=12, radius=[10])
                
                detalles = f"Ticket #{pedido.get('id', 'N/A')}  |  Total Adquirido: ${pedido['total']:.2f}\nMétodo: {pedido.get('metodo', 'N/A')}  |  Estado Actual: {pedido['status']}"
                box.add_widget(Label(text=detalles, font_name="Roboto", color=(0.25, 0.2, 0.2, 1), font_size=12, halign='center'))
                orders_layout.add_widget(box)

        scroll.add_widget(orders_layout)
        layout.add_widget(scroll)

        btn_back = CatalogButton(text="Volver al Perfil", bg_color=(0.4, 0.25, 0.15, 1), size_hint_y=0.08, radius=[10])
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size