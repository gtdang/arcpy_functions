import arcpy
import numpy as np
import pandas as pd

def fc_to_pd_df(feature_class, field_list=None):
    '''
    This function converts a feature class to a pandas dataframe. The default returns all fields but you may supply a
    list of fields to extract. Fields with the "Geometry" datatype like the "Shape" field of most FC are removed because
    they are not 1-dimensional and Pandas can't deal with that data type.

    Note that very large feature classes may not work due to memory limitations, especially if using 32bit python. You
    may try supplying a list of only the fields you require to get past the memory limitations.

    Written: 7/17/2019

    :param feature_class: Input ArcGIS Feature Class
    :param field_list: Fields for input (optional), default is all fields
    :return: Pandas dataframe object
    '''
    # Generate a list of fields to import.
    field_list_temp = []
    all_fields = []
    fields = arcpy.ListFields(feature_class)
    for field in fields:
        all_fields.append(field.name) # All fields list for requested fields check
        # If a list of fields is not supplied import all fields, check for and exclude geometry data types
        if field_list is None:
            if field.type != 'Geometry':
                field_list_temp.append(field.name)
            else:
                print("Field \"{0}\" is of data type \"{1}\" and will not be imported into the pandas dataframe.".format(
                    field.name, field.type))
        # If a list is supplied we will check if any of the requested fields are of geometry data type, remove, and warn user
        else:
            if (field.type != 'Geometry') & (field.name in field_list):
                    field_list_temp.append(field.name)
            elif (field.type == 'Geometry') & (field.name in field_list):
                print("Field \"{0}\" is of data type \"{1}\" and will not be imported into the pandas dataframe.".format(
                    field.name, field.type))

    # If field_list is set, check if requested fields are missing from the FC
    if field_list is not None:
        for field in field_list:
            if field.name not in all_fields:
                raise ValueError("Requested field \"{0}\" was not found in the feature class!".format(field.name))

    # Set field list to the list of verified field names to extract
    field_list = field_list_temp

    # Convert FC to numpy array with field list
    np_array = arcpy.da.FeatureClassToNumPyArray(in_table=feature_class,
                                                 field_names=field_list,
                                                 skip_nulls=False,
                                                 null_value=-999)
    return pd.DataFrame(np_array)

# Call example
if __name__ == '__main__':

    fc_path = r'C:\\FeatureClass.gdb\FeatureClass'
    df = fc_to_pd_df(fc_path)


