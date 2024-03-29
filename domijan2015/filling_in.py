"""
This Python code was adapted from MATLAB scripts that were kindly provided by
Drazan Domijan.

It contains additional functions relevant for the brightess perception model
described in:
Domijan (2015): A Neurocomputational account of the role of contour facilitation
in brightness perception

@author: lynn schmittwilken
"""

import numpy as np
import copy

if __package__ is None or __package__ == "":
    import utils
else:
    from . import utils


def fill_in(R, m_ON, m_OFF):
    """
    Function that generates brightness percept based on filing-in
    R: output of Boundary Contour System
    m_ON: combined output from ON contrast and luminance pathways
    m_OFF: combined output from OFF contrast and luminance pathways
    """

    M, N = m_ON.shape
    eps = 10.  # Controls the strength of divisive inhibition
    T_f = 3.   # Prevents filling-in for weak luminance and contrast signals

    # Initiate all relevant variables:
    # NOTE: We initiate all variable slightly larger to efficiently compute the MAX function
    # Edge map from BCS that prevents acitivity spreading across edges:
    edge = np.zeros([M+2, N+2])
    edge[1:M+1, 1:N+1] = R

    # Threshold outputs from the ON and OFF Contrast and Luminance Pathways for filling-in:
    M_ON = np.zeros([M+2, N+2])
    M_ON[1:M+1, 1:N+1] = utils.sigmoid(14., m_ON)
    M_ON_temp = copy.deepcopy(M_ON)

    M_OFF = np.zeros([M+2, N+2])
    M_OFF[1:M+1, 1:N+1] = utils.sigmoid(14., m_OFF)
    M_OFF_temp = copy.deepcopy(M_OFF)

    # Binarize outputs from the ON and OFF Contrast and Luminance Pathways to prevent
    # spreading to non-active units:
    mask_ON = np.zeros([M+2, N+2])
    mask_ON[1:M+1, 1:N+1] = utils.heaviside(m_ON - T_f)

    mask_OFF = np.zeros([M+2, N+2])
    mask_OFF[1:M+1, 1:N+1] = utils.heaviside(m_OFF - T_f)

    # Variables to efficiently compute the MAX function between neighboring pixels:
    top_ON = np.zeros([M+2, N+2])
    bottom_ON = np.zeros([M+2, N+2])
    left_ON = np.zeros([M+2, N+2])
    right_ON = np.zeros([M+2, N+2])

    top_OFF = np.zeros([M+2, N+2])
    bottom_OFF = np.zeros([M+2, N+2])
    left_OFF = np.zeros([M+2, N+2])
    right_OFF = np.zeros([M+2, N+2])

    # In order to visualize the filling-in process over time:
    fill_steps = 300  # (Domijan-code: 300, Paper: 200)
    M_ON_vid = np.zeros([M+2, N+2, fill_steps])
    M_OFF_vid = np.zeros([M+2, N+2, fill_steps])

    # Compute the recurrent MAX function among the nearest neighbors
    # (one pixel up, down, left, right)
    for t in range(fill_steps):
        # TODO: Potentially implement MAX-function as standalone
        # Select the nearest neighbors (top, bottom, left, right)
        # IMPORTANT: Activity at borders is "penalized" / strongly reduced
        top_ON[1:M+1, 1:N+1]    = M_ON[0:M,   1:N+1] / (1+eps*edge[0:M,   1:N+1] *edge[1:M+1, 1:N+1])
        bottom_ON[1:M+1, 1:N+1] = M_ON[2:M+2, 1:N+1] / (1+eps*edge[2:M+2, 1:N+1] *edge[1:M+1, 1:N+1])
        left_ON[1:M+1, 1:N+1]   = M_ON[1:M+1, 0:N]   / (1+eps*edge[1:M+1, 0:N]   *edge[1:M+1, 1:N+1])
        right_ON[1:M+1, 1:N+1]  = M_ON[1:M+1, 2:N+2] / (1+eps*edge[1:M+1, 2:N+2] *edge[1:M+1, 1:N+1])

        # Select the nearest neighbors (top, bottom, left, right)
        # IMPORTANT: Activity at borders is "penalized" / strongly reduced
        top_OFF[1:M+1, 1:N+1]    = M_OFF[0:M,   1:N+1] / (1+eps*edge[0:M,   1:N+1] *edge[1:M+1, 1:N+1])
        bottom_OFF[1:M+1, 1:N+1] = M_OFF[2:M+2, 1:N+1] / (1+eps*edge[2:M+2, 1:N+1] *edge[1:M+1, 1:N+1])
        left_OFF[1:M+1, 1:N+1]   = M_OFF[1:M+1, 0:N]   / (1+eps*edge[1:M+1, 0:N]   *edge[1:M+1, 1:N+1])
        right_OFF[1:M+1, 1:N+1]  = M_OFF[1:M+1, 2:N+2] / (1+eps*edge[1:M+1, 2:N+2] *edge[1:M+1, 1:N+1])

        # Select the MAX value between top_ON, bottom_ON, left_ON, right_ON:
        M_ON_temp[1:M+1, 1:N+1] = np.maximum(top_ON[1:M+1, 1:N+1], bottom_ON[1:M+1, 1:N+1])
        M_ON_temp[1:M+1, 1:N+1] = np.maximum(M_ON_temp[1:M+1, 1:N+1], left_ON[1:M+1, 1:N+1])
        M_ON_temp[1:M+1, 1:N+1] = np.maximum(M_ON_temp[1:M+1, 1:N+1], right_ON[1:M+1, 1:N+1])

        # Select the MAX value between top_OFF, bottom_OFF, left_OFF, right_OFF:
        M_OFF_temp[1:M+1, 1:N+1] = np.maximum(top_OFF[1:M+1, 1:N+1], bottom_OFF[1:M+1, 1:N+1])
        M_OFF_temp[1:M+1, 1:N+1] = np.maximum(M_OFF_temp[1:M+1, 1:N+1], left_OFF[1:M+1, 1:N+1])
        M_OFF_temp[1:M+1, 1:N+1] = np.maximum(M_OFF_temp[1:M+1, 1:N+1], right_OFF[1:M+1, 1:N+1])

        M_ON = np.maximum(M_ON, (mask_ON * M_ON_temp))
        M_OFF = np.maximum(M_OFF, (mask_OFF * M_OFF_temp))

        M_ON_vid[:, :, t] = M_ON
        M_OFF_vid[:, :, t] = M_OFF

    bright_raw = utils.threshold(M_ON[1:M+1, 1:N+1]-T_f) - utils.threshold(M_OFF[1:M+1, 1:N+1]-T_f)
    bright_raw = bright_raw + np.abs(bright_raw.min())
    bright = np.array(bright_raw / bright_raw.max())
    return bright, M_ON, M_OFF
