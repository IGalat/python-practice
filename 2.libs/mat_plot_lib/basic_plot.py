import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# https://stackoverflow.com/questions/73745245/error-using-matplotlib-in-pycharm-has-no-attribute-figurecanvas
matplotlib.use("TkAgg")


def main() -> None:

    xpoints = np.array([1, 2, 6, 8])
    ypoints = np.array([3, 8, 1, 10])
    y2 = np.array([6, 2, 7, 11])

    plt.plot(xpoints, ypoints)
    plt.plot(xpoints, y2)
    plt.show()


if __name__ == "__main__":
    main()
