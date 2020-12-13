from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from . import db
from . import mapfunctions



main = Blueprint('main', __name__)


@main.route ("/")
def index_page():
    
    return render_template('/map.html')



