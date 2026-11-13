from streamlit_cookies_controller import CookieController

controller = CookieController()

def set_cookie(key, value):
    controller.set(key, value)

def get_cookie(key):
    return controller.get(key)

def delete_cookie(key):
    try:
        if controller.get(key):  
            controller.delete(key)
    except Exception:
        pass  