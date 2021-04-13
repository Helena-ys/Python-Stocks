import pandas_datareader as pdr
import datetime
import pandas as pd

# Allow the full width of the data frame to show.
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def getStock(stk, numOfDays):
    # Set and show dates.
    dt     = datetime.date.today()
    dtPast = dt + datetime.timedelta(days=-numOfDays)
    # Call Yahoo finance to get stock data for the stock provided.
    df = pdr.get_data_yahoo(stk,
         start= datetime.datetime(dtPast.year, dtPast.month, dtPast.day),
         end  = datetime.datetime(dt.year, dt.month, dt.day))

    # Remove columns
    newColumnList = ['Close', 'Volume']
    df = df[newColumnList]
    # Add columns
    df["Volume % Change"] = 0.0
    df["Close % Change"] = 0.0
    # Assign column index for PCT change of Volume and Close Price
    volumeIdx = 2
    priceIdx = 3

    for idx in range(0, len(df)):
        if idx == 0:
            volPast = df.iloc[idx]['Volume']
            pricePast = df.iloc[idx]['Close']
        else:
            volPast = df.iloc[idx-1]['Volume']
            pricePast = df.iloc[idx-1]['Close']

        volume = df.iloc[idx]['Volume']
        price = df.iloc[idx]['Close']
        df.iat[idx, volumeIdx] = getPtcChange(volPast, volume, 4)
        df.iat[idx, priceIdx] = getPtcChange(pricePast, price, 4)

    # Return a dataframe containing stock data, start date, and end date to the calling instruction.
    return df, dtPast, dt

# Display Menu
def printMenu():
    print("-------------------------------------------------")
    print("Stock Report Menu Options")
    print("-------------------------------------------------")
    print("1. Report changes for a stock")
    print("2. Quit")

# User Input & Validation: Menu
def selectMenu():
    while True:
        try:
            selectedMenu = int(input(''))
            # Allow only 1 or 2
            if selectedMenu == 1 or selectedMenu == 2:
                break
            else:
                # When enter a wrong number or a float value
                print("That's not a valid option!")
        except:
            # When enter a string value
            print("That's not a valid option!")

    return selectedMenu

# User Input & Validation: Number of Days
def numOfDays():
    while True:
        try:
            numOfDays = int(input("Please enter the number of days for the analysis: \n"))
            # Allow only integer that is greater than 0
            if isinstance(numOfDays, int) and numOfDays > 0:
                break
            else:
                # When enter a float value
                print("Invalid value, enter a whole number!")
        except:
            # When enter a string value
            print("Invalid value, enter a whole number!")

    return numOfDays

# Calculate percentage change
def getPtcChange(start, end, decimal):
    PtcChange = round((end - start)/start, decimal)
    return PtcChange

### Application Start Here ###
while True:
    # Print Menu
    printMenu()
    # Accept menu option from user
    selected = selectMenu()
    if selected == 2:
        print("The program has been terminated.")
        exit()
    # Accept Stock Symbol from user
    stockSymbol = input("Please enter the stock symbol: \n")
    # Accept number of days from user
    days = numOfDays()

    # Get stock data
    dfApple, startDate, endDate = getStock(stockSymbol, days-1)

    numRows = len(dfApple)
    ptcVolume = getPtcChange(dfApple.iloc[0]['Volume'], dfApple.iloc[numRows - 1]['Volume'], 3)
    ptcPrice = getPtcChange(dfApple.iloc[0]['Close'], dfApple.iloc[numRows - 1]['Close'], 3)

    # Print stock data
    print("\n************************************************************")
    print("Daily Percent Changes - ", end="")
    print(str(startDate) + ' to ' + str(endDate), end="")
    print(" * " + stockSymbol.upper() + " * ")
    print("************************************************************")

    print(dfApple)

    print('------------------------------------------------------------')
    print('Summary of Cumulative Changes for ' + stockSymbol)
    print('------------------------------------------------------------')
    print( str(startDate) + ' to ' + str(endDate))
    print("% Volume Change:\t\t" + str(ptcVolume))
    print("% Close Price Change:\t" + str(ptcPrice) + "\n")