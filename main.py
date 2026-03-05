import os
import requests
import sys

tg_token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")


PRECIOS_CLAVE = [
    (72000, 0.05, "Entrada inicial"),
    (70000, 0.10, "Soporte psicológico"),
    (65000, 0.10, "Zona de interés medio"),
    (60000, 0.20, "Zona fuerte"),
    (58000, 0.10, "Soporte técnico"),
    (55000, 0.20, "Máxima acumulación"),
]
PRECIO_MEDIO_OBJETIVO = 61200

def get_market_data():
    try:
        url_price = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum,solana,binancecoin,ripple"
            "&vs_currencies=usd&include_24hr_change=true"
        )
        prices = requests.get(url_price, timeout=10).json()

        url_hist = (
            "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
            "?vs_currency=usd&days=7&interval=daily"
        )
        hist = requests.get(url_hist, timeout=10).json()

        url_fg = "https://api.alternative.me/fng/"
        fg_data = requests.get(url_fg, timeout=10).json()

        return prices, hist, fg_data['data'][0]
    except Exception:
        return None, None, None

def zona_btc_activa(btc_actual):
    for precio, pct, desc in PRECIOS_CLAVE:
        distancia = ((btc_actual - precio) / precio) * 100
        if -2 <= distancia <= 3:
            return f"🎯 En zona ${precio:,} — invertir *{pct*100:.0f}%* capital\n  {desc}"
        elif -8 <= distancia < -2:
            return f"📍 Aprox. a ${precio:,} ({pct*100:.0f}% capital) — faltan {abs(distancia):.1f}%"
    for precio, pct, desc in PRECIOS_CLAVE:
        if btc_actual > precio:
            distancia = ((btc_actual - precio) / precio) * 100
            return f"⏳ Proxima zona: ${precio:,} ({pct*100:.0f}% capital) — {distancia:+.1f}% lejos"
    return "⏳ BTC por encima de todas las zonas del plan"

def barra_sentimiento(valor):
    filled = round(valor / 10)
    return "█" * filled + "░" * (10 - filled)

def traducir_sentimiento(texto):
    return {
        "Extreme Fear": "Miedo Extremo 😱",
        "Fear": "Miedo 😨",
        "Neutral": "Neutral 😐",
        "Greed": "Codicia 😏",
        "Extreme Greed": "Codicia Extrema 🤑",
    }.get(texto, texto)

def main():
    if not tg_token or not chat_id:
        sys.exit(1)

    prices, hist, fg = get_market_data()
    if not prices or not hist:
        sys.exit(1)

    try:
        precios_7d = [p[1] for p in hist['prices']]
        media_movil_btc = sum(precios_7d) / len(precios_7d)

        sentimiento_valor = int(fg['value'])
        sentimiento_texto = traducir_sentimiento(fg['value_classification'])

        btc = prices['bitcoin']
        eth = prices['ethereum']
        sol = prices['solana']
        bnb = prices['binancecoin']
        xrp = prices['ripple']
        btc_actual = btc['usd']

        tendencia_btc = "Alcista 🚀" if btc_actual > media_movil_btc else "Bajista 📉"
        dist_objetivo = ((btc_actual - PRECIO_MEDIO_OBJETIVO) / PRECIO_MEDIO_OBJETIVO) * 100
        barra = barra_sentimiento(sentimiento_valor)
        info_zona = zona_btc_activa(btc_actual)

        if sentimiento_valor < 25 and "Bajista" in tendencia_btc:
            analisis = "Miedo extremo con tendencia bajista. Condiciones óptimas para ejecutar las zonas de acumulación del plan."
        elif sentimiento_valor < 40 and btc_actual <= 65000:
            analisis = "Miedo en el mercado con BTC en zona estratégica. Evalúe ejecutar entradas según su plan."
        elif sentimiento_valor > 70:
            analisis = "Codicia elevada. Evite compras impulsivas y mantenga la disciplina de su estrategia."
        elif btc_actual > media_movil_btc:
            analisis = "Tendencia alcista activa. Si no completó sus entradas, espere correcciones a las zonas del plan."
        else:
            analisis = "Mercado en equilibrio. Continúe el DCA semanal y respete los niveles definidos."

        msg = (
            "🛡️  *CryptoSentinel Ultra*\n"
            "_Reporte Diario 2026_\n\n"

            "📊  *MERCADO EN TIEMPO REAL*\n\n"

            f"₿  *Bitcoin*\n"
            f"   ${btc_actual:,.2f}  ({btc['usd_24h_change']:+.2f}%)\n"
            f"   MA7: {tendencia_btc}\n\n"

            f"🔷  *Ethereum*\n"
            f"   ${eth['usd']:,.2f}  ({eth['usd_24h_change']:+.2f}%)\n\n"

            f"🌐  *Solana*\n"
            f"   ${sol['usd']:,.2f}  ({sol['usd_24h_change']:+.2f}%)\n\n"

            f"🟡  *BNB*\n"
            f"   ${bnb['usd']:,.2f}  ({bnb['usd_24h_change']:+.2f}%)\n\n"

            f"💧  *XRP*\n"
            f"   ${xrp['usd']:,.4f}  ({xrp['usd_24h_change']:+.2f}%)\n\n"

            "📋  *ESTRATEGIA BEARMARKET 2026*\n"
            f"  Objetivo precio medio: ${PRECIO_MEDIO_OBJETIVO:,}\n"
            f"  BTC vs objetivo: {dist_objetivo:+.1f}%\n\n"
            "  *Zonas clave — 75% capital:*\n"
        )

        for precio, pct, desc in PRECIOS_CLAVE:
            dist = ((btc_actual - precio) / precio) * 100
            if btc_actual <= precio * 1.01:
                estado = "✅"
            elif dist <= 5:
                estado = "🔔"
            else:
                estado = "⏳"
            msg += f"  {estado} ${precio:,} — {pct*100:.0f}% capital  ({dist:+.1f}%)\n"

        msg += (
            "\n  *DCA Semanal — 25% capital:*\n"
            "  1% semanal · 25 semanas\n\n"
            "  *Estado actual del plan:*\n"
            f"  {info_zona}\n\n"

            "🧠  *SENTIMIENTO DEL MERCADO*\n"
            f"  {barra}\n"
            f"  {sentimiento_valor}/100 — {sentimiento_texto}\n\n"

            "🤖  *ANÁLISIS SENTINEL*\n"
            f"  {analisis}\n"
        )

        url_tg = f"https://api.telegram.org/bot{tg_token}/sendMessage"
        r = requests.post(url_tg, json={
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": "Markdown"
        })

        if r.status_code == 200:
            print("✅ Reporte enviado.")
        else:
            sys.exit(1)

    except Exception:
        sys.exit(1)

if __name__ == '__main__':
    main()
