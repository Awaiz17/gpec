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

# Accommodation recommendations for each destination
accommodations = {
    "International Space Station": ["Orbital Suite", "Zero-G Pod"],
    "Lunar Hotel": ["Lunar Suite", "Crater View Room"],
    "Mars Colony": ["Red Planet Villa", "Dome Habitat"]
}

# AI-based travel tips (mock data)
travel_tips = {
    "International Space Station": {
        "Economy": "Pack light and bring a zero-gravity sleeping bag!",
        "Luxury": "Enjoy the panoramic views of Earth from your luxury suite.",
        "VIP": "Experience zero-gravity dining with a private chef."
    },
    "Lunar Hotel": {
        "Luxury": "Take a moonwalk and explore the lunar surface.",
        "VIP": "Relax in your private crater-view Jacuzzi."
    },
    "Mars Colony": {
        "VIP": "Explore the red planet with a guided rover tour."
    }
}

# User bookings (mock database)
user_bookings = []

# Function to generate AI-based travel tips
def generate_travel_tip(destination, seat_class):
    return travel_tips.get(destination, {}).get(seat_class, "Enjoy your journey to the stars! 🌌")

@app.route('/')
def home():
    error = request.args.get("error")
    return render_template('index.html', destinations=destinations, error=error)

@app.route('/book', methods=['POST'])
def book():
    destination_name = request.form.get('destination')
    seat_class = request.form.get('class')
    departure_date = request.form.get('date')

    # Validate departure date
    try:
        departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d")
        if departure_date_obj < datetime.now():
            return redirect(url_for('home', error="Invalid departure date. Please select a future date."))
    except ValueError:
        return redirect(url_for('home', error="Invalid date format. Please use YYYY-MM-DD."))

    # Find the selected destination
    destination = next((d for d in destinations if d["name"] == destination_name), None)
    if not destination:
        return redirect(url_for('home', error="Destination not found!"))

    # Validate seat class
    if seat_class not in destination["class"]:
        return redirect(url_for('home', error=f"Invalid seat class for {destination_name}. Available classes: {', '.join(destination['class'])}"))

    # Generate a booking ID
    booking_id = random.randint(1000, 9999)
    user_bookings.append({
        "id": booking_id,
        "destination": destination_name,
        "class": seat_class,
        "date": departure_date,
        "countdown": (departure_date_obj - datetime.now()).days,
        "accommodation": random.choice(accommodations.get(destination_name, ["Standard Room"])),
        "travel_tip": generate_travel_tip(destination_name, seat_class)  # Add AI-based travel tip
    })

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', bookings=user_bookings)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable or default to 5000
    app.run(host="0.0.0.0", port=port)  # Bind to all available IP addresses