# value_investment

Python version 3.10.12


#### Website

This project runs in [tickersarena.com](http://www.tickersarena.com)

#### Frontend

To run frontend : `npm start`

#### Backend

To run backend : `python backend/app.py`

#### Pipelines

To run pipelines : 

* Runner: `celery -A celery_app worker --loglevel=info --pool=solo` or `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES && celery -A celery_app worker --loglevel=info --pool=solo` 

* Scheduler : `celery -A celery_app beat --loglevel=info`

### Next steps (last update 03/11/2024)
  
  - check date discrepancy in site DONE
  - filter CNY companies
  - get real / original symbols
  - backtest eps-x approach
  - make the app executable via *docker-compose -f ...yml -d up*
  - update ncav and epsx pipelines for daily instead of monthly DONE
  - associate current prices table to ncav & epsx pipelines DONE
