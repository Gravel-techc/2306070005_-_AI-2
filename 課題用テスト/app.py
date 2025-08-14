import streamlit as st
from converter import get_exchange_rate, get_past_rates
import matplotlib.pyplot as plt
from matplotlib import rcParams

# --------------------------
# 日本語フォント設定（Windowsの場合）
rcParams['font.family'] = 'Yu Gothic'  # または 'Meiryo'
# --------------------------

# 通貨コードと日本語名称の対応
currency_dict = {
    "USD": "米ドル (USD)",
    "EUR": "ユーロ (EUR)",
    "JPY": "日本円 (JPY)",
    "GBP": "英ポンド (GBP)",
    "AUD": "豪ドル (AUD)",
    "CAD": "カナダドル (CAD)",
    "CHF": "スイスフラン (CHF)",
    "CNY": "中国元 (CNY)",
    "HKD": "香港ドル (HKD)",
    "SGD": "シンガポールドル (SGD)",
    "KRW": "韓国ウォン (KRW)",
    "NZD": "ニュージーランドドル (NZD)",
    "THB": "タイバーツ (THB)",
    "INR": "インドルピー (INR)",
    "SEK": "スウェーデンクローナ (SEK)",
    "NOK": "ノルウェークローネ (NOK)",
    "DKK": "デンマーククローネ (DKK)",
    "ZAR": "南アフリカランド (ZAR)",
    "TWD": "台湾ドル (TWD)",
    "IDR": "インドネシアルピア (IDR)"
}

st.title("為替レート換算アプリ 💱")

# selectbox 用リスト（表示名）
currency_list = list(currency_dict.values())
name_to_code = {v: k for k, v in currency_dict.items()}

from_display = st.selectbox("変換元通貨", currency_list, index=currency_list.index("日本円 (JPY)"))
to_display   = st.selectbox("変換先通貨", currency_list, index=currency_list.index("米ドル (USD)"))

from_currency = name_to_code[from_display]
to_currency   = name_to_code[to_display]

amount = st.number_input("金額", min_value=0.0, step=1.0, value=100.0)

if st.button("換算する"):
    rate = get_exchange_rate(from_currency, to_currency)
    if isinstance(rate, (int, float)):
        converted = amount * rate
        st.success(f"{amount} {from_display} = {converted:.2f} {to_display}")
        st.caption(f"レート: 1 {from_display} = {rate:.6f} {to_display}")
        
        # 過去7日間のレート推移グラフ
        past_rates = get_past_rates(from_currency, to_currency, days=7)
        if past_rates:
            fig, ax = plt.subplots(figsize=(8, 4))
            dates = list(past_rates.keys())
            values = list(past_rates.values())
            ax.plot(dates, values, marker='o')
            ax.set_title(f"{from_display} → {to_display} 過去7日間レート")
            ax.set_xlabel("日付")
            ax.set_ylabel("為替レート")
            ax.grid(True)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("過去7日間のレート取得に失敗しました。")
    else:
        st.error("為替レートの取得に失敗しました。時間をおいて再試行してください。")
