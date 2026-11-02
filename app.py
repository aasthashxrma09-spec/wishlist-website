from flask import Flask, request, redirect, url_for, jsonify, render_template_string
from pathlib import Path
import json

app = Flask(__name__)
DATA_FILE = Path("birthday_choices.json")

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#fff1f5">
<title>Pum's recent thoughts ♡</title>
<style>
:root{--pink:#e9a9c2;--deep:#a9587c;--ink:#573d4b;--cream:#fffaf8;--line:#f2dce6}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;background:radial-gradient(circle at 10% 8%,#fff 0,transparent 32%),linear-gradient(135deg,#fff2f5,#f8efff 55%,#fff8ee);color:var(--ink);font-family:Georgia,'Times New Roman',serif;overflow-x:hidden}
button{font:inherit;cursor:pointer}
.screen{display:none;min-height:100vh;padding:28px 18px 44px;align-items:center;justify-content:center;flex-direction:column;text-align:center;animation:fade .55s ease}
.screen.active{display:flex}
@keyframes fade{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes float{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-9px) rotate(2deg)}}
@keyframes sparkle{0%,100%{opacity:.25;transform:scale(.8)}50%{opacity:1;transform:scale(1.2)}}
@keyframes openLeft{to{transform:perspective(900px) rotateY(-108deg)}}
@keyframes tail{0%,100%{transform:rotate(0)}50%{transform:rotate(15deg)}}
.kicker{font:11px Arial,sans-serif;letter-spacing:3px;text-transform:uppercase;color:#b77b98}
h1{font-size:clamp(34px,8vw,58px);font-weight:normal;line-height:1.08;margin:13px 0}
p{font:15px/1.7 Arial,sans-serif;color:#8b7180;max-width:520px}
.primary,.secondary{border:0;border-radius:999px;padding:14px 23px;margin:8px 5px;font:13px Arial,sans-serif;transition:.2s}
.primary{background:var(--deep);color:white;box-shadow:0 8px 20px #c47d9b40}
.secondary{background:#f7e6ee;color:#89566f}
.primary:hover,.secondary:hover{transform:translateY(-2px)}
.door-wrap{position:relative;width:min(260px,70vw);height:355px;margin:24px auto 28px;perspective:1000px}
.door-frame{position:absolute;inset:0;background:#d8a7b9;border:10px solid #f9e4ec;border-radius:120px 120px 8px 8px;box-shadow:0 15px 35px #9e668033;overflow:hidden}
.door{position:absolute;inset:0 0 0 0;transform-origin:left center;background:linear-gradient(135deg,#f4c9d8,#d995b1);border:2px solid #c77e9e;border-radius:108px 108px 3px 3px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:18px;box-shadow:inset 0 0 0 10px #f9dce7}
.door:before,.door:after{content:"";width:70%;height:85px;border:2px solid #fff0f5;border-radius:14px;position:absolute;left:15%}
.door:before{top:45px}.door:after{bottom:45px}
.door-knob{position:absolute;right:23px;top:51%;width:13px;height:13px;border-radius:50%;background:#b77a55;z-index:2}
.door.open{animation:openLeft 1.15s forwards ease-in-out}
.door-label{font-size:27px;z-index:1;color:#9c5575}
.spark{position:absolute;color:#d99ab5;font-size:23px;animation:sparkle 2s infinite}
.s1{top:12%;left:10%}.s2{top:23%;right:8%;animation-delay:.6s}.s3{bottom:18%;left:12%;animation-delay:1s}
.photo{width:min(320px,82vw);max-height:360px;object-fit:cover;border-radius:22px;border:7px solid white;box-shadow:0 12px 30px #9d6c8425}
.dog-photo{object-position:center 42%;animation:float 3.5s ease-in-out infinite}
.speech{background:white;border:1px solid var(--line);border-radius:22px;padding:16px 22px;margin:-8px 0 18px;box-shadow:0 8px 22px #9d6c8415;font-size:21px;max-width:430px}
.speech:after{content:"";display:block;position:relative;width:15px;height:15px;background:white;border-right:1px solid var(--line);border-bottom:1px solid var(--line);transform:rotate(45deg);margin:13px auto -24px}
.wish-card{width:min(540px,94vw);background:#ffffffdf;border:1px solid var(--line);border-radius:26px;padding:24px 20px;box-shadow:0 12px 34px #9d6c8418;margin:18px auto}
.wish-card h2{font-size:clamp(27px,6vw,39px);font-weight:normal;line-height:1.2;margin:12px 0}
.wish-card .emoji{font-size:44px;display:block}
.wish-photo{width:min(340px,100%);max-height:360px;object-fit:cover;border-radius:17px;margin:10px auto 4px;display:block}
.note{font:13px/1.6 Arial,sans-serif;color:#987f8d}
.progress{font:11px Arial,sans-serif;color:#b18a9d;letter-spacing:2px;margin-top:20px}
.important{background:linear-gradient(145deg,#fff7fa,#ffe9f0);border:2px solid #edc0d2}
.important h2{color:#a34870}
.choice-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:18px}
.choice{border:1px solid #e8c7d5;background:#fff7fa;color:#89566f;border-radius:999px;padding:10px 15px;font:12px Arial,sans-serif}
.choice.selected{background:#a9587c;color:white;border-color:#a9587c}
.final-heart{font-size:55px;animation:float 3s infinite}
.footer{font:11px Arial,sans-serif;color:#b18a9d;margin-top:25px}
@media(max-width:420px){.door-wrap{height:320px}.photo{max-height:320px}.wish-card{padding:20px 15px}}
</style>
</head>
<body>
<section class="screen active" id="doorScreen">
  <div class="kicker">a little something for dad</div>
  <h1>Someone left<br>the door open…</h1>
  <p>There's a tiny message waiting for you inside.</p>
  <div class="door-wrap">
    <span class="spark s1">✦</span><span class="spark s2">♡</span><span class="spark s3">✧</span>
    <div class="door-frame">
      <div class="door" id="door"><div class="door-label">♡</div><div class="door-knob"></div></div>
    </div>
  </div>
  <button class="primary" id="openDoor">Tap to look into Pum's recent thoughts ♡</button>
</section>

<section class="screen" id="dogScreen">
  <div class="kicker">special delivery from yuki</div>
  <img class="photo dog-photo" src="{{ url_for('static', filename='yuki.jpeg') }}" alt="Yuki, a fluffy white dog">
  <div class="speech">Hi Dad! This is Mom's wishlist! 🐾</div>
  <button class="primary" onclick="showScreen('wish1')">Hello! Let's continue ♡</button>
</section>

<section class="screen" id="wish1">
  <div class="kicker">mom's birthday wishlist · 01</div>
  <div class="wish-card">
    <span class="emoji">🎀</span>
    <h2>You can get Mom STICKERRRSS on her bday!</h2>
    <p class="note">You know she loves her little stickersss ♡</p>
  </div>
  <div class="choice-row" data-id="stickers">
    <button class="choice" onclick="choose(this,'stickers','I'm getting these!')">I'm getting these! ♡</button>
    <button class="choice" onclick="choose(this,'stickers','Maybe!')">Maybe!</button>
  </div>
  <button class="primary" onclick="showScreen('wish2')">Next little thought →</button>
  <div class="progress">01 / 04</div>
</section>

<section class="screen" id="wish2">
  <div class="kicker">mom's birthday wishlist · 02</div>
  <div class="wish-card">
    <img class="wish-photo" src="{{ url_for('static', filename='clothes.jpeg') }}" alt="Cute pastel clothes inspiration">
    <h2>You can get her cute clothes!</h2>
    <p class="note">Look at all the pretty pink things. 🎀</p>
  </div>
  <div class="choice-row" data-id="clothes">
    <button class="choice" onclick="choose(this,'clothes','I'm getting these!')">I'm getting these! ♡</button>
    <button class="choice" onclick="choose(this,'clothes','Maybe!')">Maybe!</button>
  </div>
  <button class="primary" onclick="showScreen('wish3')">Next little thought →</button>
  <div class="progress">02 / 04</div>
</section>

<section class="screen" id="wish3">
  <div class="kicker">mom's birthday wishlist · 03</div>
  <div class="wish-card">
    <span class="emoji">📚</span>
    <h2>She wouldn't say no to books!</h2>
    <p class="note">A book-shaped present is always a good idea. ♡</p>
  </div>
  <div class="choice-row" data-id="books">
    <button class="choice" onclick="choose(this,'books','I'm getting books!')">I'm getting books! ♡</button>
    <button class="choice" onclick="choose(this,'books','Maybe!')">Maybe!</button>
  </div>
  <button class="primary" onclick="showScreen('wish4')">One VERY important thing →</button>
  <div class="progress">03 / 04</div>
</section>

<section class="screen" id="wish4">
  <div class="kicker">mom's birthday wishlist · 04</div>
  <div class="wish-card important">
    <span class="emoji">💐🍫</span>
    <h2>THE MOST IMPORTANT</h2>
    <p style="font: bold 17px/1.65 Arial,sans-serif;color:#9d4f72">You must get her flowersss and chocolates on her bday. Don't forget like you did on your anniversary 😭</p>
    <img class="wish-photo" src="{{ url_for('static', filename='flowers_chocolates.jpeg') }}" alt="Pink roses and a chocolate bouquet">
  </div>
  <div class="choice-row" data-id="flowers">
    <button class="choice" onclick="choose(this,'flowers','I promise!')">I PROMISE! 💗</button>
    <button class="choice" onclick="choose(this,'flowers','Noted…')">Noted…</button>
  </div>
  <button class="primary" onclick="showScreen('ending')">Okay okay, anything else? →</button>
  <div class="progress">04 / 04</div>
</section>

<section class="screen" id="ending">
  <div class="final-heart">♡</div>
  <div class="kicker">one last thing from mom</div>
  <div class="wish-card">
    <h2>Just kidding!</h2>
    <p style="font-size:17px;color:#795c6c">She doesn't expect anything else now, but I do hope that you do hang out with Mom on her bday. ♡</p>
    <span class="emoji">🐾💗</span>
  </div>
  <button class="primary" onclick="showScreen('thanks')">I hear you, Yuki! ♡</button>
</section>

<section class="screen" id="thanks">
  <div class="final-heart">💗</div>
  <h1>Good boy, Dad!</h1>
  <p>Yuki has officially delivered Mom's message.</p>
  <p class="note">Your choices have been saved on this website.</p>
  <button class="secondary" onclick="showScreen('dogScreen')">Read it again ♡</button>
  <div class="footer">made with love by Pum (and Yuki) ♡</div>
</section>

<script>
function showScreen(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  window.scrollTo({top:0,behavior:'smooth'});
}
document.getElementById('openDoor').addEventListener('click',()=>{
  const door=document.getElementById('door');
  door.classList.add('open');
  document.getElementById('openDoor').disabled=true;
  setTimeout(()=>showScreen('dogScreen'),1050);
});
async function choose(button, id, value){
  const row=button.closest('.choice-row');
  row.querySelectorAll('.choice').forEach(b=>b.classList.remove('selected'));
  button.classList.add('selected');
  try{
    await fetch('/choose',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,value})});
  }catch(e){ console.log('Could not save choice',e); }
}
async function loadChoices(){
  try{
    const data=await (await fetch('/choices')).json();
    document.querySelectorAll('.choice-row').forEach(row=>{
      const selected=data[row.dataset.id];
      if(selected) row.querySelectorAll('.choice').forEach(b=>{
        if(b.textContent.trim().startsWith(selected.split(' ')[0]) || b.textContent.trim()===selected) b.classList.add('selected');
      });
    });
  }catch(e){}
}
loadChoices();
</script>
</body>
</html>
"""

def read_choices():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
    return {}

@app.route("/")
def home():
    return render_template_string(PAGE)

@app.route("/choose", methods=["POST"])
def choose():
    data = request.get_json(silent=True) or {}
    key, value = data.get("id"), data.get("value")
    allowed = {"stickers", "clothes", "books", "flowers"}
    if key in allowed and isinstance(value, str):
        choices = read_choices()
        choices[key] = value
        DATA_FILE.write_text(json.dumps(choices, indent=2), encoding="utf-8")
    return jsonify({"ok": True})

@app.route("/choices")
def choices():
    return jsonify(read_choices())

if __name__ == "__main__":
    app.run(debug=True)
