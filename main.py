from flask import Flask, render_template_string, redirect, url_for
import os
import html

app = Flask(__name__)
app.config["DEBUG"] = False


# ---------- COMMON CSS ----------
STYLE = """
<style>
* {
    box-sizing: border-box;
}

body {
    background: #000;
    color: #fff;
    font-family: "Courier New", monospace;
    text-align: center;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

.container {
    width: 100%;
    max-width: 700px;
    margin: auto;
}

h1 {
    color: #ff00ff;
    font-size: 30px;
    text-shadow: 0 0 10px #ff00ff;
    margin: 10px 0;
}

h2 {
    font-size: 20px;
    margin-bottom: 25px;
}

.button-box {
    width: 90%;
    margin: 15px auto;
    padding: 20px;
    border: 2px solid #00ffff;
    border-radius: 10px;
    background: #000;
    box-shadow: 0 0 15px #00ffff;
}

.button-box a,
.admin a,
.back {
    display: block;
    padding: 13px;
    border-radius: 7px;
    text-decoration: none;
    font-weight: bold;
    transition: 0.2s;
}

.button-box a {
    background: #00ffff;
    color: #000;
}

.button-box a:hover,
.admin a:hover,
.back:hover {
    transform: scale(1.02);
    opacity: 0.9;
}

.admin {
    width: 90%;
    margin: 28px auto;
}

.admin a {
    background: #ff00ff;
    color: #000;
    box-shadow: 0 0 15px #ff00ff;
}

.panel {
    width: 90%;
    max-width: 600px;
    margin: 30px auto;
    padding: 25px;
    border: 2px solid #00ffff;
    border-radius: 10px;
    box-shadow: 0 0 15px #00ffff;
}

.back {
    width: 90%;
    max-width: 600px;
    margin: 20px auto;
    background: #00ffff;
    color: #000;
}

input,
textarea {
    width: 100%;
    margin: 8px 0;
    padding: 12px;
    border: 1px solid #00ffff;
    border-radius: 6px;
    background: #111;
    color: #fff;
    font-family: inherit;
}

textarea {
    min-height: 100px;
    resize: vertical;
}

button {
    width: 100%;
    margin-top: 10px;
    padding: 12px;
    border: 0;
    border-radius: 6px;
    background: #00ffff;
    color: #000;
    font-weight: bold;
    cursor: pointer;
}

.note {
    color: #aaa;
    font-size: 13px;
    line-height: 1.6;
}

.result {
    min-height: 22px;
    margin-top: 15px;
    color: #00ff88;
    font-size: 13px;
}

footer {
    margin-top: 40px;
    color: #aaa;
    font-size: 12px;
    line-height: 1.7;
}

footer a {
    color: #00ffff;
    text-decoration: none;
}

@media (max-width: 500px) {
    body {
        padding: 15px 8px;
    }

    h1 {
        font-size: 24px;
    }

    h2 {
        font-size: 17px;
    }

    .button-box,
    .admin,
    .panel,
    .back {
        width: 95%;
    }
}
</style>
"""


# ---------- PAGE TEMPLATE ----------
def make_page(title, heading, message, color="#00ffff", form_type=None):
    safe_title = html.escape(title)
    safe_heading = html.escape(heading)
    safe_message = html.escape(message)

    form_html = ""

    if form_type == "post":
        form_html = """
        <input type="text" placeholder="UID">
        <input type="password" placeholder="Token">
        <textarea placeholder="Message लिखें"></textarea>
        <button onclick="showResult('Post Server page ready है।')">
            SUBMIT
        </button>
        """

    elif form_type == "token":
        form_html = """
        <input type="text" placeholder="UID">
        <input type="password" placeholder="Token">
        <button onclick="showResult('Token check page ready है।')">
            CHECK TOKEN
        </button>
        """

    elif form_type == "download":
        form_html = """
        <input type="url" placeholder="URL यहाँ paste करें">
        <button onclick="showResult('Downloader page ready है।')">
            DOWNLOAD
        </button>
        """

    elif form_type == "admin":
        form_html = """
        <input type="text" placeholder="Username">
        <input type="password" placeholder="Password">
        <button onclick="showResult('Admin page ready है।')">
            LOGIN
        </button>
        """

    else:
        form_html = """
        <input type="text" placeholder="Input यहाँ भरें">
        <textarea placeholder="Details लिखें"></textarea>
        <button onclick="showResult('Feature page ready है।')">
            SUBMIT
        </button>
        """

    return f"""
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    {STYLE}
    <style>
        h1 {{
            color: {color};
            text-shadow: 0 0 10px {color};
        }}

        .panel {{
            border-color: {color};
            box-shadow: 0 0 15px {color};
        }}
    </style>
</head>
<body>

<main class="container">
    <div class="panel">
        <h1>{safe_heading}</h1>
        <p class="note">{safe_message}</p>

        {form_html}

        <p id="result" class="result"></p>
    </div>

    <a class="back" href="/">◄ BACK HOME ►</a>
</main>

<script>
function showResult(message) {{
    document.getElementById("result").textContent = message;
}}
</script>

</body>
</html>
"""


# ---------- HOME PAGE ----------
HOME_PAGE = f"""
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RK RAJA XWD PANEL</title>
    {STYLE}
</head>
<body>

<main class="container">

    <h1>RK RAJA XWD</h1>
    <h2>(ALL OPTIONS)</h2>

    <div class="button-box">
        <a href="/section/1">◄ 1 – CONVO SERVER ►</a>
    </div>

    <div class="button-box">
        <a href="/go/backup_convo">◄ 2 – BACKUP CONVO ►</a>
    </div>

    <div class="button-box">
        <a href="/section/2">◄ 3 – POST SERVER ►</a>
    </div>

    <div class="button-box">
        <a href="/go/backup_post">◄ 4 – BACKUP POST SERVER ►</a>
    </div>

    <div class="button-box">
        <a href="/section/3">◄ 5 – TOKEN CHECK VALIDITY ►</a>
    </div>

    <div class="button-box">
        <a href="/section/4">◄ 6 – FETCH ALL UID WITH TOKEN ►</a>
    </div>

    <div class="button-box">
        <a href="/section/5">◄ 7 – FETCH PAGE TOKENS ►</a>
    </div>

    <div class="button-box">
        <a href="/go/group_name_locker">◄ 8 – GROUP NAME LOCKER ►</a>
    </div>

    <div class="button-box">
        <a href="/go/yt_downloader">◄ 9 – YOUTUBE DOWNLOADER ►</a>
    </div>

    <div class="button-box">
        <a href="/go/insta_downloader">◄ 10 – INSTAGRAM DOWNLOADER ►</a>
    </div>

    <div class="button-box">
        <a href="/go/fb_downloader">◄ 11 – FACEBOOK DOWNLOADER ►</a>
    </div>

    <div class="button-box">
        <a href="/go/cookie_json">◄ 12 – COOKIE TO JSON ►</a>
    </div>

    <div class="admin">
        <a href="/admin">⚙ ADMIN PANEL</a>
    </div>

    <footer>
        <p>© 2026 MADE BY: RK RAJA XWD PANEL</p>
        <p>ALWAYS ON FIRE 🔥</p>
        <p>
            <a href="https://www.facebook.com/" target="_blank">
                Chat on Messenger
            </a>
        </p>
    </footer>

</main>

</body>
</html>
"""


# ---------- HOME ----------
@app.route("/", methods=["GET"])
def home():
    return HOME_PAGE


# ---------- ADMIN ----------
@app.route("/admin", methods=["GET"])
def admin():
    return make_page(
        title="RK RAJA ADMIN",
        heading="RK RAJA ADMIN",
        message="Admin panel successfully running है।",
        color="#ff00ff",
        form_type="admin"
    )


# ---------- SECTIONS ----------
@app.route("/section/<int:section_id>", methods=["GET"])
def section(section_id):
    section_data = {
        1: ("CONVO SERVER", "Convo Server page successfully open है।", None),
        2: ("POST SERVER", "Post Server page successfully open है।", "post"),
        3: ("TOKEN CHECK VALIDITY", "Token validity page successfully open है।", "token"),
        4: ("FETCH ALL UID WITH TOKEN", "UID fetch page successfully open है।", "token"),
        5: ("FETCH PAGE TOKENS", "Page token page successfully open है।", "token"),
    }

    data = section_data.get(section_id)

    if data is None:
        return redirect(url_for("home"))

    title, message, form_type = data

    return make_page(
        title=title,
        heading=title,
        message=message,
        color="#00ffff",
        form_type=form_type
    )


# ---------- OTHER FEATURES ----------
@app.route("/go/<name>", methods=["GET"])
def go(name):
    feature_data = {
        "backup_convo": ("BACKUP CONVO", "Backup Convo page successfully open है।", None),
        "backup_post": ("BACKUP POST SERVER", "Backup Post page successfully open है।", None),
        "group_name_locker": ("GROUP NAME LOCKER", "Group Name Locker page successfully open है।", None),
        "yt_downloader": ("YOUTUBE DOWNLOADER", "YouTube Downloader page successfully open है।", "download"),
        "insta_downloader": ("INSTAGRAM DOWNLOADER", "Instagram Downloader page successfully open है।", "download"),
        "fb_downloader": ("FACEBOOK DOWNLOADER", "Facebook Downloader page successfully open है।", "download"),
        "cookie_json": ("COOKIE TO JSON", "Cookie conversion page successfully open है।", None),
    }

    data = feature_data.get(name)

    if data is None:
        return redirect(url_for("home"))

    title, message, form_type = data

    return make_page(
        title=title,
        heading=title,
        message=message,
        color="#ff00ff",
        form_type=form_type
    )


# ---------- ANY UNKNOWN URL ----------
@app.route("/<path:unknown_path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def unknown_path(unknown_path):
    return redirect(url_for("home"))


# ---------- FINAL 404 HANDLER ----------
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("home"))


# ---------- SERVER START ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
  )
