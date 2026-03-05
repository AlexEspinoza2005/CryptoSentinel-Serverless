import os
import requests
import sys


tg_token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

def get_market_data():
    try:
    
        url_price = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
        prices = requests.get(url_price, timeout=10).json()
        

        url_hist = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7&interval=daily"
        hist = requests.get(url_hist, timeout=10).json()
        

        url_fg = "https://api.alternative.me/fng/"
        fg_data = requests.get(url_fg, timeout=10).json()
        
        return prices, hist, fg_data['data'][0]
    except Exception as e:
        print(f"❌ Error al consultar APIs: {e}")
        return None, None, None

def main():
    if not tg_token or not chat_id:
        print("❌ Error: Faltan variables de entorno TELEGRAM_TOKEN o TELEGRAM_CHAT_ID.")
        sys.exit(1)

    prices, hist, fg = get_market_data()
    
    if not prices or not hist:
        print("❌ No se pudieron obtener los datos del mercado.")
        sys.exit(1)

    try:
        # Lógica de Media Móvil
        precios_7d = [p[1] for p in hist['prices']]
        media_movil = sum(precios_7d) / len(precios_7d)
        btc_actual = prices['bitcoin']['usd']
        tendencia = "🚀 ALCISTA" if btc_actual > media_movil else "📉 BAJISTA"
        
        # Lógica de Sentimiento
        sentimiento_valor = int(fg['value'])
        sentimiento_texto = fg['value_classification']
        
        mensaje = (
            "🛡️ *CryptoSentinel Ultra: Reporte 2026* 🛡️\n\n"
            f"💰 *BTC:* ${btc_actual:,.2f} ({prices['bitcoin']['usd_24h_change']:+.2f}%)\n"
            f"📊 *Tendencia (MA7):* {tendencia}\n"
            f"🌡️ *Sentimiento:* {sentimiento_valor}/100 ({sentimiento_texto})\n\n"
            "🧠 *Análisis de IA Sentinel:* \n"
        )
        
        if sentimiento_valor < 30 and tendencia == "📉 BAJISTA":
            mensaje += "🔥 *Oportunidad:* Miedo extremo + tendencia baja. Revisa tus zonas de compra."
        elif sentimiento_valor > 70:
            mensaje += "⚠️ *Alerta:* Codicia alta. Mantén la disciplina y evita el FOMO."
        else:
            mensaje += "⚖️ *Neutral:* Mercado estable. Sigue tu plan de acumulación."

        mensaje += "\n\n✅ _Reporte Automatizado UTN_"

        # Envío a Telegram
        url_tg = f"https://api.telegram.org/bot{tg_token}/sendMessage"
        r = requests.post(url_tg, json={"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"})
        
        if r.status_code == 200:
            print("✅ ¡Súper-Reporte enviado con éxito!")
        else:
            print(f"❌ Error de Telegram: {r.text}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error en la lógica del script: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
