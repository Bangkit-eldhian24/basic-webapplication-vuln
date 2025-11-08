from flask import Flask, request, render_template_string, session, redirect
import sqlite3
import subprocess
import requests
import os
import html

app = Flask(__name__)
app.secret_key = 'vulnerable_secret_key_12345'
app.config['SECRET_KEY'] = 'vulnerable_secret_key_12345'

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        'title': 'VulnWeb - Security Vulnerability Demo',
        'warning': '⚠️ WARNING: This application contains intentional security vulnerabilities. Use only in controlled testing environments! Do not deploy on the internet!',
        'search_placeholder': 'Search something...',
        'search_button': 'Search',
        'xss_examples': 'XSS Examples:',
        'sql_injection': 'SQL Injection',
        'username': 'Username',
        'password': 'Password',
        'login': 'Login',
        'test_credentials': 'Test Credentials:',
        'sql_payloads': 'SQL Injection Payloads:',
        'rce': 'Remote Code Execution (RCE)',
        'host_placeholder': 'Enter host/ip',
        'ping': 'Ping',
        'rce_examples': 'RCE Payload Examples:',
        'idor': 'Insecure Direct Object Reference (IDOR)',
        'view_my_profile': 'View My Profile (ID: 1)',
        'view_other_profile': 'View Other User Profile (ID: 2)',
        'view_nonexistent': 'View Non-Existent Profile (ID: 100)',
        'idor_vulnerability': 'Vulnerability: Can access other users data without authorization',
        'csrf': 'Cross-Site Request Forgery (CSRF)',
        'amount_placeholder': 'Transfer amount',
        'account_placeholder': 'Destination account',
        'transfer_money': 'Transfer Money',
        'csrf_vulnerability': 'Vulnerability: No CSRF token protection',
        'ssrf': 'Server-Side Request Forgery (SSRF)',
        'url_placeholder': 'URL to fetch',
        'fetch_url': 'Fetch URL',
        'ssrf_examples': 'SSRF Payload Examples:',
        'port_scanning': 'Port scanning',
        'back_home': '← Back to Home',
        'login_success': 'Login Successful!',
        'welcome': 'Welcome',
        'login_failed': 'Login Failed!',
        'wrong_credentials': 'Wrong username or password',
        'sql_error': 'SQL Error',
        'query_executed': 'Query executed',
        'ping_results': 'Ping Results',
        'command_executed': 'Command executed',
        'error': 'Error',
        'user_profile': 'User Profile',
        'user_not_found': 'User not found',
        'transfer_success': 'Transfer Successful! 💸',
        'amount': 'Amount',
        'to_account': 'To account',
        'transaction_processed': 'Transaction processed',
        'csrf_vulnerable': 'This request has no CSRF token protection!',
        'fetch_results': 'URL Fetch Results',
        'status_code': 'Status Code',
        'content_preview': 'Content Preview (first 2000 chars)',
        'error_fetch': 'Fetch Error',
        'idor_vulnerable': 'You can access other user profiles without authorization!',
        'try_again': '← Try Again',
        'search_results': 'Search Results',
        'query': 'Query',
        'xss_vulnerable': 'This is vulnerable to XSS! Try injecting scripts.'
    },
    'id': {
        'title': 'VulnWeb - Demonstrasi Kerentanan Keamanan',
        'warning': '⚠️ PERINGATAN: Aplikasi ini mengandung kerentanan keamanan yang disengaja. Hanya gunakan di lingkungan testing yang terkontrol! Jangan deploy di internet!',
        'search_placeholder': 'Cari sesuatu...',
        'search_button': 'Cari',
        'xss_examples': 'Contoh XSS:',
        'sql_injection': 'SQL Injection',
        'username': 'Username',
        'password': 'Password',
        'login': 'Login',
        'test_credentials': 'Kredensial Testing:',
        'sql_payloads': 'Payload SQL Injection:',
        'rce': 'Remote Code Execution (RCE)',
        'host_placeholder': 'Masukkan host/ip',
        'ping': 'Ping',
        'rce_examples': 'Contoh Payload RCE:',
        'idor': 'Insecure Direct Object Reference (IDOR)',
        'view_my_profile': 'Lihat Profil Saya (ID: 1)',
        'view_other_profile': 'Lihat Profil User Lain (ID: 2)',
        'view_nonexistent': 'Lihat Profil Tidak Ada (ID: 100)',
        'idor_vulnerability': 'Kerentanan: Bisa akses data user lain tanpa authorization',
        'csrf': 'Cross-Site Request Forgery (CSRF)',
        'amount_placeholder': 'Jumlah transfer',
        'account_placeholder': 'Rekening tujuan',
        'transfer_money': 'Transfer Uang',
        'csrf_vulnerability': 'Kerentanan: Tidak ada CSRF token protection',
        'ssrf': 'Server-Side Request Forgery (SSRF)',
        'url_placeholder': 'URL untuk di-fetch',
        'fetch_url': 'Fetch URL',
        'ssrf_examples': 'Contoh Payload SSRF:',
        'port_scanning': 'Port scanning',
        'back_home': '← Kembali ke Home',
        'login_success': 'Login Berhasil!',
        'welcome': 'Selamat datang',
        'login_failed': 'Login Gagal!',
        'wrong_credentials': 'Username atau password salah',
        'sql_error': 'Error SQL',
        'query_executed': 'Query yang dijalankan',
        'ping_results': 'Hasil Ping',
        'command_executed': 'Command yang dijalankan',
        'error': 'Error',
        'user_profile': 'Profil User',
        'user_not_found': 'User tidak ditemukan',
        'transfer_success': 'Transfer Berhasil! 💸',
        'amount': 'Jumlah',
        'to_account': 'Ke rekening',
        'transaction_processed': 'Transaksi diproses',
        'csrf_vulnerable': 'Request ini tidak ada CSRF token protection!',
        'fetch_results': 'Hasil Fetch URL',
        'status_code': 'Status Code',
        'content_preview': 'Preview Konten (2000 karakter pertama)',
        'error_fetch': 'Error Fetch',
        'idor_vulnerable': 'Anda bisa akses profil user lain tanpa authorization!',
        'try_again': '← Coba Lagi',
        'search_results': 'Hasil Pencarian',
        'query': 'Query',
        'xss_vulnerable': 'Ini vulnerable to XSS! Coba inject script.'
    }
}

def get_translation(key, lang='en'):
    return TRANSLATIONS[lang].get(key, key)

def get_current_language():
    return session.get('lang', 'en')

def generate_html():
    lang = get_current_language()
    t = lambda key: get_translation(key, lang)
    
    return f'''
<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t('title')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .nav {{ background: #333; padding: 10px; margin-bottom: 20px; border-radius: 5px; }}
        .nav a {{ color: white; text-decoration: none; padding: 10px 15px; display: inline-block; }}
        .nav a:hover {{ background: #555; border-radius: 3px; }}
        .vuln-section {{ border: 2px solid #ddd; padding: 20px; margin: 15px 0; border-radius: 8px; background: #fafafa; }}
        .warning {{ background: #fff3cd; border: 2px solid #ffeaa7; padding: 15px; margin: 15px 0; border-radius: 5px; }}
        form {{ margin: 15px 0; }}
        input, button {{ padding: 10px; margin: 5px; border: 1px solid #ccc; border-radius: 4px; }}
        button {{ background: #007bff; color: white; cursor: pointer; }}
        button:hover {{ background: #0056b3; }}
        code {{ background: #eee; padding: 2px 5px; border-radius: 3px; }}
        .result {{ background: #e9ecef; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .lang-switcher {{ float: right; margin-top: -50px; }}
        .lang-btn {{ background: #6c757d; color: white; border: none; padding: 8px 15px; border-radius: 3px; cursor: pointer; text-decoration: none; display: inline-block; }}
        .lang-btn:hover {{ background: #545b62; }}
        .lang-active {{ background: #0056b3; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="lang-switcher">
            <a href="/set_language/en" class="lang-btn {'lang-active' if lang == 'en' else ''}">English</a>
            <a href="/set_language/id" class="lang-btn {'lang-active' if lang == 'id' else ''}">Indonesia</a>
        </div>
        
        <h1>🔓 {t('title')}</h1>
        
        <div class="warning">
            <strong>{t('warning')}</strong>
        </div>

        <div class="nav">
            <a href="#xss">XSS</a>
            <a href="#sqli">SQLi</a>
            <a href="#rce">RCE</a>
            <a href="#idor">IDOR</a>
            <a href="#csrf">CSRF</a>
            <a href="#ssrf">SSRF</a>
        </div>

        <!-- XSS Section -->
        <div id="xss" class="vuln-section">
            <h2>🔍 XSS</h2>
            <form method="GET" action="/search">
                <input type="text" name="q" placeholder="{t('search_placeholder')}" style="width: 300px;" value="">
                <button type="submit">{t('search_button')}</button>
            </form>
            <p><strong>{t('xss_examples')}</strong></p>
            <ul>
                <li><code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code></li>
                <li><code>&lt;img src=x onerror=alert('Hacked')&gt;</code></li>
            </ul>
        </div>

        <!-- SQL Injection Section -->
        <div id="sqli" class="vuln-section">
            <h2>🗃️ {t('sql_injection')}</h2>
            <form method="POST" action="/login">
                <input type="text" name="username" placeholder="{t('username')}" required>
                <input type="password" name="password" placeholder="{t('password')}" required>
                <button type="submit">{t('login')}</button>
            </form>
            <p><strong>{t('test_credentials')}</strong></p>
            <ul>
                <li>Username: <code>admin</code> | Password: <code>password123</code></li>
                <li>Username: <code>user1</code> | Password: <code>pass123</code></li>
            </ul>
            <p><strong>{t('sql_payloads')}</strong></p>
            <ul>
                <li>Username: <code>' OR '1'='1' --</code> | Password: <code>anything</code></li>
                <li>Username: <code>admin' --</code> | Password: <code>[empty]</code></li>
            </ul>
        </div>

        <!-- RCE Section -->
        <div id="rce" class="vuln-section">
            <h2>⚡ {t('rce')}</h2>
            <form method="POST" action="/ping">
                <input type="text" name="host" placeholder="{t('host_placeholder')}" value="127.0.0.1" style="width: 300px;">
                <button type="submit">{t('ping')}</button>
            </form>
            <p><strong>{t('rce_examples')}</strong></p>
            <ul>
                <li><code>127.0.0.1; whoami</code></li>
                <li><code>127.0.0.1 && ls -la</code></li>
                <li><code>127.0.0.1 | dir</code> (Windows)</li>
            </ul>
        </div>

        <!-- IDOR Section -->
        <div id="idor" class="vuln-section">
            <h2>👁️ {t('idor')}</h2>
            <p><a href="/profile/1" style="color: blue; text-decoration: underline;">📄 {t('view_my_profile')}</a></p>
            <p><a href="/profile/2" style="color: blue; text-decoration: underline;">👤 {t('view_other_profile')}</a></p>
            <p><a href="/profile/100" style="color: blue; text-decoration: underline;">❌ {t('view_nonexistent')}</a></p>
            <p><strong>{t('idor_vulnerability')}</strong></p>
        </div>

        <!-- CSRF Section -->
        <div id="csrf" class="vuln-section">
            <h2>🔄 {t('csrf')}</h2>
            <form method="POST" action="/transfer">
                <input type="number" name="amount" placeholder="{t('amount_placeholder')}" value="1000000">
                <input type="text" name="to_account" placeholder="{t('account_placeholder')}" value="ATTACKER123">
                <button type="submit">{t('transfer_money')}</button>
            </form>
            <p><strong>{t('csrf_vulnerability')}</strong></p>
        </div>

        <!-- SSRF Section -->
        <div id="ssrf" class="vuln-section">
            <h2>🌐 {t('ssrf')}</h2>
            <form method="POST" action="/fetch">
                <input type="text" name="url" placeholder="{t('url_placeholder')}" style="width: 400px;" value="http://localhost:5000">
                <button type="submit">{t('fetch_url')}</button>
            </form>
            <p><strong>{t('ssrf_examples')}</strong></p>
            <ul>
                <li><code>file:///etc/passwd</code> (Linux)</li>
                <li><code>file:///C:/Windows/System32/drivers/etc/hosts</code> (Windows)</li>
                <li><code>http://localhost:22</code> ({t('port_scanning')})</li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

# Database setup
def init_db():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
    
    # Clear existing data and insert fresh
    c.execute("DELETE FROM users")
    c.execute("INSERT INTO users VALUES (1, 'admin', 'password123', 'admin@example.com')")
    c.execute("INSERT INTO users VALUES (2, 'user1', 'pass123', 'user1@example.com')")
    c.execute("INSERT INTO users VALUES (3, 'john', 'john123', 'john@example.com')")
    conn.commit()
    conn.close()
    print("✅ Database initialized!")

# Language switcher
@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'id']:
        session['lang'] = lang
    return redirect('/')

# 🔓 XSS Vulnerability
@app.route('/search')
def search():
    query = request.args.get('q', '')
    lang = get_current_language()
    t = lambda key: get_translation(key, lang)
    
    # Vulnerable: No output encoding - XSS here!
    return f'''
    <div class="container">
        <h2>🔍 {t('search_results')}</h2>
        <div class="result">
            <h3>{t('query')}: {query}</h3>
            <p><em>{t('xss_vulnerable')}</em></p>
        </div>
        <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('back_home')}</a>
    </div>
    '''

# 🗃️ SQL Injection Vulnerability
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    lang = get_current_language()
    t = lambda key: get_translation(key, lang)
    
    # Vulnerable: Direct string concatenation
    conn = sqlite3.connect('database.db', check_same_thread=False)
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    try:
        c.execute(query)
        user = c.fetchone()
        if user:
            result = f'''
            <div class="container">
                <h2>✅ {t('login_success')}</h2>
                <div class="result" style="background: #d4edda;">
                    <h3>{t('welcome')} {user[1]}!</h3>
                    <p><strong>ID:</strong> {user[0]}</p>
                    <p><strong>Email:</strong> {user[3]}</p>
                </div>
                <p><strong>{t('query_executed')}:</strong></p>
                <code>{html.escape(query)}</code>
                <br><br>
                <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('back_home')}</a>
            </div>
            '''
        else:
            result = f'''
            <div class="container">
                <h2>❌ {t('login_failed')}</h2>
                <div class="result" style="background: #f8d7da;">
                    <p>{t('wrong_credentials')}</p>
                </div>
                <p><strong>{t('query_executed')}:</strong></p>
                <code>{html.escape(query)}</code>
                <br><br>
                <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('try_again')}</a>
            </div>
            '''
    except Exception as e:
        result = f'''
        <div class="container">
            <h2>💥 {t('sql_error')}</h2>
            <div class="result" style="background: #f8d7da;">
                <p><strong>{t('error')}:</strong> {str(e)}</p>
            </div>
            <p><strong>{t('query_executed')}:</strong></p>
            <code>{html.escape(query)}</code>
            <br><br>
            <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('back_home')}</a>
        </div>
        '''
    finally:
        conn.close()
    
    return result

# ⚡ RCE Vulnerability
@app.route('/ping', methods=['POST'])
def ping():
    host = request.form.get('host', '127.0.0.1')
    lang = get_current_language()
    t = lambda key: get_translation(key, lang)
    
    # Vulnerable: Direct command execution
    try:
        # Deteksi OS
        if os.name == 'nt':  # Windows
            cmd = f'ping -n 2 {host}'
        else:  # Linux/Mac
            cmd = f'ping -c 2 {host}'
            
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        output = f'''
        <div class="container">
            <h2>⚡ {t('ping_results')}</h2>
            <div class="result">
                <p><strong>{t('command_executed')}:</strong></p>
                <code>{html.escape(cmd)}</code>
                <pre style="background: black; color: lime; padding: 15px; border-radius: 5px; overflow-x: auto;">{html.escape(result.decode())}</pre>
            </div>
            <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('back_home')}</a>
        </div>
        '''
    except subprocess.CalledProcessError as e:
        output = f'''
        <div class="container">
            <h2>❌ {t('error_ping')}</h2>
            <div class="result" style="background: #f8d7da;">
                <p><strong>{t('command_executed')}:</strong> <code>{html.escape(cmd)}</code></p>
                <pre>{t('error')}: {html.escape(e.output.decode())}</pre>
            </div>
            <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('back_home')}</a>
        </div>
        '''
    except Exception as e:
        output = f'''
        <div class="container">
            <h2>💥 {t('error')}</h2>
            <div class="result" style="background: #f8d7da;">
                <p>{t('error')}: {str(e)}</p>
            </div>
            <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('back_home')}</a>
        </div>
        '''
    
    return output

# 👁️ IDOR Vulnerability
@app.route('/profile/<int:user_id>')
def profile(user_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    
    lang = get_current_language()
    t = lambda key: get_translation(key, lang)
    
    if user:
        # Vulnerable: No authorization check
        return f'''
        <div class="container">
            <h2>👤 {t('user_profile')}</h2>
            <div class="result">
                <p><strong>ID:</strong> {user[0]}</p>
                <p><strong>Username:</strong> {user[1]}</p>
                <p><strong>Password:</strong> {user[2]}</p>
                <p><strong>Email:</strong> {user[3]}</p>
            </div>
            <div class="warning">
                <strong>🔓 {t('idor_vulnerable')}</strong>
            </div>
            <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('back_home')}</a>
        </div>
        '''
    else:
        return f'''
        <div class="container">
            <h2>❌ {t('user_not_found')}</h2>
            <div class="result" style="background: #f8d7da;">
                <p>{t('user_not_found')}.</p>
            </div>
            <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('back_home')}</a>
        </div>
        '''

# 🔄 CSRF Vulnerability
@app.route('/transfer', methods=['POST'])
def transfer():
    amount = request.form.get('amount')
    to_account = request.form.get('to_account')
    lang = get_current_language()
    t = lambda key: get_translation(key, lang)
    
    # Vulnerable: No CSRF protection
    return f'''
    <div class="container">
        <h2>✅ {t('transfer_success')}</h2>
        <div class="result" style="background: #d4edda;">
            <p><strong>{t('amount')}:</strong> Rp {amount}</p>
            <p><strong>{t('to_account')}:</strong> {to_account}</p>
            <p><strong>Time:</strong> {t('transaction_processed')}</p>
        </div>
        <div class="warning">
            <strong>🔓 {t('csrf_vulnerable')}</strong>
        </div>
        <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('back_home')}</a>
    </div>
    '''

# 🌐 SSRF Vulnerability
@app.route('/fetch', methods=['POST'])
def fetch_url():
    url = request.form.get('url', 'http://localhost:5000')
    lang = get_current_language()
    t = lambda key: get_translation(key, lang)
    
    # Vulnerable: No URL validation
    try:
        response = requests.get(url, timeout=5, verify=False)
        return f'''
        <div class="container">
            <h2>🌐 {t('fetch_results')}</h2>
            <div class="result">
                <p><strong>URL:</strong> {html.escape(url)}</p>
                <p><strong>{t('status_code')}:</strong> {response.status_code}</p>
                <p><strong>{t('content_preview')}:</strong></p>
                <pre style="background: #eee; padding: 15px; border-radius: 5px; overflow-x: auto; max-height: 400px;">{html.escape(response.text[:2000])}</pre>
            </div>
            <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('back_home')}</a>
        </div>
        '''
    except Exception as e:
        return f'''
        <div class="container">
            <h2>❌ {t('error_fetch')}</h2>
            <div class="result" style="background: #f8d7da;">
                <p><strong>URL:</strong> {html.escape(url)}</p>
                <p><strong>{t('error')}:</strong> {str(e)}</p>
            </div>
            <a href="/" style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">{t('back_home')}</a>
        </div>
        '''

@app.route('/')
def index():
    return render_template_string(generate_html())

if __name__ == '__main__':
    print("🔓 Starting VulnWeb - Security Vulnerability Demo")
    print("🌐 Available in English and Indonesian")
    print("⚠️  WARNING: For educational purposes only!")
    print("🌐 Server will run at: http://localhost:5000")
    print("=" * 60)
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)