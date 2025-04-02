import json
import numpy as np
from shapely.geometry import shape, Point

def generate_maze(geojson_file, output_file, grid_size=50):
    """
    Generates a maze from a GeoJSON file containing building data.

    :param geojson_file: Path to the GeoJSON file with building data.
    :param output_file: Path to save the generated maze file.
    :param grid_size: Number of rows and columns in the grid.
    """
    # Load the GeoJSON file
    with open(geojson_file, "r") as f:
        data = json.load(f)

    # Extract the bounding box from the GeoJSON file
    features = data["features"]
    all_coords = []
    for feature in features:
        if feature["geometry"]["type"] == "Polygon":
            all_coords.extend(feature["geometry"]["coordinates"][0])
    all_coords = np.array(all_coords)
    min_lon, min_lat = all_coords.min(axis=0)
    max_lon, max_lat = all_coords.max(axis=0)

    # Define the grid
    latitudes = np.linspace(min_lat, max_lat, grid_size)
    longitudes = np.linspace(min_lon, max_lon, grid_size)
    maze = [[" " for _ in range(grid_size)] for _ in range(grid_size)]

    # Mark buildings as walls in the grid
    for feature in features:
        if feature["geometry"]["type"] == "Polygon":
            building = shape(feature["geometry"])
            for i, lat in enumerate(latitudes):
                for j, lon in enumerate(longitudes):
                    point = Point(lon, lat)
                    if building.contains(point):
                        maze[i][j] = "#"

    # Add start (A) and goal (B) points
    maze[1][1] = "A"  # Top-left corner
    maze[-2][-2] = "B"  # Bottom-right corner

    # Save the maze to a text file
    with open(output_file, "w") as f:
        for row in maze:
            f.write("".join(row) + "\n")

    print(f"Maze saved as {output_file}")


if __name__ == "__main__":
    # Input GeoJSON file and output maze file
    geojson_file = "map/export.geojson"  # Path to the GeoJSON file
    output_file = "maze4.txt"  # Path to save the maze file

    # Generate the maze
    generate_maze(geojson_file, output_file)