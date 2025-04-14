import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables de estado: se conservan entre ejecuciones
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

# Gráfico inicial
chart = st.line_chart([0.5])

# Función que simula el lanzamiento de monedas
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

# Slider y botón
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

# Al hacer clic en el botón
if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    
    # Aumentar número de experimento
    st.session_state['experiment_no'] += 1

    # Ejecutar lanzamiento
    mean = toss_coin(number_of_trials)

    # Agregar resultado a la tabla
    nuevo_resultado = pd.DataFrame([[st.session_state['experiment_no'], number_of_trials, mean]],
                                   columns=['no', 'iteraciones', 'media'])

    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], nuevo_resultado],
        axis=0
    ).reset_index(drop=True)

# Mostrar la tabla
st.write(st.session_state['df_experiment_results'])