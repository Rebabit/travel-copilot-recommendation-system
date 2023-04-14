import json
import ast
from math import radians, sin, cos, sqrt, atan2
import os
import datetime as dt
from dateutil import parser
from dateutil import rrule
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from bing_image_downloader import downloader

photos_file = '../yelp_photos/yelp_photos'
business_file = '../yelp_dataset/yelp_academic_dataset_business.json'

# filter businesses by business_id from yelp_academic_dataset_business.json
def filter_businesses(business_ids):
    filtered_data = []

    with open(business_file, 'r', encoding = 'utf8') as file:
        for line in file:
            data = json.loads(line)
            if data['business_id'] in business_ids:
                filtered_data.append(data)

    return filtered_data

def filter_businesses_by_type(input_data, business_categories):
    filtered_data = []
    for d in input_data:
        try:
            categories = d["categories"].split(", ")
        except:
            continue
        if any(category in categories for category in business_categories):
            filtered_data.append(d)
    return filtered_data


def contains_dict(a, b):
    def str_dict(strx):
        try:
            dictionary = ast.literal_eval(strx)
            if isinstance(dictionary, dict):
                return dictionary
            else:
                return strx
        except (SyntaxError, ValueError):
            return strx
    a = str_dict(a)
    for key, value in b.items():
        if isinstance(value, dict):
            if key not in a or not isinstance(str_dict(a[key]), dict):
                return False
            if not contains_dict(str_dict(a[key]), value):
                return False
        else:
            if key not in a or a[key] != value:
                return False
    return True

def filter_data_by_attributes(input_data, restrictions):
    filtered_data = []
    for d in input_data:
        try:
            if contains_dict(d['attributes'], restrictions):
                filtered_data.append(d)
        except:
            continue
    return filtered_data



def filter_by_distance(longitude, latitude, input_data, max_distance):
    filtered_data = []

    for data in input_data:
        dlon = radians(data['longitude'] - longitude)
        dlat = radians(data['latitude'] - latitude)
        a = sin(dlat / 2) ** 2 + cos(radians(latitude)) * cos(radians(data['latitude'])) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6371 * c * 1000  # distance in meters

        if distance <= max_distance:
            data['distance'] = distance

            filtered_data.append(data)

    return filtered_data


def sort_data_by_business_ids(business_ids, Input_data):
    sorted_data = []
    for business_id in business_ids:
        for data in Input_data:
            try:
                if data['business_id'] == business_id:
                    sorted_data.append(data)
                    break
            except:
                continue
    return sorted_data




def download_images(input_data):
    for d in input_data:
        query = f"{d['name']} {d['city']}"
        downloader.download(query, limit=1,  output_dir='../downloads', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
        # d['PhotoPath'] = '../downloads/'+query+'/Image_1.jpg'

        directory = '../downloads/'+query+'/'
        files = os.listdir(directory)
        for file in files:
            if os.path.isfile(os.path.join(directory, file)):
                d['PhotoPath'] = os.path.join(directory, file)
                break
    return input_data


def find_photo_ids(input_data, label_limit=None):
    with open(photos_file, encoding="utf8") as f:
        photos_data = []
        for line in f:
            try:
                photo = json.loads(line)
                if label_limit is None or photo['label'] == label_limit:
                    photos_data.append(photo)
            except json.decoder.JSONDecodeError:
                pass

    for data in input_data:
        data['photo_id'] = []
        photo_ids = []
        for photo in photos_data:
            if data['business_id'] == photo['business_id']:
                photo_ids.append(photo['photo_id'])
        data['photo_id'] = photo_ids

    return input_data




