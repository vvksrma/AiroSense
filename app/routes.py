from flask import Blueprint, render_template, jsonify
import pandas as pd

main = Blueprint('main', __name__, template_folder='../templates', static_folder='../static')

@main.route('/')
def dashboard():
    return render_template('index.html')

# @main.route('/api/heatmap-data')
# def heatmap_data():
#     df = pd.read_csv("data/processed/combined_pollution_data.csv")
#     return jsonify(df.to_dict(orient="records"))
