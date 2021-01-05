''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Script Name: 
mutli apply and group summarise function

Purpose:
function to apply multiple functions to a column
function to aggregate multiple fields by multiple groups 

Script Dependencies:
pandas module
numoy module

Parent Script(s):
N/A

Child Scripts(s):
N/A

Notes:
(1) build version indicates the module version the script was created on (pip modules only)


Changes:

Name            Date            Version         Change
Lee Rock        05/01/2021      v1.0.0          initial version

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    start of script
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
install required non standard external modules if missing
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

import sys
import subprocess
import pkg_resources

required = {'numpy', 'pandas'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)


''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import modules
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

import pandas as pd #install (build version: 1.1.5)
import numpy as np #install (build version: 1.19.4)

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
multi function function
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

#function to apply multiple functions to a vector at once
def multi_func(x):

   # x = column/vector to be passed

    #dictionary holding methods
    method_dict = {

        #insert your function with a key name
        'count': round(len(x), 2),
        'sum': round(np.nansum(x), 2),
        'avg': round(np.nanmean(x), 2),
        'min': round(np.nanmin(x), 2),
        'max': round(np.nanmax(x), 2),
        'Q1': round(np.nanquantile(x, 0.25), 2),
        'Median': round(np.nanmedian(x), 2),
        'Q3': round(np.nanquantile(x, 0.75), 2)
        }

    return method_dict


''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
group summarise function
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

#apply a function to a set of target columns by group(s)
def grp_summarise(dataset, grp, agg_fields, func):

    #dataset = input dataset (pandas dataframe)
    #grp = a list [] of grouping variables e.g. [field_1] or [field_1, field_2]
    #agg_fields = a list [] of aggregation variables e.g. [field_1] or [field_1, field_2]
    #func = the aggregation function to be applied
   
    #list to store dataframe for each aggregated field by group(s)
    frame_list = []

   #pair each aggregation field with the function, store in dictionary
    func_dict = dict.fromkeys(agg_fields, func)
    #aggregate the chosen fields by group using the function stored in the dictionary
    agg_data = dataset.groupby(grp).agg(func_dict)
    #convert results to a dataframe keeping the row index as the group by fields

    #loop to convert each aggregation to a dataframe and add to dataframe list
    for field in agg_fields:
        frame = pd.DataFrame(agg_data[field].values.tolist(), index = agg_data.index)
        
        frame_list.append(frame)

    #conactonate dataframes of aggregated fields
    final_results = pd.concat(frame_list, axis = 1, keys = agg_fields)

    return final_results



''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
example calls
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

#prop_desc_stats = grp_summarise(raw, ['prop_type'], ['price', 'beds', 'baths'], multi_func)
#agent_desc_stats = grp_summarise(raw, ['agent'], ['price', 'beds', 'baths'], multi_func)
#prop_and_agent_desc_stats = grp_summarise(raw, ['prop_type', 'agent'], ['price'], multi_func)

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    end of script
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''