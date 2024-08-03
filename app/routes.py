from flask import render_template, request, send_file
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from app import app
import io
import re

def custom_transliterate(text):
    # Transliterate using IAST
    transliterated_text = transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
    
    # Replace remaining diacritics manually if necessary
    transliterated_text = re.sub(r'॑', 'ʼ', transliterated_text)  # Example for specific diacritic
    transliterated_text = re.sub(r'॒', '˘', transliterated_text)  # Example for specific diacritic
    # Add more replacements here if needed
    
    return transliterated_text

@app.route('/', methods=['GET', 'POST'])
def index():
    devanagari_text = ""  # Initialize the variable
    transliterated_text = ""
    if request.method == 'POST':
        devanagari_text = request.form['devanagari_text']
        transliterated_text = custom_transliterate(devanagari_text)
    return render_template('index.html', original_text=devanagari_text, transliterated_text=transliterated_text)

@app.route('/download', methods=['POST'])
def download():
    transliterated_text = request.form['transliterated_text']
    return send_file(
        io.BytesIO(transliterated_text.encode('utf-8')),
        as_attachment=True,
        download_name='transliterated_text.txt',
        mimetype='text/plain'
    )
