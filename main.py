import psycopg2
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# กำหนด user เดียว
USER_ID = "admin"
USER_PASSWORD = "1234"

# Config PostgreSQL
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "mydatabase"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"

N8N_WEBHOOK_URL = "http://localhost:5678/webhook/edit_pgvector"
N8N_WEBHOOK_URL_Insert = "http://localhost:5678/webhook/insert"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def get_base_styles():
    return """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .content {
            padding: 40px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        input[type="text"]:focus, input[type="password"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            margin: 10px 5px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        .btn-secondary {
            background: linear-gradient(45deg, #74b9ff, #0984e3);
        }
        
        .btn-success {
            background: linear-gradient(45deg, #00b894, #00a085);
        }
        
        .btn-danger {
            background: linear-gradient(45deg, #e17055, #d63031);
        }
        
        .alert {
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            font-weight: 500;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .table th {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        .table td {
            padding: 15px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .table tr:hover {
            background-color: #f8f9fa;
        }
        
        .table input[type="text"] {
            margin: 0;
        }
        
        .home-link {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .home-link:hover {
            color: #764ba2;
            text-decoration: underline;
        }
        
        .welcome-card {
            text-align: center;
            padding: 30px;
        }
        
        .welcome-card h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2em;
        }
        
        .button-group {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }
        
        @media (max-width: 600px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .content {
                padding: 20px;
            }
            
            .button-group {
                flex-direction: column;
                align-items: center;
            }
            
            .table {
                font-size: 14px;
            }
        }
    </style>
    """

@app.get("/", response_class=HTMLResponse)
def login_form():
    return f"""
    <html>
        <head>
            <title>Data Management System</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {get_base_styles()}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Data Management</h1>
                    <p>ระบบจัดการข้อมูล PostgreSQL</p>
                </div>
                <div class="content">
                    <form action="/login" method="post">
                        <div class="form-group">
                            <label for="id">👤 User ID:</label>
                            <input type="text" id="id" name="id" placeholder="กรอก User ID" required>
                        </div>
                        <div class="form-group">
                            <label for="password">🔑 Password:</label>
                            <input type="password" id="password" name="password" placeholder="กรอก Password" required>
                        </div>
                        <div class="form-group" style="text-align: center;">
                            <button type="submit" class="btn">🚀 เข้าสู่ระบบ</button>
                        </div>
                    </form>
                </div>
            </div>
        </body>
    </html>
    """

@app.post("/login", response_class=HTMLResponse)
def login(id: str = Form(...), password: str = Form(...)):
    if id == USER_ID and password == USER_PASSWORD:
        return f"""
        <html>
            <head>
                <title>Dashboard - Data Management</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                {get_base_styles()}
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 ยินดีต้อนรับ!</h1>
                        <p>สวัสดี {id} - เข้าสู่ระบบสำเร็จ</p>
                    </div>
                    <div class="content">
                        <div class="welcome-card">
                            <div class="alert alert-success">
                                ✅ เข้าสู่ระบบเรียบร้อยแล้ว!
                            </div>
                            <h2>เลือกฟังก์ชันที่ต้องการ</h2>
                            <div class="button-group">
                                <form action="/add" method="get" style="margin: 0;">
                                    <button type="submit" class="btn btn-success">
                                        ➕ เพิ่มข้อมูลใหม่
                                    </button>
                                </form>
                                <form action="/edit" method="get" style="margin: 0;">
                                    <button type="submit" class="btn btn-secondary">
                                        ✏️ แก้ไขข้อมูล
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """
    return f"""
    <html>
        <head>
            <title>Login Failed - Data Management</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {get_base_styles()}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>❌ เข้าสู่ระบบไม่สำเร็จ</h1>
                </div>
                <div class="content">
                    <div class="alert alert-error">
                        <strong>ขออภัย!</strong> User ID หรือ Password ไม่ถูกต้อง
                    </div>
                    <div style="text-align: center;">
                        <a href="/" class="btn">🔄 ลองอีกครั้ง</a>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/add", response_class=HTMLResponse)
def add_page():
    return f"""
    <html>
        <head>
            <title>Add Data - Data Management</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {get_base_styles()}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>➕ เพิ่มข้อมูลใหม่</h1>
                    <p>เพิ่มข้อมูลเข้าสู่ระบบ</p>
                </div>
                <div class="content">
                    <form action="/add/save" method="post">
                        <div class="form-group">
                            <label for="text">📝 ข้อมูลใหม่:</label>
                            <input type="text" id="text" name="text" placeholder="กรอกข้อมูลที่ต้องการเพิ่ม" required>
                        </div>
                        <div class="form-group">
                            <button type="submit" class="btn btn-success">💾 บันทึกข้อมูล</button>
                            <a href="/" class="btn btn-secondary">🏠 กลับหน้าแรก</a>
                        </div>
                    </form>
                </div>
            </div>
        </body>
    </html>
    """


# @app.get("/edit", response_class=HTMLResponse)
# def edit_page():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT id, text FROM csv_data ORDER BY id")
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()

#     table_rows = ""
#     for row in rows:
#         table_rows += f"""
#         <tr>
#             <form action="/edit/save" method="post" style="display: contents;">
#                 <td><strong>#{row[0]}</strong><input type="hidden" name="id" value="{row[0]}"></td>
#                 <td><input type="text" name="text" value="{row[1]}" style="width:100%; border: 1px solid #ddd; border-radius: 4px; padding: 8px;"></td>
#                 <td><button type="submit" class="btn" style="margin: 0; padding: 8px 15px; font-size: 14px;">💾 บันทึก</button></td>
#             </form>
#         </tr>
#         """

#     return f"""
#     <html>
#         <head>
#             <title>Edit Data - Data Management</title>
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             {get_base_styles()}
#         </head>
#         <body>
#             <div class="container">
#                 <div class="header">
#                     <h1>✏️ แก้ไขข้อมูล</h1>
#                     <p>จัดการและแก้ไขข้อมูลในระบบ</p>
#                 </div>
#                 <div class="content">
#                     <table class="table">
#                         <thead>
#                             <tr>
#                                 <th style="width: 80px;">🆔 ID</th>
#                                 <th>📝 ข้อความ</th>
#                                 <th style="width: 120px;">⚡ จัดการ</th>
#                             </tr>
#                         </thead>
#                         <tbody>
#                             {table_rows}
#                         </tbody>
#                     </table>
#                     <div style="text-align: center; margin-top: 30px;">
#                         <a href="/" class="btn btn-secondary">🏠 กลับหน้าแรก</a>
#                     </div>
#                 </div>
#             </div>
#         </body>
#     </html>
#     """

@app.get("/edit", response_class=HTMLResponse)
def edit_page():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, text FROM csv_data ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    table_rows = ""
    for row in rows:
        # Escape HTML characters to prevent XSS and display correctly
        escaped_text = str(row[1]).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')
        table_rows += f"""
        <tr>
            <form action="/edit/save" method="post" style="display: contents;">
                <td><strong>#{row[0]}</strong><input type="hidden" name="id" value="{row[0]}"></td>
                <td><textarea name="text" rows="3" style="width:100%; border: 1px solid #ddd; border-radius: 4px; padding: 8px; resize: vertical; min-height: 60px;">{escaped_text}</textarea></td>
                <td><button type="submit" class="btn" style="margin: 0; padding: 8px 15px; font-size: 14px;">💾 บันทึก</button></td>
            </form>
        </tr>
        """

    return f"""
    <html>
        <head>
            <title>Edit Data - Data Management</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {get_base_styles()}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✏️ แก้ไขข้อมูล</h1>
                    <p>จัดการและแก้ไขข้อมูลในระบบ</p>
                </div>
                <div class="content">
                    <table class="table">
                        <thead>
                            <tr>
                                <th style="width: 80px;">🆔 ID</th>
                                <th>📝 ข้อความ</th>
                                <th style="width: 120px;">⚡ จัดการ</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="/" class="btn btn-secondary">🏠 กลับหน้าแรก</a>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.post("/edit/save", response_class=HTMLResponse)
def save_edit(id: str = Form(...), text: str = Form(...)):
    # ส่ง webhook ไป n8n
    payload = {"id": id, "text": text}
    try:
        requests.post(N8N_WEBHOOK_URL, json=payload)
        webhook_status = "✅ ส่ง webhook เรียบร้อย"
        alert_class = "alert-success"
    except Exception as e:
        webhook_status = f"❌ ส่ง webhook ไม่สำเร็จ ({e})"
        alert_class = "alert-error"

    return f"""
    <html>
        <head>
            <title>Save Complete - Data Management</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {get_base_styles()}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💾 บันทึกข้อมูลเรียบร้อย</h1>
                    <p>ข้อมูลได้รับการอัพเดทแล้ว</p>
                </div>
                <div class="content">
                    <div class="alert {alert_class}">
                        <h3>📋 รายละเอียดการบันทึก</h3>
                        <p><strong>🆔 ID:</strong> {id}</p>
                        <p><strong>📝 ข้อความ:</strong> {text}</p>
                        <p><strong>🔔 สถานะ Webhook:</strong> {webhook_status}</p>
                    </div>
                    <div style="text-align: center;">
                        <a href="/edit" class="btn btn-secondary">↩️ กลับไปแก้ไขข้อมูล</a>
                        <a href="/" class="btn">🏠 หน้าแรก</a>
                    </div>s
                </div>
            </div>
        </body>
    </html>
    """

@app.post("/add/save", response_class=HTMLResponse)
def save_add(text: str = Form(...)):
    # ส่ง webhook ไป n8n
    payload = {"text": text}
    try:
        requests.post(N8N_WEBHOOK_URL_Insert, json=payload)
        webhook_status = "✅ ส่ง webhook เรียบร้อย"
        alert_class = "alert-success"
    except Exception as e:
        webhook_status = f"❌ ส่ง webhook ไม่สำเร็จ ({e})"
        alert_class = "alert-error"

    return f"""
    <html>
        <head>
            <title>Insert Complete - Data Management</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {get_base_styles()}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💾 บันทึกข้อมูลเรียบร้อย</h1>
                    <p>ข้อมูลได้รับการอัพเดทแล้ว</p>
                </div>
                <div class="content">
                    <div class="alert {alert_class}">
                        <h3>📋 รายละเอียดการบันทึก</h3>
                        <p><strong>🆔 ID:</strong> {id}</p>
                        <p><strong>📝 ข้อความ:</strong> {text}</p>
                        <p><strong>🔔 สถานะ Webhook:</strong> {webhook_status}</p>
                    </div>
                    <div style="text-align: center;">
                        <a href="/add" class="btn btn-secondary">↩️ กลับไปแก้ไขข้อมูล</a>
                        <a href="/" class="btn">🏠 หน้าแรก</a>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    