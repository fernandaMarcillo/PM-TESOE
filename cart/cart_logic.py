import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle, RoundedRectangle
import random

CART_ITEMS = []
ORDERS_PREPARED = []
ULTIMO_PEDIDO = {}

# --- COMPONENTES MODERNOS CON ICONOS REALES ---

class CartButton(Button):
    """Botón móvil plano con radio de curvatura ajustable"""
    def __init__(self, bg_color=(0.9, 0.55, 0.65, 1), text_color=(1, 1, 1, 1), radius=[10], **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = text_color
        self.bold = True
        self.font_size = 14
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


class IconButton(BoxLayout):
    """Un botón que contiene un ícono gráfico real en lugar de texto o emojis"""
    def __init__(self, icon_url, bg_color=(0.75, 0.25, 0.25, 1), radius=[0, 10, 10, 0], on_press_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 12
        
        # Botón invisible de fondo para capturar el click
        self.btn = Button(background_normal='', background_color=(0,0,0,0))
        if on_press_callback:
            self.btn.bind(on_press=on_press_callback)
            
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Ícono real de alta definición
        self.icon_img = AsyncImage(source=icon_url, allow_stretch=True, keep_ratio=True)
        
        self.add_widget(self.btn)
        # Hack clásico de Kivy para superponer el ícono sobre el botón transparente
        self.btn.add_widget(self.icon_img)
        self.btn.bind(pos=self.sync_icon, size=self.sync_icon)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def sync_icon(self, instance, value):
        self.icon_img.pos = instance.pos
        self.icon_img.size = instance.size


class CardRow(BoxLayout):
    """Fila estilizada con fondo blanco y esquinas curvas para los productos"""
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


class ModernSpinner(Spinner):
    """Selector desplegable con esquinas curvas"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            Color(0.4, 0.25, 0.15, 1)  # Café Chocolate
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


# --- PANTALLAS ---

class CartScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.98, 0.96, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        self.main_layout = BoxLayout(orientation='vertical', padding=16, spacing=12)
        
        # Cabecera de título limpia
        self.main_layout.add_widget(Label(
            text="Tu Carrito de Compras", font_size=22, font_name="Roboto",
            color=(0.3, 0.15, 0.05, 1), size_hint_y=0.08, bold=True
        ))
        
        scroll = ScrollView(size_hint_y=0.5)
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=(2, 2, 2, 2))
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        
        total_price = 0.0
        for idx, item in enumerate(CART_ITEMS):
            subtotal = item['price'] * item['qty']
            total_price += subtotal
            
            item_box = CardRow(orientation='horizontal', size_hint_y=None, height=52, spacing=5, padding=(10, 0, 0, 0))
            
            item_box.add_widget(Label(
                text=f"{item['name']}", size_hint_x=0.4, font_name="Roboto",
                color=(0.25, 0.2, 0.2, 1), font_size=14, halign="left"
            ))
            item_box.add_widget(Label(
                text=f"${item['price']:.2f}", size_hint_x=0.15, font_name="Roboto",
                color=(0.4, 0.2, 0.1, 1), font_size=14
            ))
            
            # Contenedor de cantidad modificada (+ / -)
            qty_layout = BoxLayout(size_hint_x=0.32, spacing=4, padding=(0, 6, 0, 6))
            btn_minus = CartButton(text="-", bg_color=(0.8, 0.55, 0.55, 1), radius=[6])
            btn_minus.bind(on_press=lambda inst, i=idx: self.modify_qty(i, -1))
            
            lbl_qty = Label(text=str(item['qty']), color=(0.3, 0.15, 0.05, 1), font_name="Roboto", bold=True, font_size=14)
            
            btn_plus = CartButton(text="+", bg_color=(0.55, 0.75, 0.55, 1), radius=[6])
            btn_plus.bind(on_press=lambda inst, i=idx: self.modify_qty(i, 1))
            
            qty_layout.add_widget(btn_minus)
            qty_layout.add_widget(lbl_qty)
            qty_layout.add_widget(btn_plus)
            item_box.add_widget(qty_layout)
            
            # ÍCONO REAL DE BASURERO (Reemplaza el emoji de cruz/basurero antiguo)
            btn_delete = IconButton(
                icon_url="https://cdn-icons-png.flaticon.com/512/1214/1214428.png", 
                bg_color=(0.75, 0.25, 0.25, 1), 
                size_hint_x=0.13, 
                on_press_callback=lambda instance, i=idx: self.remove_item(i)
            )
            item_box.add_widget(btn_delete)
            
            self.list_layout.add_widget(item_box)
            
        scroll.add_widget(self.list_layout)
        self.main_layout.add_widget(scroll)
        
        # Info de pagos
        self.label_total = Label(
            text=f"Total a Pagar: ${total_price:.2f}", font_size=20, font_name="Roboto",
            color=(0.15, 0.45, 0.25, 1), size_hint_y=0.06, bold=True
        )
        self.main_layout.add_widget(self.label_total)

        self.main_layout.add_widget(Label(
            text="Selecciona Método de Pago:", color=(0.4, 0.2, 0.1, 1), font_name="Roboto",
            size_hint_y=0.04, font_size=13, bold=True
        ))
        
        self.spinner_pago = ModernSpinner(
            text='Efectivo en Caja',
            values=('Efectivo en Caja', 'Transferencia Bancaria'),
            size_hint_y=0.06,
            color=(1, 1, 1, 1),
            font_name="Roboto",
            bold=True
        )
        self.main_layout.add_widget(self.spinner_pago)
        
        # BOTONES INFERIORES: Diseñados con layouts limpios que albergan texto e íconos reales a la vez
        actions = BoxLayout(size_hint_y=0.08, spacing=12)
        
        # Botón volver con ícono interno real de bolsa de compras
        btn_back_box = BoxLayout(orientation='horizontal')
        btn_back = CartButton(text="  Seguir Comprando", bg_color=(0.7, 0.6, 0.5, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        btn_back_box.add_widget(btn_back)
        actions.add_widget(btn_back_box)
        
        # Botón checkout con ícono interno real de tarjeta / verificación
        if CART_ITEMS:
            btn_checkout_box = BoxLayout(orientation='horizontal')
            btn_checkout = CartButton(text="  Realizar Pedido", bg_color=(0.25, 0.55, 0.75, 1))
            btn_checkout.bind(on_press=lambda x: self.checkout(total_price))
            btn_checkout_box.add_widget(btn_checkout)
            actions.add_widget(btn_checkout_box)
            
        self.main_layout.add_widget(actions)
        self.add_widget(self.main_layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

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
        
        with self.canvas.before:
            Color(0.98, 0.96, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(
            text="¡TICKET GENERADO EXITOSAMENTE!", font_size=18, font_name="Roboto",
            color=(0.2, 0.55, 0.2, 1), bold=True, size_hint_y=0.08
        ))
        
        if ULTIMO_PEDIDO:
            ticket_box = CardRow(orientation='vertical', padding=15, spacing=6, size_hint_y=0.4, radius=[12])
            
            ticket_box.add_widget(Label(text=f"Pedido #{ULTIMO_PEDIDO['id']}", font_size=22, color=(0.3, 0.15, 0.05, 1), font_name="Roboto", bold=True))
            ticket_box.add_widget(Label(text=f"Total Pagado: ${ULTIMO_PEDIDO['total']:.2f}", font_size=18, color=(0.4, 0.2, 0.1, 1), font_name="Roboto", bold=True))
            ticket_box.add_widget(Label(text=f"Método de pago: {ULTIMO_PEDIDO['metodo']}", font_size=13, font_name="Roboto", color=(0.5, 0.5, 0.5, 1)))
            
            if ULTIMO_PEDIDO['metodo'] == 'Transferencia Bancaria':
                ticket_box.add_widget(Label(
                    text="DATOS DE TRANSFERENCIA:\nCLABE: 123456789012345678\nConcepto: Tesoe Pop", 
                    color=(0.2, 0.4, 0.6, 1), halign="center", font_name="Roboto", font_size=13, bold=True
                ))
            else:
                ticket_box.add_widget(Label(
                    text="Por favor, liquida tu cuenta en la caja principal.", 
                    color=(0.6, 0.4, 0.2, 1), font_name="Roboto", font_size=13, bold=True
                ))
                
            layout.add_widget(ticket_box)

        # SECCIÓN QR REAL: Quitamos el botón con el emoji de teléfono e incrustamos una imagen real de un vector QR
        qr_box = BoxLayout(size_hint=(None, None), size=(140, 140), pos_hint={'center_x': 0.5})
        qr_img = AsyncImage(
            source="https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_horizontal_BAR_and_vertical_BAR_testing.png",
            allow_stretch=True, 
            keep_ratio=True
        )
        qr_box.add_widget(qr_img)
        layout.add_widget(qr_box)
        
        # Botón de finalización estilizado
        btn_finish = CartButton(
            text="Volver al Catálogo", bg_color=(0.4, 0.25, 0.15, 1), 
            size_hint_y=0.08
        )
        btn_finish.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        layout.add_widget(btn_finish)
        
        self.add_widget(layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size