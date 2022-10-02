
import pandas as pd
from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file





if __name__ == "__main__":
  data = pd.read_excel("AviationData.xlsx")
  
  print(data.head())
  
  # Generate the Profiling Report
  profile = ProfileReport(data, title="Aviation Dataset", html={"style": {"full_width": True}}, sort=None)
  
  
