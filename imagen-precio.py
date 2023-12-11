from flask import Flask, send_file
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

app = Flask(__name__)

def generar_imagen(precio_bitcoin,precio_ars ):
    # Crea una imagen en blanco

    imagen = Image.new('RGB', (200, 50), color='white')
    d = ImageDraw.Draw(imagen)
    
    # Usa una fuente predeterminada (puedes proporcionar una fuente personalizada)
    font = ImageFont.load_default()

    # Dibuja el texto en la imagen
    d.text((10, 10), f'Programacion CMdeOrta', font=font, fill='black')
    d.text((10, 20), f'Precio ARS: ${round(float(precio_ars),2)}', font=font, fill='black')
    d.text((10, 30), f'Precio BTC: ${precio_bitcoin}', font=font, fill='black')

    # Guarda la imagen en un búfer de Bytes
    img_buffer = BytesIO()
    imagen.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return img_buffer

@app.route('/imagen')

def obtener_imagen():
    # Obtener el precio actual del Bitcoin desde una API (por ejemplo, CoinGecko)
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    precio_bitcoin = data['bitcoin']['usd']
    url = 'https://api.binance.com/api/v3/ticker/price?symbol=USDTARS'
    response = requests.get(url)
    data = response.json()
    precio_ars = data['price']
    # Generar la imagen dinámicamente
    imagen = generar_imagen(precio_bitcoin, precio_ars)

    # Devolver la imagen como respuesta
    return send_file(imagen, mimetype='image/png', download_name='precio_bitcoin.png')

if __name__ == '__main__':
    app.run(debug=True)