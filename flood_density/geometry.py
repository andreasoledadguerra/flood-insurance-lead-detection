
from shapely.geometry import Polygon


class Geometry:
    def __init__(self):

#Function that convert dictionary of coordinates in polygon
    def coordinates_to_box(coord : dict)-> Polygon:
    
        return box(
            coord['x_min'],
            coord['y_min'],
            coord['x_max'],
            coord['y_max'],
        )
    
    def extract_bounds_polygon(coordinates: Dict[str, float]) -> Polygon:
       return Polygon([
           (coordinates["x_min"], coordinates["y_min"]),   # SW (suroeste)
           (coordinates["x_max"], coordinates["y_min"]),   # SE (sureste)  
           (coordinates["x_max"], coordinates["y_max"]),   # NE (noreste)
           (coordinates["x_min"], coordinates["y_max"]),   # NW (noroeste)
           (coordinates["x_min"], coordinates["y_min"])    # Cerrar polígono
       ])
    
    def points_geocoordinates(df: pd.DataFrame) -> Polygon:
     # Crear geometría de puntos usando X,Y como longitud,latitud
     geometry = [Point(xy) for xy in zip(df['X'], df['Y'])]
     return Polygon(geometry)