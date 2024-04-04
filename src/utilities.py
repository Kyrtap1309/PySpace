import spiceypy
import numpy as np
import matplotlib.pyplot as plt

def kernels_load(kernels_path):
    for kernel_path in kernels_path:
        spiceypy.furnsh(kernel_path)

def merge_plots(plot1, plot2):
    plt.rcParams.update({'text.color': 'white'})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    plot1(ax1)  # Pierwsza funkcja na pierwszym subplotcie
    plot2(ax2)  # Druga funkcja na drugim subplotcie

    plt.tight_layout()  # Dopasowanie wykresów, aby nie nakładały się na siebie

    fig.set_facecolor('#1E2A4C')

    plt.show()  # Wyświetlenie wykresów`
    

    