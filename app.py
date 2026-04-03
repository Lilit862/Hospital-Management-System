# app.py — Main Flask application entry point
import os
from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS

# Import our route blueprints
from routes.auth     import auth_bp
from routes.patients import patients_bp
from routes.hospital import hospital_bp

app = Flask(__name__)

# Secret key for sessions — CHANGE THIS in production!
#app.secret_key = os.environ.get("SECRET_KEY", "hospital-secret-key-change-me-2024")
app.secret_key = "inch_uzes_karox_es_grel"

# Allow cross-origin requests (useful during development)
CORS(app, supports_credentials=True)

# Register all route blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(hospital_bp)


# ── PAGE ROUTES ─────────────────────────────────────────────
@app.route("/")
def root():
    """Redirect root to login page."""
    return redirect(url_for("login_page"))


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


# ── RUN ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  🏥  Hospital Management System  — Backend")
    print("  Running at: http://MedCore.Hospital")
    print("  Default login: admin / admin123")
    print("="*55 + "\n")
    app.run(debug=True, port=5000)
