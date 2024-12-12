"""
Documentation
Author: Samuel Crouse
Lab: WSBC Sun Lab

"""

import CountNuclei as cn
import pathlib


def main():
    """ Documentation
    This code provides code for testing and outputting multiple types of images using
    the nucleiCounter function. This makes use of prepImage() function to speed this process.

    :return:
    """

    print("grayscaling and counting...")
    directory = str(pathlib.Path().absolute().resolve()) + "\\images\\directoryName\\"
    imgNum = 1
    name = "brain-slice"

    # prep the image by grayscaling and normalizing it
    """
    imgName = f"{name}_{imgNum}.PNG"
    imgPath = directory + imgName
    graySavePath = directory + f"{name}_gray_{imgNum}.PNG"
    gray = cn.prepImage(imgPath=imgPath, savePath=graySavePath, log=True)
    # """

    # note: load an already grayscaled and normalized img
    # """
    grayToLoadPath = directory + f"brain-slice_gray_1.PNG"
    gray = cn.loadImageGrayscale(grayToLoadPath)
    # """

    print("\ncounting nuclei and outputting very simple, simple, and normal images...")
    counts = []
    for i in range(3):
        verySimple = True
        simple = False
        sType = "VS"

        if i == 1:
            verySimple = False
            simple = True
            sType = "S"

        if i == 2:
            verySimple = False
            simple = False
            sType = "N"

        imgNum = 1  # insert this into the img path if you want to track different images
        lowThresh = 60
        upThresh = 200
        width = 6
        markedSavePath = directory + f"{name}_marked_{lowThresh}-{upThresh}-{width}-{sType}.PNG"
        if i != 2: markedSavePath = None
        count = cn.countNuclei(img=gray, upperThreshold=upThresh, lowerThreshold=lowThresh, nucleiPixelWidth=width,
                               mark=True, simple=simple, verySimple=verySimple,
                               savePath=markedSavePath, saveCountsToIMG=True)
        counts.append(count)

    print("final counts: very simple: {} | simple: {} | normal: {}".format(*counts))
    # """


if __name__ == '__main__':
    main()
