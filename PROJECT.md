Project: Market Signal Pipeline

Goal:
Build a Python-based data pipeline that downloads market data,
stores it in Supabase, generates signals, and displays them on a website.

Stack:
Python
Supabase (database)
Railway (scheduled jobs)
Vercel (frontend hosting)
GitHub (version control)
Cursor + Claude (development)

Pipeline:
1. Fetch market data from APIs
2. Store raw data in Supabase
3. Generate signals from processed data
4. Store signals in Supabase
5. Display signals on website

Architecture principles:
Keep scripts modular
Separate fetching and signal generation
Keep deployment Railway-compatible
Keep frontend independent from backend