from flask import Flask, render_template_string, request
import string
import numpy as np
from math import gcd

app = Flask(__name__)
ALPHABET = string.ascii_uppercase


def vigenere(text, key, decrypt=False):
    result = ""
    key = key.upper()
    key_index = 0

    for char in text.upper():
        if char in ALPHABET:
            shift = ord(key[key_index % len(key)]) - 65
            if decrypt:
                shift = -shift
            result += chr((ord(char) - 65 + shift) % 26 + 65)
            key_index += 1
    return result


def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine(text, a, b, decrypt=False):
    result = ""
    if decrypt:
        a = mod_inverse(a, 26)

    for char in text.upper():
        if char in ALPHABET:
            x = ord(char) - 65
            if decrypt:
                result += chr((a * (x - b)) % 26 + 65)
            else:
                result += chr((a * x + b) % 26 + 65)
    return result


def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    used = set()
    matrix = []

    for char in key + ALPHABET:
        if char not in used and char != 'J':
            used.add(char)
            matrix.append(char)

    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_pos(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c

def playfair_prepare(text):
    text = text.upper().replace("J", "I")
    text = ''.join([c for c in text if c in ALPHABET])
    if len(text) % 2 != 0:
        text += "X"
    return text

def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = playfair_prepare(text)
    result = ""

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)

        if r1 == r2:
            result += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            result += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]

    return result, matrix

def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = playfair_prepare(text)
    result = ""

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)

        if r1 == r2:
            result += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
        elif c1 == c2:
            result += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]

    return result, matrix


def hill_encrypt(text, matrix):
    text = ''.join([c for c in text.upper() if c in ALPHABET])
    if len(text) % 2 != 0:
        text += "X"

    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i])-65, ord(text[i+1])-65]
        res = np.dot(matrix, pair) % 26
        result += chr(res[0]+65) + chr(res[1]+65)
    return result

def hill_decrypt(text, matrix):
    text = ''.join([c for c in text.upper() if c in ALPHABET])

    det = int(round(np.linalg.det(matrix))) % 26

    if gcd(det, 26) != 1:
        return "Matrix tidak dapat di-inverse (det tidak relatif prima dengan 26)"

 
    det_inv = None
    for i in range(1, 26):
        if (det * i) % 26 == 1:
            det_inv = i
            break


    inv_matrix = np.array([
        [ matrix[1][1], -matrix[0][1]],
        [-matrix[1][0],  matrix[0][0]]
    ])

    inv_matrix = (det_inv * inv_matrix) % 26

    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i])-65, ord(text[i+1])-65]
        res = np.dot(inv_matrix, pair) % 26
        result += chr(int(res[0])+65) + chr(int(res[1])+65)

    return result


rotor_wiring = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

def enigma(text, start_pos=0):
    result = ""
    rotor_pos = start_pos

    for char in text.upper():
        if char in ALPHABET:
            shifted = ALPHABET[(ord(char)-65+rotor_pos)%26]
            step1 = rotor_wiring[ord(shifted)-65]
            step2 = reflector[ord(step1)-65]
            back = ALPHABET[rotor_wiring.index(step2)]
            final = ALPHABET[(ord(back)-65-rotor_pos)%26]
            result += final
            rotor_pos = (rotor_pos + 1) % 26
    return result


HTML = """
<!doctype html>
<html>
<head>
<title>Kalkulator Kriptografi</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{
    background: linear-gradient(135deg,#1f1c2c,#928dab);
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    font-family: 'Segoe UI', sans-serif;
}
.calculator{
    width:600px;
    min-height:650px;
    padding:40px;
    border-radius:35px;
    backdrop-filter: blur(20px);
    background: rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.2);
    box-shadow:0 30px 80px rgba(0,0,0,0.6);
    color:white;

    transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1),
                box-shadow 0.4s cubic-bezier(0.25, 1, 0.5, 1);
}

.calculator:hover{
    transform: translateY(-6px);
    box-shadow:0 40px 100px rgba(0,0,0,0.75);
}
.title{
    text-align:center;
    font-size:28px;
    font-weight:900;
    margin-bottom:30px;
    background: linear-gradient(90deg,#8e9eab,#eef2f3,#8e9eab);
    background-size:200% auto;
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation: gradientMove 4s linear infinite;
}
@keyframes gradientMove{
    0%{background-position:0%;}
    100%{background-position:200%;}
}
textarea,input,select{
    width:100%;
    background:#2c2c3e;
    border:none;
    color:white;
    border-radius:12px;
    padding:12px;
    margin-bottom:15px;
}
.label-title{
    font-size:13px;
    letter-spacing:1.5px;
    font-weight:600;
    margin-bottom:6px;
    opacity:0.75;
    text-transform:uppercase;
}
.button-grid{
    display:flex;
    justify-content:space-between;
}
.btn-custom{
    width:48%;
    border-radius:20px;
    font-weight:bold;
    padding:10px;
    border:none;
}
.encrypt-btn{ background:#00c853; color:white; }
.decrypt-btn{ background:#ff5252; color:white; }
.display{
    background:#000;
    border-radius:15px;
    padding:20px;
    margin-top:15px;
    min-height:100px;
}
.display{
    position:relative;
    background:#000;
    border-radius:15px;
    padding:20px;
    margin-top:15px;
    min-height:100px;
    word-wrap:break-word;
}

.copy-btn{
    position:absolute;
    top:10px;
    right:15px;
    background:#444;
    border:none;
    color:white;
    padding:5px 12px;
    border-radius:10px;
    font-size:12px;
    cursor:pointer;
    transition:0.2s;
}

.copy-btn:hover{
    background:#666;
}
</style>
</head>
<body>
<div class="calculator">
<div class="title">KALKULATOR KRIPTOGRAFI</div>
<form method="POST">
<div class="label-title">Cipher</div>
<select name="cipher">
<option value="vigenere" {% if cipher=="vigenere" %}selected{% endif %}>Vigenere</option>
<option value="affine" {% if cipher=="affine" %}selected{% endif %}>Affine</option>
<option value="playfair" {% if cipher=="playfair" %}selected{% endif %}>Playfair</option>
<option value="hill" {% if cipher=="hill" %}selected{% endif %}>Hill</option>
<option value="enigma" {% if cipher=="enigma" %}selected{% endif %}>Enigma</option>
</select>
<div class="label-title">Plaintext / Ciphertext</div>
<textarea name="text">{{ text }}</textarea>
<div class="label-title">Key</div>
<input id="keyInput" name="key" value="{{ key }}">
<div class="button-grid">
<button name="action" value="encrypt" class="btn-custom encrypt-btn">Encrypt</button>
<button name="action" value="decrypt" class="btn-custom decrypt-btn">Decrypt</button>
</div>
</form>
{% if result %}
<div class="display" id="resultBox">
    <div id="resultText">{{ result }}</div>
    <button class="copy-btn" onclick="copyResult()">Copy</button>
</div>
{% endif %}
</div>

<script>
const cipherSelect = document.querySelector('select[name="cipher"]');
const textArea = document.querySelector('textarea[name="text"]');
const keyInput = document.getElementById("keyInput");

function updatePlaceholder(){
    const cipher = cipherSelect.value;
    if(cipher==="vigenere") keyInput.placeholder="Contoh: UNDIP";
    else if(cipher==="affine") keyInput.placeholder="Contoh: 7,10";
    else if(cipher==="playfair") keyInput.placeholder="Contoh: GADJAH";
    else if(cipher==="hill") keyInput.placeholder="Contoh: 3,3,2,5";
    else if(cipher==="enigma") keyInput.placeholder="Contoh: 3";
}

cipherSelect.addEventListener("change", function(){
    updatePlaceholder();
    textArea.value="";
    keyInput.value="";
    const display=document.querySelector(".display");
    if(display) display.remove();
});

window.onload=updatePlaceholder;
</script>
<script>
function copyResult(){
    const text = document.getElementById("resultText").innerText;

    navigator.clipboard.writeText(text).then(function(){
        const btn = document.querySelector(".copy-btn");
        btn.innerText = "Copied!";
        setTimeout(()=>{ btn.innerText = "Copy"; },1500);
    });
}
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    cipher = "vigenere"
    text = ""
    key = ""

    if request.method == "POST":
        cipher = request.form["cipher"]
        text = request.form["text"]
        key = request.form["key"]
        action = request.form["action"]

        try:
            if cipher == "vigenere":
                result = vigenere(text, key, decrypt=(action=="decrypt"))

            elif cipher == "affine":
                a,b = map(int,key.split(","))
                result = affine(text,a,b,decrypt=(action=="decrypt"))

            elif cipher == "playfair":
                if action == "encrypt":
                    result, _ = playfair_encrypt(text,key)
                else:
                    result, _ = playfair_decrypt(text,key)

            elif cipher == "hill":
                nums = list(map(int,key.split(",")))
                matrix_np = np.array([[nums[0],nums[1]],[nums[2],nums[3]]])
                if action == "encrypt":
                    result = hill_encrypt(text,matrix_np)
                else:
                    result = hill_decrypt(text,matrix_np)

            elif cipher == "enigma":
                start = int(key) if key else 0
                result = enigma(text,start)

        except:
            result = "Error!!!"

    return render_template_string(HTML,
        result=result,
        cipher=cipher,
        text=text,
        key=key
    )

if __name__ == "__main__":
    app.run(debug=True)