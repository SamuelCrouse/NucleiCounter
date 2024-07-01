# note: import statements
from PIL import Image
import pathlib
import math


# loads an image and converts it to grayscale
def loadImageGrayscale(filePath, savePath=None):
    img = Image.open(filePath).convert('L')

    if savePath is not None:
        img.save(savePath)

    return img


# normalizes a greyscale image
def normalizeImage(img, normalToImg, savePath=None):
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
def countNuclei(img, threshold, nucleiPixelWidth=5, mark=False, simple=False, verySimple=False, savePath=None):
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
                if gray < threshold:
                    if simple:
                        canMark = False

                    markedPixels.append((x, y))

                    count += 1
                    if mark is True:
                        markedPix[x, y] = (255, 0, 0)

            if simple:
                if gray >= threshold:
                    canMark = True

    if savePath is not None and mark is True:
        markedImg.save(savePath)

    return count


def main():
    print("start tests...")
    directory = str(pathlib.Path().absolute().resolve()) + "\\images\\"
    imgNum = 3

    # code for grayscaling and normalizing a new img
    """
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
    count = countNuclei(img, 120, nucleiPixelWidth=10, mark=True, simple=False, verySimple=False,
                        savePath=directory + "gray{}_normal_marked8.png".format(imgNum))

    print("final count:", count)


if __name__ == "__main__":
    main()
