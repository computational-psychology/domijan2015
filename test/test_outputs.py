import os
import sys
import numpy as np
from PIL import Image
import pytest
from domijan2015 import utils, main

current_dir = __file__
project_path = os.path.abspath(current_dir + "../../../")
sys.path.append(project_path)
sep = os.path.sep
ground_truth_dir = os.path.abspath(current_dir + "../../Ground_truth") + sep

stimlist = [
    [1, "dungeon_illusion"],
    [2, "cube_illusion"],
    [3, "grating_illusion"],
    [4, "ring_illusion"],
    [5, "bullseye_illusion"],
    [6, "SC_illusion"],
    [7, "white_illusion"],
    [8, "benarys_cross"],
    [9, "todorovic_illusion"],
    [10, "contrast_illusion"],
    [11, "checkerboard_illusion"],
    [12, "checkerboard_extended_illusion"],
    ]


@pytest.mark.parametrize("stim", stimlist)
def test_stim(stim):
    img, _, _ = utils.generate_input(stim[0])
    res = main.main(img, extensive=False)
    output = utils.img_to_png(res['model_output'])
    test_output = np.asarray(Image.open(f"{ground_truth_dir}{stim[1]}.png").convert("L"))
    assert utils.compare_arrays(output, test_output), "outputs are different"
