# 📡 CryptoSentinel Ultra — Serverless Crypto Intelligence & Automated DCA Bot

<div align="center">

[![CryptoSentinel-Serverless](https://github.com/AlexEspinoza2005/CryptoSentinel-Serverless/actions/workflows/bot.yml/badge.svg)](https://github.com/AlexEspinoza2005/CryptoSentinel-Serverless/actions/workflows/bot.yml)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Serverless](https://img.shields.io/badge/Serverless-GitHub_Actions_CRON-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot_Alerts-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)
![CoinGecko](https://img.shields.io/badge/CoinGecko-REST_API-8DC63F?style=for-the-badge&logo=coingecko&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)

<p align="center">
  <strong>Automated cloud-native financial intelligence engine running 100% serverless on GitHub Actions. Delivers scheduled quantitative market analysis, technical moving averages (MA7), fear & greed sentiment scoring, and strategic Dollar-Cost Averaging (DCA) notifications directly to Telegram.</strong>
</p>

</div>

---

## 📋 System Overview

**CryptoSentinel Ultra** is a serverless market analytics daemon designed for autonomous financial tracking and disciplined portfolio accumulation. The engine requires zero persistent servers or VPS instances; it operates through scheduled GitHub Actions runners triggered by CRON expressions, executes Python quantitative analysis against live cryptocurrency feeds, and dispatches rich formatted briefings to Telegram channels.

---

## 🏛️ Serverless Architecture & Execution Lifecycle

```
 ┌─────────────────────────────────────────────────────────────┐
 │                GitHub Actions CRON Scheduler                │
 │                     (Daily @ 13:00 UTC)                     │
 └──────────────────────────────┬──────────────────────────────┘
                                │ Triggers Runner (Ubuntu-latest)
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                   CryptoSentinel Engine                     │
 │ ┌─────────────────────────────────────────────────────────┐ │
 │ │ Environment: Decrypts TELEGRAM_TOKEN & CHAT_ID Secrets │ │
 │ ├─────────────────────────────────────────────────────────┤ │
 │ │ Ingestion 1: CoinGecko REST API (BTC, ETH, SOL, BNB, XRP)│ │
 │ ├─────────────────────────────────────────────────────────┤ │
 │ │ Ingestion 2: Alternative.me Crypto Fear & Greed Index   │ │
 │ ├─────────────────────────────────────────────────────────┤ │
 │ │ Quantitative Core:                                      │ │
 │ │ • 7-Day Moving Average (MA7) calculation               │ │
 │ │ • Strategic DCA key price zones ($72k to $55k)          │ │
 │ │ • Target deviation math vs $61,200 baseline             │ │
 │ │ • Dynamic ASCII sentiment bar visualization             │ │
 │ └────────────────────────────┬────────────────────────────┘ │
 └──────────────────────────────┼──────────────────────────────┘
                                │ HTTPS POST (Markdown format)
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                    Telegram Bot API                         │
 │               Real-Time Investor Notification               │
 └─────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Capabilities

1. **Zero-Cost Serverless Infrastructure**: Runs completely within GitHub Actions free-tier runners, eliminating cloud server hosting costs.
2. **Multi-Asset Real-Time Pricing**: Queries CoinGecko API for real-time USD valuation and 24-hour percentage deltas across top cryptographic assets:
   - Bitcoin (`BTC`)
   - Ethereum (`ETH`)
   - Solana (`SOL`)
   - Binance Coin (`BNB`)
   - Ripple (`XRP`)
3. **Quantitative Trend Analysis**:
   - Computes 7-day Simple Moving Average (SMA/MA7) to identify micro-trend direction (Bullish vs Bearish regime).
4. **Bear Market Accumulation Matrix**:
   - Analyzes distance from target accumulation zones (`$72,000`, `$70,000`, `$65,000`, `$60,000`, `$58,000`, `$55,000`).
   - Advises percentage-based capital allocation (e.g. 5% initial entry to 20% max accumulation).
   - Tracks target price delta relative to `$61,200` median target.
5. **Sentiment Index Scoring**:
   - Integrates Alternative.me Fear & Greed Index API (0–100 scale).
   - Generates dynamic visual sentiment bars (`██████░░░░`) with algorithmic recommendations based on extreme fear/greed boundaries.
6. **Secure Secret Management**:
   - Telegram credentials and bot tokens are isolated within GitHub Encrypted Secrets, preventing exposure in public repositories.

---

## 📊 Sample Telegram Intelligence Dispatch

```markdown
🤖  CryptoSentinel Ultra
Reporte Diario 2026

📊  MERCADO EN TIEMPO REAL

⚡  Bitcoin
   $64,850.00  (+1.85%)
   MA7: Alcista 🟢

🔹  Ethereum: $3,420.50 (+2.10%)
🔹  Solana: $148.20 (+4.30%)
🔹  BNB: $580.00 (+0.95%)
🔹  XRP: $0.5840 (+1.20%)

🎯  ESTRATEGIA BEARMARKET 2026
  Objetivo precio medio: $61,200
  BTC vs objetivo: +5.9%

  Zonas clave - 75% capital:
  ⏳ $70,000 - 10% capital (+7.9%)
  🎯 $65,000 - 10% capital (+0.2%)
  ⏳ $60,000 - 20% capital (-7.5%)

  DCA Semanal - 25% capital:
  1% semanal × 25 semanas

🎭  SENTIMIENTO DEL MERCADO
  ████░░░░░░
  38/100 - Miedo 🟡

🧠  ANÁLISIS SENTINEL
  Miedo en el mercado con BTC en zona estratégica. Evalúe ejecutar entradas según su plan.
```

---

## 🚀 Local Setup & Testing

### Prerequisites
- Python 3.10 or higher
- Telegram Bot Token ([BotFather](https://t.me/botfather))
- Telegram Chat ID

### Installation
```bash
# Clone repository
git clone https://github.com/AlexEspinoza2005/CryptoSentinel-Serverless.git
cd CryptoSentinel-Serverless

# Install dependencies
pip install requests
```

### Environment Variables
Set the required Telegram secrets in your terminal or `.env` file:

```bash
# Linux/macOS
export TELEGRAM_TOKEN="your_telegram_bot_token"
export TELEGRAM_CHAT_ID="your_telegram_chat_id"

# Windows (PowerShell)
$env:TELEGRAM_TOKEN="your_telegram_bot_token"
$env:TELEGRAM_CHAT_ID="your_telegram_chat_id"
```

### Run Locally
```bash
python main.py
```

---

## ⚙️ CI/CD Serverless Workflow

The engine is orchestrated via `.github/workflows/bot.yml`:

```yaml
name: CryptoSentinel-Serverless
on:
  schedule:
    - cron: '0 13 * * *'  # Runs daily at 13:00 UTC
  workflow_dispatch:      # Allows manual one-click trigger
jobs:
  monitor_market:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install Dependencies
        run: pip install requests
      - name: Run CryptoSentinel Engine
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python main.py
```

---

## 👨‍💻 Author

**Alex Espinoza**  
- GitHub: [@AlexEspinoza2005](https://github.com/AlexEspinoza2005)  
- Email: [alexespinozacangas2018@gmail.com](mailto:alexespinozacangas2018@gmail.com)  
- Education: Software Engineering Student — PUCE (Quito, Ecuador)