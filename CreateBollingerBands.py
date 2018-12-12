# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 21:49:49 2018

@author: Michael Townsend

Steps:
    Read in data
    Determine 10 or 20 minute moving average
    Determine upper and lower bands, 2 standard deviations from moving average
    Add to each row in data and write to output file
"""

import pandas as pd


def main():
    inputPath = "C:\\Users\\Michael Townsend\\Desktop\\StockInfo\\FOREX\\Data\\DAT_ASCII_USDJPY_M1_2017_TRIMMED.csv"
    outputPath = "C:\\Users\\Michael Townsend\\Desktop\\StockInfo\\FOREX\\Data\\BollingerBands.txt"
    inputDataFrame = pd.read_csv(inputPath, delimiter=';')
    inputDataFrame['20 Min MA'] = inputDataFrame['BarCloseBid'].rolling(window=20).mean()
    print("Exiting")
    
main()