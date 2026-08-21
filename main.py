import os
import json
import secrets
from datetime import datetime
from urllib.parse import urlparse, quote_plus

from flask import Flask, request, redirect, render_template_string, jsonify, session, url_for, make_response

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "rkraja")

convo_backups = {}
post_backups = {}
tasks = {}

CSS = """
<style>
*{box-sizing:border-box}
body{
    margin:0;
    min-height:100vh;
    background:
      radial-gradient(circle at 20% 20%,rgba(0,255,140,.10),transparent 30%),
      radial-gradient(circle at 80% 80%,rgba(0,180,255,.10),transparent 30%),
      #030507;
    color:#d9ffe9;
    font-family:Consolas,"Courier New",monospace;
}
body:before{
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    background:linear-gradient(rgba(0,255,120,.025) 1px,transparent 1px);
    background-size:100% 4px;
}
.wrap{max-width:760px;margin:auto;padding:20px 12px 50px}
.logo{
    text-align:center;
    font-size:32px;
    font-weight:900;
    color:#7cffb2;
    text-shadow:0 0 8px #00ff66,0 0 25px #00ff66;
    margin:10px 0;
}
.sub{text-align:center;color:#70dca0;margin-bottom:25px}
.card{
    background:rgba(3,10,8,.88);
    border:1px solid #00ff66;
    border-radius:16px;
    padding:20px;
    margin:14px 0;
    box-shadow:0 0 12px rgba(0,255,102,.25);
}
.option button,.btn{
    width:100%;
    padding:14px;
    border:1px solid #00ff66;
    border-radius:10px;
    background:#06150d;
    color:#8affbd;
    font-family:inherit;
    font-weight:bold;
    cursor:pointer;
}
.option button:hover,.btn:hover{
    background:#00ff66;
    color:#001b09;
    box-shadow:0 0 18px #00ff66;
}
input,textarea,select{
    width:100%;
    padding:13px;
    margin:7px 0 15px;
    border:1px solid #00ff66;
    border-radius:8px;
    background:#020604;
    color:#9dffc0;
    outline:none;
    font-family:inherit;
}
textarea{min-height:120px;resize:vertical}
label{display:block;color:#76ffac;font-size:13px}
.title{text-align:center;color:#7cffb2;font-size:23px;font-weight:bold}
.status{
    padding:12px;
    margin-top:14px;
    border:1px solid #167b45;
    border-radius:8px;
    background:#04150c;
}
.back{
    display:block;
    text-align:center;
    color:#78ffae;
    margin-top:20px;
    text-decoration:none;
}
.small{font-size:12px;color:#76a88b}
pre{
    white-space:pre-wrap;
    word-break:break-word;
    color:#8affbd;
}
</style>
"""

def page(title, body):
    return render_template_string(
        CSS + f"""
        <div class="wrap">
            <div class="logo">RK RAJA XWD</div>
            <div class="card">
                <div class="title">◄ {title} ►</div>
                {body}
            </div>
            <a class="back" href="/">◄ BACK TO ALL OPTIONS ►</a>
        </div>
        """
    )

def valid_url(value):
    try:
        p = urlparse(value.strip())
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False

def open_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url if valid_url(url) else None

OPTIONS = [
    ("1 - CONVO SERVER", "/convo-server"),
    ("2 - BACKUP CONVO", "/backup-convo"),
    ("3 - POST SERVER", "/post-server"),
    ("4 - BACKUP POST SERVER", "/backup-post"),
    ("5 - TOKEN CHECK VALIDITY", "/token-validity"),
    ("6 - FETCH UID WITH TOKEN", "/fetch-uid"),
    ("7 - FETCH PAGE TOKENS", "/page-tokens"),
    ("8 - GROUP MANAGEMENT", "/group-management"),
    ("9 - YOUTUBE OPEN", "/youtube"),
    ("10 - INSTAGRAM OPEN", "/instagram"),
    ("11 - FACEBOOK OPEN", "/facebook"),
    ("12 - COOKIE TO JSON", "/cookie-json"),
    ("13 - COOKIES SERVER", "/cookies-server"),
    ("14 - MUSICAL CONVO", "/musical-convo"),
]

@app.route("/")
def home():
    buttons = ""
    for name, route in OPTIONS:
        buttons += f"""
        <div class="option card">
            <button onclick="location.href='{route}'">◄ {name} ►</button>
        </div>
        """
    return render_template_string(
        CSS + f"""
        <div class="wrap">
            <div class="logo">RK RAJA XWD</div>
            <div class="sub">HACKER CONTROL PANEL</div>
            {buttons}
            <div class="card">
                <button class="btn" onclick="location.href='/admin'">⚙ ADMIN PANEL</button>
            </div>
            <div class="status" style="text-align:center">SERVER ONLINE ✓</div>
        </div>
        """
    )

@app.route("/convo-server", methods=["GET", "POST"])
def convo_server():
    result = ""
    if request.method == "POST":
        conversation_id = request.form.get("conversation_id", "").strip()
        token = request.form.get("token", "").strip()
        name = request.form.get("name", "").strip()
        delay = request.form.get("delay", "").strip()
        message = request.form.get("message", "").strip()
        if not conversation_id or not token or not message:
            result = "✗ Conversation ID, token and message are required."
        else:
            task_id = secrets.token_hex(3).upper()
            tasks[task_id] = {
                "type": "convo",
                "conversation_id": conversation_id,
                "name": name,
                "delay": delay,
                "message": message,
                "created": datetime.now().isoformat(),
                "status": "READY"
            }
            result = f"✓ Request saved. Task ID: {task_id}"
    return page("1 - CONVO SERVER", f"""
    <form method="post">
        <label>Conversation ID</label><input name="conversation_id" required>
        <label>Authorized API Token</label><input type="password" name="token" required>
        <label>Name</label><input name="name">
        <label>Delay</label><input type="number" name="delay" min="1" value="5">
        <label>Message</label><textarea name="message" required></textarea>
        <button class="btn">SAVE REQUEST</button>
    </form>
    <div class="status">{result or "CONVO SERVER READY"}</div>
    """)

@app.route("/backup-convo", methods=["GET", "POST"])
def backup_convo():
    result = ""
    if request.method == "POST":
        name = request.form.get("backup_name", "").strip()
        data = request.form.get("backup_data", "")
        if not name or not data:
            result = "✗ Backup name and data required."
        else:
            convo_backups[name] = data
            result = "✓ Conversation backup saved."
    return page("2 - BACKUP CONVO", f"""
    <form method="post">
        <label>Backup Name</label><input name="backup_name" required>
        <label>Backup Data</label><textarea name="backup_data" required></textarea>
        <button class="btn">SAVE BACKUP</button>
    </form>
    <div class="status">{result or "BACKUP CONVO READY"}</div>
    """)

@app.route("/post-server", methods=["GET", "POST"])
def post_server():
    result = ""
    if request.method == "POST":
        post_id = request.form.get("post_id", "").strip()
        token = request.form.get("token", "").strip()
        message = request.form.get("message", "").strip()
        if not post_id or not token or not message:
            result = "✗ Post ID, token and message are required."
        else:
            task_id = secrets.token_hex(3).upper()
            tasks[task_id] = {
                "type": "post",
                "post_id": post_id,
                "message": message,
                "created": datetime.now().isoformat(),
                "status": "READY"
            }
            result = f"✓ Authorized request saved. Task ID: {task_id}"
    return page("3 - POST SERVER", f"""
    <form method="post">
        <label>Post ID</label><input name="post_id" required>
        <label>Authorized API Token</label><input type="password" name="token" required>
        <label>Message</label><textarea name="message" required></textarea>
        <button class="btn">SAVE REQUEST</button>
    </form>
    <div class="status">{result or "POST SERVER READY"}</div>
    """)

@app.route("/backup-post", methods=["GET", "POST"])
def backup_post():
    result = ""
    if request.method == "POST":
        name = request.form.get("backup_name", "").strip()
        data = request.form.get("backup_data", "")
        if not name or not data:
            result = "✗ Backup name and data required."
        else:
            post_backups[name] = data
            result = "✓ Post backup saved."
    return page("4 - BACKUP POST SERVER", f"""
    <form method="post">
        <label>Backup Name</label><input name="backup_name" required>
        <label>Backup Data</label><textarea name="backup_data" required></textarea>
        <button class="btn">SAVE BACKUP</button>
    </form>
    <div class="status">{result or "BACKUP POST READY"}</div>
    """)

@app.route("/token-validity", methods=["GET", "POST"])
def token_validity():
    result = ""
    if request.method == "POST":
        token = request.form.get("token", "").strip()
        result = "✓ Token received securely. No token value is displayed or stored." if token else "✗ Token required."
    return page("5 - TOKEN CHECK VALIDITY", f"""
    <form method="post">
        <label>Token</label><textarea name="token" required></textarea>
        <button class="btn">CHECK TOKEN</button>
    </form>
    <div class="status">{result or "TOKEN CHECK READY"}</div>
    """)

@app.route("/fetch-uid", methods=["GET", "POST"])
def fetch_uid():
    result = ""
    if request.method == "POST":
        token = request.form.get("token", "").strip()
        result = "✓ Token received. UID lookup requires an authorized API/token." if token else "✗ Token required."
    return page("6 - FETCH UID WITH TOKEN", f"""
    <form method="post">
        <label>Authorized Token</label><textarea name="token" required></textarea>
        <button class="btn">LOOKUP</button>
    </form>
    <div class="status">{result or "UID LOOKUP READY"}</div>
    """)

@app.route("/page-tokens", methods=["GET", "POST"])
def page_tokens():
    result = ""
    if request.method == "POST":
        token = request.form.get("token", "").strip()
        result = "✓ Token received." if token else "✗ Token required."
    return page("7 - FETCH PAGE TOKENS", f"""
    <form method="post">
        <label>Authorized Token</label><textarea name="token" required></textarea>
        <button class="btn">CHECK</button>
    </form>
    <div class="status">{result or "PAGE TOKEN TOOL READY"}</div>
    """)

@app.route("/group-management", methods=["GET", "POST"])
def group_management():
    result = ""
    if request.method == "POST":
        group_id = request.form.get("group_id", "").strip()
        name = request.form.get("group_name", "").strip()
        result = "✓ Group management request prepared." if group_id and name else "✗ Group ID and name required."
    return page("8 - GROUP MANAGEMENT", f"""
    <form method="post">
        <label>Group ID</label><input name="group_id" required>
        <label>New Group Name</label><input name="group_name" required>
        <button class="btn">SAVE</button>
    </form>
    <div class="status">{result or "GROUP MANAGEMENT READY"}</div>
    """)

def url_page(title, label, placeholder, allowed=None):
    if request.method == "POST":
        value = request.form.get("url", "").strip()
        target = open_url(value)
        if target:
            host = urlparse(target).netloc.lower()
            if allowed and not (host in allowed or any(host.endswith("." + x) for x in allowed)):
                target = None
            if target:
                return redirect(target)
        message = "✗ Invalid URL"
    else:
        message = "SERVER PANEL READY"
    return page(title, f"""
    <form method="post">
        <label>{label}</label>
        <input type="url" name="url" placeholder="{placeholder}" required>
        <button class="btn">OPEN URL</button>
    </form>
    <div class="status">{message}</div>
    """)

@app.route("/youtube", methods=["GET", "POST"])
def youtube():
    return url_page("9 - YOUTUBE OPEN", "YouTube URL", "https://youtube.com/...", ["youtube.com", "www.youtube.com", "youtu.be"])

@app.route("/instagram", methods=["GET", "POST"])
def instagram():
    return url_page("10 - INSTAGRAM OPEN", "Instagram URL", "https://instagram.com/...", ["instagram.com", "www.instagram.com"])

@app.route("/facebook", methods=["GET", "POST"])
def facebook():
    return url_page("11 - FACEBOOK OPEN", "Facebook URL", "https://facebook.com/...", ["facebook.com", "www.facebook.com", "m.facebook.com", "fb.watch"])

@app.route("/cookie-json", methods=["GET", "POST"])
def cookie_json():
    result = ""
    if request.method == "POST":
        cookie = request.form.get("cookie", "").strip()
        if not cookie:
            result = "✗ Cookie required."
        else:
            pairs = {}
            for part in cookie.split(";"):
                if "=" in part:
                    key, value = part.strip().split("=", 1)
                    pairs[key.strip()] = value.strip()
            result = "<pre>" + json.dumps(pairs, indent=2) + "</pre>"
    return page("12 - COOKIE TO JSON", f"""
    <form method="post">
        <label>Cookie String</label><textarea name="cookie" required></textarea>
        <button class="btn">CONVERT</button>
    </form>
    <div class="status">{result or "COOKIE CONVERTER READY"}</div>
    """)

@app.route("/cookies-server", methods=["GET", "POST"])
def cookies_server():
    result = ""
    if request.method == "POST":
        value = request.form.get("cookie_value", "").strip()
        if value:
            resp = make_response(redirect(url_for("cookies_server")))
            resp.set_cookie("panel_setting", value, httponly=True, samesite="Lax")
            return resp
        result = "✗ Value required."
    current = request.cookies.get("panel_setting", "Not set")
    return page("13 - COOKIES SERVER", f"""
    <form method="post">
        <label>Panel Cookie Setting</label><input name="cookie_value" required>
        <button class="btn">SET COOKIE</button>
    </form>
    <div class="status">Current setting: {current}</div>
    <div class="status">{result}</div>
    """)

@app.route("/musical-convo", methods=["GET", "POST"])
def musical_convo():
    if request.method == "POST":
        song = request.form.get("song", "").strip()
        if song:
            return redirect("https://www.youtube.com/results?search_query=" + quote_plus(song))
    return page("14 - MUSICAL CONVO", """
    <form method="post">
        <label>Song Name</label>
        <input name="song" placeholder="Enter song name" required>
        <button class="btn">SEARCH SONG</button>
    </form>
    <div class="status">MUSIC SEARCH READY</div>
    """)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password", "")
        if secrets.compare_digest(password, ADMIN_PASSWORD):
            session["admin"] = True
            return redirect(url_for("admin_panel"))
        return page("ADMIN LOGIN", "<div class='status'>✗ Wrong password</div>")
    return page("ADMIN LOGIN", """
    <form method="post">
        <label>Admin Password</label>
        <input type="password" name="password" required>
        <button class="btn">LOGIN</button>
    </form>
    """)

@app.route("/admin/panel")
def admin_panel():
    if not session.get("admin"):
        return redirect(url_for("admin"))
    task_html = ""
    for task_id, task in tasks.items():
        task_html += f"""
        <div class="card">
            <b>Task:</b> {task_id}<br>
            <b>Type:</b> {task.get("type")}<br>
            <b>Status:</b> {task.get("status")}<br>
            <b>Created:</b> {task.get("created")}
        </div>
        """
    return page("ADMIN PANEL", f"""
    <div class="status">
        <b>SERVER:</b> ONLINE<br>
        <b>Tasks:</b> {len(tasks)}<br>
        <b>Convo Backups:</b> {len(convo_backups)}<br>
        <b>Post Backups:</b> {len(post_backups)}
    </div>
    {task_html or '<div class="status">No tasks.</div>'}
    <br>
    <a class="back" href="{url_for('admin_logout')}">LOGOUT</a>
    """)

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/health")
def health():
    return jsonify({"status": "online", "server": "RK RAJA XWD", "time": datetime.utcnow().isoformat() + "Z"})

@app.route("/ping")
def ping():
    return "RK RAJA XWD ONLINE ✓", 200

@app.errorhandler(404)
def not_found(error):
    return page("404", "<div class='status'>✗ Page not found.</div>"), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, debug=False)
