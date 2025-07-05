import csv
import requests
import time

# This is the code used for integrating datasets found into its major csv - accomodations.csv, activities.csv, places.csv


# To add another place to the dataset, remove the pre-existing objects (goa,munnar,jaipur,mumbai) and instead
# add accomodations.csv, activities.csv as the objects with its corresponding maps
# and then make another object with the csv files of the new place you want to add (make sure to add both accomodations and activities)

API_KEY = 'f5b2231e60ae473abdc291628285bd7a'

class Places:
    class Accomodations:
        _next_id = 1
        def __init__(self, place, name, location, landmark, ratings, info, price, tag, accessibility, occupancy, description, reviews, lat, lng, tax):
            self.id = Places.Accomodations._next_id
            Places.Accomodations._next_id += 1

            self.place = place
            self.name = name
            self.location = location
            self.landmark = landmark
            self.ratings = ratings
            self.info = info
            self.price = price
            self.tag = tag
            self.accessibility = accessibility
            self.occupancy = occupancy
            self.description = description
            self.reviews = reviews
            self.lat = lat
            self.lng = lng
            self.tax = tax

    class Activities:
        _next_id = 1
        def __init__(self, city, name, tag, price, lat, lng):
            self.id = Places.Activities._next_id
            Places.Activities._next_id += 1

            self.city = city
            self.name = name
            self.tag = tag
            self.price = price
            self.lat = lat
            self.lng = lng

def get_lat_lng(place):
    try:
        url = f'https://api.opencagedata.com/geocode/v1/json?q={place}&key={API_KEY}'
        response = requests.get(url)
        data = response.json()
        if data['results']:
            lat = data['results'][0]['geometry']['lat']
            lng = data['results'][0]['geometry']['lng']
            time.sleep(1)  # Respect API rate limits
            return lat, lng
    except Exception as e:
        print(f"Geocoding failed for '{place}': {e}")
    return None, None

def main():
    allplaces = []
    allactivities = []
    allaccomodations = []

    def process_accommodations(csv_file, place_name, colmap):
        local_acc = []
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header
            for each in reader:
                try:
                    name = each[colmap['name']]
                    location = each[colmap['location']] if 'location' in colmap else place_name
                    landmark = each[colmap['landmark']] if 'landmark' in colmap else None
                    ratings = each[colmap['ratings']] if 'ratings' in colmap else None
                    info = each[colmap['info']] if 'info' in colmap else None
                    price = each[colmap['price']]
                    tag = each[colmap['tag']] if 'tag' in colmap else None
                    accessibility = each[colmap['accessibility']] if 'accessibility' in colmap else None
                    occupancy = each[colmap['occupancy']] if 'occupancy' in colmap else None
                    description = each[colmap['description']] if 'description' in colmap else None
                    reviews = each[colmap['reviews']] if 'reviews' in colmap else None
                    tax = each[colmap['tax']] if 'tax' in colmap else None
                    lat = each[colmap['lat']] if 'lat' in colmap else None
                    lng = each[colmap['lng']] if 'lng' in colmap else None

                    if not lat or not lng:
                        lat, lng = get_lat_lng(f"{name}, {place_name}")

                    acc = Places.Accomodations(place_name, name, location, landmark, ratings, info, price, tag,
                                               accessibility, occupancy, description, reviews, lat, lng, tax)
                    allaccomodations.append(acc)
                    local_acc.append(acc)
                except Exception as e:
                    print(f"Error in accommodation row: {e}")
        return local_acc

    def process_activities(csv_file, place_name):
        local_acts = []
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header
            for each in reader:
                try:
                    name = each[1]
                    tag = each[2]
                    price = each[3]
                    lat = each[4]
                    lng = each[5]
                    act = Places.Activities(place_name, name, tag, price, lat, lng)
                    allactivities.append(act)
                    local_acts.append(act)
                except Exception as e:
                    print(f"Error in activity row: {e}")
        return local_acts

    # Goa
    goa_map = {
        'name': 0, 'location': 1, 'landmark': 2, 'ratings': 3, 'info': 4, 'price': 5,
        'tag': 6, 'accessibility': 7, 'occupancy': 8, 'description': 9
    }
    accs = process_accommodations("dataset/goa.csv", "Goa", goa_map)
    acts = process_activities("dataset/actgoa.csv", "Goa")
    allplaces.append(("Goa", accs, acts))

    # Munnar
    munnar_map = {
        'name': 0, 'ratings': 1, 'reviews': 3, 'location': 5, 'landmark': 6,
        'price': 8, 'tax': 9
    }
    accs = process_accommodations("dataset/munnar.csv", "Munnar", munnar_map)
    acts = process_activities("dataset/actmunnar.csv", "Munnar")
    allplaces.append(("Munnar", accs, acts))

    # Jaipur
    jaipur_map = {
        'name': 1, 'price': 2, 'reviews': 3, 'lat': 4, 'lng': 5
    }
    accs = process_accommodations("dataset/jaipur.csv", "Jaipur", jaipur_map)
    acts = process_activities("dataset/actjaipur.csv", "Jaipur")
    allplaces.append(("Jaipur", accs, acts))

    # Mumbai
    mumbai_map = {
        'name': 0, 'ratings': 1, 'reviews': 3, 'location': 5, 'landmark': 6, 'price': 8, 'tax': 9
    }
    accs = process_accommodations("dataset/mumbai.csv", "Mumbai", mumbai_map)
    acts = process_activities("dataset/actmumbai.csv", "Mumbai")
    allplaces.append(("Mumbai", accs, acts))

    # Write all accommodations
    with open("accommodations.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "place", "location", "landmark", "ratings", "info", "price", "tag",
                         "accessibility", "occupancy", "description", "reviews", "lat", "lng", "tax"])
        for each in allaccomodations:
            writer.writerow([each.id, each.name, each.place, each.location, each.landmark, each.ratings,
                             each.info, each.price, each.tag, each.accessibility, each.occupancy,
                             each.description, each.reviews, each.lat, each.lng, each.tax])

    # Write all activities
    with open("activities.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "city", "name", "tag", "price", "lat", "lng"])
        for each in allactivities:
            writer.writerow([each.id, each.city, each.name, each.tag, each.price, each.lat, each.lng])

    # Optional: write place-level summary
    with open("places.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["place", "num_accommodations", "num_activities"])
        for each in allplaces:
            writer.writerow([each[0], len(each[1]), len(each[2])])

if __name__ == "__main__":
    main()
