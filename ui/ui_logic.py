from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from login.login_logic import SplashScreen, LoginScreen, RegisterScreen, ProfileScreen
from products.products_logic import CatalogScreen, ProductDetailScreen, ClientOrdersScreen
from cart.cart_logic import CartScreen, OrderSummaryScreen
from admin.admin_logic import AdminPanelScreen

def aplicar_estilos_pastel():
    Window.clearcolor = (0.98, 0.95, 0.92, 1)
    Window.size = (360, 640)  # Forzar tamaño móvil para probar

def build_screen_manager():
    aplicar_estilos_pastel()
    sm = ScreenManager()
    
    sm.add_widget(SplashScreen(name='splash'))
    sm.add_widget(LoginScreen(name='login'))
    sm.add_widget(RegisterScreen(name='register'))
    sm.add_widget(ProfileScreen(name='profile'))
    sm.add_widget(CatalogScreen(name='catalog'))
    sm.add_widget(ProductDetailScreen(name='product_detail'))
    sm.add_widget(ClientOrdersScreen(name='client_orders'))
    sm.add_widget(CartScreen(name='cart'))
    sm.add_widget(OrderSummaryScreen(name='order_summary'))
    sm.add_widget(AdminPanelScreen(name='admin_panel'))
    
    return sm
