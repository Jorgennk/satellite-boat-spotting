from pyproj import Proj, transform

# Define the projection for UTM Zone 33N
utm33n = Proj(proj='utm', zone=33, ellps='WGS84', datum='WGS84', units='m', north=True)

# Define the projection for WGS84
wgs84 = Proj(proj='latlong', datum='WGS84')

# Convert coordinates
coordinates = [
    (247560.71568, 6624439.078240001),
    (247688.71568, 6624439.078240001)
]

# Transform the coordinates
latlong_coords = [transform(utm33n, wgs84, x, y) for x, y in coordinates]

for idx, (lon, lat) in enumerate(latlong_coords):
    print(f"Coordinate {idx + 1}: Longitude = {lon}, Latitude = {lat}")
