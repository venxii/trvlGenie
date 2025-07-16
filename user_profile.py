from flask import Flask, request, render_template
import json
import os
import datetime

app = Flask(__name__)

# Ensure folder exists
os.makedirs("user_profiles", exist_ok=True)

@app.route('/')
def index():
    return render_template('your_form.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Get form data
        form_data = {
            'Adventure': request.form['Adventure'],
            'Culture': request.form['Culture'],
            'Nature': request.form['Nature'],
            'Relaxation': request.form['Relaxation'],
            'Spirituality': request.form['Spirituality'],
            'Luxury': request.form['Luxury'],
            'Wildlife': request.form['Wildlife'],
            'Photography': request.form['Photography'],
            'FoodExperiences': request.form['FoodExperiences'],
            'FestivalsEvents': request.form['FestivalsEvents'],
            'Budget': request.form['Budget'],
            'Days': request.form['daysValue'],
            'Occupation': request.form['Occupation'],
            'Pace': request.form['Pace'],
            'TravelWith': request.form.getlist('TravelWith'),  # for multi-select checkboxes
            'Accessibility': request.form['Accessibility']
        }

        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"user_profiles/user_{timestamp}.json"

        # Save to JSON
        with open(filename, "w") as f:
            json.dump(form_data, f, indent=4)

        return f"Profile saved as {filename}!"

if __name__ == '__main__':
    app.run(debug=True)
