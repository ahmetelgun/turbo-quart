import random
import re
import sys
import threading
import time

from quart import Quart, render_template
from turbo_quart import Turbo

app = Quart(__name__)
turbo = Turbo(app)


@app.context_processor
async def inject_load():
    if sys.platform.startswith("linux"):
        with open("/proc/loadavg", "rt") as f:
            load = f.read().split()[0:3]
    else:
        load = [int(random.random() * 100) / 100 for _ in range(3)]
    return {"load1": load[0], "load5": load[1], "load15": load[2]}


@app.route("/")
async def index():
    return render_template("index.html")


@app.route("/page2")
async def page2():
    return render_template("page2.html")


def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template("loadavg.html"), "load"))


th = threading.Thread(target=update_load)
th.daemon = True
th.start()
