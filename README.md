# Value Investment

A Python-based project for analyzing and identifying value investment opportunities. This project includes a backend, a frontend, and data processing pipelines to support investment decision-making.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [License](#license)

---

## Overview

This project is designed to analyze financial data and identify value investment opportunities using various metrics such as NCAV (Net Current Asset Value) and EPS-X (Earnings Per Share Exclusion). It includes:

- A **backend** for data processing and API services.
- A **frontend** for user interaction and visualization.
- **Pipelines** for data ingestion, processing, and scheduling.

The project is hosted at [tickersarena.com](http://www.tickersarena.com).

---

## Features

- **Frontend**: Interactive web interface for data visualization.
- **Backend**: Python-based API for data processing.
- **Data Pipelines**: Automated workflows using Celery for task scheduling.
- **Backtesting**: Tools for evaluating investment strategies.

---

## Installation

### Prerequisites

- Python 3.10.12 or greater
- Node.js (for the frontend)
- Redis (for Celery task queue)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/value_investment.git
   cd value_investment
   ```


2. Install backend dependencies:
  ```bash
  pip install -r requirements.txt
  ```

3. Install frontend dependencies:
  ```bash
  cd frontend
  npm install
  ```

4. Set up environment variables:

  - Backend: Create a local.env file in the root directory.
  - Frontend: Update .env in the frontend folder.

### Usage

#### Running the Backend

Start the backend server:
  ```bash
  python [app.py](backend/app.py)
  ```

#### Running the Frontend

Start the frontend development server:
  ```bash
  cd frontend
  npm start
  ```


#### Running Pipelines

Start the Celery worker:
  ```bash
  celery -A celery_app worker --loglevel=info --pool=solo
  ```

  or 

  ```bash
  celery -A celery_app worker --loglevel=info --pool=solo` or `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES && celery -A celery_app worker --loglevel=info --pool=solo
  ```

Start the Celery scheduler:
  ```bash
  celery -A celery_app beat --loglevel=info
  ```

### License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

### Next steps (last update 16/02/2025)
  
  - filter CNY companies
  - make real / original symbols mapping
  - filter out eps-x candidates without float value
  - backtest eps-x approach
  - make the app executable via *docker-compose -f ...yml -d up*
