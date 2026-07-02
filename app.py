import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 網頁基本設定
st.set_page_config(page_title="宸品股份 - 溫濕度雲端戰情室", page_icon="🌡️", layout="wide")

# 1. 載入 6 月份溫濕度數據
data = {
    '日期': [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 15, 16, 17, 18, 22, 24, 25, 26, 29, 30],
    '上午溫度': [25.0, 24.6, 24.2, None, 25.0, 24.5, 24.3, 24.5, 24.3, 23.5, 24.8, 25.2, 22.7, 26.8, 25.5, 25.0, 25.6, 27.4, 26.2, 24.4],
    '上午濕度': [42, 43, 46, None, 44, 50, 49, 50, 48, 44, 50, 48, None, 52, 49, 50, 45, 46, 47, 45],
    '下午溫度': [25.3, 24.7, None, 23.8, 25.4, 24.9, 24.5, 24.8, 24.5, 24.8, 23.7, 25.0, 23.0, None, 26.0, 25.7, None, None, 26.7, 24.9],
    '下午濕度': [46, 45, None, 44, 47, 53, 50, 52, 44, 50, 47, 53, 49, None, 49, 53, None, None, 41, 48]
}
df = pd.DataFrame(data)

# 計算分析摘要
max_temp = max(df['上午溫度'].max(), df['下午溫度'].max())
max_humid = max(df['上午濕度'].max(), df['下午濕度'].max())

# 網頁標題與橫幅
st.title("🏢 宸品股份有限公司 — 雲端環境監控系統")
st.subheader("📍 1樓成品區 溫濕度數據儀表板 (115年06月)")

st.markdown("---")

# 2. 頂部區塊：即時 KPI 燈號與數據指標
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="🌡️ 本月最高溫度", value=f"{max_temp} °C")
with col2:
    status_t = "🟢 全數合規" if max_temp <= 30 else "🔴 溫度超標！"
    st.metric(label="📌 溫度管制狀態 (標準 <= 30°C)", value=status_t)
with col3:
    st.metric(label="💧 本月最高相對濕度", value=f"{max_humid} %")
with col4:
    status_h = "🟢 全數合規" if max_humid <= 70 else "🔴 濕度超標！"
    st.metric(label="📌 濕度管制狀態 (標準 <= 70%)", value=status_h)

st.markdown("---")

# 3. 中部區塊：左邊放數據圖表，右邊放原始資料表
left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown("### 📊 溫濕度趨勢分析圖")
    
    # 繪製 Matplotlib 圖表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DejaVu Sans'] # 支援中文
    plt.rcParams['axes.unicode_minus'] = False

    # 溫度折線
    ax1.plot(df['日期'], df['上午溫度'], marker='o', label='上午溫度', color='#ff7f0e')
    ax1.plot(df['日期'], df['下午溫度'], marker='s', label='下午溫度', color='#d62728')
    ax1.axhline(y=30, color='r', linestyle='--', label='溫度上限 (30°C)')
    ax1.set_ylabel('溫度 (°C)')
    ax1.legend()
    ax1.grid(True)

    # 濕度折線
    ax2.plot(df['日期'], df['上午濕度'], marker='o', label='上午濕度', color='#1f77b4')
    ax2.plot(df['日期'], df['下午濕度'], marker='s', label='下午濕度', color='#17becf')
    ax2.axhline(y=70, color='r', linestyle='--', label='濕度上限 (70%)')
    ax2.set_ylabel('濕度 (%)')
    ax2.set_xlabel('日期 (號)')
    ax2.legend()
    ax2.grid(True)
    
    st.pyplot(fig)

with right_col:
    st.markdown("### 📋 歷史數據明細")
    # 美化表格並填補缺失值顯示
    st.dataframe(df.fillna("-"), height=400, use_container_width=True)

# 4. 底部區塊：系統資訊
st.markdown("---")
st.caption("⚙️ 儀器編號：C-032 | 文件編號：P-4-04-01 第二版 | 保存期限：5年")