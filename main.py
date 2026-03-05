import os
import requests

tg_token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

def get_market_data():
  
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7&interval=daily"
    data_hist = requests.get(url).json()
    
    url_price = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
    prices = requests.get(url_price).json()
    
 
    url_fg = "https://api.alternative.me/fng/"
    fg_data = requests.get(url_fg).json()
    
    return prices, data_hist, fg_data['data'][0]

def main():
    try:
        prices, hist, fg = get_market_data()
        
        # 1. Análisis de Media 
        precios_7d = [p[1] for p in hist['prices']]
        media_movil = sum(precios_7d) / len(precios_7d)
        btc_actual = prices['bitcoin']['usd']
        tendencia = "🚀 ALCISTA" if btc_actual > media_movil else "📉 BAJISTA"
        
        # 2. Análisis de Sentimiento (Fear & Greed)
        sentimiento_valor = int(fg['value'])
        sentimiento_texto = fg['value_classification']
        
        # 3. Construcción del Reporte Estratégico
        mensaje = (
            "🛡️ *CryptoSentinel Ultra: Reporte 2026* 🛡️\n\n"
            f"💰 *BTC:* ${btc_actual:,.2f} ({prices['bitcoin']['usd_24h_change']:+.2f}%)\n"
            f"📊 *Tendencia (MA7):* {tendencia}\n"
            f"🌡️ *Sentimiento:* {sentimiento_valor}/100 ({sentimiento_texto})\n\n"
            "🧠 *Análisis de IA Sentinel:* \n"
        )
        
        # Lógica de sentimiento
        if sentimiento_valor < 30 and tendencia == "📉 BAJISTA":
            mensaje += "🔥 *Oportunidad:* Miedo extremo + tendencia baja. Revisa tus zonas de compra del Excel."
        elif sentimiento_valor > 70:
            mensaje += "⚠️ *Alerta:* Codicia alta. No caigas en FOMO, respeta el 10% de capital."
        else:
            mensaje += "⚖️ *Neutral:* Mantén la calma y sigue tu plan de acumulación Bear."

        mensaje += (
            "\n\n📋 *Recordatorio Estratégico:* \n"
            "• Máximo 10 monedas.\n"
            "• Plan de salida definido.\n"
            "✅ _Reporte Generado Automáticamente_"
        )

        # Envío a Telegram
        url_tg = f"https://api.telegram.org/bot{tg_token}/sendMessage"
        requests.post(url_tg, json={"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"})
        print("¡Súper-Reporte enviado con éxito!")

    except Exception as e:
        print(f"Error en el sistema: {e}")

if __name__ == '__main__':
    main()
