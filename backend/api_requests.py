import requests

base_url = "https://www.dolthub.com/api/v1alpha1/post-no-preference/earnings/master?q="

def get_earnings_info():
    query = "SELECT+*%0AFROM+%60earnings_calendar%60%0Awhere+date+%3E%3D+curdate%28%29%0Aand+date+%3C+date_add%28curdate%28%29%2C+interval+14+day%29%0Aand+%60when%60+%3E+%27%27%0AORDER+BY+%60date%60+ASC%0ALIMIT+1000%3B%0A"
    response = requests.get(base_url + query)
    return response.json()

def get_rank_info():
    queries = [
        "SELECT+*%0Afrom+%60rank_score%60%0Awhere+date+%3E+date_sub%28curdate%28%29%2C+interval+8+day%29%0AORDER+BY+%60date%60+desc%2C+%60act_symbol%60+asc",
        "SELECT+*%0Afrom+%60rank_score%60%0Awhere+date+%3E+date_sub%28curdate%28%29%2C+interval+8+day%29%0Aand+%60act_symbol%60+%3E+%27DEO%27%0AORDER+BY+%60date%60+desc%2C+%60act_symbol%60+asc",
        "SELECT+*%0Afrom+%60rank_score%60%0Awhere+date+%3E+date_sub%28curdate%28%29%2C+interval+8+day%29%0Aand+%60act_symbol%60+%3E+%27LPRO%27%0AORDER+BY+%60date%60+desc%2C+%60act_symbol%60+asc",
        "SELECT+*%0Afrom+%60rank_score%60%0Awhere+date+%3E+date_sub%28curdate%28%29%2C+interval+8+day%29%0Aand+%60act_symbol%60+%3E+%27SLDB%27%0AORDER+BY+%60date%60+desc%2C+%60act_symbol%60+asc"
    ]
    rank_info = []
    for query in queries:
        response = requests.get(base_url + query)
        rank_info.extend(response.json().get("rows", []))

    merged_rank_info = {"rows": rank_info}
    return merged_rank_info

def get_eps_history():
    queries = [
        "select+*%0AFROM+%28%0Aselect+*%0Afrom+%60earnings_calendar%60%0Awhere+date+%3E%3D+curdate%28%29+%0Aand+date+%3C+date_add%28curdate%28%29%2C+interval+14+day%29%0Aand+%60when%60+%3E+%27%27+%0AORDER+BY+date%0A%29+earnings%0Ajoin+%28%0Aselect+%60act_symbol%60%2C+%60period_end_date%60%2C+%60reported%60%0Afrom+%60eps_history%60%0Awhere+%60period_end_date%60+%3E%3D+date_sub%28curdate%28%29%2C+interval+5+month%29%0A%29+history%0Aon+history.act_symbol+%3D+earnings.act_symbol%0A",
        "select+*%0AFROM+%28%0Aselect+*%0Afrom+%60earnings_calendar%60%0Awhere+date+%3E%3D+curdate%28%29+%0Aand+date+%3C+date_add%28curdate%28%29%2C+interval+14+day%29%0Aand+%60when%60+%3E+%27%27+%0AORDER+BY+date%0A%29+earnings%0Ajoin+%28%0Aselect+%60act_symbol%60%2C+%60period_end_date%60%2C+%60reported%60%0Afrom+%60eps_history%60%0Awhere+%60period_end_date%60+%3E%3D+date_sub%28curdate%28%29%2C+interval+5+month%29%0Aand+%60act_symbol%60+%3E+%27DEO%27%0A%29+history%0Aon+history.act_symbol+%3D+earnings.act_symbol%0A",
        "select+*%0AFROM+%28%0Aselect+*%0Afrom+%60earnings_calendar%60%0Awhere+date+%3E%3D+curdate%28%29+%0Aand+date+%3C+date_add%28curdate%28%29%2C+interval+14+day%29%0Aand+%60when%60+%3E+%27%27+%0AORDER+BY+date%0A%29+earnings%0Ajoin+%28%0Aselect+%60act_symbol%60%2C+%60period_end_date%60%2C+%60reported%60%0Afrom+%60eps_history%60%0Awhere+%60period_end_date%60+%3E%3D+date_sub%28curdate%28%29%2C+interval+5+month%29%0Aand+%60act_symbol%60+%3E+%27LPRO%27%0A%29+history%0Aon+history.act_symbol+%3D+earnings.act_symbol%0A",
        "select+*%0AFROM+%28%0Aselect+*%0Afrom+%60earnings_calendar%60%0Awhere+date+%3E%3D+curdate%28%29+%0Aand+date+%3C+date_add%28curdate%28%29%2C+interval+14+day%29%0Aand+%60when%60+%3E+%27%27+%0AORDER+BY+date%0A%29+earnings%0Ajoin+%28%0Aselect+%60act_symbol%60%2C+%60period_end_date%60%2C+%60reported%60%0Afrom+%60eps_history%60%0Awhere+%60period_end_date%60+%3E%3D+date_sub%28curdate%28%29%2C+interval+5+month%29%0Aand+%60act_symbol%60+%3E+%27SLDB%27%0A%29+history%0Aon+history.act_symbol+%3D+earnings.act_symbol%0A"
        ]
    eps_history = []
    for query in queries:
        response = requests.get(base_url + query)
        eps_history.extend(response.json().get("rows", []))

    merged_eps_history = {"rows": eps_history}
    return merged_eps_history