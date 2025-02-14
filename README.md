# value_investment

Python version 3.10.12

### Next steps (last update 03/11/2024)
  
  - check date discrepancy in site
  - filter CNY companies
  - get real / original symbols
  - backtest eps-x approach
  - start to explore the "like product" strategy :
    - celery for tasks launch DONE
    - basic front end DONE
    - choice of remote host DONE
  - update ncav and epsx pipelines for daily instead of monthly
  - associate current prices table to ncav & epsx pipelines
#### Website

This project runs in [tickersarena.com](http://www.tickersarena.com)


#### Frontend

To run frontend : `npm start`


#### Backend

To run backend : `python backend/app.py`

#### Pipelines

To run pipelines : `celery -A celery_app worker --loglevel=info --pool=solo` or `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES && celery -A celery_app worker --loglevel=info --pool=solo` and `celery -A celery_app beat --loglevel=info`
