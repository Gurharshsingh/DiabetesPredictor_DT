import streamlit as st
import numpy as np
import joblib


def load_model():
    model = joblib.load('diabetes.pkl')  
    return model

model = load_model()

def predict_diabetes(answers):
    arr = np.array([answers])
    return model.predict(arr)[0]

st.set_page_config(
    page_title="DIABETES PREDICTOR",
    page_icon="🩺",
    layout="wide"
)


st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, var(--background-color), var(--secondary-background-color) 72%);
}
.question-card {
    background-color: var(--secondary-background-color);
    border-radius: 1.2rem;
    box-shadow: 0 4px 15px 0 rgba(39, 140, 245, 0.8);
    margin-bottom: 1.8rem;
    padding: 0.5rem;
    color: var(--text-color);
}
.section-title {
    text-align: center;
    color: var(--primary-color);
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    margin-bottom: 1.1rem;
    font-family: 'Segoe UI Semibold', 'Arial', sans-serif;
    border-bottom: 2px solid #38d6ae22;
    padding-bottom: 0.4em;
}
.result-alert {
    border-radius: 0.8em;
    font-weight: 700;
    text-align: center;
    margin: 1.1em auto 1em auto;
    padding: 1.1em 1.5em;
    box-shadow: 0 2px 16px 0 rgba(40, 60, 105, 0.13);
}
.result-positive {background:#e74c3c!important;color:#fff;}
.result-negative {background:#239B56!important;color:#fff;}
.answers-table th, .answers-table td {
    padding: 0.59em 1.1em;
    font-size: 1.04em;
    color: var(--text-color);
    background: var(--secondary-background-color);
    border-bottom: 1px solid #38d6ae21;
    text-align: center;
}
.answers-table th {
    font-weight: 800;
    background: var(--background-color)!important;
}
            
.answers-table {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<h1 style="text-align:center;color: var(--primary-color); font-weight: 900; font-size: 2.4rem; letter-spacing:.04em;">🩺 DIABETES SCREENING QUESTIONNAIRE</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<div style="text-align:center; font-size:1.11em; color: var(--text-color); margin-bottom: 2em;">Professional Medical Risk Assessment</div>',
    unsafe_allow_html=True
)

cols = st.columns([1.1, 3.4, 1.1])

# --- Left Medical Image ---
with cols[0]:
    st.image(
        "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=500&q=80",
        use_container_width=True
    )
    st.markdown('<div style="height:32vh;"></div>', unsafe_allow_html=True)


with cols[1]:
    # Personal Details

    st.markdown('<div class="question-card"><div class="section-title">PERSONAL DETAILS</div>', unsafe_allow_html=True)
    gender = st.radio("**GENDER**", options=["Female", "Male"], horizontal=True)
    age = st.number_input("**AGE**", min_value=0, max_value=120, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

    # Health Status
    st.markdown('<div class="question-card"><div class="section-title">HEALTH STATUS</div>', unsafe_allow_html=True)
    hypertension = st.radio("**HYPERTENSION**", options=["No", "Yes"], horizontal=True)
    smoke_options = [
        "Not known", "Current", "Yes", "Former", "Never", "Not current"
    ]
    smoke_mapping = {
        "Not known": 0, "Current": 1, "Yes": 2, "Former": 3, "Never": 4, "Not current": 5
    }
    smoking_history = st.radio("**SMOKING HISTORY**", options=smoke_options, horizontal=True)
    heart_disease = st.radio("**HEART DISEASE**", options=["No", "Yes"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Biological Metrics
   
    st.markdown('<div class="question-card"><div class="section-title">BIOLOGICAL METRICS</div>', unsafe_allow_html=True)
    bmi = st.number_input("**BMI**", min_value=0.0, max_value=60.0, step=0.1, format="%.2f")
    hba1c = st.number_input("**HbA1c LEVEL**", min_value=0.0, max_value=20.0, step=0.1, format="%.2f")
    blood_glucose = st.number_input("**BLOOD GLUCOSE LEVEL**", min_value=0.0, max_value=600.0, step=0.1, format="%.1f")
    st.markdown('</div>', unsafe_allow_html=True)

    answers = [
        0 if gender == "Female" else 1,
        age,
        1 if hypertension == "Yes" else 0,
        smoke_mapping[smoking_history],
        1 if heart_disease == "Yes" else 0,
        bmi,
        hba1c,
        blood_glucose,
    ]

    submit = st.button("🔎 SUBMIT FOR ANALYSIS", use_container_width=True)

    if submit:
        prediction = predict_diabetes(answers)
        result = "POSITIVE (Consult a Doctor)" if prediction == 1 else "NEGATIVE (No Indication Detected)"
        result_class = "result-positive" if prediction == 1 else "result-negative"
        st.markdown(f'<div class="section-title">RESULT</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="result-alert {result_class}">Result: {result}</div>',
            unsafe_allow_html=True
        )

        qa = [
            ["Gender", "Female" if answers[0]==0 else "Male"],
            ["Age", int(answers[1])],
            ["Hypertension", "Yes" if answers[2]==1 else "No"],
            ["Smoking History", smoke_options[answers[3]]],
            ["Heart Disease", "Yes" if answers[4]==1 else "No"],
            ["BMI", f"{answers[5]:.2f}"],
            ["HbA1c Level", f"{answers[6]:.2f}"],
            ["Blood Glucose Level", f"{answers[7]:.1f}"],
        ]

        st.markdown('<div class="section-title">SUMMARY OF RESPONSES</div>', unsafe_allow_html=True)
        st.markdown('<table class="answers-table"><tr><th>QUESTION</th><th>ANSWER</th></tr>' +
            ''.join(f"<tr><td>{q}</td><td>{a}</td></tr>" for q,a in qa) +
            '</table>',
            unsafe_allow_html=True
        )

        

# --- Right Medical Image ---
with cols[2]:
    st.image(
        "https://images.unsplash.com/photo-1511174511562-5f7f18b874f8?auto=format&fit=crop&w=500&q=80",
        use_container_width=True
    )
    st.markdown('<div style="height:32vh;"></div>', unsafe_allow_html=True)

st.markdown(
    "<center><small>This dashboard is for demonstration purposes only.<br>For medical advice, consult a qualified healthcare professional.</small></center>",
    unsafe_allow_html=True
)

