#!/usr/bin/env python3
''' A simple webserver to present logs & basic functionality '''

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    ''' Home page '''
    return render_template('home.html')

@app.route("/esp32_log")
def esp32_log():
    ''' ESP32 Log page '''
    return render_template('esp32_log.html')

@app.route("/rpi_log")
def rpi_log():
    ''' RPi Log page '''
    return render_template('rpi_log.html')

@app.route("/settings")
def settings():
    ''' Settings page '''
    return render_template('settings.html')

@app.route("/about")
def about():
    ''' About page '''
    return render_template('about.html')

if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost', port=8080, threaded=True, use_reloader=False)
