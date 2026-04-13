from flask import Flask, render_template_string
from supabase import create_client

app = Flask(__name__)

# Данные подключения
URL = "https://ojrrzkjzdpiqektrmayj.supabase.co"
KEY = "sb_secret_GDS1jjSuepVKkXjLzPUtmg_nherw0OV"
supabase = create_client(URL, KEY)

@app.route('/')
def dashboard():
    try:
        # 1. Загружаем данные
        res = supabase.table("orders").select("*").execute()
        data = res.data
        
        # 2. Считаем итоги (без pandas, чтобы не было ошибок)
        count = len(data)
        total = sum(float(item.get('total_sum', 0)) for item in data)
        
        # 3. Формируем таблицу
        rows = "".join([
            f"<tr><td>{o['id']}</td><td>{o.get('first_name', '—')}</td><td>{o['total_sum']} ₸</td><td>{o['status']}</td></tr>" 
            for o in data
        ])

        return render_template_string(f'''
            <html>
                <head>
                    <meta charset="utf-8">
                    <title>CRM Dashboard</title>
                    <style>
                        body {{ font-family: sans-serif; padding: 40px; background: #f4f7f6; color: #333; }}
                        .container {{ max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                        .stats {{ display: flex; gap: 20px; margin-bottom: 20px; }}
                        .card {{ flex: 1; padding: 20px; border: 1px solid #eee; border-radius: 10px; text-align: center; }}
                        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
                        th {{ background: #007bff; color: white; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>📊 Итоги заказов</h1>
                        <div class="stats">
                            <div class="card"><h3>📦 Заказов</h3><p style="font-size: 24px; font-weight: bold;">{count}</p></div>
                            <div class="card"><h3>💰 Сумма</h3><p style="font-size: 24px; font-weight: bold; color: green;">{total:,.0f} ₸</p></div>
                        </div>
                        <table>
                            <tr><th>ID</th><th>Имя</th><th>Сумма</th><th>Статус</th></tr>
                            {rows}
                        </table>
                    </div>
                </body>
            </html>
        ''')
    except Exception as e:
        return f"<h1>Ошибка!</h1><p>{str(e)}</p>"

# Это нужно для Vercel
app = app
