# <summary><strong>Basic-Webapplication-vulneralbilites </strong></summary>

<img src="https://img.shields.io/badge/Apache--2.0-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/MIT-green?style=for-the-badge" />

# <summary><strong>⚠️ SECURITY DISCLAMER ⚠️</strong></summary>

⚠️⚠️This application is provided solely for educational and testing purposes in an environment you control. Do not use it to attack systems or networks without explicit permission.⚠️⚠️

**The maintainers are not responsible for any misuse or damages caused by this software.**

🛡️ A small intentionally-vulnerable web application meant for learning web penetration testing, exploit development basics, and defensive validation. Use it only in a controlled environment. 🛡️

### Features (vulnerabilities included)🎯
- SQL Injection (login or search parameters)
- Stored & Reflected XSS (comment forms, user-supplied output)
- Broken Authentication (weak session management, predictable passwords)
- IDOR (accessing other users' resources via parameters)
- Insecure file upload (can upload malicious files)
- CSRF (sensitive forms without tokens)
- Basic command injection on debug endpoint
- Bilingual (English/Indonesian **available specifically for the first webapp**) 
- Educational purpose only

# <summary><strong>**INTENDED USE** </strong></summary>
- Security education and awareness
- Penetration testing practice in controlled labs
- Learning about web application security
- Security researcher training

# <summary><strong>NOTE 📝</strong></summary>
This repo includes two intentionally vulnerable web applications created for penetration testing training and practice. While both serve the same educational purpose, each application implements different flows and outputs to support specific exercises (e.g., reflective vs. persistent XSS scenarios, basic SQLi vs. chained RCE). Both applications are still under development: documentation, additional test cases, and deployment options (e.g., docker-compose) need to be completed to support secure and scalable lab use.
Read the source file to identify the vulnerability implementation. This web application is still in development, so there may be some issues during testing.☕☕


 # <summary><strong>**WEBAPP INSTALLATION** </strong></summary>
 THIS TEST THIS WEBAPP HAS ENGLISH AND INDONESIAN LANGUAGES
```
git clone https://github.com/Bangkit-eldhian24/basic-webapplication-vuln.git
cd basic-webapplication-vuln
cd l0g1nx
```
if you want it fast you can move it
```
mv l0g1nx ~/
mv ~/basic-webapplication-vuln/l0g1nx ~/
```

**make virtual env**
```
python -m venv vuln_env
source vuln_env/bin/activate 
```
vuln_env\Scripts\activate  # Windows

**install dependencies**
```
pip install -r requirements.txt
```
**RUN**
```
python server.py
```

### <summary><strong>**visualization👁️** </strong></summary>
WEB APP V1

<img width="1302" height="947" alt="Screenshot_20251109_035029" src="https://github.com/user-attachments/assets/3eb27b1e-a766-4a20-94f5-4c8eda96a320" />

<img width="1392" height="737" alt="Screenshot_20251109_045651" src="https://github.com/user-attachments/assets/f05ba7f4-9ccc-46c5-b700-7d9714e58b1c" />

WEB APP V2

<img width="1920" height="915" alt="Screenshot_20251109_034932" src="https://github.com/user-attachments/assets/f5842cd0-9a01-4041-afbf-50f059acc712" />






