

def get_estimate_volume(current_volume, current_time: str) -> float:
    min_time = 0
    min_time_index = 0
    max_time = 0
    max_time_index = 0

    if is_between(int(current_time), 900, 905):
        return int(current_volume) * 15
    if is_between(int(current_time), 905, 910):
        min_time = 905
        min_time_index = 15
        max_time = 910
        max_time_index = 10
    if is_between(int(current_time), 910, 915):
        min_time = 910
        min_time_index = 10
        max_time = 915
        max_time_index = 8
    if is_between(int(current_time), 915, 930):
        min_time = 915
        min_time_index = 8
        max_time = 930
        max_time_index = 4.5
    if is_between(int(current_time), 930, 945):
        min_time = 930
        min_time_index = 4.5
        max_time = 945
        max_time_index = 3.5
    if is_between(int(current_time), 945, 1000):
        min_time = 945
        min_time_index = 3.5
        max_time = 1000
        max_time_index = 2.9
    if is_between(int(current_time), 1000, 1015):
        min_time = 1000
        min_time_index = 2.9
        max_time = 1015
        max_time_index = 2.5
    if is_between(int(current_time), 1015, 1030):
        min_time = 1015
        min_time_index = 2.5
        max_time = 1030
        max_time_index = 2.22
    if is_between(int(current_time), 1030, 1045):
        min_time = 1030
        min_time_index = 2.22
        max_time = 1045
        max_time_index = 2.01
    if is_between(int(current_time), 1045, 1100):
        min_time = 1045
        min_time_index = 2.01
        max_time = 1100
        max_time_index = 1.85
    if is_between(int(current_time), 1100, 1115):
        min_time = 1100
        min_time_index = 1.85
        max_time = 1115
        max_time_index = 1.74
    if is_between(int(current_time), 1115, 1130):
        min_time = 1115
        min_time_index = 1.74
        max_time = 1130
        max_time_index = 1.63
    if is_between(int(current_time), 1130, 1145):
        min_time = 1130
        min_time_index = 1.63
        max_time = 1145
        max_time_index = 1.54
    if is_between(int(current_time), 1145, 1200):
        min_time = 1145
        min_time_index = 1.54
        max_time = 1200
        max_time_index = 1.45
    if is_between(int(current_time), 1200, 1215):
        min_time = 1200
        min_time_index = 1.45
        max_time = 1215
        max_time_index = 1.38
    if is_between(int(current_time), 1215, 1230):
        min_time = 1215
        min_time_index = 1.38
        max_time = 1230
        max_time_index = 1.32
    if is_between(int(current_time), 1230, 1245):
        min_time = 1230
        min_time_index = 1.32
        max_time = 1245
        max_time_index = 1.26
    if is_between(int(current_time), 1245, 1300):
        min_time = 1245
        min_time_index = 1.26
        max_time = 1300
        max_time_index = 1.2
    if is_between(int(current_time), 1300, 1315):
        min_time = 1300
        min_time_index = 1.2
        max_time = 1315
        max_time_index = 1.11
    if is_between(int(current_time), 1315, 1330):
        min_time = 1315
        min_time_index = 1.11
        max_time = 1330
        max_time_index = 1

    time_diff_ratio = (max_time - int(current_time))/(max_time - min_time)
    ratio = max_time_index + ((min_time_index - max_time_index) * time_diff_ratio)
    return round(int(current_volume) * ratio)


def is_between(compare_int: int, min_int: int, max_int: int) -> bool:
    if min_int < compare_int <= max_int:
        return True
    else:
        return False
