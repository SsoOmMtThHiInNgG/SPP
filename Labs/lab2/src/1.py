class FloatSet:
    def __init__(self, items=None):
        self.items = []

        if items:
            for item in items:
                self.add(item)

    def add(self, value):
        if value not in self.items:
            self.items.append(float(value))

    def remove(self, value):
        self.items.remove(float(value))

    def contains(self, value):
        return float(value) in self.items

    def union(self, other):
        return FloatSet(self.items + other.items)

    def __eq__(self, other):
        return sorted(self.items) == sorted(other.items)

    def __str__(self):
        return str(self.items)


a = FloatSet([1.1, 2.2, 3.3])
b = FloatSet([3.3, 4.4])

print(a.union(b))
print(a.contains(2.2))
