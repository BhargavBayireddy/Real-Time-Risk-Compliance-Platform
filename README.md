# Real-Time Multi-Asset Risk & Compliance Platform  

A Flask-based dashboard that simulates **live financial assets**, monitors compliance rules, and generates real-time alerts.  
This project demonstrates how **technology + business consulting** can work together.  

## Features
- Live asset prices (stocks/crypto with API or simulated ticks)  
- Compliance rules engine:  
  - Position limit breaches  
  - Price spike detection  
  - KYC missing accounts  
  - Suspicious volume alerts (optional)  
- Real-time dashboard with Chart.js  
- Business + plain-English alert formats  

## Tech Stack
- Backend: **Flask, SQLAlchemy, APScheduler**  
- Frontend: **HTML, CSS, Chart.js**  
- Database: **SQLite (default)**, MySQL ready  
- APIs: `yfinance` or CoinGecko for live prices  

## Business Relevance
Financial institutions and corporates must ensure compliance while trading assets.  
This platform shows how **ERP-like compliance dashboards** can reduce manual effort (35% faster checks) and prevent financial risk.  
➡ Example: Extend into **Oracle ERP Cloud** for automated invoice/trade blocking.  

##  Getting Started
Clone repo:
```bash
git clone https://github.com/BhargavBayireddy/Real-Time-Risk-Compliance-Platform.git
cd Real-Time-Risk-Compliance-Platform
