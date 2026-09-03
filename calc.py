import streamlit as st
from decimal import Decimal, ROUND_HALF_UP

st.set_page_config(
    page_title="FH計算機",
    page_icon="📐",
    layout="centered"
)

# --------------------------------------------------
# 入力欄をクリックした際、最初だけ全選択にするJavaScript
# --------------------------------------------------
st.components.v1.html(
    """
    <script>
        const applyAutoSelect = () => {
            const inputs = window.parent.document.querySelectorAll(
                'input[type="number"]'
            );

            inputs.forEach(input => {
                if (!input.dataset.autoselectApplied) {
                    input.dataset.autoselectApplied = "true";

                    input.addEventListener('focus', function() {
                        this.select();
                    });
                }
            });
        };

        applyAutoSelect();
        setInterval(applyAutoSelect, 500);
    </script>
    """,
    height=0
)


# --------------------------------------------------
# タイトル
# --------------------------------------------------
st.title("📐 計画標高（FH）計算ツール")

st.caption(
    "中心線標高（CL高）、片勾配、CLからの距離を入力するとFHを算出します。"
)

st.write("---")


# --------------------------------------------------
# FHの表示桁数を選択
# --------------------------------------------------
decimal_places = st.segmented_control(
    "FHの表示桁数",
    options=[2, 3],
    format_func=lambda x: f"小数点以下{x}桁",
    default=3
)


# --------------------------------------------------
# 1. 中心線標高（CL高）
# --------------------------------------------------
cl_height = st.number_input(
    "中心線標高: CL高 (m)",
    value=50.000,
    step=0.001,
    format="%.3f"
)


# --------------------------------------------------
# 2. 片勾配
# 3. CLからの距離
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    cross_slope = st.number_input(
        "片勾配 (%)",
        value=-2.00,
        step=0.10,
        format="%.2f"
    )

with col2:
    distance = st.number_input(
        "CLからの距離 (m)",
        min_value=0.000,
        value=3.500,
        step=0.100,
        format="%.3f"
    )

st.caption("※ Tabキーで入力欄を移動できます。入力後、Enterキーで計算結果を更新できます。")

# --------------------------------------------------
# 計算処理
# --------------------------------------------------
cl_dec = Decimal(f"{cl_height:.3f}")
slope_dec = Decimal(f"{cross_slope:.2f}")
dist_dec = Decimal(f"{distance:.3f}")

# 高低差 = 距離 × (勾配 / 100)
delta_height = dist_dec * (
    slope_dec / Decimal("100")
)

# FH = CL + 高低差
fh_height = cl_dec + delta_height


# --------------------------------------------------
# 選択した桁数に応じて四捨五入
# --------------------------------------------------
if decimal_places == 2:
    quantizer = Decimal("0.01")
else:
    quantizer = Decimal("0.001")

fh_height_rounded = fh_height.quantize(
    quantizer,
    rounding=ROUND_HALF_UP
)

delta_height_rounded = delta_height.quantize(
    quantizer,
    rounding=ROUND_HALF_UP
)


# --------------------------------------------------
# 表示用文字列
# --------------------------------------------------
fh_display = f"{fh_height_rounded:.{decimal_places}f}"

delta_display = (
    f"{delta_height_rounded:+.{decimal_places}f}"
)


st.write("---")


# --------------------------------------------------
# 計算結果 + FHコピーボタン
# --------------------------------------------------
result_col, copy_col = st.columns([1.4, 4], gap=None)

with result_col:
    st.metric(
        label="計画標高 (FH)",
        value=f"{fh_display} m",
        delta=f"{delta_display} m"
    )


with copy_col:
    st.components.v1.html(
        f"""
        <div style="
            display: flex;
            align-items: center;
            padding-top: 34px;
        ">
            <button
                id="copyBtn"
                style="
                    padding: 8px 14px;
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 8px;
                    background: white;
                    color: rgb(49, 51, 63);
                    cursor: pointer;
                    font-family: 'Source Sans Pro', -apple-system,
                                 BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    font-size: 14px;
                    font-weight: 400;
                    white-space: nowrap;
                "
            >
                📋 コピー
            </button>
        </div>

        <script>
            const button = document.getElementById("copyBtn");
            const copyValue = "{fh_display}";

            button.addEventListener("click", function() {{
                const textarea = document.createElement("textarea");

                textarea.value = copyValue;
                textarea.style.position = "fixed";
                textarea.style.left = "-9999px";

                document.body.appendChild(textarea);

                textarea.focus();
                textarea.select();

                try {{
                    const success = navigator.clipboard.writeText(copyValue);

                    if (success) {{
                        button.textContent = "✓ コピー済み";
                    }} else {{
                        button.textContent = "コピー失敗";
                    }}

                }} catch (err) {{
                    button.textContent = "コピー失敗";
                }}

                document.body.removeChild(textarea);

                setTimeout(function() {{
                    button.textContent = "📋 コピー";
                }}, 1500);
            }});
        </script>
        """,
        height=100
    )


# --------------------------------------------------
# 入力内容の確認表示
# --------------------------------------------------
st.caption(
    f"CL高 {cl_height:.3f} m ｜ "
    f"片勾配 {cross_slope:+.2f} % ｜ "
    f"距離 {distance:.3f} m ｜ "
    f"{decimal_places}桁表示"
)


# --------------------------------------------------
# 計算式の詳細
# --------------------------------------------------
with st.expander(
    "計算式の詳細を確認"
):

    st.latex(
        r"FH = CL + \left("
        r"\text{距離} \times "
        r"\frac{\text{片勾配(\%)}}{100}"
        r"\right)"
    )


    st.write(
        f"$$FH = {cl_height:.3f} + "
        f"\\left("
        f"{distance:.3f} "
        f"\\times "
        f"\\frac{{{cross_slope:.2f}}}{{100}}"
        f"\\right)"
        f"= {fh_height:.6f}"
        f"\\text{{ m}}$$"
    )
