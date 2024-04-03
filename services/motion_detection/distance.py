import math


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_closes_point(x1, y1, arr):
    closest_point = None
    for x2, y2 in arr:
        distance = calculate_distance(x1, y1, x2, y2)
        if closest_point is None or distance < closest_point[2]:
            closest_point = (x2, y2, distance)
    if closest_point:
        arr.remove(closest_point[:2])
    return closest_point


def estimate_new_position(arr_n, arr_m):
    res = []

    for x1, y1 in arr_n:
        closest_point = get_closes_point(x1, y1, arr_m)
        if closest_point:
            res.append(closest_point[:2])
        # for any remaining points in arr_m, add to res
    if len(arr_n) < len(arr_m):
        for i in range(len(arr_m) - len(arr_n)):
            res.append(arr_m[i])
    return res


if __name__ == '__main__':
    arr_m = [(1, 1)]
    arr_n = [(4, 5), (1, 3)]
    print(estimate_new_position(arr_m, arr_n))


