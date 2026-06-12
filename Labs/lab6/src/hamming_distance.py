def hamming_distance(str1, str2):
    if str1 is None and str2 is None:
        raise TypeError("Both strings are None")

    if str1 is None or str2 is None:
        return -1

    if len(str1) != len(str2):
        raise ValueError("Strings must have equal length")

    distance = 0

    for char1, char2 in zip(str1, str2):
        if char1 != char2:
            distance += 1

    return distance
