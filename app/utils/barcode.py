import io
from flask import send_file
import barcode
from barcode.writer import ImageWriter

def generate_barcode(item):
    code = barcode.get('code128', str(item.id), writer=ImageWriter())
    buffer = io.BytesIO()
    code.write(buffer)
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name=f'barcode_{item.id}.png') 