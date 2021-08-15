import SimpleITK as sitk

def intensity_window(im_itk, transform_itk=False):
    '''
    Pulmonary window for chest CT.
    Parameters:
        im_itk -- input image, can be a numpy array or a SimpleITK Image.
        transform_itk (default=False) -- change to True if input is a SimpleITK
                                         Image.
    Return:
        numpy array if transform_itk=False or
        SimpleITK image if transform_itk=True
    '''
    if transform_itk:
        im_itk = sitk.GetImageFromArray(im_itk)
    im_itk = sitk.Cast(sitk.IntensityWindowing(im_itk,
                                               windowMinimum=-1000, windowMaximum=170,
                                               outputMinimum=0.0, outputMaximum=255.0),
                                               sitk.sitkUInt8)
    if transform_itk:
        return sitk.GetArrayFromImage(im_itk)
    else:
        return im_itk
