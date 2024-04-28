# KrakenPriceAPI
Simple program making use of kraken's API to retrieve historical price data and metrics - usable in the future to create an automated trading bot. Includes performing basic Technical Analysis (TA) on some candlestick data.

# Full Descriton

This is a personal project of mine in which I was following a series of video tutorials (https://www.youtube.com/watch?v=zKk2iuuNJO0&list=PLZ1QII7yudbecO6a-zAI6cuGP1LLnmW8e) to help me improve my knowledge around APIs as well as allowing me to potentially go forward to create a trading bot. The tutorials were using a different service and API for collecting candlestick data which I had to adapt to work with Kraken's API (https://docs.kraken.com/api/).

This project is written entirely in python and uses libraries found in the Anaconda environment. This reposityory is simply a showcase of my (not very professional) work and isn't intended to be downloaded and used.

# What each file does

## candles_plot.ipynb
Uses market data and plotly to create a candle stick chart to visualise past data.

## creating_data.ipynb
A core file that allows the user to input a pair name or list of pair names, a time interval and number of candles to be retrieved to generate historical data.

## defs.py
A file where the user defines their API Public and Private keys as well as the 'base' API link on which different functions append different endpoints.

## instrument.py
A file dedicated to retrieving information of a given instrument pair such as SOL/USD.

## kraken_api.py
An extensive file containing many functions, each of which creates a API request to the chosen endpoint depending on the command being executed. E.g. get_history() which creates a request to the required endpoint with the parmameters required.

## ma_excel.py
Create an excel spreadsheet from a .pkl file for the moving average Technical Analysis (TA).

## ma_result.py
Collates the results of the crosses of moving averages into a dataframe.

## ma_sim.py
Use collected data with different candlestick time intervals to find where moving averages cross and record these points.

## ma_sim_explore.ipynb
Explore the results of simulating the moving averages and the poin at which they cross. If you traded based off the crossing of moving averages, would you become profitable? Which time intervals are best matched together for the most gain - e.g. 16 against 32 day vs 16 against 64 day moving averages.

## utils.py
Some simple functions for repeated use.
  
