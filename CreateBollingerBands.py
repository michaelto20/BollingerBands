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
    outputPath = "C:\\Users\\Michael Townsend\\Desktop\\StockInfo\\FOREX\\Data\\BollingerBands.csv"
    stdDeviations = 3
    rollingWindow = 50
    inputDataFrame = pd.read_csv(inputPath, delimiter=';')
    inputDataFrame['20 Min MA'] = inputDataFrame['BarCloseBid'].rolling(window=rollingWindow).mean()
    inputDataFrame['20 Min STD'] = inputDataFrame['BarCloseBid'].rolling(window=rollingWindow).std()
    inputDataFrame['UpperBand'] = inputDataFrame['20 Min MA'] + (inputDataFrame['20 Min STD'] * stdDeviations)
    inputDataFrame['LowerBand'] = inputDataFrame['20 Min MA'] - (inputDataFrame['20 Min STD'] * stdDeviations)
    
    # Crossed above over Upper Bollinger Band
    inputDataFrame['CrossedUpper'] = inputDataFrame.where(inputDataFrame['BarCloseBid'] > inputDataFrame['UpperBand'], False, False).any(axis=1).astype(int)
    
    # Crossed under over Lower Bollinger Band
    inputDataFrame['CrossedLower'] = inputDataFrame.where(inputDataFrame['BarCloseBid'] < inputDataFrame['LowerBand'], False, False).any(axis=1).astype(int)
    
    # Slope
    inputDataFrame['Slope'] = (inputDataFrame['BarCloseBid'] - inputDataFrame['BarCloseBid'].shift(1)) / 5
    
    # Crossed Upper Bound in the previous time interval (speculating that what goes up must come down, hopefully in this time interval)
    inputDataFrame['PreviouslyCrossedUpper'] = inputDataFrame.where(inputDataFrame['CrossedUpper'].shift(1) == True, False, False).any(axis = 1).astype(int)
    
    # a win occurrs if a given row's BarCloseBid is less then the previous row's value
    inputDataFrame['SellWins'] = inputDataFrame.where(inputDataFrame['BarCloseBid'] >= inputDataFrame['BarCloseBid'].shift(-1), False, False).any(axis=1).astype(int)
    
    # filter data
    previouslyCrossedUpper = inputDataFrame['PreviouslyCrossedUpper'] == True
    negativeSlope = inputDataFrame['Slope'] < -0.004
    
    # print out analyzed data
    #header = ['CrossedUpper', 'Slope', 'PreviouslyCrossedUpper', 'SellWins']
    header = ['DateTimeStamp','BarOpenBid','BarHighBid','BarLowBid','BarCloseBid','Volume','20 Min MA', '20 Min STD', 'UpperBand', 'LowerBand', 'CrossedUpper', 'CrossedLower', 'Slope', 'PreviouslyCrossedUpper','SellWins']
    
    inputDataFrame[previouslyCrossedUpper & negativeSlope].to_csv(outputPath, columns = header)
    #inputDataFrame.to_csv(outputPath, columns = header)
    #print("Exiting")
    
main()