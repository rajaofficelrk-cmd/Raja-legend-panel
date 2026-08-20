import os
from flask import Flask, render_template_string

app = Flask(__name__)

# ============================================================
# STYLE
# ============================================================

CSS = """
<style>
* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    margin: 0;
    background: #000;
    color: #fff;
    font-family: "Courier New", monospace;
}

.container {
    width: 100%;
    max-width: 680px;
    margin: auto;
    padding: 20px 10px 50px;
}

/* ================= TITLE ================= */

.logo {
    text-align: center;
    font-family: Georgia, serif;
    font-size: 34px;
    font-weight: bold;
    color: #ff00ff;

    text-shadow:
        0 0 5px #ff00ff,
        0 0 15px #ff00ff,
        0 0 30px #ff00ff;

    margin: 5px 0 8px;
}

.subtitle {
    text-align: center;
    font-family: Georgia, serif;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 25px;
}

/* ================= HOME BUTTON ================= */

.option {
    border: 2px solid #00ffff;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 14px;

    box-shadow:
        0 0 7px #00ffff,
        0 0 18px rgba(0,255,255,.55);

    background: #010101;
}

.option button {
    width: 100%;
    min-height: 55px;

    border: 0;
    border-radius: 9px;

    background: #08e8e8;
    color: #000;

    font-family: "Courier New", monospace;
    font-size: 15px;
    font-weight: bold;

    cursor: pointer;

    transition: .2s;
}

.option button:hover {
    transform: scale(1.015);

    box-shadow:
        0 0 10px #00ffff,
        0 0 22px #00ffff;
}

/* ================= INNER PAGE ================= */

.panel {
    border: 2px solid #00ffff;
    border-radius: 17px;

    padding: 25px;

    box-shadow:
        0 0 10px #00ffff,
        0 0 25px rgba(0,255,255,.55);

    background: #010101;
}

.panel-title {
    text-align: center;

    color: #ff00ff;

    font-family: Georgia, serif;
    font-size: 27px;
    font-weight: bold;

    text-shadow:
        0 0 7px #ff00ff,
        0 0 18px #ff00ff;

    margin-bottom: 25px;
}

.line {
    height: 2px;
    background: #00ffff;
    box-shadow: 0 0 8px #00ffff;
    margin: 18px 0;
}

.label {
    color: #00ffff;
    font-size: 14px;
    margin: 12px 0 5px;
}

input,
textarea,
select {
    width: 100%;

    padding: 14px;
    margin-bottom: 8px;

    background: #050505;
    color: #fff;

    border: 2px solid #00ffff;
    border-radius: 9px;

    outline: none;

    font-family: "Courier New", monospace;
    font-size: 14px;
}

textarea {
    min-height: 130px;
    resize: vertical;
}

.action {
    width: 100%;

    margin-top: 12px;
    padding: 15px;

    border: 0;
    border-radius: 9px;

    background: #08e8e8;
    color: #000;

    font-family: "Courier New", monospace;
    font-size: 15px;
    font-weight: bold;

    cursor: pointer;
}

.action:hover {
    box-shadow:
        0 0 10px #00ffff,
        0 0 20px #00ffff;
}

.status {
    text-align: center;

    margin-top: 18px;
    padding: 13px;

    border: 1px solid #00ffff;
    border-radius: 9px;

    color: #00ffff;

    font-size: 13px;
}

.back {
    display: block;

    text-align: center;

    margin-top: 25px;

    color: #00ffff;
    text-decoration: none;

    font-weight: bold;
}

.back:hover {
    text-shadow: 0 0 10px #00ffff;
}

/* ================= ADMIN ================= */

.admin {
    width: 94%;

    display: block;
    margin: 20px auto;

    padding: 14px;

    border: 0;
    border-radius: 8px;

    background: #ff00ff;
    color: #000;

    font-family: "Courier New", monospace;
    font-weight: bold;

    cursor: pointer;

    box-shadow:
        0 0 8px #ff00ff,
        0 0 18px rgba(255,0,255,.6);
}

/* ================= FOOTER ================= */

.footer {
    text-align: center;

    margin-top: 25px;

    color: #777;

    font-size: 11px;

    line-height: 2;
}

.fire {
    color: #999;
    font-style: italic;
    font-weight: bold;
}

.messenger {
    color: #00ffff;
}

/* ================= MOBILE ================= */

@media (max-width: 500px) {

    .container {
        padding: 16px 9px 45px;
    }

    .logo {
        font-size: 30px;
    }

    .subtitle {
        font-size: 21px;
    }

    .option {
        padding: 17px;
    }

    .option button {
        font-size: 13px;
    }

    .panel {
        padding: 21px;
    }

    .panel-title {
        font-size: 24px;
    }
}
</style>
"""


# ============================================================
# ALL OPTIONS
# ============================================================

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


# ============================================================
# HOME PAGE
# ============================================================

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

                <span class="fire">
                    ALWAYS ON FIRE 🔥
                </span>

                <br>

                <span class="messenger">
                    Chat on Messenger
                </span>

            </div>

        </div>
        """
    )


# ============================================================
# PAGE GENERATOR
# ============================================================

def create_page(title, description, fields):

    field_html = ""

    for field_type, placeholder in fields:

        if field_type == "textarea":

            field_html += f"""
            <div class="label">
                {placeholder}
            </div>

            <textarea
                placeholder="Enter {placeholder.lower()}">
            </textarea>
            """

        else:

            field_html += f"""
            <div class="label">
                {placeholder}
            </div>

            <input
                type="{field_type}"
                placeholder="Enter {placeholder.lower()}">
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

                <div class="line"></div>

                <div style="
                    text-align:center;
                    color:#aaa;
                    font-size:13px;
                    margin-bottom:18px;
                ">
                    {description}
                </div>

                {field_html}

                <button class="action"
                        onclick="openServer()">

                    OPEN SERVER

                </button>

                <div id="status" class="status">
                    SERVER PANEL READY
                </div>

                <a href="/" class="back">
                    ◄ BACK TO ALL OPTIONS ►
                </a>

            </div>

        </div>

        <script>

        function openServer() {{

            document.getElementById("status").innerHTML =
                "✓ {title} SERVER OPEN";

        }}

        </script>
        """
    )


# ============================================================
# 1 - CONVO SERVER
# ============================================================

@app.route("/convo-server")
def convo_server():

    return create_page(
        "1 - CONVO SERVER",
        "CONVO SERVER PANEL",
        [
            ("text", "Conversation ID"),
            ("text", "Name"),
            ("number", "Delay"),
            ("textarea", "Message")
        ]
    )


# ============================================================
# 2 - BACKUP CONVO
# ============================================================

@app.route("/backup-convo")
def backup_convo():

    return create_page(
        "2 - BACKUP CONVO",
        "BACKUP CONVO PANEL",
        [
            ("text", "Conversation ID"),
            ("text", "Backup Name"),
            ("textarea", "Backup Data")
        ]
    )


# ============================================================
# 3 - POST SERVER
# ============================================================

@app.route("/post-server")
def post_server():

    return create_page(
        "3 - POST SERVER",
        "POST SERVER PANEL",
        [
            ("text", "Post ID"),
            ("text", "Token"),
            ("textarea", "Post Message")
        ]
    )


# ============================================================
# 4 - BACKUP POST SERVER
# ============================================================

@app.route("/backup-post")
def backup_post():

    return create_page(
        "4 - BACKUP POST SERVER",
        "BACKUP POST SERVER PANEL",
        [
            ("text", "Post ID"),
            ("text", "Backup Name"),
            ("textarea", "Backup Data")
        ]
    )


# ============================================================
# 5 - TOKEN CHECK VALIDITY
# ============================================================

@app.route("/token-validity")
def token_validity():

    return create_page(
        "5 - TOKEN CHECK VALIDITY",
        "TOKEN VALIDITY PANEL",
        [
            ("textarea", "Token")
        ]
    )


# ============================================================
# 6 - FETCH ALL UID WITH TOKEN
# ============================================================

@app.route("/fetch-uid")
def fetch_uid():

    return create_page(
        "6 - FETCH ALL UID WITH TOKEN",
        "UID FETCH PANEL",
        [
            ("textarea", "Token")
        ]
    )


# ============================================================
# 7 - FETCH PAGE TOKENS
# ============================================================

@app.route("/page-tokens")
def page_tokens():

    return create_page(
        "7 - FETCH PAGE TOKENS",
        "PAGE TOKEN PANEL",
        [
            ("textarea", "Token")
        ]
    )


# ============================================================
# 8 - GROUP NAME LOCKER
# ============================================================

@app.route("/group-locker")
def group_locker():

    return create_page(
        "8 - GROUP NAME LOCKER",
        "GROUP NAME LOCKER PANEL",
        [
            ("text", "Group ID"),
            ("text", "Group Name")
        ]
    )


# ============================================================
# 9 - YOUTUBE DOWNLOADER
# ============================================================

@app.route("/youtube-downloader")
def youtube_downloader():

    return create_page(
        "9 - YOUTUBE DOWNLOADER",
        "YOUTUBE DOWNLOADER PANEL",
        [
            ("url", "YouTube URL")
        ]
    )


# ============================================================
# 10 - INSTAGRAM DOWNLOADER
# ============================================================

@app.route("/instagram-downloader")
def instagram_downloader():

    return create_page(
        "10 - INSTAGRAM DOWNLOADER",
        "INSTAGRAM DOWNLOADER PANEL",
        [
            ("url", "Instagram URL")
        ]
    )


# ============================================================
# 11 - FACEBOOK DOWNLOADER
# ============================================================

@app.route("/facebook-downloader")
def facebook_downloader():

    return create_page(
        "11 - FACEBOOK DOWNLOADER",
        "FACEBOOK DOWNLOADER PANEL",
        [
            ("url", "Facebook URL")
        ]
    )


# ============================================================
# 12 - COOKIE TO JSON
# ============================================================

@app.route("/cookie-json")
def cookie_json():

    return create_page(
        "12 - COOKIE TO JSON",
        "COOKIE TO JSON PANEL",
        [
            ("textarea", "Cookie")
        ]
    )


# ============================================================
# ADMIN PANEL
# ============================================================

@app.route("/admin")
def admin():

    return create_page(
        "ADMIN PANEL",
        "RK RAJA XWD ADMIN PANEL",
        [
            ("text", "Admin Name")
        ]
    )


# ============================================================
# NO 404
# ============================================================

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
                    SERVER PANEL
                </div>

                <div class="status">
                    SERVER IS RUNNING ✓
                </div>

                <a href="/" class="back">
                    ◄ BACK TO ALL OPTIONS ►
                </a>

            </div>

        </div>
        """
    ), 200


# ============================================================
# RUN
# ============================================================

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
