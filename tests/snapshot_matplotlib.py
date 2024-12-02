# Each PDF generated will have different /CreationDate field within metadata
# but visually identical

import matplotlib.pyplot as plt
import numpy as np


def generate_plot(output_file):
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    plt.figure(figsize=(6, 4))
    plt.plot(x, y, label="Sine Wave")
    plt.title("Example Plot")
    plt.xlabel("Angle [rad]")
    plt.ylabel("sin(x)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file, format="pdf")
    plt.close()

    return output_file
