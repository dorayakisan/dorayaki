import streamlit as st

st.set_page_config(page_title="FH計算機", page_icon="📐", layout="centered")

# --------------------------------------------------
# 入力欄をクリックした際、最初だけ全選択にするJavaScript
# --------------------------------------------------
st.components.v1.html("""
<script>
    // 画面上の全 number_input 要素を監視してフォーカス時に全選択させる
    const applyAutoSelect = () => {
        const inputs = window.parent.document.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            if (!input.dataset.autoselectApplied) {
                input.dataset.autoselectApplied = "true";
                input.addEventListener('focus', function() {
                    // 1回目のフォーカス時にテキストを全選択
                    this.select();
                });
            }
        });
    };
    
    // 初回実行およびStreamlitの再描画に合わせて定期監視
    applyAutoSelect();
    setInterval(applyAutoSelect, 500);
</script>
""", height=0)

st.title("📐 計画標高（FH）計算ツール")
st.caption("中心線標高（CL高）、片勾配、CLからの距離を入力するとFHを算出します。")

st.write("---")

# 1. 中心線標高 (CL高)
cl_height = st.number_input(
    "中心線標高: CL高 (m)",
    value=50.000,
    step=0.001,
    format="%.3f"
)


col1, col2 = st.columns(2)

with col1:
    # 2. 片勾配 (%)
    cross_slope = st.number_input(
        "片勾配 (%)",
        value=-2.00,
        step=0.10,
        format="%.2f"
    )

with col2:
    # 3. CLからの距離 (m)
    distance = st.number_input(
        "CLからの距離 (m)",
        min_value=0.000,
        value=3.500,
        step=0.100,
        format="%.3f"
    )

# --------------------------------------------------
# 計算処理
# --------------------------------------------------
delta_height = distance * (cross_slope / 100.0)
fh_height = cl_height + delta_height

st.write("---")

# --------------------------------------------------
# 計算結果表示
# --------------------------------------------------
st.metric(
    label="計画標高 (FH)",
    value=f"{fh_height:.3f} m",
    delta=f"{delta_height:+.3f} m"
)

# 計算式の確認
with st.expander("計算式の詳細を確認"):
    st.latex(r"FH = CL + \left( \text{距離} \times \frac{\text{片勾配(\%)}}{100} \right)")
    st.write(
        f"$$FH = {cl_height:.3f} + \\left( {distance:.3f} \\times \\frac{{{cross_slope:.2f}}}{{100}} \\right) = {fh_height:.3f}\\text{{ m}}$$"
    )