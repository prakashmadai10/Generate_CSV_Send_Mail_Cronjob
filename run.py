from flask import Flask, render_template, jsonify

import Scheduler.scheduler as scheduler
import pandas as pd
from waitress import serve
import json
from dotenv import dotenv_values, load_dotenv
load_dotenv()
app = Flask(__name__)

if __name__ == '__main__':
    scheduler.scheduler.start()
    serve(app, host='localhost', port=5000)
    