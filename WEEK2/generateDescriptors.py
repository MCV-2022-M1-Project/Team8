import cv2
import numpy as np
import os
from utils.changeColorSpace import changeBGRtoHSV, changeBGRtoYCBCR, changeBGRtoCIELAB, changeBGRtoCIELUV
from multiResDescriptors import generateMultiResDescriptors
from hist2Doptimized import Create2DHistogram
from hist3Doptimized import Create3DHistogram



def computeDescriptors(imagesPath, outputPath, colorSpace, numBins, histGenFunc, levels,
                       backgroundMaskDir = None, textBox = None):
    """ This function computes the descriptors of the images from the input path 
    and save them in the output path.
    

    Parameters
    ----------
    imagesPath : string
        The path were input images are.
    outputPath : string
        The path were descriptors will be saved.
    colorSpace : string
        The color space were the descriptors will be generated. 
        rgb, hsv, cielab, cieluv, ycbcr are the options.
    numBins: int
        The number of bins in each dimension
    histGenFunc: function
        The function to generate the descriptors
    levels: int
        The number of multidimensional levels
    backgroundMaskDir : str
        Path where binary mask to know which pixel is related to the background are.
        Default: None  -> No background
    textBox: numpy array (np.int)
        List of the text box coordinates

    Returns
    -------


    """
    
    
    # Get file names of the database
    files = os.listdir(imagesPath)
    
    for file in files:
        # Check if it is an image
        if file[-4:] == ".jpg":
            
            image = cv2.imread(imagesPath + file)
            
            if backgroundMaskDir is None:
                # Take into account every pixel
                mask = np.zeros(image.shape[:2], dtype = np.uint8) + 255
            else:
                mask = cv2.imread(backgroundMaskDir + file[:-4] + ".png", cv2.IMREAD_GRAYSCALE)

            # Convert the image into the new color space
            if colorSpace == "hsv":
                image = changeBGRtoHSV(image)
            elif colorSpace == "cielab":
                image = changeBGRtoCIELAB(image)
            elif colorSpace == "cieluv":
                image = changeBGRtoCIELUV(image)
            elif colorSpace == "ycbcr":
                image = changeBGRtoYCBCR(image)
            
            descriptor = generateMultiResDescriptors(image, mask, levels, histGenFunc, numBins)
            
            descriptorPath = outputPath + file[:-4] + ".npy"
            np.save(descriptorPath, descriptor)
            
    