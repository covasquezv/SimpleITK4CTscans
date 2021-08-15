import os, time, datetime
import SimpleITK as sitk
import numpy as np

## =============================================================================
##                                 RGB DICOM
## =============================================================================
def writeSlices_rgb(series_tag_values, new_img, i, writer, output_path,
                    serie_id, position):

    '''
    Write instances as dicom.
    Parameters:
    series_tag_values -- list of tags to add as metadata
    new_img -- SimpleITK image
    i -- current slice index
    output_path -- path to save
    serie_id -- identification of the serie being saved
    position -- patient position (from metadata)

    Returns:
    (nothing)
    '''

    image_slice = new_img[:,:,i]

    # Tags shared by the series.
    list(map(lambda tag_value: image_slice.SetMetaData(tag_value[0], tag_value[1]), series_tag_values))

    modification_time = time.strftime("%H%M%S")
    modification_date = time.strftime("%Y%m%d")
    name = '1.'+serie_id+"."+modification_date+modification_time+"."+str(i+1)

    # # Slice specific tags.
    image_slice.SetMetaData("0008|0012", modification_date) # Instance Creation Date
    image_slice.SetMetaData("0008|0013", modification_time) # Instance Creation Time

    # Setting the type to CT preserves the slice location.
    image_slice.SetMetaData("0008|0060", "CT")   # set the type to CT so the thickness is carried over
    image_slice.SetMetaData("0008|0018", name)   # SOP Instance UID
    image_slice.SetMetaData("0020|0013", str(i+1)) # Instance number
    image_slice.SetMetaData("0018|0050", "1.5")  # Slice thickness

    # (0020, 0032) image position patient determines the 3D spacing between slices.
    image_slice.SetMetaData("0020|0032", '\\'.join(map(str,new_img.TransformIndexToPhysicalPoint((0,0,i))))) # Image Position (Patient)

    ## RGB
    image_slice.SetMetaData("0028| 0002", "3")
    image_slice.SetMetaData("0028| 0004", "RGB")
    image_slice.SetMetaData("0028| 0006", "0")
    image_slice.SetMetaData("0028| 0008", "1")
    image_slice.SetMetaData("0028| 0008", "1")
    image_slice.SetMetaData("0028| 0100", "8")
    image_slice.SetMetaData("0028| 0101", "8")
    image_slice.SetMetaData("0028| 0102", "7")
    image_slice.SetMetaData("0028| 0103", "0")
    image_slice.SetMetaData("0028| 0006", "0")
    image_slice.SetMetaData("0028| 1052", "0")
    image_slice.SetMetaData("0028| 1053", "1")

    # Write to the output directory and add the extension dcm, to force writing in DICOM format.
    writer.SetFileName(os.path.join(output_path,name+'.dcm'))

    writer.Execute(image_slice)

def array2dcm_rgb(new_img, spacing, depth, data_directory, serie_id,
                  study_id, patient_id, p_direction, position, acc_number,
                  study_uid, study_desc, serie_desc):
    '''
        Save array to RGB dicom.
        Parameters:
        new_img -- SimpleITK image
        spacing -- CT spacing (from metadata)
        depth -- volume depth (slices number)
        data_directory -- path to save
        study_id -- CT study id (from metadata)
        patient_id -- patient id (from metadata)
        p_direction -- patient direction (from metadata)
        position -- patient position (from metadata)
        acc_number -- accession number (from metadata)
        study_uid -- study uid (from metadata)
        study_desc -- description of the study (string)
        serie_desc -- description of the serie (string)

        Returns:
        boolean -- success of process
    '''
    try:

        new_img.SetSpacing(spacing)

        writer = sitk.ImageFileWriter()
        writer.SetImageIO('GDCMImageIO')

        # Use the study/series/frame of reference information given in the meta-data
        # dictionary and not the automatically generated information from the file IO
        writer.KeepOriginalImageUIDOn()

        writer.SetUseCompression(True)
        # writer.SetCompressor("JPEG")
        writer.SetCompressor("JPEG2000")
        # writer.SetCompressor("JPEGLS")
        writer.SetCompressionLevel(90)

        modification_time = time.strftime("%H%M%S")
        modification_date = time.strftime("%Y%m%d")

        # Copy some of the tags and add the relevant tags indicating the change.
        # For the series instance UID (0020|000e), each of the components is a number, cannot start
        # with zero, and separated by a '.' We create a unique series ID using the date and time.
        # tags of interest:

        series_tag_values = [("0008|0031",modification_time), # Series Time
                          ("0008|0021",modification_date), # Series Date
                          ("0008|0008","DERIVED\\SECONDARY"), # Image Type
                          ("0020|0037", p_direction),
                          ("0020|0010", study_id), # Study ID
                          ("0020|000e", '1.'+serie_id+"."+modification_date+modification_time), # Series Instance UID
                          ("0010|0020", patient_id), # Patient ID
                          ("0008|0050", acc_number), # Accesion number
                          ("0020|000d", study_uid), # Study Instance UID
                          ("0008,1030", study_desc),  # Study description
                          ("0008|103e", serie_desc)] # Series Description

        # Write slices to output directory
        list(map(lambda i: writeSlices_rgb(series_tag_values, new_img, i, writer, data_directory, serie_id, position), range(depth)))
        return True
    except RuntimeError as e:
        print(str(datetime.datetime.now())+';ERROR: '+str(e))
        return False

## =============================================================================
##                              Grayscale DICOM
## =============================================================================

def writeSlices(series_tag_values, new_img, i, writer, output_path, serie_id, position):
    image_slice = new_img[i,:,:]

    # Tags shared by the series.
    list(map(lambda tag_value: image_slice.SetMetaData(tag_value[0], tag_value[1]), series_tag_values))

    modification_time = time.strftime("%H%M%S")
    modification_date = time.strftime("%Y%m%d")
    name = '1.'+serie_id+"."+modification_date+modification_time+"."+str(i+1)

    # # Slice specific tags.
    image_slice.SetMetaData("0008|0012", modification_date) # Instance Creation Date
    image_slice.SetMetaData("0008|0013", modification_time) # Instance Creation Time

    # Setting the type to CT preserves the slice location.
    image_slice.SetMetaData("0008|0060", "CT")   # set the type to CT so the thickness is carried over
    image_slice.SetMetaData("0008|0018", name)   # SOP Instance UID
    image_slice.SetMetaData("0020|0013", str(i+1)) # Instance number

    # (0020, 0032) image position patient determines the 3D spacing between slices.
    image_slice.SetMetaData("0020|0032", '\\'.join(map(str,new_img.TransformIndexToPhysicalPoint((0,0,i))))) # Image Position (Patient)

    # Write to the output directory and add the extension dcm, to force writing in DICOM format.
    writer.SetFileName(os.path.join(output_path,name+'.dcm'))
    writer.Execute(image_slice)

def array2dcm(new_arr, spacing, depth, data_directory, serie_id,
              study_id, patient_id, p_direction, position, acc_number,
              study_uid, study_desc, serie_desc):
    try:
        new_img = sitk.GetImageFromArray(new_arr)
        new_img.SetSpacing(spacing)

        writer = sitk.ImageFileWriter()
        # Use the study/series/frame of reference information given in the meta-data
        # dictionary and not the automatically generated information from the file IO
        writer.KeepOriginalImageUIDOn()

        writer.SetUseCompression(True)
        writer.SetCompressionLevel(90)
        writer.SetCompressor("JPEG")

        modification_time = time.strftime("%H%M%S")
        modification_date = time.strftime("%Y%m%d")

        # Copy some of the tags and add the relevant tags indicating the change.
        # For the series instance UID (0020|000e), each of the components is a number, cannot start
        # with zero, and separated by a '.' We create a unique series ID using the date and time.
        # tags of interest:
        series_tag_values = [("0008|0031",modification_time), # Series Time
                          ("0008|0021",modification_date), # Series Date
                          ("0008|0008","DERIVED\\SECONDARY"), # Image Type
                          ("0020|0037", p_direction),
                          ("0020|0010", study_id), # Study ID
                          ("0020|000e", "1."+serie_id+"."+modification_date+modification_time), # Series Instance UID
                          ("0010|0020", patient_id), # Patient ID
                          ("0008|0050", acc_number), # Accesion number
                          ("0020|000d", study_uid), # Study Instance UID
                          ("0008,1030", study_desc),  # Study description
                          ("0008|103e", serie_desc)] # Series Description

        # Write slices to output directory
        list(map(lambda i: writeSlices(series_tag_values, new_img, i, writer, data_directory, serie_id, position), range(depth)))
        return True
    except RuntimeError as e:
        print(str(datetime.datetime.now())+';ERROR: '+str(e))
        return False
