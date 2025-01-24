from flask import Blueprint, render_template, request, jsonify
from app.services import fetch_property_details, generate_property_summary

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/fetch-property", methods=['POST'])
def fetch_property():
    data = request.get_json()
    address = data.get("address")

    if not address:
        return jsonify({"error": "Address is required"}), 400

    property_info = fetch_property_details(address)

    if not property_info:
        return jsonify({"error": "Could not fetch property details. Try another address."}), 404

    return jsonify({
        "address": address,
        "details": property_info
    })

@main_bp.route("/generate-summary", methods=["POST"])
def generate_summary():
    data = request.get_json()
    property_info = data.get("property_info")

    if not property_info:
        return jsonify({"error": "Property information is required"}), 400

    summary = generate_property_summary(property_info)

    return jsonify({
        "summary": summary
    })
