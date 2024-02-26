import utils.config as cfg
from utils.helper import Cache, ExportReview, IliasReader
import numpy as np


"""
TODO:

- SingleChoice only enters ILIAS Points as those are always correct
  --> No result check implemented yet
  
- Bonuspunkte were already available in this version 
  --> Summing and evaluating Bonuspunkte needs to be reimplemented
  
- No check if students were really present at the exam 
  --> check with signature list is not implemented yet
  
- ILIAS Overview columns are implicitly indexed for simplicity
  --> not futureproof
  
- Parsing the formula string from ILIAS to Python is directly copied from the earlier version 
  --> doesn't seem like the best way to do it

"""

if __name__ == "__main__":
    cfg.cache = Cache()
    results = {}
    member_dict = {}
    for file_path in cfg.ilias_files:
        results[file_path] = IliasReader(file_path)
        member_dict.update(results[file_path].member)

    # delete NaN Matrikelnummer --> Eberhard, etc
    del member_dict[np.nan]

    exporter = ExportReview(member_dict)
