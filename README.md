Precious Metal Agent
AI-Powered Precious Metals Trading Assistant

An intelligent trading assistant built with Python that simulates how modern trading
desks can combine market data pipelines, financial analytics, risk assessment, and
agentic AI workflows to generate market insights and trading recommendations.

The system collects and normalizes precious metals market data, performs
quantitative analysis, evaluates trading risk, and uses a ReAct-style AI 
agent to answer trading-related questions using tool-calling and reasoning loops.

Project Highlights
Market Data Pipeline
Fetches data from multiple market sources
Handles inconsistent source formats
Retries failed API calls
Deduplicates records
Normalizes data into a unified schema
Stores market data in SQLite
Financial Analytics

The analysis engine calculates:

Volume-Weighted Average Price (VWAP)
Moving Averages
Bid-Ask Spread Analysis
Rolling Z-Score Anomaly Detection
Bullish/Bearish Trend Classification
Risk Assessment Engine

The system evaluates multiple market risk factors:

Market spread stress
Price anomalies
Inventory coverage
Trend direction
Liquidity and volume decline

It generates a risk score and classifies market conditions as:

Low Risk
Medium Risk
High Risk
Agentic AI Framework

A ReAct-style AI agent powers decision making through:

Question
   ↓
Reason
   ↓
Select Tool
   ↓
Execute Tool
   ↓
Observe Result
   ↓
Generate Answer

The agent can:

Retrieve market prices
Calculate VWAP
Evaluate trends
Check inventory
Compare spreads
Generate trading recommendations
Example Agent Query
User Question
Should I buy gold?
Agent Reasoning
Trend = Bearish
Risk Score = 55
Risk Level = Medium
VWAP = 2348.00
Agent Response
Recommendation for gold: WAIT.

Trend is bearish,
risk is medium (55/100),
and VWAP is 2348.00.
Architecture
Market API Layer
        │
        ▼
 Data Pipeline
        │
        ▼
 SQLite Storage
        │
        ▼
 Analytics Engine
        │
        ▼
 Risk Engine
        │
        ▼
 Agent Tools
        │
        ▼
 ReAct Agent
        │
        ▼
 Trading Recommendation
 
Technology Stack
Core
Python 3
SQLite
Git
AI Engineering
ReAct Agent Framework
Tool Calling
Prompt Engineering
Structured Output Parsing
Agent Reasoning Loops
Analytics
Statistical Analysis
VWAP Calculation
Anomaly Detection
Risk Scoring
Trend Analysis


Project Structure

precious-metal-agent/
├── main.py
├── market_api.py
├── pipeline.py
├── analysis.py
├── risk.py
├── tools.py
├── prompts.py
├── agent.py
├── requirements.txt
└── README.md

Running the Project

Clone the repository:
git clone https://github.com/Amazing-P/precious-metal-agent.git

Navigate into the project:
cd precious-metal-agent

Create a virtual environment:
python -m venv venv

Activate the environment:
venv\Scripts\activate

Run the application:
python main.py

Sample Output
Gold VWAP: 2348.00
Trend: Bearish
Risk Level: Medium
Risk Score: 55/100

Agent Recommendation:
'Recommendation for gold: WAIT. Trend is bearish, risk is medium '


Skills Demonstrated
This project demonstrates practical experience in:

Python Software Engineering
Data Pipelines
API Integration
Financial Analytics
Risk Modeling
Agentic AI
Prompt Engineering
Tool Calling
Structured Output Parsing
SQLite Databases
ReAct Agent Design
Future Improvements
Real-time market data integration
OpenAI / Claude API integration
FastAPI REST endpoints
Streamlit dashboard
Machine Learning price forecasting
Portfolio optimization engine
Docker deployment
Cloud hosting
Disclaimer

This project is intended for educational, research, and portfolio purposes only.

It does not provide financial advice and should not be used for live trading decisions.
