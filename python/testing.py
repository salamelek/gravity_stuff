# points = ["a", "b", "c", "d", "e"]
points = ["a", "b"]

for i in range(len(points)):
    for j in range(len(points) - (i + 1)):
        a = points[i]
        b = points[j + 1 + i]

        print(a, b)

