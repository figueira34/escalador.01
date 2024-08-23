import streamlit as st
import pandas as pd
import escalador

# Set up the page
st.set_page_config(page_title="Escalador Cartola FC", layout="centered", page_icon="⚽")

# Set custom styles
st.markdown(
    """
    <style>
    body {
        background-color: #333;
        color: #f4f4f4;
    }
    h1 {
        color: #ff6600;
        text-align: center;
    }
    h2 {
        color: #ff6600;
        text-align: center;
        font-size: 1.5em;  /* Smaller subtitle */
    }
    .stButton>button {
        background-color: #ff6600;
        color: #fff;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s ease, transform 0.3s ease;
        width: 150px;  /* Thinner button */
        height: 40px;  /* Set a height for consistency */
        text-align: center;
    }
    .stButton>button:hover {
        background-color: #e65c00;  /* Darker shade of orange on hover */
        color: #fff;  /* Keep the font white on hover */
        transform: scale(1.05);  /* Slightly larger on hover */
    }
    .result-container {
        font-size: 0.9em;  /* Smaller font size */
        color: #ff6600;  /* Orange color for the results */
        text-align: right;
        padding: 5px;  /* Padding for better spacing */
    }
    .result-label {
        color: #fff;  /* White color for the text before ":" */
    }
    .dropdown-container {
        width: 200px;  /* Adjust width as needed */
        margin: 0 auto;  /* Center the dropdown */
    }
    .stSelectbox>div>div>select {
        width: 50%;  /* Ensure the select box takes full width of the container */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle
st.title("Escalador Cartola FC")
st.subheader("Pronto para Mitar?")

# Formations options
formacao = {
    "3-4-3": {"Goleiro": 1, "Zagueiro": 3, "Lateral": 0, "Meia": 4, "Atacante": 3, "Técnico": 1},
    "3-5-2": {"Goleiro": 1, "Zagueiro": 3, "Lateral": 0, "Meia": 5, "Atacante": 2, "Técnico": 1},
    "4-3-3": {"Goleiro": 1, "Zagueiro": 2, "Lateral": 2, "Meia": 3, "Atacante": 3, "Técnico": 1},
    "4-4-2": {"Goleiro": 1, "Zagueiro": 2, "Lateral": 2, "Meia": 4, "Atacante": 2, "Técnico": 1},
    "5-3-2": {"Goleiro": 1, "Zagueiro": 3, "Lateral": 2, "Meia": 3, "Atacante": 2, "Técnico": 1},
    "5-4-1": {"Goleiro": 1, "Zagueiro": 3, "Lateral": 2, "Meia": 4, "Atacante": 1, "Técnico": 1}
}

# Container for dropdown and button
with st.container():
    # Dropdown to select formation
    st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
    selected_formation = st.selectbox(
        "Escolha a formação",
        list(formacao.keys())
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Button to generate the roster
if st.button("Gerar Escalação"):
    # Get the formation details
    formation_details = formacao[selected_formation]

    # Run the code to generate the roster
    starters_df, roster_df = escalador.run_my_code(formation_details)

    if roster_df.empty:
        st.warning("Nenhum jogador disponível para a formação selecionada.")
    else:
        # Display the resulting roster
        st.subheader("Escalação")
        st.dataframe(roster_df)

        # Calculate totals from starters_df
        media_total = starters_df['media_num'].sum()
        preco_total = starters_df['preco_num'].sum()

        # Create columns for button and totals
        col1, col2, col3 = st.columns([1, 2, 1])

        # Display button in the first column
        with col1:
            csv = roster_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar Escalação",
                data=csv,
                file_name='escalacao.csv',
                mime='text/csv',
                use_container_width=False 
            )

        # Display totals in the second column
        with col2:
            st.markdown(
                f'<div class="result-container"><span class="result-label">Média Total:</span> {media_total:.2f}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="result-container"><span class="result-label">Preço Total:</span> R${preco_total:.2f}</div>',
                unsafe_allow_html=True
            )
