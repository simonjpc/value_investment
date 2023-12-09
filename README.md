# value_investment

Python version 3.10.12

### Next steps

These is the list of tasks to do that do not depend on any other task:

- Code unit tests for the functions of script `extractor.py`. Here some mockup will be needed. DONE
- Create script where the calculations of the EPS X valuation is done using the functions from `eps_multiple.py`. DONE
- Add/create functions that compute the liquidation value and ncav. DONE
- Add utils functions used for the liquidation/ncav calculations. DONE
- Design the data storage system (simples system):
  - read some balance sheet info. DONE
  - define columns/keys to keep for balance sheet info. DONE
  - read some income statement info. DONE
  - define columns/keys to keep for income statement info. DONE
  - concat on datetime. DONE
  - create table that will store all the info. DONE
  - define the column names and types. DONE
  - dump the data of a single company into de db. DONE
  - look for how to parallelize the dump to avoid for loops with companies. DONE
  - Do the same for all the companies.

  - Create table of id, ticker
  - Create table of daily prices per ticker

- Define how to automatically choose companies below fair value (both approaches).


#### Regarding the price extraction for backtesting

How it happens today:
- I get the mrq balance sheet info and with it I compute the intrinsic value of a company
- I get the price of today
- I check whether the intrinsic value computed with the mrq balance sheet is greater that today's price

How it should happen in the past:
- I select a given balance sheet, that will be my mrq balance sheet
- I get the prices for every X period of time after the filling date of the selected balance sheet and before the filling date of the next balance sheet
- I check whether for any of the extracted prices I am below intrinsic value

#### last update 09/12/2023 : 

 - Relaunch de tickers pipeline, stmts data pipeline and prices data before full backtesting