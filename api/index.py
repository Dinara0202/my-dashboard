from flask import Flask, render_template_string
from supabase import create_client
import pandas as pd

app = Flask(__name__)

# Твои рабочие данные Supabase
URL = "https://ojrrzkjzdpiqektrmayj.supabase.co"
KEY = "sb_secret_GDS1jjSuepVKkXjLzPUtmg_nherw0OV"
supabase = create_client(URL, KEY)

@app.route('/')
def dashboard():
    try:
        # Получаем данные из таблицы orders
        response = supabase.table("orders").select("*").execute()
        df = pd.DataFrame(response.data)
        
        total_orders = len(df)
        total_sum = df['total_sum'].sum() if not df.empty else 0
        
        # HTML-код страницы
        html = f'''
        <html>
            <head>
                <meta charset="utf-8">
                <title>CRM Dashboard</title>
                <style>
                    body {{ font-family: -apple-system, sans-serif; padding: 40px; background: #f0f2f5; color: #1c1e21; }}
                    .container {{ max-width: 1000px; margin: auto; }}
                    .stats {{ display: flex; gap: 20px; margin-bottom: 30px; }}
                    .card {{ background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); flex: 1; }}
                    h3 {{ margin: 0; color: #65676b; font-size: 14px; text-transform: uppercase; }}
                    .value {{ font-size: 32px; font-weight: bold; margin-top: 10px; color: #007bff; }}
                    table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
                    th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #eee; }}
                    th {{ background: #007bff; color: white; font-weight: 500; }}
                    tr:last-child td {{ border-bottom: none; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📊 Дашборд заказов</h1>
                    <div class="stats">
                        <div class="card">
                            <h3>Всего заказов</h3>
                            <div class="value">{total_orders}</div>
                        </div>
                        <div class="card">
                            <h3>Общая сумма</h3>
                            <div class="value" style="color: #28a745;">{total_sum:,.0f} ₸</div>
                        </div>
                    </div>
                    
                    <h2>Детализация</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Клиент</th>
                                <th>Сумма</th>
                                <th>Статус</th>
                            </tr>
                        </thead>
                        <tbody>
                            {"".join([f"<tr><td>{r['id']}</td><td>{r.get('first_name', '—')}</td><td>{r['total_sum']} ₸</td><td>{r['status']}</td></tr>" for r in response.data])}
                        </tbody>
                    </table>
                </div>
            </body>
        </html>
        '''
        return render_template_string(html)
    except Exception as e:
        return f" Ошибка загрузки данных: {str(e)}"
