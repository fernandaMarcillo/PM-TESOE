from kivy.uix.screenmanager import Screen
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
