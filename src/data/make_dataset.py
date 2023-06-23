# -*- coding: utf-8 -*-
import argparse
import logging
from pathlib import Path
import pandas as pd

def clean_data(df):
    '''Replace dot (.) with underscore (_) in column names'''
    df.columns = [col.replace('.', '_') for col in df.columns]
    return df

def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    df = pd.read_csv(input_filepath)
    df = clean_data(df)
    df.to_csv(output_filepath, index=False)
    logger.info('data saved to %s', output_filepath)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('-i', '--input_filepath', type=str, default='data/raw/iris.csv', \
                        help='the path to the input file')
    parser.add_argument('-o', '--output_filepath', type=str, default='data/processed/iris_processed.csv', \
                        help='the path to the output file')
    args = parser.parse_args()
    print(args)
    
    # Call the main function with the arguments
    main(args.input_filepath, args.output_filepath)
