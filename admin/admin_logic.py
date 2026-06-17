from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle
from products.products_logic import PRODUCTS_LIST
from cart.cart_logic import ORDERS_PREPARED

PRODUCTO_A_EDITAR = None

# --- COMPONENTES MODERNOS CON ESQUINAS REDONDEADAS ---

class AdminTextInput(BoxLayout):
    """Contenedor que envuelve un TextInput nativo en una hermosa tarjeta blanca curva"""
    def __init__(self, hint_text="", text="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (14, 4, 14, 4)
        self.size_hint_y = None
        self.height = 46
        
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Blanco puro
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        self.input = TextInput(
            text=text,
            hint_text=hint_text,
            multiline=False,
            background_normal='',
            background_active='',
            background_color=(0, 0, 0, 0),
            foreground_color=(0.2, 0.2, 0.2, 1),
            cursor_color=(0.3, 0.15, 0.05, 1),
            font_name="Roboto",
            font_size=14,
            padding=(0, 8, 0, 8)
        )
        self.add_widget(self.input)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    @property
    def text(self):
        return self.input.text

    @text.setter
    def text(self, value):
        self.input.text = value


class AdminButton(Button):
    """Botón móvil plano con radio de curvatura adaptable"""
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


class CardRow(BoxLayout):
    """Fila estilizada con fondo blanco y esquinas curvas para inventario y pedidos"""
    def __init__(self, bg_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[8])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


# --- PANTALLAS PRINCIPALES DEL ADMINISTRADOR ---

class AdminPanelScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        global PRODUCTO_A_EDITAR
        
        # --- FONDO DE LA PANTALLA ---
        with self.canvas.before:
            Color(0.98, 0.96, 0.95, 1)  # Crema unificado
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # Contenedor Principal
        layout = BoxLayout(orientation='vertical', padding=16, spacing=12)
        
        # --- DASHBOARD DE METRICAS ---
        total_ganancias = sum(order["total"] for order in ORDERS_PREPARED)
        pedidos_activos = len([o for o in ORDERS_PREPARED if "Listo" not in o["status"]])
        
        dash_box = BoxLayout(size_hint_y=0.07, spacing=12)
        
        lbl_ventas = Label(
            text=f"💰 Ventas: ${total_ganancias:.2f}", 
            font_size=15, color=(0.15, 0.45, 0.25, 1), bold=True, font_name="Roboto"
        )
        lbl_activos = Label(
            text=f"📋 Activos: {pedidos_activos} pedidos", 
            font_size=15, color=(0.4, 0.2, 0.1, 1), bold=True, font_name="Roboto"
        )
        
        dash_box.add_widget(lbl_ventas)
        dash_box.add_widget(lbl_activos)
        layout.add_widget(dash_box)
        
        # --- SECCIÓN FORMULARIO ---
        form_title = "✏️ Editar Producto Seleccionado" if PRODUCTO_A_EDITAR else "➕ Agregar Nuevo Producto"
        layout.add_widget(Label(
            text=form_title, font_size=14, color=(0.3, 0.15, 0.05, 1), 
            bold=True, size_hint_y=0.03, halign="left"
        ))
        
        form_layout = BoxLayout(orientation='vertical', spacing=8, size_hint_y=0.28)
        
        self.name_in = AdminTextInput(hint_text="Nombre del postre")
        self.price_in = AdminTextInput(hint_text="Precio (Ej: 3.50)")
        self.category_in = AdminTextInput(hint_text="Categoría")
        self.img_in = AdminTextInput(hint_text="URL de la Imagen")
        
        if PRODUCTO_A_EDITAR:
            self.name_in.text = PRODUCTO_A_EDITAR["name"]
            self.price_in.text = str(PRODUCTO_A_EDITAR["price"])
            self.category_in.text = PRODUCTO_A_EDITAR["category"]
            self.img_in.text = PRODUCTO_A_EDITAR["img"]
            
        form_layout.add_widget(self.name_in)
        form_layout.add_widget(self.price_in)
        form_layout.add_widget(self.category_in)
        form_layout.add_widget(self.img_in)
        layout.add_widget(form_layout)
        
        # Botones del Formulario
        btn_layout = BoxLayout(size_hint_y=0.06, spacing=10)
        if PRODUCTO_A_EDITAR:
            btn_save = AdminButton(text="Actualizar Cambios", bg_color=(0.2, 0.5, 0.7, 1))
            btn_save.bind(on_press=self.actualizar_producto)
            btn_cancel = AdminButton(text="Cancelar", bg_color=(0.5, 0.5, 0.5, 1))
            btn_cancel.bind(on_press=self.cancelar_edicion)
            btn_layout.add_widget(btn_save)
            btn_layout.add_widget(btn_cancel)
        else:
            btn_add = AdminButton(text="Guardar Nuevo Producto", bg_color=(0.35, 0.55, 0.3, 1))
            btn_add.bind(on_press=self.agregar_producto)
            btn_layout.add_widget(btn_add)
        layout.add_widget(btn_layout)
        
        # --- SECCIÓN INVENTARIO ---
        layout.add_widget(Label(
            text="🍩 Inventario Actual:", font_size=14, 
            color=(0.3, 0.15, 0.05, 1), bold=True, size_hint_y=0.03
        ))
        
        scroll_inv = ScrollView(size_hint_y=0.22)
        inv_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=(2, 2, 2, 2))
        inv_layout.bind(minimum_height=inv_layout.setter('height'))
        
        for prod in PRODUCTS_LIST:
            p_box = CardRow(orientation='horizontal', size_hint_y=None, height=45, spacing=5, padding=(8, 0, 0, 0))
            
            p_box.add_widget(Label(
                text=f"{prod['name']} (${prod['price']:.2f})", 
                color=(0.25, 0.2, 0.2, 1), font_size=13, halign="left", font_name="Roboto", size_hint_x=0.7
            ))
            
            btn_edit = AdminButton(text="✏️", size_hint_x=0.15, bg_color=(0.85, 0.65, 0.25, 1), radius=[0, 8, 8, 0])
            btn_edit.bind(on_press=lambda inst, p=prod: self.cargar_para_editar(p))
            
            btn_del = AdminButton(text="🗑️", size_hint_x=0.15, bg_color=(0.75, 0.25, 0.25, 1), radius=[0, 8, 8, 0])
            btn_del.bind(on_press=lambda inst, p=prod: self.eliminar_producto(p))
            
            p_box.add_widget(btn_edit)
            p_box.add_widget(btn_del)
            inv_layout.add_widget(p_box)
            
        scroll_inv.add_widget(inv_layout)
        layout.add_widget(scroll_inv)
        
        # --- SECCIÓN COLA DE PRODUCCIÓN ---
        layout.add_widget(Label(
            text="👨‍🍳 Cola de Producción:", font_size=14, 
            color=(0.3, 0.15, 0.05, 1), bold=True, size_hint_y=0.03
        ))
        
        scroll_orders = ScrollView(size_hint_y=0.24)
        orders_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=(2, 2, 2, 2))
        orders_layout.bind(minimum_height=orders_layout.setter('height'))
        
        for idx, order in enumerate(ORDERS_PREPARED):
            o_box = CardRow(orientation='horizontal', size_hint_y=None, height=50, spacing=5, padding=(8, 0, 0, 0))
            txt_pedido = f" #{order.get('id', '?')} @{order['usuario']} | Total: ${order['total']} \n [{order['status']}]"
            
            o_box.add_widget(Label(
                text=txt_pedido, color=(0.2, 0.25, 0.3, 1), 
                font_size=12, font_name="Roboto", size_hint_x=0.65, halign="left"
            ))
            
            if "⏳" in order["status"]:
                btn_status = AdminButton(text="🧑‍🍳 Cocinar", size_hint_x=0.35, bg_color=(0.25, 0.5, 0.75, 1), radius=[0, 8, 8, 0])
                btn_status.bind(on_press=lambda inst, i=idx: self.cambiar_estado_pedido(i, "👩‍🍳 En Cocina"))
            elif "Cocina" in order["status"]:
                btn_status = AdminButton(text="✅ Listo", size_hint_x=0.35, bg_color=(0.25, 0.65, 0.35, 1), radius=[0, 8, 8, 0])
                btn_status.bind(on_press=lambda inst, i=idx: self.cambiar_estado_pedido(i, "✅ Listo para retirar"))
            else:
                btn_status = AdminButton(text="📦 Despachar", size_hint_x=0.35, bg_color=(0.5, 0.5, 0.5, 1), radius=[0, 8, 8, 0])
                btn_status.bind(on_press=lambda inst, i=idx: self.remover_pedido(i))
                
            o_box.add_widget(btn_status)
            orders_layout.add_widget(o_box)
            
        scroll_orders.add_widget(orders_layout)
        layout.add_widget(scroll_orders)
        
        # --- BOTÓN LOGOUT ---
        btn_logout = AdminButton(
            text="🔒 Cerrar Sesión de Administrador", 
            bg_color=(0.6, 0.15, 0.15, 1), 
            size_hint_y=0.06
        )
        btn_logout.bind(on_press=self.logout)
        layout.add_widget(btn_logout)
        
        self.add_widget(layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

    # --- LÓGICA DE CONTROL ---
    def cambiar_estado_pedido(self, index, nuevo_estado):
        ORDERS_PREPARED[index]["status"] = nuevo_estado
        self.on_enter()

    def remover_pedido(self, index):
        ORDERS_PREPARED.pop(index)
        self.on_enter()

    def agregar_producto(self, instance):
        if self.name_in.text and self.price_in.text:
            try:
                url_img = self.img_in.text if self.img_in.text else "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400"
                categoria = self.category_in.text if self.category_in.text else "Reposteria"
                new_p = {
                    "id": len(PRODUCTS_LIST) + 1,
                    "name": self.name_in.text,
                    "price": float(self.price_in.text),
                    "category": categoria,
                    "img": url_img
                }
                PRODUCTS_LIST.append(new_p)
                self.on_enter()
            except ValueError:
                self.price_in.text = "Error"

    def cargar_para_editar(self, producto):
        global PRODUCTO_A_EDITAR
        PRODUCTO_A_EDITAR = producto
        self.on_enter()

    def actualizar_producto(self, instance):
        global PRODUCTO_A_EDITAR
        if PRODUCTO_A_EDITAR and self.name_in.text and self.price_in.text:
            try:
                PRODUCTO_A_EDITAR["name"] = self.name_in.text
                PRODUCTO_A_EDITAR["price"] = float(self.price_in.text)
                PRODUCTO_A_EDITAR["category"] = self.category_in.text if self.category_in.text else PRODUCTO_A_EDITAR.get("category", "Reposteria")
                PRODUCTO_A_EDITAR["img"] = self.img_in.text if self.img_in.text else PRODUCTO_A_EDITAR.get("img", "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400")
                PRODUCTO_A_EDITAR = None
                self.on_enter()
            except ValueError:
                self.price_in.text = "Error"
        else:
            if not self.name_in.text:
                self.name_in.text = "Falta nombre"
            if not self.price_in.text:
                self.price_in.text = "Falta precio"

    def cancelar_edicion(self, instance):
        global PRODUCTO_A_EDITAR
        PRODUCTO_A_EDITAR = None
        self.on_enter()

    def logout(self, instance):
        global PRODUCTO_A_EDITAR
        PRODUCTO_A_EDITAR = None
        self.manager.current = "login"