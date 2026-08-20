import os
from urllib.parse import urlparse

from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# =========================================================
# CSS
# =========================================================

CSS = """
<style>
*{box-sizing:border-box}

body{
    margin:0;
    background:#000;
    color:#fff;
    font-family:"Courier New",monospace;
}

.container{
    width:100%;
    max-width:680px;
    margin:auto;
    padding:18px 10px 50px;
}

.logo{
    text-align:center;
    font-family:Georgia,serif;
    font-size:34px;
    font-weight:bold;
    color:#ff00ff;
    text-shadow:
        0 0 6px #ff00ff,
        0 0 18px #ff00ff,
        0 0 30px #ff00ff;
    margin:5px 0 8px;
}

.subtitle{
    text-align:center;
    font-family:Georgia,serif;
    font-size:22px;
    font-weight:bold;
    margin-bottom:22px;
}

.option{
    border:2px solid #00ffff;
    border-radius:15px;
    padding:17px;
    margin-bottom:14px;
    box-shadow:
        0 0 7px #00ffff,
        0 0 18px rgba(0,255,255,.5);
}

.option button{
    width:100%;
    min-height:55px;
    border:0;
    border-radius:9px;
    background:#08e8e8;
    color:#000;
    font-family:"Courier New",monospace;
    font-size:14px;
    font-weight:bold;
    cursor:pointer;
}

.option button:hover{
    transform:scale(1.01);
    box-shadow:0 0 15px #00ffff;
}

.panel{
    border:2px solid #00ffff;
    border-radius:17px;
    padding:24px;
    background:#010101;
    box-shadow:
        0 0 10px #00ffff,
        0 0 25px rgba(0,255,255,.5);
}

.panel-title{
    text-align:center;
    color:#ff00ff;
    font-family:Georgia,serif;
    font-size:26px;
    font-weight:bold;
    text-shadow:0 0 12px #ff00ff;
    margin-bottom:20px;
}

.label{
    color:#00ffff;
    font-size:13px;
    margin:13px 0 6px;
}

input,textarea{
    width:100%;
    padding:14px;
    border:2px solid #00ffff;
    border-radius:9px;
    background:#050505;
    color:#fff;
    outline:none;
    font-family:"Courier New",monospace;
    font-size:14px;
}

textarea{
    min-height:115px;
    resize:vertical;
}

.action{
    width:100%;
    padding:15px;
    margin-top:15px;
    border:0;
    border-radius:9px;
    background:#08e8e8;
    color:#000;
    font-family:"Courier New",monospace;
    font-size:15px;
    font-weight:bold;
    cursor:pointer;
}

.action:hover{
    box-shadow:0 0 12px #00ffff;
}

.status{
    margin-top:16px;
    padding:12px;
    border:1px solid #00ffff;
    border-radius:8px;
    text-align:center;
    color:#00ffff;
    font-size:13px;
}

.back{
    display:block;
    text-align:center;
    margin-top:23px;
    color:#00ffff;
    text-decoration:none;
    font-weight:bold;
}

.admin{
    display:block;
    width:94%;
    margin:20px auto;
    padding:14px;
    border:0;
    border-radius:8px;
    background:#ff00ff;
    color:#000;
    font-weight:bold;
    cursor:pointer;
    box-shadow:0 0 12px #ff00ff;
}

.footer{
    text-align:center;
    color:#777;
    font-size:11px;
    line-height:2;
    margin-top:20px;
}

.fire{
    color:#999;
    font-style:italic;
    font-weight:bold;
}

.cyan{
    color:#00ffff;
}

@media(max-width:500px){
    .container{
        padding:15px 9px 40px;
    }

    .logo{
        font-size:30px;
    }

    .subtitle{
        font-size:21px;
    }

    .option{
        padding:16px;
    }

    .option button{
        font-size:13px;
    }

    .panel{
        padding:20px;
    }
}
</style>
"""


# =========================================================
# OPTIONS
# =========================================================

OPTIONS = [
    ("1 - CONVO SERVER", "/convo-server"),
    ("2 - BACKUP CONVO", "/backup-convo"),
    ("3 - POST SERVER", "/post-server"),
    ("4 - BACKUP POST SERVER", "/backup-post"),
    ("5 - TOKEN CHECK VALIDITY", "/token-validity"),
    ("6 - FETCH ALL UID WITH TOKEN", "/fetch-uid"),
    ("7 - FETCH PAGE TOKENS", "/page-tokens"),
    ("8 - GROUP NAME LOCKER", "/group-locker"),
    ("9 - YOUTUBE DOWNLOADER", "/youtube-downloader"),
    ("10 - INSTAGRAM DOWNLOADER", "/instagram-downloader"),
    ("11 - FACEBOOK DOWNLOADER", "/facebook-downloader"),
    ("12 - COOKIE TO JSON", "/cookie-json"),
]


# =========================================================
# URL VALIDATION
# =========================================================

def valid_url(value, domains=None):
    try:
        parsed = urlparse(value.strip())

        if parsed.scheme not in ("http", "https"):
            return False

        if not parsed.netloc:
            return False

        if domains:
            host = parsed.netloc.lower().split(":")[0]

            return any(
                host == domain or host.endswith("." + domain)
                for domain in domains
            )

        return True

    except Exception:
        return False


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    buttons = ""

    for name, url in OPTIONS:

        buttons += f"""
        <div class="option">
            <button onclick="location.href='{url}'">
                ◄ {name} ►
            </button>
        </div>
        """

    return render_template_string(
        CSS + f"""
        <div class="container">

            <div class="logo">
                RK RAJA XWD
            </div>

            <div class="subtitle">
                ( ALL OPTION )
            </div>

            {buttons}

            <button class="admin"
                    onclick="location.href='/admin'">
                ⚙ ADMIN PANEL
            </button>

            <div class="footer">
                © 2026 MADE BY :- RK RAJA XWD PANEL
                <br>
                <span class="fire">ALWAYS ON FIRE 🔥</span>
                <br>
                <span class="cyan">SERVER ONLINE ✓</span>
            </div>

        </div>
        """
    )


# =========================================================
# GENERIC SERVER PAGE
# =========================================================

def server_page(title, fields):

    html = ""

    for field in fields:

        kind = field["type"]
        label = field["label"]
        name = field["name"]

        if kind == "textarea":

            html += f"""
            <div class="label">{label}</div>

            <textarea
                id="{name}"
                name="{name}"
                placeholder="{label}">
            </textarea>
            """

        else:

            html += f"""
            <div class="label">{label}</div>

            <input
                type="{kind}"
                id="{name}"
                name="{name}"
                placeholder="{label}">
            """

    return render_template_string(
        CSS + f"""
        <div class="container">

            <div class="logo">
                RK RAJA XWD
            </div>

            <div class="panel">

                <div class="panel-title">
                    ◄ {title} ►
                </div>

                {html}

                <button class="action"
                        onclick="openPanel()">
                    OPEN SERVER
                </button>

                <div id="status" class="status">
                    SERVER PANEL READY
                </div>

                <a class="back" href="/">
                    ◄ BACK TO ALL OPTIONS ►
                </a>

            </div>

        </div>

        <script>
        function openPanel(){{
            document.getElementById("status").innerText =
                "✓ {title} SERVER OPEN";
        }}
        </script>
        """
    )


# =========================================================
# 1 CONVO
# =========================================================

@app.route("/convo-server")
def convo_server():

    return server_page(
        "1 - CONVO SERVER",
        [
            {"type":"text","name":"conversation_id","label":"Conversation ID"},
            {"type":"text","name":"token","label":"Token"},
            {"type":"text","name":"name","label":"Name"},
            {"type":"number","name":"delay","label":"Delay"},
            {"type":"textarea","name":"message","label":"Message"}
        ]
    )


# =========================================================
# 2 BACKUP CONVO
# =========================================================

@app.route("/backup-convo")
def backup_convo():

    return server_page(
        "2 - BACKUP CONVO",
        [
            {"type":"text","name":"conversation_id","label":"Conversation ID"},
            {"type":"text","name":"token","label":"Token"},
            {"type":"text","name":"backup_name","label":"Backup Name"},
            {"type":"textarea","name":"backup_data","label":"Backup Data"}
        ]
    )


# =========================================================
# 3 POST SERVER
# =========================================================

@app.route("/post-server")
def post_server():

    return server_page(
        "3 - POST SERVER",
        [
            {"type":"text","name":"post_id","label":"Post ID"},
            {"type":"text","name":"token","label":"Token"},
            {"type":"textarea","name":"message","label":"Post Message"}
        ]
    )


# =========================================================
# 4 BACKUP POST
# =========================================================

@app.route("/backup-post")
def backup_post():

    return server_page(
        "4 - BACKUP POST SERVER",
        [
            {"type":"text","name":"post_id","label":"Post ID"},
            {"type":"text","name":"token","label":"Token"},
            {"type":"text","name":"backup_name","label":"Backup Name"},
            {"type":"textarea","name":"backup_data","label":"Backup Data"}
        ]
    )


# =========================================================
# 5 TOKEN VALIDITY
# =========================================================

@app.route("/token-validity")
def token_validity():

    return server_page(
        "5 - TOKEN CHECK VALIDITY",
        [
            {"type":"textarea","name":"token","label":"Token"}
        ]
    )


# =========================================================
# 6 FETCH UID
# =========================================================

@app.route("/fetch-uid")
def fetch_uid():

    return server_page(
        "6 - FETCH ALL UID WITH TOKEN",
        [
            {"type":"textarea","name":"token","label":"Token"}
        ]
    )


# =========================================================
# 7 PAGE TOKENS
# =========================================================

@app.route("/page-tokens")
def page_tokens():

    return server_page(
        "7 - FETCH PAGE TOKENS",
        [
            {"type":"textarea","name":"token","label":"Token"}
        ]
    )


# =========================================================
# 8 GROUP LOCKER
# =========================================================

@app.route("/group-locker")
def group_locker():

    return server_page(
        "8 - GROUP NAME LOCKER",
        [
            {"type":"text","name":"group_id","label":"Group ID"},
            {"type":"text","name":"token","label":"Token"},
            {"type":"text","name":"group_name","label":"Group Name"}
        ]
    )


# =========================================================
# 9 YOUTUBE
# =========================================================

@app.route("/youtube-downloader", methods=["GET","POST"])
def youtube_downloader():

    message = ""

    if request.method == "POST":

        url = request.form.get("url", "")

        if valid_url(
            url,
            ["youtube.com", "youtu.be"]
        ):
            message = "✓ YouTube URL valid"
        else:
            message = "✗ Invalid YouTube URL"

    return render_template_string(
        CSS + f"""
        <div class="container">

            <div class="logo">RK RAJA XWD</div>

            <div class="panel">

                <div class="panel-title">
                    ◄ 9 - YOUTUBE DOWNLOADER ►
                </div>

                <div class="label">
                    YouTube URL
                </div>

                <form method="POST">

                    <input
                        type="url"
                        name="url"
                        placeholder="https://youtube.com/... "
                        required>

                    <button class="action">
                        CHECK URL
                    </button>

                </form>

                <div class="status">
                    {message if message else "SERVER PANEL READY"}
                </div>

                <a class="back" href="/">
                    ◄ BACK TO ALL OPTIONS ►
                </a>

            </div>

        </div>
        """
    )


# =========================================================
# 10 INSTAGRAM
# =========================================================

@app.route("/instagram-downloader", methods=["GET","POST"])
def instagram_downloader():

    message = ""

    if request.method == "POST":

        url = request.form.get("url", "")

        if valid_url(
            url,
            ["instagram.com"]
        ):
            message = "✓ Instagram URL valid"
        else:
            message = "✗ Invalid Instagram URL"

    return render_template_string(
        CSS + f"""
        <div class="container">

            <div class="logo">RK RAJA XWD</div>

            <div class="panel">

                <div class="panel-title">
                    ◄ 10 - INSTAGRAM DOWNLOADER ►
                </div>

                <div class="label">
                    Instagram URL
                </div>

                <form method="POST">

                    <input
                        type="url"
                        name="url"
                        placeholder="https://instagram.com/..."
                        required>

                    <button class="action">
                        CHECK URL
                    </button>

                </form>

                <div class="status">
                    {message if message else "SERVER PANEL READY"}
                </div>

                <a class="back" href="/">
                    ◄ BACK TO ALL OPTIONS ►
                </a>

            </div>

        </div>
        """
    )


# =========================================================
# 11 FACEBOOK
# =========================================================

@app.route("/facebook-downloader", methods=["GET","POST"])
def facebook_downloader():

    message = ""

    if request.method == "POST":

        url = request.form.get("url", "")

        if valid_url(
            url,
            ["facebook.com", "fb.watch"]
        ):
            message = "✓ Facebook URL valid"
        else:
            message = "✗ Invalid Facebook URL"

    return render_template_string(
        CSS + f"""
        <div class="container">

            <div class="logo">RK RAJA XWD</div>

            <div class="panel">

                <div class="panel-title">
                    ◄ 11 - FACEBOOK DOWNLOADER ►
                </div>

                <div class="label">
                    Facebook URL
                </div>

                <form method="POST">

                    <input
                        type="url"
                        name="url"
                        placeholder="https://facebook.com/..."
                        required>

                    <button class="action">
                        CHECK URL
                    </button>

                </form>

                <div class="status">
                    {message if message else "SERVER PANEL READY"}
                </div>

                <a class="back" href="/">
                    ◄ BACK TO ALL OPTIONS ►
                </a>

            </div>

        </div>
        """
    )


# =========================================================
# 12 COOKIE TO JSON
# =========================================================

@app.route("/cookie-json")
def cookie_json():

    return server_page(
        "12 - COOKIE TO JSON",
        [
            {"type":"textarea","name":"cookie","label":"Cookie"}
        ]
    )


# =========================================================
# ADMIN
# =========================================================

@app.route("/admin")
def admin():

    return server_page(
        "ADMIN PANEL",
        [
            {"type":"text","name":"admin_name","label":"Admin Name"}
        ]
    )


# =========================================================
# API HEALTH
# =========================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "server": "RK RAJA XWD",
        "message": "Server is running"
    })


# =========================================================
# NO 404
# =========================================================

@app.errorhandler(404)
def not_found(error):

    return render_template_string(
        CSS + """
        <div class="container">

            <div class="logo">
                RK RAJA XWD
            </div>

            <div class="panel">

                <div class="panel-title">
                    SERVER ONLINE ✓
                </div>

                <div class="status">
                    PANEL IS RUNNING
                </div>

                <a href="/" class="back">
                    ◄ BACK TO HOME ►
                </a>

            </div>

        </div>
        """
    ), 200


# =========================================================
# RENDER
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            "10000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
            )
