from skimage import feature
import numpy as np
import cv2


def createLBPhistogram(image, num_blocks, radius, bins):
    """
    This function creates the LBP histogram of the image given. The radius for the LBP and the number
    of bins of the result histogram are given.

    Parameters
    ----------
    image : numpy array (np.uint8)
        image to compute the lbp histogram.
    num_blocs: int
        number of block to divide each image
    radius : int
        radius number to compute lbp.
    bins : int
        number of bins of the histogram per block.

    Returns
    -------
    hist : numpy array 1D
        lbp histogram result of the given image.

    """

    numPoints = 8*radius
    
    # Turn to grayscale image
    imageG = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Init result
    resultHist = []
    
            
    # Compute histograms
    difW = int(image.shape[1]/num_blocks)
    remainingW = image.shape[1] % num_blocks
    difH = int(image.shape[0]/num_blocks)
    remainingH = image.shape[0] % num_blocks
    
    
    actualH = 0
    
    
    # Compute every block
    for h in range(num_blocks):
        # Compute roi height
        if remainingH > 0:
            roiH = difH + 1
            remainingH -= 1
        else:
            roiH = difH
        
        actualW = 0
        remainingW = image.shape[1] % num_blocks
        
        for w in range(num_blocks): 
            # Compute roi width
            if remainingW > 0:
                roiW = difW + 1
                remainingW -= 1
            else:
                roiW = difW
        
            
            blockImage = imageG[actualH: actualH + roiH, actualW: actualW + roiW]
            
            
            # Compute lbp
            lbp = feature.local_binary_pattern(blockImage, numPoints, radius, method="uniform")
            
            # Compute histogram
            (hist, _) = np.histogram(lbp.ravel(), bins=bins, range=(0, 2**numPoints - 1))
            
            
            
            # Concatenate
            resultHist = np.concatenate([resultHist, hist])
            
            actualW = actualW + roiW
        
        actualH = actualH + roiH 
    
    
    # normalize the histogram
    resultHist = resultHist.astype("float")
    eps = 1e-7
    resultHist /= (resultHist.sum() + eps)
    
    
    return resultHist
