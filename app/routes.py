from flask import Blueprint, render_template, request, jsonify
from app.services import fetch_property, generate_summary


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/api/")
def api():
    return render_template("api/fetch_property.html")


@main_bp.route("/api/fetch-property", methods=['POST'])
def fetch_property_route():
    return fetch_property()


@main_bp.route("/api/generate-summary", methods=['POST'])
def generate_summary_route():
    return generate_summary()
