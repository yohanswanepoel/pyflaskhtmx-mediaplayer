import webview
from threading import Thread, Event
from app import app

stop_event = Event()

app_title = "Flask Media Player"
host = "http://127.0.0.1"
port = 22345

#def configure_webkit():
#    settings = WebKitSettings()
#    settings.setAutoPlayPolicy(WebKitSettings.AutoPlayPolicy.Allow)
#    return settings

def run():
    while not stop_event.is_set():
        app.run(port=port, use_reloader=False)

if __name__ == '__main__':
    t = Thread(target=run)
    t.daemon = True
    t.start()

    # webview.platforms.webkit.initialize(settings=configure_webkit())

    webview.create_window(
        app_title,
        f"{host}:{port}",
        height=800,
        width=800,
        easy_drag=True
    )

    #webview.start(debug=True, http_server=True, user_agent="Chrome")
    webview.start(user_agent="Chrome")
    
    stop_event.set()
