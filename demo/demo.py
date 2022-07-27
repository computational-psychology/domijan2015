"""
This Python script demonstrates how the Domijan model could be used to reproduce all the results
shown in the original paper: Domijan (2015): A Neurocomputational account of the role of contour
facilitation in brightness perception

This Python code was adapted from MATLAB scripts that were kindly provided by Drazan Domijan.

@authors: Matko Matic & Lynn Schmittwilken
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from domijan2015 import utils
from domijan2015 import main


def run_demo():
    # Do you want to save the result plots?´
    save_plot = True
    S = 20

    # If you want to run specific inputs, use list of the indices you want instead of range(1,13)
    for i in range(1, 13):
        # Create the input stimulus:
        input_stim, illusion_name, cut_height = utils.generate_input(i)
        M, N = input_stim.shape
        print("Processing stimulus " + str(i) + ": " + illusion_name)

        # Run the model:
        res = main.main(input_stim, S, extensive=False)
        model_output = res["model_output"]
        model_output = utils.remove_surround(model_output, int(S/2))

        if save_plot:
            # Create outputs folder:
            result_folder = 'model_outputs/'
            save_path = result_folder + illusion_name
            if not os.path.exists(result_folder):
                os.mkdir(result_folder)

            # Plot: Brightness estimate
            plot_result(save_path, input_stim, model_output, cut_height-int(S/2))


def plot_result(save_path, input_image, bright, cut_height):
    plt.figure(figsize=(22, 6))
    plt.subplot(131)
    plt.imshow(input_image, cmap='gray')
    plt.title('Input stimulus')
    plt.colorbar()

    plt.subplot(132)
    plt.imshow(bright, cmap='coolwarm')
    plt.axhline(y=cut_height, color='k')
    plt.title('Brightness output')
    plt.clim(-bright.max(), bright.max())
    plt.colorbar()

    plt.subplot(133)
    x_ax = np.arange(0, np.size(bright, 1))
    plt.plot(x_ax, np.squeeze(bright[cut_height, :]), 'k')
    plt.ylim([-0.1, 1.1])
    plt.xlim([0, bright.shape[1]])
    plt.title('Cut through')
    plt.savefig(save_path + '.png')
    plt.close()


if __name__ == "__main__":
    run_demo()
