def hamming_weight(number: int) -> int:
    if number < 0:
        raise ValueError("Number must be non-negative")

    return bin(number).count("1")


n = int(input())

print(hamming_weight(n))
