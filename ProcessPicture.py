
# https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3

# https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?prox=37.7442%2C-119.5931%2C1000&mode=#retrieveAreas&app_id=devportal-demo-20180625&app_code=9v2BkviRwi9Ot26kp2IysQ&gen=9

# the following functions use Python PIL to get geociding data from pictures. Functions 1-5 
# the function returnes a dataframe with the geodata for the picture that matches the columns of our database.


import os
import requests

from PIL import Image

# funtion 1
def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()



from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
# funtion #2
def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


#funtion 3
def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


# funtion 4

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)


# Funtion 5

def get_location(geotags):
    coords = get_coordinates(geotags)

    uri = 'https://reverse.geocoder.api.here.com/6.2/reversegeocode.json'
    headers = {}
    params = {
        'app_id': 'cjIyVcZ1rzUhd0Xb9r0q',
        'app_code': 'f9pU60MvwiOVXVRl5N5HmA',
        'prox': "%s,%s" % coords,
        'gen': 9,
        'mode': 'retrieveAddresses',
        'maxresults': 1,
    }

    response = requests.get(uri, headers=headers, params=params)
    try:
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        print(str(e))
        return {}

# FUnction 6 to shrik pictures
def make_thumbnail(filename):
    img = Image.open(filename)

    (width, height) = img.size
    if width > height:
        ratio = 1200.0 / width
    else:
        ratio = 1200.0 / height

    img.thumbnail((round(width * ratio), round(height * ratio)), Image.LANCZOS)
    img.save(filename)
# ____________________________________________________________________________________________________________________________________#

# create a function to put the geotag data into a dictionary
# create a filed with file address to point to the image directory: ../static/Images/pic.jpg or  ../static/Images/uploads/pic.jpg

def ExtractPicData(picAddress):
    PicData={'latitude':"",'longitude':'','landmark':'','country':'','state':'','county':'','city':'','zipcode':'','ImageTimeStamp':'','FileAddress':''}
    exif = get_exif(picAddress)
    geotags = get_geotagging(exif)
    location = get_location(geotags)

    latitude=location['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude']
    longitude=location['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Longitude']
    landmark=location['Response']['View'][0]['Result'][0]['Location']['Address']['Label']
    country=location['Response']['View'][0]['Result'][0]['Location']['Address']['Country']
    state=location['Response']['View'][0]['Result'][0]['Location']['Address']['State']
    county=location['Response']['View'][0]['Result'][0]['Location']['Address']['County']
    city=location['Response']['View'][0]['Result'][0]['Location']['Address']['City']
    zipcode=location['Response']['View'][0]['Result'][0]['Location']['Address']['PostalCode']
    ImageTimeStamp=location['Response']['View'][0]['Result'][0]['Location']['MapReference']['MapReleaseDate']
    FileAddress=picAddress

    PicData['latitude']=latitude
    PicData['longitude']=longitude
    PicData['landmark']=landmark
    PicData['country']=country
    PicData['state']=state
    PicData['county']=county
    PicData['city']=city
    PicData['zipcode']=zipcode
    PicData['ImageTimeStamp']=ImageTimeStamp
    PicData['FileAddress']="../"+FileAddress

    
    
    return PicData
