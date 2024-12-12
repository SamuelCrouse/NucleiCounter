""" Documentation
Author: Samuel Crouse
Lab: WSBC Sun Lab

"""

# note: import statements
from PIL import Image
import pathlib
import math


# loads an image and converts it to grayscale
def loadImageGrayscale(filePath, savePath=None):
    """ Documentation
    Loads an image from filePath and converts it to grayscale. Saves the new image
    to savePath if savePath is set.

    :param filePath: str: The absolute path to the image file.
    :param savePath: str: The absolute path to save the gray scaled image to.
    :returns: PIL Image Obj: The pillow image object.
    """

    img = Image.open(filePath).convert('L')

    if savePath is not None:
        img.save(savePath)

    return img


# normalizes a grayscale image
def normalizeImage(img, normalToImg, savePath=None):
    """ Documentation
    Given a PIL img, normalizes it an existing grayscale image. Saves new image to
    savePath if savePath is set.

    :param img: PIL obj: The img to normalize.
    :param normalToImg: PIL obj: The PIL img to use as the base for normalization.
    :param savePath: str: The path to save the normalized image to.
    :returns: PIL Obj: The normalized image.
    """

    pix = img.load()
    width = normalToImg.width
    height = normalToImg.height

    # get the scale values from the normalToImg
    minPix = 256
    maxPix = 0
    for y in range(height):
        for x in range(width):
            gray = pix[x, y]
            if gray < minPix:
                minPix = gray

            if gray > maxPix:
                maxPix = gray

    img = img.copy()  # don't modify input image

    pix = img.load()
    width = img.width
    height = img.height

    # scale the input img to the normalToImg
    for y in range(height):
        for x in range(width):
            gray = pix[x, y]
            zi = math.floor(((gray - minPix) / (maxPix - minPix)) * 255)
            pix[x, y] = zi

    if savePath is not None:
        img.save(savePath)

    return img


# note: counts the nuclei in the image based on a threshold grayscale value
# threshold and lowerThreshold are inclusive bounds
def countNuclei(img, upperThreshold, lowerThreshold=None, nucleiPixelWidth=5, mark=False, simple=False, verySimple=False, savePath=None, saveCountsToIMG=False):
    """ Documentation
    Count and mark the cells in the image based on the provided settings. simple and verySimple should be set to False
    to perform most accurate count. This is set by default. They can be enabled for testing to increase program speed.

    :param img: PIL obj: The image to count.
    :param upperThreshold: float: The upper rgb value to mark. Below this value is counted.
    :param lowerThreshold: float: If active, check gray value must be above this and below upperThreshold to count.
    :param nucleiPixelWidth: int: The estimated pixel size of the nuclei in the image. Prevents duplicate marking.
    :param mark: bool: Whether to mark the image with red dot or not.
    :param simple: bool: Second-fastest marking. Marks left edge of nuclei. Useful for determining nuclei pixel size.
    :param verySimple: bool: Fastest marking. Marks entire selected region. Useful for picking settings. Overrides simple.
    :param savePath: str: The absolute path to save the output image. If None, doesn't save.
    :param saveCountsToIMG: bool: Appends the cell count onto the file name.
    :returns: count: int: The number of cells counted in the image.
    """

    if lowerThreshold is None:
        lowerThreshold = 0

    if verySimple is True:
        simple = True

    img = img.copy()
    pix = img.load()
    width = img.width
    height = img.height

    if mark:
        markedImg = Image.new("RGB", img.size)
        markedImg.paste(img)
        markedPix = markedImg.load()

    count = 0
    markedPixels = []  # column indexes that have been marked

    canMark = True
    for y in range(height):
        print("progress: {}%".format(round((y / len(range(height))) * 100, 4)))
        # update the marked pixels
        newMarkedPixels = []
        for index in markedPixels:
            if y < index[1] + nucleiPixelWidth:
                newMarkedPixels.append(index)
        markedPixels = newMarkedPixels

        for x in range(width):
            if simple:
                markedPixels = []

            # determine if we are far enough away from other nuclei
            else:
                canMark = True
                for index in markedPixels:
                    # check x and y
                    if (index[0] - nucleiPixelWidth) < x < (index[0] + nucleiPixelWidth):
                        if (index[1] - nucleiPixelWidth) < y < (index[1] + nucleiPixelWidth):
                            canMark = False
                            break

            if verySimple:
                canMark = True

            gray = pix[x, y]
            if canMark:
                if lowerThreshold <= gray <= upperThreshold:
                    if simple:
                        canMark = False

                    markedPixels.append((x, y))

                    count += 1
                    if mark is True:
                        markedPix[x, y] = (255, 0, 0)

            if simple:
                if gray > upperThreshold or gray < lowerThreshold:
                    canMark = True

    if savePath is not None and mark is True:
        if saveCountsToIMG is True:
            endIndex = savePath.index('.')
            countString = "_" + str(count)
            savePath = savePath[:endIndex] + countString + savePath[endIndex:]

        markedImg.save(savePath)

    return count


def prepImage(imgPath, savePath=None, normalPath=None, log=False):
    """ Documentation
    Speeds the process of gray-scaling and normalizing an image.
    Returns the normalized image for counting.

    :param imgPath: str: File path to the image.
    :param savePath: str: Path to save the normalized image at.
    :param normalPath: str: Path to the image to normalize to.
    :param log: bool: Log image information or not.
    :returns: PIL Obj: The img object to pass to countNuclei().
    """

    if normalPath is None:
        normalPath = imgPath

    if log: print("\ngrayscaling image...")

    img_path = imgPath
    img = loadImageGrayscale(img_path, savePath=savePath)
    normalToImg = loadImageGrayscale(normalPath)

    if log:
        print("width: {}, height: {}".format(img.width, img.height))
        print("width: {}, height: {}".format(normalToImg.width, normalToImg.height))

        print("\nnormalizing image...")

    img = normalizeImage(img=img, normalToImg=normalToImg, savePath=savePath)

    return img


def main():
    """ Documentation
    Contains some tests for the above functions.
    Loads an image, gray-scales, normalizes, and saves.
    Imports previous from an images directory an image and counts/marks/saves.

    :returns: None
    """

    print("start tests...")
    directory = str(pathlib.Path().absolute().resolve()) + "\\images\\"
    imgNum = 3

    # code for grayscaling and normalizing a new img
    # """
    img_path = directory + "img{}.png".format(imgNum)
    print("\ngrayscaling image...")
    img = loadImageGrayscale(img_path, savePath=directory+"gray{}.png".format(imgNum))
    normalToImg = loadImageGrayscale(directory + "img1.png")

    print("width: {}, height: {}".format(img.width, img.height))
    print("width: {}, height: {}".format(normalToImg.width, normalToImg.height))

    print("\nnormalizing image...")
    img = normalizeImage(img=img, normalToImg=normalToImg, savePath=directory+"gray{}_normal.png".format(imgNum))
    # """

    # load an already grayscaled and normalized img
    # """
    img_path = directory + "gray{}_normal.png".format(imgNum)
    img = loadImageGrayscale(img_path)
    # """

    print("\ncounting nuclei...")  # 110 is a pretty good threshold  # 100 is maybe even better for darker images
    count = countNuclei(img, upperThreshold=120, lowerThreshold=90, nucleiPixelWidth=10, mark=True, simple=False,
                        verySimple=False, savePath=directory + "gray{}_normal_marked_new_4.png".format(imgNum))

    print("final count:", count)


if __name__ == "__main__":
    main()
