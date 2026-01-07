import streamlit as st
import random
import time


if 'bal' not in st.session_state:
    st.session_state.bal = 500

if 'result' not in st.session_state:
    st.session_state.result = None

if 'history' not in st.session_state:
    st.session_state.history = []  

# ---------------- SPIN LOGIC ----------------
def spin_result():
    r = random.random() * 100  # 0–100%

    if r < 45:  # 0x probability
        return '0x'
    elif r < 60:  # 45 + 15 → 1x–2x
        return f"{random.randint(1, 2)}x"
    elif r < 90:  # 60 + 30 → 3x–5x
        return f"{random.randint(3, 5)}x"
    elif r < 115:  # 90 + 25 → 6x–10x
        return f"{random.randint(6, 10)}x"
    elif r < 135:  # 115 + 20 → 11x–15x
        return f"{random.randint(11, 15)}x"
    else:  # remaining 10% → 16x–20x
        return f"{random.randint(16, 20)}x"

# ---------------- UI ----------------
st.markdown("<h1 style='text-align:center; color:#00ffff;'>🎰 THE AWAL CASINO 🤑</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center; color:#ff00ff;'>📈 Balance: {st.session_state.bal}</h3>", unsafe_allow_html=True)
#------------------------------------------


bet = st.number_input(
    '💸 Place your bet',
    min_value=1,
    max_value=st.session_state.bal,
    step=1
)


if st.button('🎰 SPIN'):

    if bet > st.session_state.bal:
        st.error("❌ Not enough balance")

    else:
        
        st.session_state.bal -= bet

        # loading animation
        progress = st.progress(0)
        status = st.empty()
        for i in range(100):
            progress.progress(i + 1)
            status.text(f"Spinning {i+1}%")
            time.sleep(0.04)
        progress.empty()
        status.empty()
        #-----------------------
        
        result = spin_result()
        st.session_state.result = result
        multiplier = int(result.replace('x', ''))

        
        if multiplier == 0:
            outcome = f"-{bet}"
            st.error("💥 You lost the bet!")
        else:
            win = bet * multiplier
            st.session_state.bal += win
            outcome = f"+{win}"
            st.success(f"🏆 You won {win}!")

        st.session_state.history.append((bet, result, outcome))

# ---------------- ANIMATED RESULT ----------------
if st.session_state.result:
    m = int(st.session_state.result.replace('x', ''))
    color = "red" if m == 0 else "lime"

    st.markdown(
        f"""
        <style>
        .spin {{
            animation: zoom 0.6s ease-in-out;
            font-size:90px;
            font-weight:900;
            text-align:center;
            color:{color};
            margin-top:20px;
        }}

        @keyframes zoom {{
            0% {{ transform: scale(0.2); opacity: 0; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        </style>

        <div class="spin">{st.session_state.result}</div>
        """,
        unsafe_allow_html=True
    )
#---------------------------------------------------------

st.text('🪫 Recharge')
amount = st.text_input('💰 Amount')

if st.button('🪫 Recharge'):
    if amount.isdigit():
        st.session_state.bal += int(amount)
        st.success('Balance added!')
    else:
        st.error('Invalid amount')

# ---------------- HISTORY PANEL ----------------
st.sidebar.markdown("<h2 style='color:#ffff00;'>📜 Spin History</h2>", unsafe_allow_html=True)

if st.session_state.history:
    for i, (bet_amount, result, outcome) in enumerate(reversed(st.session_state.history[-10:]), 1):  # last 10 spins
        color = "red" if result == '0x' else "lime"
        st.sidebar.markdown(f"<p style='color:{color};'>#{i} Bet: {bet_amount}, Result: {result}, Outcome: {outcome}</p>", unsafe_allow_html=True)
#------------------------------------------------

st.button('refresh')
if st.button('withdraw:'):
    st.text('hahaha you got scamed')