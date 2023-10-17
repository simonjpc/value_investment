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
  - look for how to parallelize the dump to avoid for loops with companies.
  - Do the same for all the companies.
- Define how to automatically choose companies below fair value (both approaches).
