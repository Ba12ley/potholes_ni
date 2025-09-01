from pyproj import Transformer

def xy2irishgrid(x, y):
    """
    Convert x and y coordinate integers into irish grid reference string
    """
    x = str(x)
    y = str(y)

    grid = [("V", "W", "X", "Y", "Z"),
            ("Q", "R", "S", "T", "U"),
            ("L", "M", "N", "O", "P"),
            ("F", "G", "H", "J", "K"),
            ("A", "B", "C", "D", "E")]

    if (len(x) > 6) | (len(y) > 6):
        return "Not in IRE"

    if len(x) < 6:
        easting_corr = '0'
        easting = x
    else:
        easting_corr = x[0]
        easting = x[1:]

    if len(y) < 6:
        northing_corr = '0'
        northing = y
    else:
        northing_corr = y[0]
        northing = y[1:]
    try:
        letter = grid[int(northing_corr)][int(easting_corr)]
    except:
        return "Not in IRE"
    grid_ref = '%s %s %s' % (letter, easting, northing)
    return grid_ref

def xy2latlon(x, y):
    transformer = Transformer.from_crs("epsg:29903", "epsg:4326")
    lat, lon = transformer.transform(x , y)
    lat, lon = round(lat,6), round(lon,6)
    return lat, lon