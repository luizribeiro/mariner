from flask import Flask

from mariner.mars import ElegooMars


app = Flask(__name__)


@app.route("/")
def hello() -> str:
    try:
        elegoo_mars = ElegooMars()
        elegoo_mars.open()
        return "Hello, World!"
    except Exception:
        return "Error"
    finally:
        try:
            elegoo_mars.close()
        except Exception:
            pass
