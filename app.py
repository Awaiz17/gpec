from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)

# Mock data for destinations and packages
destinations = [
    {"name": "International Space Station", "price": 500000, "class": ["Economy", "Luxury", "VIP"]},
    {"name": "Lunar Hotel", "price": 1000000, "class": ["Luxury", "VIP"]},
    {"name": "Mars Colony", "price": 2000000, "class": ["VIP"]}
]

# User bookings (mock database)
user_bookings = []

@app.route('/')
def home():
    return render_template('index.html', destinations=destinations)

@app.route('/book', methods=['POST'])
def book():
    destination_name = request.form.get('destination')
    seat_class = request.form.get('class')
    departure_date = request.form.get('date')

    # Find the selected destination
    destination = next((d for d in destinations if d["name"] == destination_name), None)
    if not destination:
        return "Destination not found!", 404

    # Generate a booking ID
    booking_id = random.randint(1000, 9999)
    user_bookings.append({
        "id": booking_id,
        "destination": destination_name,
        "class": seat_class,
        "date": departure_date,
        "countdown": (datetime.strptime(departure_date, "%Y-%m-%d") - datetime.now()).days
    })

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', bookings=user_bookings)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable or default to 5000
    app.run(host="0.0.0.0", port=port)  # Bind to all available IP addresses