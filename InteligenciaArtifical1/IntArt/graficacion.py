import numpy as np
import matplotlib.pyplot as plt


def plot_2d_function(func, x_range=(-3, 3), y_range=(-3, 3), points=300, cmap="viridis"):
    x = np.linspace(x_range[0], x_range[1], points)
    y = np.linspace(y_range[0], y_range[1], points)
    X, Y = np.meshgrid(x, y)
    Z = func(X, Y)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    surface = ax.plot_surface(X, Y, Z, cmap=cmap, linewidth=0, antialiased=True)
    fig.colorbar(surface, ax=ax, shrink=0.6, label="f(x, y)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(x, y)")
    ax.set_title("Gráfica 3D de f(x, y)")
    plt.show()


if __name__ == "__main__":
    def booth(x, y):
        return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2
    
    def peaks(x, y):
        return  3*(1 - x)**2 * np.exp(-(x**2) - (y + 1)**2) \
            - 10*(x/5 - x**3 - y**5) * np.exp(-x**2 - y**2) \
            - (1/3)*np.exp(-(x + 1)**2 - y**2)

    #plot_2d_function(booth, x_range=(-10, 10), y_range=(-10, 10), points=400)
    plot_2d_function(peaks, x_range=(-10, 10), y_range=(-10, 10), points=400)