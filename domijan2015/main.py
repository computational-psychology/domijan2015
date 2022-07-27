"""
This Python code was adapted from MATLAB scripts that were kindly provided by
Drazan Domijan.

This code contains the re-implementation of the brightness perception model
described in:
Domijan (2015): A Neurocomputational account of the role of contour facilitation
in brightness perception

It can be used to reproduce all the results that were presented in the paper.
For more details, see functions.py

@author: lynn schmittwilken
"""

from . import utils, retina, boundary_detection, filling_in


def main(stimulus, S=20, extensive=False, crop=True):
    """
    Parameters
    -----------
    stimulus : Stimulus object
        stimulus on which the model should be run
    S : int
        size of the added padding during the model calculation (originally 20)
    extensive : bool
        should the model return intermediate results or not (e.g., used for the demo script
        to be able to plot the intermediate results)
    crop : bool
        if True, crop the model output to the input size

    Returns
    -----------
    {"model_output": output image} or {"model_output": output image, <all the intermediate results>}
    """
    input_image = utils.add_surround(stimulus, S)

    # Extract contrast and luminance information:
    c_ON, c_OFF, l_ON, l_OFF = retina.run(input_image, int(S / 2))

    # Contrast and luminance integration in the ON channel:
    w1 = 3.
    w2 = 1.
    m_ON = w1*c_ON + w2*l_ON

    # Contrast and lumiance integration in the OFF channel
    m_OFF = w1*c_OFF + w2*l_OFF

    # Contour detection and processing:
    bcs_res = boundary_detection.BCS(c_ON, c_OFF, extensive=extensive)
    R = bcs_res["R"]

    # Filling-in:
    bright, M_ON, M_OFF = filling_in.fill_in(R, m_ON, m_OFF)

    if crop:
        bright = utils.remove_surround(bright, int(S/2))

    if extensive:
        output = {"c_ON": c_ON,
                  "c_OFF": c_OFF,
                  "l_ON": l_ON,
                  "l_OFF": l_OFF,
                  "M_ON": M_ON,
                  "M_OFF": M_OFF,
                  "R_h": bcs_res["R_h"],
                  "R_v": bcs_res["R_v"],
                  "model_output": bright,
                  "LBD_h": bcs_res["LBD_h"],
                  "LBD_v": bcs_res["LBD_v"],
                  "GBD_h": bcs_res["GBD_h"],
                  "GBD_v": bcs_res["GBD_v"]}
    else:
        output = {"model_output": bright}

    return output
