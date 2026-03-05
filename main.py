import os
import requests
import sys

tg_token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")


PRECIOS_CLAVE = [
    (72000, 0.05, "Entrada inicial — zona de testeo"),
    (70000, 0.10, "Soporte psicológico — acumular"),
    (65000, 0.10, "Zona de interés medio"),
    (60000, 0.20, "Zona fuerte — mayor acumulación"),
    (58000, 0.10, "Soporte técnico relevante"),
    (55000, 0.20, "Zona de máxima acumulación"),
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

def señal_crypto(cambio_24h, precio_actual, media_movil=None):
    if media_movil:
        if precio_actual > media_movil and cambio_24h > 1:
            return "🟢 COMPRA"
        elif precio_actual < media_movil and cambio_24h < -1:
            return "🔴 VENTA"
        else:
            return "🟡 NEUTRAL"
    else:
        if cambio_24h > 2:
            return "🟢 COMPRA"
        elif cambio_24h < -2:
            return "🔴 VENTA"
        else:
            return "🟡 NEUTRAL"

def traducir_sentimiento(texto):
    return {
        "Extreme Fear": "Miedo Extremo",
        "Fear": "Miedo",
        "Neutral": "Neutral",
        "Greed": "Codicia",
        "Extreme Greed": "Codicia Extrema",
    }.get(texto, texto)

def alerta_estrategia(btc_actual):
    alertas = []
    for precio, pct, descripcion in PRECIOS_CLAVE:
        distancia = ((btc_actual - precio) / precio) * 100
        if -2 <= distancia <= 3:
            alertas.append(
                f"   🎯 *Zona activa* ${precio:,} ({pct*100:.0f}% capital) — {descripcion}"
            )
        elif -8 <= distancia < -2:
            alertas.append(
                f"   📍 Aproximándose a ${precio:,} — {descripcion} ({distancia:+.1f}%)"
            )
    return alertas

def main():
    if not tg_token or not chat_id:
        sys.exit(1)

    prices, hist, fg = get_market_data()
    if not prices or not hist:
        sys.exit(1)

    try:
        # Media Móvil 
        precios_7d = [p[1] for p in hist['prices']]
        media_movil_btc = sum(precios_7d) / len(precios_7d)

        # Sentimiento
        sentimiento_valor = int(fg['value'])
        sentimiento_texto = traducir_sentimiento(fg['value_classification'])

        # Precios
        btc = prices['bitcoin']
        eth = prices['ethereum']
        sol = prices['solana']
        bnb = prices['binancecoin']
        xrp = prices['ripple']

        btc_actual = btc['usd']

        # Señales
        señal_btc = señal_crypto(btc['usd_24h_change'], btc_actual, media_movil_btc)
        señal_eth = señal_crypto(eth['usd_24h_change'], eth['usd'])
        señal_sol = señal_crypto(sol['usd_24h_change'], sol['usd'])
        señal_bnb = señal_crypto(bnb['usd_24h_change'], bnb['usd'])
        señal_xrp = señal_crypto(xrp['usd_24h_change'], xrp['usd'])

        tendencia_btc = "Alcista 🚀" if btc_actual > media_movil_btc else "Bajista 📉"
        dist_objetivo = ((btc_actual - PRECIO_MEDIO_OBJETIVO) / PRECIO_MEDIO_OBJETIVO) * 100

        # Alertas de estrategia
        alertas = alerta_estrategia(btc_actual)

        # Análisis IA
        if sentimiento_valor < 25 and "Bajista" in tendencia_btc:
            analisis = "Miedo extremo y tendencia bajista. Condiciones óptimas para ejecutar zonas de acumulación de su plan."
        elif sentimiento_valor < 40 and btc_actual <= 65000:
            analisis = "Miedo en el mercado con BTC en zona estratégica. Evalúe ejecutar entradas según su plan de acumulación."
        elif sentimiento_valor > 70:
            analisis = "Codicia elevada en el mercado. Evite compras impulsivas. Mantenga la disciplina de su estrategia."
        elif btc_actual > media_movil_btc:
            analisis = "Tendencia alcista activa. Si no ha completado sus entradas, espere correcciones a zonas de su plan."
        else:
            analisis = "Mercado en equilibrio. Continúe el DCA semanal y respete los niveles de su estrategia definida."

       
        msg = (
            "🛡️ *CryptoSentinel Ultra — Reporte Diario 2026* 🛡️\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "📊 *MERCADO CRIPTO*\n\n"
            f"₿ *Bitcoin (BTC)*\n"
            f"   Precio: ${btc_actual:,.2f}  ({btc['usd_24h_change']:+.2f}%)\n"
            f"   Tendencia MA7: {tendencia_btc}\n"
            f"   Señal: {señal_btc}\n\n"
            f"🔷 *Ethereum (ETH)*\n"
            f"   Precio: ${eth['usd']:,.2f}  ({eth['usd_24h_change']:+.2f}%)\n"
            f"   Señal: {señal_eth}\n\n"
            f"🌐 *Solana (SOL)*\n"
            f"   Precio: ${sol['usd']:,.2f}  ({sol['usd_24h_change']:+.2f}%)\n"
            f"   Señal: {señal_sol}\n\n"
            f"🟡 *BNB*\n"
            f"   Precio: ${bnb['usd']:,.2f}  ({bnb['usd_24h_change']:+.2f}%)\n"
            f"   Señal: {señal_bnb}\n\n"
            f"💧 *XRP*\n"
            f"   Precio: ${xrp['usd']:,.2f}  ({xrp['usd_24h_change']:+.2f}%)\n"
            f"   Señal: {señal_xrp}\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📋 *ESTRATEGIA BEARMARKET 2026*\n\n"
            f"   Precio objetivo medio: ${PRECIO_MEDIO_OBJETIVO:,}\n"
            f"   BTC actual vs objetivo: {dist_objetivo:+.1f}%\n\n"
            "   *Zonas de compra (75% capital):*\n"
        )

        for precio, pct, desc in PRECIOS_CLAVE:
            dist = ((btc_actual - precio) / precio) * 100
            estado = "✅ ALCANZADO" if btc_actual <= precio * 1.01 else f"{dist:+.1f}%"
            msg += f"   • ${precio:,} → {pct*100:.0f}% capital ({estado})\n"

        msg += "\n   *DCA Semanal (25% capital):*\n"
        msg += "   1% del capital por semana durante 25 semanas\n\n"

        if alertas:
            msg += "⚠️ *ALERTAS DE ENTRADA*\n"
            msg += "\n".join(alertas) + "\n\n"

        msg += (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "🧠 *ÍNDICE DE SENTIMIENTO*\n"
            f"   {sentimiento_valor}/100 — {sentimiento_texto}\n\n"
            "🤖 *ANÁLISIS SENTINEL*\n"
            f"   {analisis}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "✅ _Reporte Automatizado_"
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
