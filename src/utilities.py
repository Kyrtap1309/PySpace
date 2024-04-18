import spiceypy
import numpy as np
import matplotlib.pyplot as plt

NAIF_PLANETS_ID = {
                    'Mars': 4,
                    'Jupiter': 5,
                    'Saturn': 6,
                    'Uran': 7,
                    'Neptun': 8,
                   }

PLANETS_COLOR = {
                    'Sun': 'gold',
                    'Mercury': 'maroon',
                    'Venus': 'palegoldenrod',
                    'Earth': 'mediumseagreen',
                    'Moon': 'silver',
                    'Mars': 'tomato',
                    'Jupiter': 'burlywood',
                    'Saturn': 'darkkhaki',
                    'Uran': 'paleturquoise', 
                    'Neptun': 'blue'
                }

PLANETS_SIZE = {
                    'Sun': 20,
                    'Mercury': 8,
                    'Venus': 11,
                    'Earth': 12,
                    'Moon': 6,
                    'Mars': 10,
                    'Jupiter': 15,
                    'Saturn': 17,
                    'Uran': 18, 
                    'Neptun': 19
                }

def kernels_load(kernels_path):
    for kernel_path in kernels_path:
        spiceypy.furnsh(kernel_path)

def merge_plots(plot1, plot2):
    plt.rcParams.update({'text.color': 'whit e'})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    plot1(ax1)  # Pierwsza funkcja na pierwszym subplotcie
    plot2(ax2)  # Druga funkcja na drugim subplotcie

    plt.tight_layout()  # Dopasowanie wykresów, aby nie nakładały się na siebie

    fig.set_facecolor('#1E2A4C')

    plt.show()  # Wyświetlenie wykresów`
    

    