import matplotlib.pyplot as plt


def plot(points, path: list, title):
    x = []
    y = []
    labels = ["{0}".format(i) for i in range(1, len(points) + 1)]
    for point in points:
        x.append(point[0])
        y.append(point[1])
    plt.plot(x, y, 'bo')
    for _ in range(1, len(path)):
        i = path[_ - 1] - 1
        j = path[_] - 1
        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)

    plt.xlim(-0.1 * max(x), max(x) * 1.1)
    plt.ylim(-0.1 * max(y), max(y) * 1.1)
    plt.title(title)
    for _ in range(len(points)):
        plt.annotate(labels[_], (x[_], y[_]))
    plt.show()
