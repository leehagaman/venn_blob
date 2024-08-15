import numpy as np

# learned about this from https://happyruin.wordpress.com/2013/03/24/edwards-venn-diagrams/


def rounded_rect_curve(left_edge, right_edge, top_edge, bottom_edge, rounded_corners_radius, num_points):

    horizontal_segment_dist = right_edge - left_edge - 2 * rounded_corners_radius
    vertical_segment_dist = top_edge - bottom_edge - 2 * rounded_corners_radius
    straight_dist = 2 * horizontal_segment_dist + 2 * vertical_segment_dist
    curved_dist = 2 * np.pi * rounded_corners_radius
    curved_corner_dist = curved_dist / 4
    total_dist = straight_dist + curved_dist
    spacing = num_points / total_dist
    num_points_per_curve = int(curved_corner_dist * spacing)
    angular_spacing = (np.pi / 2) / num_points_per_curve
    curve = []
    for i in range(int(horizontal_segment_dist * spacing)):
        curve.append([left_edge + rounded_corners_radius + i / spacing, bottom_edge])
    for i in range(num_points_per_curve):
        theta = -np.pi / 2 + i * angular_spacing
        curve.append([right_edge - rounded_corners_radius + rounded_corners_radius * np.cos(theta), bottom_edge + rounded_corners_radius + rounded_corners_radius * np.sin(theta)])
    for i in range(int(vertical_segment_dist * spacing)):
        curve.append([right_edge, bottom_edge + rounded_corners_radius + i / spacing])
    for i in range(num_points_per_curve):
        theta = i * angular_spacing
        curve.append([right_edge - rounded_corners_radius + rounded_corners_radius * np.cos(theta), top_edge - rounded_corners_radius + rounded_corners_radius * np.sin(theta)])
    for i in range(int(horizontal_segment_dist * spacing)):
        curve.append([right_edge - rounded_corners_radius - i / spacing, top_edge])
    for i in range(num_points_per_curve):
        theta = np.pi / 2 + i * angular_spacing
        curve.append([left_edge + rounded_corners_radius + rounded_corners_radius * np.cos(theta), top_edge - rounded_corners_radius + rounded_corners_radius * np.sin(theta)])
    for i in range(int(vertical_segment_dist * spacing)):
        curve.append([left_edge, top_edge - rounded_corners_radius - i / spacing])
    for i in range(num_points_per_curve):
        theta = np.pi + i * angular_spacing
        curve.append([left_edge + rounded_corners_radius + rounded_corners_radius * np.cos(theta), bottom_edge + rounded_corners_radius + rounded_corners_radius * np.sin(theta)])

    return np.array(curve)


def make_edwards_venn(n, num_points):

    curves = []
    if n >= 1: # circle
        curve = []
        for i in range(num_points):
            theta = 2*np.pi*i/num_points
            x = np.cos(theta)
            y = np.sin(theta)
            curve.append([x, y])
        curves.append(np.array(curve))
    
    if n >= 2: # bottom hemisphere
        right_edge = 3
        left_edge = -3
        top_edge = 0
        bottom_edge = -1.75
        rounded_corners_radius = 0.3
        curves.append(rounded_rect_curve(left_edge, right_edge, top_edge, bottom_edge, rounded_corners_radius, num_points))

    if n >= 3: # right hemispheres
        right_edge = 3.25
        left_edge = 0
        top_edge = 1.5
        bottom_edge = -1.5
        rounded_corners_radius = 0.3
        curves.append(rounded_rect_curve(left_edge, right_edge, top_edge, bottom_edge, rounded_corners_radius, num_points))

        
    if n >= 4: # tennis-ball-like sections

        for curr_n in range(4, n+1):

            iteration = curr_n - 4
            num_circles = 4 * 2**iteration

            circle_center_radius = 1 / np.cos(np.pi/num_circles)
            circle_radius = np.tan(np.pi / num_circles)

            curve = []
            estimated_total_dist = num_circles * np.pi * circle_radius
            num_points_per_dist = num_points / estimated_total_dist
            for j in range(num_circles):

                theta_j_center = 2*np.pi*j/num_circles
                theta_j_start = theta_j_center - np.pi/num_circles
                convex = (j % 2 == 0)

                center_x = circle_center_radius * np.cos(theta_j_center)
                center_y = circle_center_radius * np.sin(theta_j_center)

                if convex:
                    circle_arc_measure = np.pi + 2 * np.pi/num_circles
                    curr_num_points = int(num_points_per_dist * circle_arc_measure * circle_radius)
                    for i in range(curr_num_points):
                        theta = theta_j_start - np.pi/2 + circle_arc_measure * i / curr_num_points
                        x = center_x + circle_radius * np.cos(theta)
                        y = center_y + circle_radius * np.sin(theta)
                        curve.append([x, y])
                else:
                    circle_arc_measure = np.pi - 2 * np.pi/num_circles
                    curr_num_points = int(num_points_per_dist * circle_arc_measure * circle_radius)
                    for i in range(curr_num_points):
                        theta = theta_j_start - np.pi / 2 - circle_arc_measure * i / curr_num_points
                        x = center_x + circle_radius * np.cos(theta)
                        y = center_y + circle_radius * np.sin(theta)
                        curve.append([x, y])
            curves.append(np.array(curve))

    return curves

