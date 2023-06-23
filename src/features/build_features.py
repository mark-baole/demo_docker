# -*- coding: utf-8 -*-
import argparse
import logging
from pathlib import Path
import pandas as pd

def feature_engineer(df):
    '''Dummy function to clean data'''
    pass
    return df

def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('feature engineering data set from processed data')

    df = pd.read_csv(input_filepath)
    df = feature_engineer(df)
    df.to_csv(output_filepath, index=False)
    logger.info('data saved to %s', output_filepath)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    parser = argparse.ArgumentParser(description='Feature engineer some data.')
    parser.add_argument('-i', '--input_filepath', type=str, default='data/processed/iris_processed.csv', \
                        help='the path to the input file')
    parser.add_argument('-o', '--output_filepath', type=str, default='data/processed/iris_feature_engineered.csv', \
                        help='the path to the output file')
    args = parser.parse_args()
    print(args)
    
    # Call the main function with the arguments
    main(args.input_filepath, args.output_filepath)
