import os
from ModifyAnalysisFile import modAnalysisFile as mAF
from ModifyDataFile import modDataFile as mDF

dir = os.path.dirname(__file__)
mDF(dir)
os.chdir(dir)
mAF(dir)
    
