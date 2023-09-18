# %%
from PIL import Image
import glob
from exif import Image

# %%
def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref =='W' :
        decimal_degrees = -decimal_degrees
    return decimal_degrees

files = glob.glob('*.jpg')

for path in files:
    print('###', path)
    with open(path, 'rb') as f:
        image = Image(f)
    if image.has_exif is None:
        continue
    try:
        image.gps_longitude
    except AttributeError:
        print ('No GPS Info')
        continue
    print(image.gps_latitude)
    print()
    coords = (decimal_coords(image.gps_latitude, image.gps_latitude_ref)
              , decimal_coords(image.gps_longitude,image.gps_longitude_ref))
    print(coords[0], ',', coords[1])
    print('lat', coords[0])
    print('lng', coords[1])


