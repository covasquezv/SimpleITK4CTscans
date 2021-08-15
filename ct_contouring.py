import SimpleITK as sitk
import pulmonary_window

def contour_images(input_im, input_segm, color=[0,255,0]):
    '''
    Lung contouring over CT.
    Parameters:
        input_im -- array containing CT volume
        input_segm -- array containing lung segmentation.
        color -- color palette, default: green [0,255,0].
    Returns:
        arr_contour -- array with contoured volume.

    '''
    z = input_im.shape[-1]  # CT depth

    contours = []
    for i in range(z):
        # Select slice
        im_slice = input_im[:,:,i]
        segm_slice = input_segm[:,:,i]

        # Transform slice into SimpleITK Image and apply pulmonar window
        im_itk = sitk.GetImageFromArray(im_slice)
        im_itk = pulmonary_window.intensity_window(im_itk)

        # Transfor segmentation slice into SimpleITK Image and change type
        seg_itk = sitk.GetImageFromArray(segm_slice.astype(np.uint8))
        seg_itk = sitk.Cast(seg_itk, sitk.sitkLabelUInt8)

        # Perform contouring
        contour = sitk.LabelMapContourOverlay(seg_itk,
                                              im_itk,
                                              opacity = 1,
                                              contourThickness=[1,1],
                                              dilationRadius=[1,1],
                                              colormap=color)
        # Get array from SimpleITK Image
        contour_arr = sitk.GetArrayFromImage(contour)
        # Append to list to build volume
        contours.append(contour_arr)
    # Build back volume
    arr_contour = np.stack(contours, axis=0 )

    return arr_contour
