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

    # Amount of padding to add a gray background behind the stimuli:
    S = 20

    # If you want to run specific inputs, use list of the indices you want instead of range(1,13)
    for i in range(1, 13):
        print("Processing stimulus", str(i))
        # Create the input stimulus:
        input_stim, illusion_name, cut_height = utils.generate_input(i)
        M, N = input_stim.shape

        # Run the model:
        res = main.main(input_stim, S, extensive=True)
        c_ON, c_OFF, l_ON, l_OFF, M_ON, M_OFF, LBD_h, LBD_v, GBD_h, GBD_v, R_h, R_v, bright = \
            res["c_ON"], res["c_OFF"], res["l_ON"], res["l_OFF"], res["M_ON"], res["M_OFF"], \
            res["LBD_h"], res["LBD_v"], res["GBD_h"], res["GBD_v"], res["R_h"], res["R_v"], res["image"]

        if save_plot:
            # Create outputs folder:
            result_folder = 'outputs/'
            save_path = result_folder + illusion_name
            if not os.path.exists(result_folder):
                os.mkdir(result_folder)

            # Plot 1: Contrast, luminance and filling-in outputs
            plot1(save_path, c_ON, c_OFF, l_ON, l_OFF, M_ON, M_OFF)

            # Plot 2: BCS outputs
            plot2(save_path, LBD_h, LBD_v, GBD_h, GBD_v, R_h, R_v)

            # Plot 3: Brightness estimate
            plot3(save_path, input_stim, bright, cut_height, N + S)


# Plot first part of results:
def plot1(save_path, c_ON, c_OFF, l_ON, l_OFF, M_ON, M_OFF):
    cmap = 'coolwarm'
    plt.figure(figsize=(15, 15))
    plt.subplot(321)
    plt.imshow(c_ON, cmap=cmap)
    plt.axis('off')
    plt.title('ON network: contrast')
    plt.clim(-c_ON.max(), c_ON.max())
    plt.colorbar()

    plt.subplot(322)
    plt.imshow(c_OFF, cmap=cmap)
    plt.axis('off')
    plt.title('OFF network: contrast')
    plt.clim(-c_OFF.max(), c_OFF.max())
    plt.colorbar()

    plt.subplot(323)
    plt.imshow(l_ON, cmap=cmap)
    plt.axis('off')
    plt.title('ON network: luminance')
    plt.clim(-l_ON.max(), l_ON.max())
    plt.colorbar()

    plt.subplot(324)
    plt.imshow(l_OFF, cmap=cmap)
    plt.axis('off')
    plt.title('OFF network: luminance')
    plt.clim(-l_OFF.max(), l_OFF.max())
    plt.colorbar()

    plt.subplot(325)
    plt.imshow(M_ON, cmap=cmap)
    plt.axis('off')
    plt.title('ON network: filled')
    plt.clim(-M_ON.max(), M_ON.max())
    plt.colorbar()

    plt.subplot(326)
    plt.imshow(M_OFF, cmap=cmap)
    plt.axis('off')
    plt.title('OFF network: filled')
    plt.clim(-M_OFF.max(), M_OFF.max())
    plt.colorbar()
    plt.savefig(save_path + '1.png')
    plt.close()


# Plot second part of results:
def plot2(save_path, LBD_h, LBD_v, GBD_h, GBD_v, R_h, R_v):
    cmap = 'coolwarm'
    plt.figure(figsize=(15, 15))
    plt.subplot(321)
    plt.imshow(LBD_h, cmap=cmap)
    plt.axis('off')
    plt.title('Local boundaries')
    plt.clim(-LBD_h.max(), LBD_h.max())
    plt.colorbar()

    plt.subplot(322)
    plt.imshow(LBD_v, cmap=cmap)
    plt.axis('off')
    plt.title('Local boundaries')
    plt.clim(-LBD_v.max(), LBD_v.max())
    plt.colorbar()

    plt.subplot(323)
    plt.imshow(GBD_h, cmap=cmap)
    plt.axis('off')
    plt.title('Global boundaries')
    plt.clim(-GBD_h.max(), GBD_h.max())
    plt.colorbar()

    plt.subplot(324)
    plt.imshow(GBD_v, cmap=cmap)
    plt.axis('off')
    plt.title('Global boundaries')
    plt.clim(-GBD_v.max(), GBD_v.max())
    plt.colorbar()

    plt.subplot(325)
    plt.imshow(R_h, cmap=cmap)
    plt.axis('off')
    plt.title('Integration')
    plt.clim(-R_h.max(), R_h.max())
    plt.colorbar()

    plt.subplot(326)
    plt.imshow(R_v, cmap=cmap)
    plt.axis('off')
    plt.title('Integration')
    plt.clim(-R_v.max(), R_v.max())
    plt.colorbar()
    plt.savefig(save_path + '2.png')
    plt.close()


# Plot third part of results:
def plot3(save_path, input_image, bright, cut_height, NS):
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
    plt.xlim([0, NS])
    plt.title('Cut through')
    plt.savefig(save_path + '3.png')
    plt.close()


if __name__ == "__main__":
    run_demo()
