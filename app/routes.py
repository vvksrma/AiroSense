from flask import Blueprint, render_template, jsonify, send_from_directory
import pandas as pd
import os

main = Blueprint('main', __name__, template_folder='../templates', static_folder='../static')

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/processed'))

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/airmap')
def airmap():
    return render_template('airmap.html')

@main.route('/data/processed/combined_pollution_data.csv')
def data():
    # Serve the CSV file as a download (or set as inline for browser view)
    return send_from_directory(DATA_DIR, 'combined_pollution_data.csv', mimetype='text/csv')