import os
import requests

# Secrets de GitHub
tg_token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

def get_market_data():
    # Dirección API de CoinGecko
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
    response = requests.get(url).json()
    return response

def main():
    try:
        data = get_market_data()
        
        # Extracción de precios
        coins = {
            "BTC": (data['bitcoin']['usd'], data['bitcoin']['usd_24h_change']),
            "ETH": (data['ethereum']['usd'], data['ethereum']['usd_24h_change']),
            "SOL": (data['solana']['usd'], data['solana']['usd_24h_change'])
        }

        # Mensaje de cartera
        mensaje = "🚀 *Crypto-Pulse: Monitor de Estrategia* 🚀\n\n"
        
        for ticker, (price, change) in coins.items():
            emoji = "📈" if change >= 0 else "📉"
            mensaje += f"{emoji} *{ticker}:* ${price:,.2f} ({change:+.2f}%)\n"

        mensaje += (
            "\n⚠️ *Recordatorios de tu Plan:* ⚠️\n"
            "• Máximo 10% de capital por moneda.\n"
            "• Mantén el control (no más de 10 activos).\n"
            "• ¿Ya revisaste tu plan de salida hoy? 📉\n\n"
            "✅ _Reporte automático generado con éxito._"
        )

        # Enviar a Telegram
        url_tg = f"https://api.telegram.org/bot{tg_token}/sendMessage"
        requests.post(url_tg, json={"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"})
        print("¡Reporte de estrategia enviado!")

    except Exception as e:
        print(f"Error en la ejecución: {e}")

if __name__ == '__main__':
    main()
