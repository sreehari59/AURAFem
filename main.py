import streamlit as st

st.set_page_config(page_title="AURAFem", page_icon="🤖")
st.markdown("""
    <div style='text-align: center;'>
        <h1> AURAFem </h1>
    </div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }
    .stButton button {
        background-color: #4CAF50; /* Button color */
        color: white;
        padding: 80px 60px; /* Size of the button */
        font-size: 20px; /* Font size */
        border-radius: 10px; /* Rounded corners */
        border: none; /* Remove border */
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #45a049; /* Hover effect */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create buttons inside a container
col1, col2, col3 = st.columns(3)
with col1:
    for i in range(12):
        st.write("\n")
    if st.button("Patient"):
        st.switch_page(page="pages/patient.py")
with col2:
    for i in range(12):
        st.write("\n")
    if st.button("Doctor"):
        st.switch_page(page="pages/doctor.py")
    
with col3:
    for i in range(12):
        st.write("\n")
    if st.button("Insurance Agent"):
        st.switch_page(page="pages/insurance.py")