"""
This Python script can be used to compare our Python implementation of the Domijan2015 model with
the outputs of the original MATLAB scripts that were kindly provided by Drazan Domijan.

This script compares the brightness estimates produced by the MATLAB implementation with the
brightness estimates of our Python implementation by plotting those outputs side-by-side as well
as plotting their pixel-wise difference.

@authors: Matko Matic & Lynn Schmittwilken
"""

import os
import sys
import matplotlib.pyplot as plt
import scipy.io as sio

sys.path.append('..')
from domijan2015 import utils
from domijan2015 import main


def run_comparison():
    # Do you want to save the result plots?´
    save_plot = True

    # Amount of padding to add a gray background behind the stimuli:
    S = 20

    # If you want to run specific inputs, use list of the indices you want instead of range(1,13)
    for i in range(1, 13):
        print("Processing stimulus", str(i))
        # Create the input stimulus:
        input_stim, illusion_name, _ = utils.generate_input(i)

        # Run the model:
        res = main.main(input_stim, S)
        bright = res["image"]

        # Load Matlab model outputs:
        outputs_mat = sio.loadmat('./matlab_ground_truth/' + illusion_name + '.mat')
        bright_mat = outputs_mat['bright']

        if save_plot:
            # Create outputs folder for comparisons:
            result_folder = 'matlab_comparisons/'
            save_path = result_folder + illusion_name
            if not os.path.exists(result_folder):
                os.mkdir(result_folder)

            # Plot 3: Brightness estimates for Matlab and Python outputs and their differences:
            plot_comparison(save_path, bright_mat, bright)


def plot_comparison(save_path, bright_mat, bright):
    # Plot differences between Matlab and Python model output:
    plt.figure(figsize=(22, 6))
    plt.subplot(131)
    plt.imshow(bright_mat, cmap='coolwarm')
    plt.title('Brightness output: MATLAB')
    plt.clim(-bright_mat.max(), bright_mat.max())
    plt.colorbar()

    plt.subplot(132)
    plt.imshow(bright, cmap='coolwarm')
    plt.title('Brightness output: Python')
    plt.clim(-bright.max(), bright.max())
    plt.colorbar()

    plt.subplot(133)
    plt.imshow(bright_mat-bright, cmap='coolwarm')
    plt.title('Brightness output: Differences')
    plt.colorbar()
    plt.savefig(save_path + '.png')
    plt.close()


run_comparison()
