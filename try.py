import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geojson
from geographiclib.geodesic import Geodesic

def calculate_azimuth_and_elevation(v0, artillery_lat, artillery_lon, target_lat, target_lon):
    """
    Calculate azimuth, elevation angle, and range to the target.
    """
    g = 9.81  # Gravity (m/s^2)

    # Compute geodesic distance and azimuth
    geod = Geodesic.WGS84
    location = geod.Inverse(artillery_lat, artillery_lon, target_lat, target_lon)
    distance = location['s12']  # Distance in meters
    azimuth = location['azi1']  # Azimuth in degrees

    # Calculate elevation angle using projectile motion equation
    theta_rad = np.arcsin((distance * g) / (v0**2)) / 2
    elevation = np.degrees(theta_rad)

    return azimuth, elevation, distance

def calculate_trajectory_points(v0, artillery_lat, artillery_lon, elevation_angle_deg, azimuth, num_points=100):
    """
    Compute trajectory points in latitude and longitude.
    """
    g = 9.81  # Gravity (m/s^2)
    elevation_angle_rad = np.radians(elevation_angle_deg)
    azimuth_rad = np.radians(azimuth)

    # Compute time of flight
    t_flight = (2 * v0 * np.sin(elevation_angle_rad)) / g
    t = np.linspace(0, t_flight, num_points)

    # Compute Cartesian trajectory
    x = v0 * np.cos(elevation_angle_rad) * t
    y = v0 * np.sin(elevation_angle_rad) * t - 0.5 * g * t**2

    # Convert to geographic coordinates
    geod = Geodesic.WGS84
    trajectory_points = []
    for xi, yi in zip(x, y):
        if yi >= 0:  # Only include points above ground
            point = geod.Direct(artillery_lat, artillery_lon, azimuth, xi)
            trajectory_points.append((point['lat2'], point['lon2']))
    return trajectory_points

def plot_trajectory_on_map(trajectory_points, artillery_lat, artillery_lon, target_lat, target_lon):
    """
    Plot trajectory on a real-world map using Cartopy.
    """
    # Setup the map
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([artillery_lon - 0.1, target_lon + 0.1, artillery_lat - 0.05, target_lat + 0.05], crs=ccrs.PlateCarree())

    # Add map features
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    # Plot trajectory
    lats, lons = zip(*trajectory_points)
    ax.plot(lons, lats, color='blue', label='Projectile Trajectory', transform=ccrs.PlateCarree())

    # Plot artillery and target locations
    ax.plot(artillery_lon, artillery_lat, 'ro', label='Artillery Location', transform=ccrs.PlateCarree())
    ax.plot(target_lon, target_lat, 'go', label='Target Location', transform=ccrs.PlateCarree())

    # Add labels and legend
    plt.title('Artillery Projectile Trajectory on Map', fontsize=16)
    plt.legend(fontsize=12)
    plt.show()

def export_to_geojson(trajectory_points, filename='trajectory.geojson'):
    """
    Export trajectory points to a GeoJSON file for CesiumJS or Google Earth.
    """
    features = []
    for lat, lon in trajectory_points:
        point = geojson.Point((lon, lat))
        features.append(geojson.Feature(geometry=point))
    feature_collection = geojson.FeatureCollection(features)
    
    with open(filename, 'w') as f:
        geojson.dump(feature_collection, f)
    
    print(f"Trajectory exported to {filename}")

# Example Inputs
initial_velocity = 800  # m/s
artillery_latitude = 22.29488
artillery_longitude = 73.14240
target_latitude = 22.33211
target_longitude = 73.21690

# Compute azimuth, elevation, and range
azimuth, elevation, range_distance = calculate_azimuth_and_elevation(
    initial_velocity, artillery_latitude, artillery_longitude, target_latitude, target_longitude
)

# Compute trajectory points
trajectory = calculate_trajectory_points(initial_velocity, artillery_latitude, artillery_longitude, elevation, azimuth)

# Plot trajectory on the real-world map
plot_trajectory_on_map(trajectory, artillery_latitude, artillery_longitude, target_latitude, target_longitude)

# Export to GeoJSON for 3D visualization
export_to_geojson(trajectory)
