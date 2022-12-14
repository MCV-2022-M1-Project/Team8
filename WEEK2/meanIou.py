from utils.managePKLfiles import read_pkl
import numpy as np

def iou(box1, box2):
    """ This function calculates the Intersect over Union value of 2 boxes.
    

    Parameters
    ----------
    box1 : list of ints
        first box min and max coordinates.
    box2 : lists of ints
        second box min and max coordinates.

    Returns
    -------
    iou : float
        iou value.

    """

    # Get coordinates max coordinates
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    # Compute the area of intersection rectangle
    interArea = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
    
    #print("X ratio: ", (box1[2] - box1[0] + 1) / (box2[2] - box2[0] + 1))
    #print("Y ratio: ", (box1[3] - box1[1] + 1) / (box2[3] - box2[1] + 1))
    
    # compute the area of both the prediction and ground-truth
    # rectangles
    box1Area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2Area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)
    
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(box1Area + box2Area - interArea)
	
    # return the intersection over union value
    return iou

def meanIoU(boxes1, boxes2):
    """ This functions calculates the meanIoU value of the given boxes.
    

    Parameters
    ----------
    boxes1 : list of list of ints
        list of box min and max coordinates.
    boxes2 : list of list of ints
        list of box min and max coordinates.

    Returns
    -------
    float
        meanIoU value.

    """

    sumIoU = 0
    numBoxes = 0
    # Sum every boxes in images
    for i in range(len(boxes1)):
        numBoxes += max(len(boxes1[i]), len(boxes2[i]))
        
        # Sum every boxes in paintings
        for j in range(min(len(boxes1[i]), len(boxes2[i]))):
            box1 = boxes1[i][j]
            box2 = boxes2[i][j]
        
            sumIoU += iou(box1, box2)
    
    # Return mean
    return sumIoU / numBoxes
        

def evaluateTextBoxes(resultFile, predictedFile):
    """
    This function evaluates the mIoU between the two path of .pkl files given.

    Parameters
    ----------
    resultFile : str
        Path of the .pkl file of the ground-truth text boxes.
    predictedFile : str
        Path of the .pkl file of the predicted text boxes.

    Returns
    -------
    None.

    """
    result = read_pkl(resultFile)
    predicted = read_pkl(predictedFile)
    
    
    mIou = meanIoU(result, predicted)
    
    print("mIoU: ", mIou)
    
    