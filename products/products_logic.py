from kivy.uix.screenmanager import Screen
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
