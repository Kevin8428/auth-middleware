import os

from flask import Flask, render_template

from middleware import auth

app = Flask(__name__)