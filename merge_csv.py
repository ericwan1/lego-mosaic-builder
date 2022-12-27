# File purpose:
# get all csv files, combine them, then output final csv in a separate folder that is not touched by glob

import pandas as pd
import glob

output_df = pd.DataFrame(columns=['colorId','name','brickCount'])

# cycle through all of the csv files
for mosaic_csv in glob.glob('./mosaic-outputs/*.csv'):
    mosaic_df = pd.read_csv(mosaic_csv)
    output_df = pd.concat([output_df, mosaic_df]).groupby(['colorId','name'])['brickCount'].sum().reset_index()

output_df.to_csv(path_or_buf="./orders/all_parts_count.csv")