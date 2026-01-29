import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. إعدادات الصفحة
st.set_page_config(page_title="CMA Financial Consultant", layout="wide")

# 2. تصميم CSS للجمالية والفوتر
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border-bottom: 4px solid #38bdf8; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; color: white; padding: 10px; background: #0f172a; font-size: 14px; border-top: 2px solid #38bdf8; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Strategic Financial Intelligence Dashboard")

# --- 3. جدول إدخال البيانات التفاعلي ---
st.sidebar.header("📥 Step 1: Input Financial Data")
st.sidebar.write("Enter your numbers below:")

categories = [
    'Sales (Revenue)', 'COGS', 'EBIT (Operating Income)', 'Net Income', 'Interest Expense',
    'Cash & Equivalents', 'Accounts Receivable', 'Inventory', 'Total Current Assets', 
    'Total Assets', 'Intangible Assets', 'Total Current Liabilities', 'Total Debt', 
    'Short Term Debt', 'Total Equity', 'Operating Cash Flow', 'Dividends Paid'
]

initial_df = pd.DataFrame({'Category': categories, 'Value': [0.0] * len(categories)})

edited_df = st.sidebar.data_editor(
    initial_df,
    column_config={"Value": st.column_config.NumberColumn("Amount ($)", min_value=0.0, format="%.0f")},
    hide_index=True,
    use_container_width=True
)

i = dict(zip(edited_df['Category'], edited_df['Value']))
def sd(n, d): return n / d if d != 0 else 0

# --- 4. محرك الحسابات الكامل لـ 20 نسبة ---
res = []
def add_r(name, val, g_range, adv_low, adv_high, adv_ok):
    status = "🟢"; advice = adv_ok
    if val < g_range[0]: status = "🔴"; advice = adv_low
    elif val > g_range[1]: status = "🟡"; advice = adv_high
    res.append({"Ratio Name": name, "Result": round(val, 2), "Status": status, "AI Recommendation": advice})

# 1-3. Liquidity
add_r('1. Current Ratio', sd(i['Total Current Assets'], i['Total Current Liabilities']), [1.2, 2.5], "Critical: Low liquidity.", "High idle cash.", "Healthy.")
add_r('2. Quick Ratio', sd(i['Cash & Equivalents'] + i['Accounts Receivable'], i['Total Current Liabilities']), [1.0, 2.0], "Inventory dependency.", "High liquid assets.", "Strong.")
add_r('3. Cash Ratio', sd(i['Cash & Equivalents'], i['Total Current Liabilities']), [0.2, 0.5], "Low cash reserves.", "Inefficient cash use.", "Optimal.")

# 4-8. Profitability
add_r('4. Gross Margin (%)', sd(i['Sales (Revenue)'] - i['COGS'], i['Sales (Revenue)']) * 100, [30, 60], "High production cost.", "Strong pricing power.", "Efficient.")
add_r('5. Net Margin (%)', sd(i['Net Income'], i['Sales (Revenue)']) * 100, [10, 30], "High overhead costs.", "Highly profitable.", "Stable.")
add_r('6. Operating Margin (%)', sd(i['EBIT (Operating Income)'], i['Sales (Revenue)']) * 100, [15, 25], "High operating costs.", "High efficiency.", "Stable.")
add_r('7. ROA (%)', sd(i['Net Income'], i['Total Assets']) * 100, [5, 15], "Inefficient assets.", "High productivity.", "Standard.")
add_r('8. ROE (%)', sd(i['Net Income'], i['Total Equity']) * 100, [15, 25], "Low equity return.", "High risk leverage.", "Solid.")

# 9-13. Efficiency
add_r('9. Inventory Turnover', sd(i['COGS'], i['Inventory']), [6, 12], "Slow stock cycle.", "Stockout risk.", "Efficient.")
add_r('10. AR Turnover', sd(i['Sales (Revenue)'], i['Accounts Receivable']), [8, 12], "Slow collection.", "Tight credit policy.", "Good cycle.")
add_r('11. Asset Turnover', sd(i['Sales (Revenue)'], i['Total Assets']), [1.0, 2.5], "Low utilization.", "High asset efficiency.", "Optimal.")
add_r('12. DSO (Days)', sd(365, sd(i['Sales (Revenue)'], i['Accounts Receivable'])), [30, 45], "Excellent collection.", "Slow collection.", "Standard.")
add_r('13. Days Inventory', sd(365, sd(i['COGS'], i['Inventory'])), [30, 60], "Fast sales cycle.", "Slow turnover.", "Standard.")

# 14-17. Solvency
add_r('14. Debt to Equity', sd(i['Total Debt'], i['Total Equity']), [0.5, 1.5], "Very safe.", "High risk leverage.", "Balanced.")
add_r('15. Debt to Assets', sd(i['Total Debt'], i['Total Assets']), [0.3, 0.6], "Low debt.", "Highly leveraged.", "Stable.")
add_r('16. Interest Coverage', sd(i['EBIT (Operating Income)'], i['Interest Expense']), [3, 10], "Interest risk.", "Very safe.", "Safe.")
add_r('17. Equity Multiplier', sd(i['Total Assets'], i['Total Equity']), [1.5, 3.0], "Low leverage.", "High risk debt.", "Balanced.")

# 18-20. Cash Flow & Retention (تعديل الـ Retention Rate هنا)
add_r('18. OCF Ratio', sd(i['Operating Cash Flow'], i['Total Current Liabilities']), [1.0, 2.0], "Poor cash coverage.", "Strong cash gen.", "Healthy.")
retention_val = (1 - sd(i['Dividends Paid'], i['Net Income'])) * 100 if i['Net Income'] > 0 else 0
add_r('19. Retention Rate (%)', retention_val, [50, 90], "Low reinvestment.", "Aggressive growth.", "Balanced.")
add_r('20. Asset Coverage', sd((i['Total Assets']-i['Intangible Assets'])-(i['Total Current Liabilities']-i['Short Term Debt']), i['Total Debt']), [1.5, 3.0], "Low protection.", "High protection.", "Safe.")

# --- 5. العرض (Layout) ---
st.subheader("📌 Live Performance Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Ratio", res[0]['Result'])
c2.metric("Net Margin", f"{res[4]['Result']}%")
c3.metric("Debt to Equity", res[13]['Result'])
c4.metric("ROE", f"{res[7]['Result']}%")

# الرسومات البيانية
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("📉 Liquidity Gauge")
    fig_g = go.Figure(go.Indicator(mode="gauge+number", value=res[0]['Result'], gauge={'axis': {'range': [0, 3]}, 'steps': [{'range': [0, 1.2], 'color': "red"}, {'range': [1.2, 3], 'color': "green"}]}))
    fig_g.update_layout(template="plotly_dark", height=250, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_g, use_container_width=True)
with col2:
    st.subheader("💰 Profit Flow")
    fig_b = go.Figure([go.Bar(x=['Gross Profit', 'EBIT', 'Net Income'], y=[i['Sales (Revenue)']-i['COGS'], i['EBIT (Operating Income)'], i['Net Income']], marker_color='#38bdf8')])
    fig_b.update_layout(template="plotly_dark", height=250, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_b, use_container_width=True)
with col3:
    st.subheader("⚖️ Capital Structure")
    fig_p = go.Figure(data=[go.Pie(labels=['Debt', 'Equity'], values=[i['Total Debt'], i['Total Equity']], hole=.5, marker_colors=['#ef4444', '#38bdf8'])])
    fig_p.update_layout(template="plotly_dark", height=250, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_p, use_container_width=True)

# الجدول الشامل
st.markdown("---")
st.subheader("📊 Detailed Financial Analysis (Full 20 Ratios)")
st.dataframe(pd.DataFrame(res), use_container_width=True, hide_index=True)

# الفوتر الاحترافي
st.markdown(f"""
    <div class="footer">
        Developed by <b>Maher Al-Momani</b> | Accountant & Data Analyst | CMA Candidate © 2026
    </div>
    """, unsafe_allow_html=True)