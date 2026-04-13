from flask import Flask, render_template_string
from supabase import create_client

app = Flask(__name__)

# Твои данные
URL = "https://ojrrzkjzdpiqektrmayj.supabase.co"
KEY = "sb_secret_GDS1jjSuepVKkXjLzPUtmg_nherw0OV"
supabase = create_client(URL, KEY)

@app.route('/')
def dashboard():
    try:
        # Получаем данные напрямую массивом
        response = supabase.table("orders").select("*").execute()
        data = response.data
        
        # Считаем суммы простым циклом (без тяжелого pandas)
        total_orders = len(data)
        total_sum = sum(float(row.get('total_sum', 0)) for row in data)
        
        html = f'''
        <html>
            <head>
                <meta charset="utf-8">
                <title>CRM Dashboard</title>
                <style>
                    body {{ font-family: -apple-system, sans-serif; padding: 40px; background: #f0f2f5; }}
                    .card {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; min-width: 200px; margin-right: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 30px; background: white; border-radius: 8px; overflow: hidden; }}
                    th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #eee; }}
                    th {{ background: #007bff; color: white; }}
                    tr:hover {{ background: #f9f9f9; }}
                </style>
            </head>
            <body>
                <h1>📊 Дашборд заказов</h1>
                <div class="card"><h3>📦 Всего заказов</h3><p style="font-size: 28px; color: #007bff; font-weight: bold;">{total_orders}</p></div>
                <div class="card"><h3>💰 Общая сумма</h3><p style="font-size: 28px; color: #28a745; font-weight: bold;">{total_sum:,.0f} ₸</p></div>
                
                <table>
                    <thead>
                        <tr><th>ID</th><th>Клиент</th><th>Сумма</th><th>Статус</th></tr>
                    </thead>
                    <tbody>
                        {"".join([f"<tr><td>{r['id']}</td><td>{r.get('first_name', '—')}</td><td>{r['total_sum']} ₸</td><td>{r['status']}</td></tr>" for r in data])}
                    </tbody>
                </table>
            </body>
        </html>
        '''
        return render_template_string(html)
    except Exception as e:
        return f"<h1>Ошибка конфигурации</h1><p>{str(e)}</p>"
