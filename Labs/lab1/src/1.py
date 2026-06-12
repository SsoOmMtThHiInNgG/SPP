def distribution(numbers: list[int]) -> dict[int, int]:
    result: dict[int, int] = {}

    for number in numbers:
        digits = len(str(abs(number)))
        result[digits] = result.get(digits, 0) + 1

    return dict(sorted(result.items()))


nums = list(map(int, input().split()))

for key, value in distribution(nums).items():
    print(f"{key}-digit: {value}")
