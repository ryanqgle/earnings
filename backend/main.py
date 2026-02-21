from fastapi import FastAPI
import requests
import json
from api_requests import get_earnings_info, get_rank_info, get_eps_history
from datetime import date, datetime

app = FastAPI()

@app.get("/debug")
async def debug():
    earnings = get_earnings_info()
    rank = get_rank_info()
    eps = get_eps_history()
    return {"earnings": earnings, "rank": rank, "eps": eps}

@app.get("/")
async def root():
    earnings_info = get_earnings_info()
    rank_info = get_rank_info()
    eps_history_info = get_eps_history()

    # normalize/parse JSON if functions returned strings
    if isinstance(earnings_info, str):
        earnings_info = json.loads(earnings_info)
    if isinstance(rank_info, str):
        rank_info = json.loads(rank_info)
    if isinstance(eps_history_info, str):
        eps_history_info = json.loads(eps_history_info)

    # normalize rows/list
    if isinstance(earnings_info, dict):
        earnings_rows = earnings_info.get("rows", [])
    elif isinstance(earnings_info, list):
        earnings_rows = earnings_info
    else:
        earnings_rows = []

    if isinstance(rank_info, dict) and "rows" in rank_info:
        rank_rows = rank_info.get("rows", [])
    elif isinstance(rank_info, list):
        rank_rows = rank_info
    else:
        rank_rows = []

    if isinstance(eps_history_info, dict) and "rows" in eps_history_info:
        eps_history_rows = eps_history_info.get("rows", [])
    elif isinstance(eps_history_info, list):
        eps_history_rows = eps_history_info
    else:
        eps_history_rows = []

    results = []
    for company in earnings_rows:
        if not isinstance(company, dict):
            continue
        results.append({
            "ticker": company.get("act_symbol"),
            "date": company.get("date"),
            "when": company.get("when"),
        })
    
    # map of rank by ticker symbol for easy lookup
    rank_map = {row.get("act_symbol"): row for row in rank_rows if isinstance(row, dict) and row.get("act_symbol")}

    # map of eps history by ticker symbol for easy lookup
    eps_history_map = {row.get("act_symbol"): row for row in eps_history_rows if isinstance(row, dict) and row.get("act_symbol")}

    for company in results:
        rank_row = rank_map.get(company["ticker"])
        if rank_row:
            company["rank"] = rank_row.get("rank")
            company["value"] = rank_row.get("value")
            company["growth"] = rank_row.get("growth")
            company["momentum"] = rank_row.get("momentum")
            company["vgm"] = rank_row.get("vgm")

        eps_history_row = eps_history_map.get(company["ticker"])
        if eps_history_row:
            company["eps_hist"] = eps_history_row.get("reported")

    return {"earningsReports": results}