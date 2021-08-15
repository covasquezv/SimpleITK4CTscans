import SimpleITK as sitk
import pulmonary_window

def overlay_images(im, segm):
    '''
    CT-segmentation overlay for 2 classes.
    Change color palette if for more classes are needed.

    Parameters:
        im  -- numpy array containing the original image.
        segm -- numpy array containing segmentation. In this case clases are:
                 0, 1, 2 for background, GGO and consolidatoin, respectively.
    '''

    im_itk = sitk.GetImageFromArray(im)    # Transform array to SimpleITK Image
    im_itk = pulmonary_window.intensity_window(im_itk)  # Apply pulmonary window
    seg_itk = sitk.GetImageFromArray(segm.astype(np.uint8)) 

    # Color palette for 2 classes, add more colors if more classes are needed.
    c1 = [26, 133, 255]
    c2 = [212, 17, 89]

    # Overlay the segmentation using default color map and an alpha value of 0.3
    overlayed = sitk.LabelOverlay(image=im_itk,
                                  labelImage=seg_itk,
                                  opacity=0.3,
                                  backgroundValue=0,
                                  colormap=c2+c1)
    return overlayed
