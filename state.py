import streamlit as st
import random
import time


if 'bal' not in st.session_state:
    st.session_state.bal = 500

if 'result' not in st.session_state:
    st.session_state.result = None

if 'history' not in st.session_state:
    st.session_state.history = []  


def spin_result():
    r = random.random() * 100  # 0–100%

    if r < 75:  # 0x → lose most of the time (75%)
        return '0x'
    elif r < 90:  # 1x–2x → small win (15%)
        return f"{random.randint(1, 2)}x"
    elif r < 97:  # 3x–5x → medium win (7%)
        return f"{random.randint(3, 5)}x"
    elif r < 99:  # 6x–10x → rare win (2%)
        return f"{random.randint(6, 10)}x"
    else:  # 16x–20x → jackpot (1%)
        return f"{random.randint(16, 20)}x"


# ---------------- UI ----------------
st.markdown("<h1 style='text-align:center; color:#00ffff;'>🎰 THE AWAL CASINO 🤑</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center; color:#ff00ff;'>📈 Balance: {st.session_state.bal} tk</h3>", unsafe_allow_html=True)
#------------------------------------------


# make bet value persistent and keep max_value constant
if 'bet' not in st.session_state:
    st.session_state.bet = 1  # default value

bet = st.number_input(
    '💸 Place your bet',
    min_value=1,
    max_value=5000,  # or any large number you want
    step=1,
    key='bet'
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
            st.success(f"🏆 You won {win} tk!")

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
st.button('refresh')
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


if st.button('withdraw:'):
    st.text('hahaha you got scamed')



