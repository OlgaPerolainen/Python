"""
This is an __init__ file for a program that shows US farmer markets.
It imports views
"""


from flask import Flask, render_template, request

app = Flask(__name__)

app.debug = True
exiting = False

import source.views

