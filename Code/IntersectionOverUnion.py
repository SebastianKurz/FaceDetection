from pprint import pprint


def points_in_intersection_area(actual_position, calculated_position):
    """
    Calculates all common points of the box of the ground-trouth and the calculated box
    """
    coordinate_points = []

    x_actual = actual_position.get("x", None)
    y_actual = actual_position.get("y", None)
    w_actual = actual_position.get("width", None)
    h_actual = actual_position.get("height", None)
    
    x_calculated = calculated_position.get("x", None)
    y_calculated = calculated_position.get("y", None)
    w_calculated = calculated_position.get("width", None)
    h_calculated =  calculated_position.get("height", None)

    x_min = x_actual if(x_actual <= x_calculated) else x_calculated
    y_min = y_actual if(y_actual <= y_calculated) else y_calculated
    x_max = (x_actual + w_actual - 1) if((x_actual + w_actual - 1) > (x_calculated + w_calculated -1)) else (x_calculated + w_calculated -1)
    y_max = (y_actual + h_actual - 1) if((y_actual + h_actual - 1) > (y_calculated + h_calculated -1)) else (y_calculated + h_calculated -1)

    for y in range(y_min , y_max):
        for x in range(x_min , x_max):
            x_in_actual =(x_actual <= x and x < (x_actual + w_actual))
            y_in_actual =(y_actual <= y and y < (y_actual + h_actual))
            x_in_calculated = (x_calculated <= x and x < (x_calculated + w_calculated))
            y_in_calculated = (y_calculated <= y and y < (y_calculated + h_calculated))

            if ((x_in_actual and y_in_actual) and (x_in_calculated and y_in_calculated)):
                coordinate_points.append({"x": x, "y": y})

    return coordinate_points


def intersection_area_position(coordinate_points):
    """
    Based on the results of the points_in_intersection_area method the coordinates of the intersection area
    will be determined in here. For this purpose the method seeks for the smalles and biggest x- and y 
    coordinate-points and returns the x-, y-, width-, and height-value of the intersection area.
    """
    x_min = None
    x_max = None
    y_min = None
    y_max = None

    for coordinate_point in coordinate_points:
        x = coordinate_point.get("x", None)
        y = coordinate_point.get("y", None)

        if(x_min == None and x_max == None and y_min == None and y_max == None):
            x_min = x
            x_max = x
            y_min = x
            y_max = x
        else:
            if(x <= x_min):
                x_min = x
            if(x_max <= x):
                x_max = x
            if(y <= y_min):
                y_min = y
            if(y_max <= y):
                y_max = y
    
    return {"x": x_min , "y": y_min, "width": (x_max -x_min + 1), "height": (y_max - y_min + 1)}

def pixel_sum(position):
    """
    Sums up the total count of pixels in the area limited by the coordinate points in position.
    """
    return position.get("width", None) * position.get("height", None)



def intersection_area_sum(actual_position, calculated_position):
    intersection_coordinate = intersection_area_position(points_in_intersection_area(actual_position, calculated_position))
    return pixel_sum(intersection_coordinate)


def union_area_sum(actual_position, calculated_position):
    return pixel_sum(actual_position) + pixel_sum(calculated_position) - intersection_area_sum(actual_position, calculated_position)


def intersection_over_union(actual_position, calculated_position):
    return intersection_area_sum(actual_position, calculated_position) / union_area_sum(actual_position, calculated_position)



# test
intersec = intersection_area_sum({"x": 2, "y": 2, "width": 5, "height": 4} , {"x": 3, "y": 1, "width": 5, "height": 4})
union = union_area_sum({"x": 2, "y": 2, "width": 5, "height": 4} , {"x": 3, "y": 1, "width": 5, "height": 4})
iou = intersection_over_union({"x": 2, "y": 2, "width": 5, "height": 4} , {"x": 3, "y": 1, "width": 5, "height": 4})
intersecCoordinates = intersection_area_position(points_in_intersection_area({"x": 2, "y": 2, "width": 5, "height": 4} , {"x": 3, "y": 1, "width": 5, "height": 4}))

pprint (intersecCoordinates)
print (str(intersec))
print (str(union))
print (str(iou))