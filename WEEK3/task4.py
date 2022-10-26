import numpy as np
import os
from mapk import mapkL
from utils.managePKLfiles import store_in_pkl, read_pkl
from utils.distanceTextMetrics import getDistance2Strings
from computeRetrieval import SimilarityFromDescriptors, SimilarityFromText
from utils.distanceMetrics import EuclidianDistance, L1_Distance, X2_Distance, Hellinger_distance, Cosine_Similarity

# New savesBestKmatches
def saveBestKmatchesNew(bbddDescriptorsPathText = None, bbddDescriptorsPathColor = None, bbddDescriptorsPathTexture = None, qDescriptorsPathText = None, qDescriptorsPathColor = None, qDescriptorsPathTexture = None, k = 10, distanceFuncText = None, distanceFuncColor = None, distanceFuncTexture = None, weightText = 1, weightColor = 1, weightTexture = 1):
    """ This function computes all the similarities between the database and query images
        using distances functions given and returns k best matches for every query image
    

    Parameters
    ----------
    bbddDescriptorsPath : string
        Path of the folder where .npy descriptor files of the database are stored.
    qDescriptorsPath : string
        Path of the folder where .npy descriptor files of the query images are stored..
    k : int
        Quantity of best matches is returned.
    distanceFuncText : function
        Distance function that will be used to compute the similarities of the text.
    distanceFuncColor : function
        Distance function that will be used to compute the similarities of the color.
    distanceFuncTexture : function
        Distance function that will be used to compute the similarities of the texture.
    weightText : float
        This float is in [0,1] and gives the importance of text compared to color and texture to find best matches
    weightColor : float
        This float is in [0,1] and gives the importance of color compared to text and texture to find best matches
    weightTexture : float
        This float is in [0,1] and gives the importance of texture compared to color and text to find best matches

    Returns
    -------
    result : list of lists of lists (int)
        The best k matches for each image in the query. The k matches are sorted from
        the most similar to the least one.

    """

    # Get names of files
    if bbddDescriptorsPathText != None:
        bbddDescriptorsPath = bbddDescriptorsPathText
        qDescriptorsPath = qDescriptorsPathText

    elif bbddDescriptorsPathColor != None:
        bbddDescriptorsPath = bbddDescriptorsPathColor
        qDescriptorsPath = qDescriptorsPathColor
    else:
        bbddDescriptorsPath = bbddDescriptorsPathTexture
        qDescriptorsPath = qDescriptorsPathTexture
    
    # Compute number of images in each set
    numBBDD = len(os.listdir(bbddDescriptorsPath))
        
    # Init result list
    result = []
    
    # For every image in query
    for i, fileQ in enumerate(os.listdir(qDescriptorsPath)):
        
        # Create list of distances
        distances = np.array([-1.]*numBBDD)
        
        # For every image in BBDD
        for j, fileBBDD in enumerate(os.listdir(bbddDescriptorsPath)):

            # Mean weighted distance
            distance = 0

            # Calculate distance
            if distanceFuncText != None:
                distanceText = SimilarityFromText(qDescriptorsPathText + fileQ,
                                                bbddDescriptorsPathText + fileBBDD,False, distanceFuncText)
                distance += weightText*distanceText
            if distanceFuncColor != None:
                distanceColor = SimilarityFromDescriptors(qDescriptorsPathColor + fileQ,
                                                bbddDescriptorsPathColor + fileBBDD,False, distanceFuncColor)
                distance += weightColor*distanceColor
            if distanceFuncTexture != None:
                distanceTexture = SimilarityFromDescriptors(qDescriptorsPathTexture + fileQ,
                                                bbddDescriptorsPathTexture + fileBBDD,False, distanceFuncTexture)
                distance += weightTexture*distanceTexture

            # Save distance
            distances[j] = distance

        # Sort the distances and get k smallest values indexes
        sortedIndexes = np.argsort(distances)
            
        # Save results in the list
        if int(fileQ[:-4].split("_")[-1]) == 0:
            result.append([sortedIndexes[:k].tolist()])
        else:
            result[-1].append(sortedIndexes[:k].tolist())
    
    return result
    

def bestCoefficient(bbddDescriptorsPathText = None, bbddDescriptorsPathColor = None, bbddDescriptorsPathTexture = None, qDescriptorsPathText = None, qDescriptorsPathColor = None, qDescriptorsPathTexture = None, k = 10, distanceFuncText = 1, distanceFuncColor = L1_Distance, distanceFuncTexture = L1_Distance):

    """This function return the best weight for each descriptors (text, color, texture) in order to get the better mapkL value

    Parameters
    ----------
    bbddDescriptorsPathText : string
        Path of the folder where .npy text descriptor  files of the database are stored.
    bbddDescriptorsPathColor : string
        Path of the folder where .npy color descriptor  files of the database are stored.  
    bbddDescriptorsPathTexture : string
        Path of the folder where .npy texture descriptor  files of the database are stored.  
    qDescriptorsPathText : string
        Path of the folder where .npy text descriptor files of the query images are stored.
    qDescriptorsPathColor : string
        Path of the folder where .npy color descriptor files of the query images are stored.
    qDescriptorsPathTexture : string
        Path of the folder where .npy texture descriptor files of the query images are stored..
    k : int
        Quantity of best matches is returned.
    distanceFuncText : function
        Distance function that will be used to compute the similarities of the text.
    distanceFuncColor : function
        Distance function that will be used to compute the similarities of the color.
    distanceFuncTexture : function
        Distance function that will be used to compute the similarities of the texture.

    Returns
    -------
    result : weightText, weightColor and weightTexture and bestmapkL

    """

    gtResults = read_pkl('WEEK3/data/qsd1_w3/gt_corresps.pkl')
    best = 0
    besti = 0
    bestj = 0

    #2 descriptors
    if(bbddDescriptorsPathText != None and bbddDescriptorsPathColor != None and bbddDescriptorsPathTexture == None 
    or bbddDescriptorsPathText != None and bbddDescriptorsPathColor == None and bbddDescriptorsPathTexture != None 
    or bbddDescriptorsPathText == None and bbddDescriptorsPathColor != None and bbddDescriptorsPathTexture != None):

        #Text and Color
        if(bbddDescriptorsPathText != None and bbddDescriptorsPathColor != None):
            for i in range(4):
                for j in range(4) :
                    if not (i == 0 and j == 0):

                        predictedResults = saveBestKmatchesNew(bbddDescriptorsPathText = bbddDescriptorsPathText, bbddDescriptorsPathColor = bbddDescriptorsPathColor,
                        qDescriptorsPathText = qDescriptorsPathText, qDescriptorsPathColor = qDescriptorsPathColor, distanceFuncText = distanceFuncText, distanceFuncColor = distanceFuncColor, k = k, weightText = i, weightColor = j)

                        mapkl = mapkL(gtResults, predictedResults, 10)

                        print(mapkl)

                        if(best < mapkl):
                            besti = i
                            bestj = j
                            best = mapkl

        print("Best combination for color and text is : weightText = " + str(besti) + " and weightColor = " + str(bestj) + " =====> " + str(best))





# # Hog descriptors
# BBDDPathTexture = 'WEEK3/descriptors/BBDD/hog/levels_3/features_160/'
# QPathTexture = 'WEEK3/descriptors/qsd1_w3/hog/levels_3/features_160/'

# # Text descriptors
# BBDDPathText = 'WEEK3/textDescriptors/BBDD_pny/'
# QPathText = 'WEEK3/textDescriptors/denoisedImages/nlmean/qsd1_w3_npy/'

# # Color descriptors
# BBDDPathColor = 'WEEK3/descriptors/BBDD/cielab/level_3/2D_bins_20/'
# QPathColor = 'WEEK3/descriptors/qsd1_w3/cielab/level_3/2D_bins_20/'


# result = saveBestKmatchesNew(bbddDescriptorsPathColor = BBDDPathColor,
#     qDescriptorsPathColor = QPathColor, distanceFuncColor= L1_Distance)

# gtResults = read_pkl('WEEK3/data/qsd1_w3/gt_corresps.pkl')
# predictedResults = read_pkl('WEEK3/results/qsd1_w3/cielab_l1/level_3/2D_bins_20/result.pkl')
# print(mapkL(gtResults, result, 10))

# bestCoefficient(bbddDescriptorsPathColor=BBDDPathColor, bbddDescriptorsPathText=BBDDPathText, qDescriptorsPathColor=QPathColor,
# qDescriptorsPathText=QPathText)

