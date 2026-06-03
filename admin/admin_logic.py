from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from products.products_logic import PRODUCTS_LIST
from cart.cart_logic import ORDERS_PREPARED

PRODUCTO_A_EDITAR = None

class AdminPanelScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        global PRODUCTO_A_EDITAR
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=8)
        
        total_ganancias = sum(order["total"] for order in ORDERS_PREPARED)
        pedidos_activos = len([o for o in ORDERS_PREPARED if "Listo" not in o["status"]])
        
        dash_box = BoxLayout(size_hint_y=0.1, spacing=10)
        dash_box.add_widget(Label(text=f"💰 Ventas: ${total_ganancias:.2f}", font_size=14, color=(0.1, 0.5, 0.1, 1), bold=True))
        dash_box.add_widget(Label(text=f"📋 Activos: {pedidos_activos} pedidos", font_size=14, color=(0.3, 0.15, 0.05, 1), bold=True))
        layout.add_widget(dash_box)
        
        form_title = "Editar Producto Seleccionado:" if PRODUCTO_A_EDITAR else "Agregar Nuevo Producto:"
        layout.add_widget(Label(text=form_title, font_size=13, color=(0.4, 0.2, 0.1, 1), bold=True))
        
        self.name_in = TextInput(hint_text="Nombre del postre", multiline=False)
        self.price_in = TextInput(hint_text="Precio (Ej: 3.50)", multiline=False)
        self.category_in = TextInput(hint_text="Categoría", multiline=False)
        self.img_in = TextInput(hint_text="URL de la Imagen", multiline=False)
        
        if PRODUCTO_A_EDITAR:
            self.name_in.text = PRODUCTO_A_EDITAR["name"]
            self.price_in.text = str(PRODUCTO_A_EDITAR["price"])
            self.category_in.text = PRODUCTO_A_EDITAR["category"]
            self.img_in.text = PRODUCTO_A_EDITAR["img"]
            
        layout.add_widget(self.name_in)
        layout.add_widget(self.price_in)
        layout.add_widget(self.category_in)
        layout.add_widget(self.img_in)
        
        btn_layout = BoxLayout(size_hint_y=0.08, spacing=5)
        if PRODUCTO_A_EDITAR:
            btn_save = Button(text="Actualizar Cambios", background_color=(0.2, 0.6, 0.8, 1))
            btn_save.bind(on_press=self.actualizar_producto)
            btn_cancel = Button(text="Cancelar", background_color=(0.6, 0.6, 0.6, 1))
            btn_cancel.bind(on_press=self.cancelar_edicion)
            btn_layout.add_widget(btn_save)
            btn_layout.add_widget(btn_cancel)
        else:
            btn_add = Button(text="Guardar Nuevo Producto", background_color=(0.4, 0.7, 0.4, 1))
            btn_add.bind(on_press=self.agregar_producto)
            btn_layout.add_widget(btn_add)
        layout.add_widget(btn_layout)
        
        scroll_inv = ScrollView(size_hint_y=0.3)
        inv_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        inv_layout.bind(minimum_height=inv_layout.setter('height'))
        for prod in PRODUCTS_LIST:
            p_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=35, spacing=5)
            p_box.add_widget(Label(text=f"{prod['name']} (${prod['price']})", color=(0.2, 0.2, 0.2, 1), font_size=12))
            btn_edit = Button(text="✏️", size_hint_x=0.15, background_color=(0.9, 0.7, 0.3, 1))
            btn_edit.bind(on_press=lambda inst, p=prod: self.cargar_para_editar(p))
            btn_del = Button(text="🗑️", size_hint_x=0.15, background_color=(0.8, 0.3, 0.3, 1))
            btn_del.bind(on_press=lambda inst, p=prod: self.eliminar_producto(p))
            p_box.add_widget(btn_edit)
            p_box.add_widget(btn_del)
            inv_layout.add_widget(p_box)
        scroll_inv.add_widget(inv_layout)
        layout.add_widget(scroll_inv)
        
        layout.add_widget(Label(text="Cola de Producción (Actualizar Estados):", font_size=13, color=(0.3, 0.15, 0.05, 1), bold=True))
        scroll_orders = ScrollView(size_hint_y=0.3)
        orders_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        orders_layout.bind(minimum_height=orders_layout.setter('height'))
        
        for idx, order in enumerate(ORDERS_PREPARED):
            o_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=5)
            txt_pedido = f"#{order.get('id', '?')} @{order['usuario']} | Total: ${order['total']} [{order['status']}]"
            o_box.add_widget(Label(text=txt_pedido, color=(0.1, 0.2, 0.3, 1), font_size=11, size_hint_x=0.7))
            
            if "⏳" in order["status"]:
                btn_status = Button(text="🧑‍🍳 Cocinar", size_hint_x=0.3, background_color=(0.3, 0.6, 0.9, 1), font_size=11)
                btn_status.bind(on_press=lambda inst, i=idx: self.cambiar_estado_pedido(i, "👩‍🍳 En Cocina"))
            elif "Cocina" in order["status"]:
                btn_status = Button(text="✅ Listo", size_hint_x=0.3, background_color=(0.3, 0.8, 0.3, 1), font_size=11)
                btn_status.bind(on_press=lambda inst, i=idx: self.cambiar_estado_pedido(i, "✅ Listo para retirar"))
            else:
                btn_status = Button(text="🗑️ Despachar", size_hint_x=0.3, background_color=(0.6, 0.6, 0.6, 1), font_size=11)
                btn_status.bind(on_press=lambda inst, i=idx: self.remover_pedido(i))
                
            o_box.add_widget(btn_status)
            orders_layout.add_widget(o_box)
            
        scroll_orders.add_widget(orders_layout)
        layout.add_widget(scroll_orders)
        
        btn_logout = Button(text="Cerrar Sesión de Administrador", background_color=(0.7, 0.2, 0.2, 1), size_hint_y=0.08)
        btn_logout.bind(on_press=self.logout)
        layout.add_widget(btn_logout)
        self.add_widget(layout)

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
        if PRODUCTO_A_EDITAR:
            try:
                PRODUCTO_A_EDITAR["name"] = self.name_in.text
                PRODUCTO_A_EDITAR["price"] = float(self.price_in.text)
                PRODUCTO_A_EDITAR["category"] = self.category_in.text
                PRODUCTO_A_EDITAR["img"] = self.img_in.text
                PRODUCTO_A_EDITAR = None
                self.on_enter()
            except ValueError:
                self.price_in.text = "Error"
                
    def cancelar_edicion(self, instance):
        global PRODUCTO_A_EDITAR
        PRODUCTO_A_EDITAR = None
        self.on_enter()
        
    def eliminar_producto(self, producto):
        if producto in PRODUCTS_LIST:
            PRODUCTS_LIST.remove(producto)
        self.on_enter()
        
    def logout(self, instance):
        self.manager.current = 'login'
