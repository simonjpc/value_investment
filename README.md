# value_investment

Python version 3.10.12

### Next steps (last update 03/11/2024)

  - add potential_ncav_candidates pipeline DONE
  - add eps-x valuation DONE
  - verify eps-x calculations ONGOING (tbfinished)
  - get real / original symbols
  - start to explore the "like product" strategy :
    - celery for tasks launch
    - basic front end
    - choice of remote host


#### Frontend

To run frontend : `npm start`


#### Backend

To run backend : `python backend/app.py`

#### Pipelines

To run pipelines : `celery -A celery_app worker --loglevel=info`
