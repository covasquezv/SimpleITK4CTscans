import SimpleITK as sitk

def read_serie(dcm_folder):
    '''
    Read dicom serie
    Parameters:
        dcm_folder -- path to dicom serie
    Returns:
        volume -- CT image as array
        spacing -- original dicom spacing
        series_tag_values -- dictionary containing metadata
    '''
    # Read Image
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dcm_folder)
    reader.SetFileNames(dicom_names)
    reader.MetaDataDictionaryArrayUpdateOn()
    reader.LoadPrivateTagsOn()
    image = reader.Execute()

    # Get relevant metadata
    spacing = image.GetSpacing()
    series_tag_values = get_metadata(reader)

    # Image to array
    volume = sitk.GetArrayFromImage(image)

    return volume, spacing, series_tag_values
