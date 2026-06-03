from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
import random

CART_ITEMS = []
ORDERS_PREPARED = []
ULTIMO_PEDIDO = {}

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
            subtotal = item['price'] * item['qty']
            total_price += subtotal
            
            item_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
            item_box.add_widget(Label(text=item['name'], size_hint_x=0.35, color=(0.3, 0.15, 0.05, 1)))
            item_box.add_widget(Label(text=f"${item['price']}", size_hint_x=0.15, color=(0.4, 0.2, 0.1, 1)))
            
            qty_layout = BoxLayout(size_hint_x=0.3, spacing=2)
            btn_minus = Button(text="-", background_color=(0.8, 0.6, 0.6, 1))
            btn_minus.bind(on_press=lambda inst, i=idx: self.modify_qty(i, -1))
            
            lbl_qty = Label(text=str(item['qty']), color=(0.3, 0.15, 0.05, 1), bold=True)
            
            btn_plus = Button(text="+", background_color=(0.6, 0.8, 0.6, 1))
            btn_plus.bind(on_press=lambda inst, i=idx: self.modify_qty(i, 1))
            
            qty_layout.add_widget(btn_minus)
            qty_layout.add_widget(lbl_qty)
            qty_layout.add_widget(btn_plus)
            item_box.add_widget(qty_layout)
            
            btn_delete = Button(text="❌", size_hint_x=0.1, background_color=(0.8, 0.3, 0.3, 1))
            btn_delete.bind(on_press=lambda instance, i=idx: self.remove_item(i))
            item_box.add_widget(btn_delete)
            
            self.list_layout.add_widget(item_box)
            
        scroll.add_widget(self.list_layout)
        self.main_layout.add_widget(scroll)
        
        self.label_total = Label(text=f"Total a Pagar: ${total_price:.2f}", font_size=18, color=(0.3, 0.15, 0.05, 1), size_hint_y=0.1, bold=True)
        self.main_layout.add_widget(self.label_total)

        self.main_layout.add_widget(Label(text="Selecciona Método de Pago:", color=(0.3, 0.15, 0.05, 1), size_hint_y=None, height=30))
        self.spinner_pago = Spinner(
            text='Efectivo en Caja',
            values=('Efectivo en Caja', 'Transferencia Bancaria'),
            size_hint_y=None, height=40,
            background_color=(0.8, 0.7, 0.6, 1)
        )
        self.main_layout.add_widget(self.spinner_pago)
        
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

    def modify_qty(self, index, amount):
        CART_ITEMS[index]["qty"] += amount
        if CART_ITEMS[index]["qty"] <= 0:
            CART_ITEMS.pop(index)
        self.on_enter()

    def remove_item(self, index):
        CART_ITEMS.pop(index)
        self.on_enter()

    def checkout(self, total):
        global CART_ITEMS, ULTIMO_PEDIDO
        if CART_ITEMS:
            from login.login_logic import CURRENT_USER
            resumen_productos = [f"{item['name']} (x{item['qty']})" for item in CART_ITEMS]
            
            pedido = {
                "id": random.randint(1000, 9999),
                "usuario": CURRENT_USER["username"],
                "productos": resumen_productos,
                "total": total,
                "metodo": self.spinner_pago.text,
                "status": "⏳ En Cola"
            }
            ORDERS_PREPARED.append(pedido)
            ULTIMO_PEDIDO = pedido
            CART_ITEMS.clear()
            
            self.manager.get_screen('order_summary').on_enter()
            self.manager.current = 'order_summary'

class OrderSummaryScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="¡TICKET GENERADO EXITOSAMENTE!", font_size=18, color=(0.2, 0.6, 0.2, 1), bold=True))
        
        if ULTIMO_PEDIDO:
            layout.add_widget(Label(text=f"Pedido #{ULTIMO_PEDIDO['id']}", font_size=20, color=(0.3, 0.15, 0.05, 1), bold=True))
            layout.add_widget(Label(text=f"Total: ${ULTIMO_PEDIDO['total']:.2f}", color=(0.3, 0.15, 0.05, 1)))
            layout.add_widget(Label(text=f"Método de pago: {ULTIMO_PEDIDO['metodo']}", color=(0.3, 0.15, 0.05, 1)))
            
            if ULTIMO_PEDIDO['metodo'] == 'Transferencia Bancaria':
                layout.add_widget(Label(text="CLABE: 123456789012345678\nConcepto: Tesoe Pop", color=(0.3, 0.15, 0.05, 1), halign="center"))
            else:
                layout.add_widget(Label(text="Por favor, paga en la cooperativa.", color=(0.3, 0.15, 0.05, 1)))

        qr_box = BoxLayout(size_hint=(None, None), size=(150, 150), pos_hint={'center_x': 0.5})
        btn_qr = Button(text="[ CÓDIGO QR ]\nMuestra esto\nen caja", background_color=(1, 1, 1, 1), color=(0,0,0,1))
        qr_box.add_widget(btn_qr)
        layout.add_widget(qr_box)
        
        btn_finish = Button(text="Volver al Catálogo", background_color=(0.9, 0.6, 0.7, 1), size_hint_y=None, height=50)
        btn_finish.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        layout.add_widget(btn_finish)
        self.add_widget(layout)
