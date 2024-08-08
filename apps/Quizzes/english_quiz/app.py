import json
import random
import dash
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import time
import plotly.express as px
from gtts import gTTS
from sentence_transformers import SentenceTransformer, util
from openai import OpenAI
from difflib import ndiff
import os
import environ
from sentence_transformers import SentenceTransformer
from django_plotly_dash import DjangoDash
from django.conf import settings
from apps.Quizzes.models import StructuredEnglishGrammarCourse, Translation
from apps.Quizzes.english_quiz.send_report import generate_pdf_from_template, send_email
import plotly.io as pio
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from dotenv import load_dotenv

# Inicializa la carga de entorno
env = environ.Env()
environ.Env.read_env()  # Esto permite cargar las variables de entorno directamente

# Obtén la clave de API de OpenAI desde las variables de entorno
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Inicializar cliente de OpenAI y modelo
client = OpenAI(api_key=OPENAI_API_KEY)
model = SentenceTransformer('all-MiniLM-L6-v2')



# Resto del código...

# Si necesitas cargar el archivo .env solo para desarrollo local, puedes hacerlo condicionalmente:
if os.getenv('RAILWAY_ENV') is None:
    # Cargar el archivo .env solo si no estás en Railway
    load_dotenv(os.path.join(os.path.dirname(__file__), '../../core/.env'))
    # Reasignar la clave de API en caso de que se haya cargado de .env
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', OPENAI_API_KEY)
    client.api_key = OPENAI_API_KEY

# Definir las rutas de los archivos JSON para las alternativas
quiz_paths_alternatives = {
    'A1': 'apps/Quizzes/english_quiz/questions/alternativas/A1_alternatives.json',
    'A2': 'apps/Quizzes/english_quiz/questions/alternativas/A2_alternatives.json',
    'B1': 'apps/Quizzes/english_quiz/questions/alternativas/B1_alternatives.json',
    'B2': 'apps/Quizzes/english_quiz/questions/alternativas/B2_alternatives.json',
    'C1': 'apps/Quizzes/english_quiz/questions/alternativas/C1_alternatives.json',
    'C2': 'apps/Quizzes/english_quiz/questions/alternativas/C2_alternatives.json'
}

# Definir las rutas de los archivos JSON para las traducciones
quiz_paths_translation = {
    'A1': 'apps/Quizzes/english_quiz/questions/traducciones/A1_translate.json',
    'A2': 'apps/Quizzes/english_quiz/questions/traducciones/A2_translate.json',
    'B1': 'apps/Quizzes/english_quiz/questions/traducciones/B1_translate.json',
    'B2': 'apps/Quizzes/english_quiz/questions/traducciones/B2_translate.json',
    'C1': 'apps/Quizzes/english_quiz/questions/traducciones/C1_translate.json',
    'C2': 'apps/Quizzes/english_quiz/questions/traducciones/C2_translate.json'
}

index_alternatives = 0
index_translation = 0
start_time_alternatives = time.time()
start_time_translation = time.time()

# Crear la primera pregunta y opciones para las alternativas
question_alternatives = None
opts_alternatives = None
level_alternatives = None
radio_items = None

final_dict_alternatives = None
final_dict_translation = None

# Inicializar la aplicación Dash
app = DjangoDash('EnglishQuizApp', external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"], suppress_callback_exceptions=True)

# Función para leer el archivo JSON y seleccionar preguntas aleatorias
def select_questions(file_path, key_type, num_questions=2):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Seleccionar índices aleatorios de las preguntas
    indices = random.sample(range(len(data[key_type])), num_questions)
    
    # Construir el diccionario con las preguntas seleccionadas
    selected_questions = {
        key_type: [data[key_type][i] for i in indices],
        'options': [data['options'][i] for i in indices],
        'ans': [data['ans'][i] for i in indices],
        'explanation': [data['explanation'][i] for i in indices],
        'valores': [data['valores'][i] for i in indices]
    }
    
    return selected_questions

# Función para seleccionar preguntas de traducción aleatorias
def select_translation_questions(file_path, num_questions=2):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Seleccionar índices aleatorios de las preguntas
    indices = random.sample(range(len(data['Spanish'])), num_questions)
    
    selected_questions = {
        'Spanish': [data['Spanish'][str(i+1)].rstrip('.') for i in indices],
        'English': [data['English'][str(i+1)].rstrip('.') for i in indices],
        'Score': [data['Score'][str(i+1)] for i in indices]
    }
    
    return selected_questions

# Variables globales
questions_alternatives = []
options_alternatives = []
levels_alternatives = []
times_alternatives = []
selected_answers = []
correct_answers = []
explanations = []

respuestas_alumno = []
respuestas_correctas_list = []
diferencias_resaltadas_list = []
similaridad_list = []
sugerencias_ia_list = []
correct_incorrect_list = []
times_translation = []

def initialize_quiz():
    global index_alternatives, index_translation, start_time_alternatives, start_time_translation
    global times_alternatives, times_translation, selected_answers, respuestas_alumno
    global respuestas_correctas_list, diferencias_resaltadas_list, similaridad_list
    global sugerencias_ia_list, correct_incorrect_list
    global questions_alternatives, options_alternatives, levels_alternatives, correct_answers, explanations
    global question_alternatives, opts_alternatives, level_alternatives, radio_items
    global final_dict_alternatives, final_dict_translation

    index_alternatives = 0
    index_translation = 0
    start_time_alternatives = time.time()
    start_time_translation = time.time()

    times_alternatives = []
    times_translation = []
    selected_answers = []
    respuestas_alumno = []
    respuestas_correctas_list = []
    diferencias_resaltadas_list = []
    similaridad_list = []
    sugerencias_ia_list = []
    correct_incorrect_list = []

    questions_alternatives = []
    options_alternatives = []
    levels_alternatives = []
    correct_answers = []
    explanations = []

    final_dict_alternatives = {}
    final_dict_translation = {'Spanish': {}, 'English': {}, 'Score': {}}

    # Seleccionar preguntas de alternativas
    for level, path in quiz_paths_alternatives.items():
        selected_questions = select_questions(path, 'ques', 2)
        questions_alternatives.extend(selected_questions['ques'])
        options_alternatives.extend(selected_questions['options'])
        levels_alternatives.extend([level] * len(selected_questions['ques']))
        correct_answers.extend(selected_questions['ans'])
        explanations.extend(selected_questions['explanation'])

    # Seleccionar preguntas de traducción
    for level, path in quiz_paths_translation.items():
        selected_questions = select_translation_questions(path, 2)
        for i in range(len(selected_questions['Spanish'])):
            new_key = f"{level}_{i+1}"
            final_dict_translation['Spanish'][new_key] = selected_questions['Spanish'][i]
            final_dict_translation['English'][new_key] = selected_questions['English'][i]
            final_dict_translation['Score'][new_key] = selected_questions['Score'][i]

    # Crear la primera pregunta y opciones para las alternativas
    question_alternatives = questions_alternatives[index_alternatives]
    opts_alternatives = options_alternatives[index_alternatives]
    level_alternatives = levels_alternatives[index_alternatives]

    # Definir RadioItems para las opciones de respuesta
    radio_items = dbc.RadioItems(
        options=[{'label': opt, 'value': i} for i, opt in enumerate(opts_alternatives)],
        id='radio-options',
        inline=False
    )


# Layout de la aplicación
def serve_layout():
    return dbc.Container(
        [
            dbc.Row([
                dbc.Col(width=1),  # Columna a la izquierda
                dbc.Col([
                    dbc.Form(
                        [
                            dbc.Row(
                                [
                                    dbc.Label("Ingresar Nombre del Estudiante", id="nombre-label"),
                                    dbc.Input(type="text", id="nombre-input", placeholder="Nombre")
                                ],
                                className="mb-3"
                            ),
                            dbc.Row(
                                [
                                    dbc.Label("Ingresar Email si desea recibir un reporte del quiz", id="email-label"),
                                    dbc.Input(type="email", id="email-input", placeholder="Email")
                                ],
                                className="mb-3"
                            ),
                            dbc.Button("Iniciar Quiz", id="start-button", color="success", className="mb-4"),
                        ]
                    ),
                    html.Div(id="quiz-content", style={'display': 'none'}, children=[
                        html.Div(id="title-container", className="text-center my-4", children=html.H1(f"English Level Quiz")),
                        html.Div(id="question-container", className="my-4"),
                        html.Div(id="options-container", className="my-4"),
                        dcc.Textarea(id='student-input', style={'display': 'none', 'width': '100%', 'height': 100}),  # Textarea para traducciones, inicialmente oculto
                        dbc.Button("Next", id="next-button", color="primary", className="me-2"),
                        html.Div(id="alert-container"),
                        html.Div(id="completion-message", className="text-center my-4"),
                        dcc.Graph(id="bar-graph-alternatives", style={'display': 'none'}),
                        html.Div(id="results-table-alternatives", style={'display': 'none'}),
                        dcc.Graph(id="bar-graph-translation", style={'display': 'none'}),
                        html.Div(id="results-table-translation", style={'display': 'none'}),
                        dbc.Row([
                            dbc.Col(dcc.Graph(id="pie-graph-alternatives", style={'display': 'none','width': '50%', 'height': '50%'}), width=6),
                            dbc.Col(html.Div(id="average-time-card-alternatives", style={'display': 'none','font-size': '4em', 'font-weight': 'bold','padding-top':'30px'}, className="d-flex align-items-center justify-content-center"), width=6)
                        ]),
                        dbc.Row([
                            dbc.Col(dcc.Graph(id="pie-graph-translation", style={'display': 'none','width': '50%', 'height': '50%'}), width=6),
                            dbc.Col(html.Div(id="average-time-card-translation", style={'display': 'none','font-size': '4em', 'font-weight': 'bold','padding-top':'30px'}, className="d-flex align-items-center justify-content-center"), width=6)
                        ]),
                        dcc.Graph(id="time-graph", style={'display': 'none'}),
                        html.Div(id="time-table", style={'display': 'none'})             
                    ]),
                    # Agregar el componente de radio-items con un valor inicial vacío
                    dbc.RadioItems(
                        id='radio-options',
                        options=[],
                        value=''
                    )
                ], width=10),  # Contenedor principal
                dbc.Col(width=1)  # Columna a la derecha
            ])
        ],
        fluid=True
    )

app.layout = serve_layout

def highlight_differences(user_answer, correct_answer):
    diff = list(ndiff(user_answer.split(), correct_answer.split()))
    diff_html = []
    for part in diff:
        if part.startswith('-'):
            diff_html.append(html.Span(part[2:] + ' ', style={'color': 'red', 'text-decoration': 'line-through'}))
        elif part.startswith('+'):
            diff_html.append(html.Span(part[2:] + ' ', style={'color': 'green', 'font-weight': 'bold'}))
        else:
            diff_html.append(html.Span(part[2:] + ' '))
    return diff_html

# Callback para manejar el botón de avance y el botón de inicio
@app.callback(
    [
        Output("quiz-content", "style"),
        Output("start-button", "style"),
        Output("email-input", "style"),
        Output("email-label", "style"),
        Output("nombre-input", "style"),
        Output("nombre-label", "style"),
        Output("email-input", "value"),
        Output("title-container", "children"),
        Output("question-container", "children"),
        Output("options-container", "children"),
        Output("completion-message", "children"),
        Output("student-input", "style"),
        Output("time-graph", "figure"),
        Output("time-graph", "style"),
        Output("time-table", "children"),
        Output("time-table", "style"),
        Output("alert-container", "children"),
        Output("results-table-alternatives", "children"),
        Output("results-table-alternatives", "style"),
        Output("bar-graph-alternatives", "figure"),
        Output("bar-graph-alternatives", "style"),
        Output("pie-graph-alternatives", "figure"),
        Output("pie-graph-alternatives", "style"),
        Output("average-time-card-alternatives", "children"),
        Output("average-time-card-alternatives", "style"),
        Output("results-table-translation", "children"),
        Output("results-table-translation", "style"),
        Output("bar-graph-translation", "figure"),
        Output("bar-graph-translation", "style"),
        Output("pie-graph-translation", "figure"),
        Output("pie-graph-translation", "style"),
        Output("average-time-card-translation", "children"),
        Output("average-time-card-translation", "style"),
        Output("student-input", "value")
    ],
    [Input("next-button", "n_clicks"),
     Input("start-button", "n_clicks")],
    [State("radio-options", "value"),
     State("student-input", "value"),
     State("email-input", "value"),
     State("nombre-input", "value")],
    prevent_initial_call=True
)
def update_question(next_clicks, start_clicks, selected_option, student_input, email_value, nombre_value):
    global index_alternatives, index_translation, start_time_alternatives, start_time_translation, times_alternatives, times_translation, selected_answers
    global respuestas_alumno, respuestas_correctas_list, diferencias_resaltadas_list, similaridad_list, sugerencias_ia_list, correct_incorrect_list
    global email_estudiante, nombre_estudiante

    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'start-button':

        initialize_quiz()
        if email_value:
            email_estudiante = email_value
        if nombre_value:
            nombre_estudiante = nombre_value

        # Comenzar con las preguntas de traducción
        selected_sentence = list(final_dict_translation['Spanish'].keys())[index_translation]
        level = selected_sentence.split('_')[0]

        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, "", \
               html.H1(f"English Level Quiz"), html.H3(f"Q{index_translation + 1}: {final_dict_translation['Spanish'][selected_sentence]}"), "", "", \
               {'display': 'block', 'width': '100%', 'height': 100}, dash.no_update, dash.no_update, dash.no_update, dash.no_update, "", \
               dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, ""

    elif triggered_id == 'next-button':
        if index_translation < len(final_dict_translation['Spanish']):
            if not student_input:
                alert = dbc.Alert(
                    [
                        html.I(className="bi bi-exclamation-circle-fill me-2"),
                        "No se ha ingresado ninguna respuesta"
                    ], 
                    color="warning", 
                    style={"overflow": "auto", "whiteSpace": "pre-wrap", "fontSize": "larger", "font-family": "Calibri"}
                )
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'display': 'block', 'width': '100%', 'height': 100}, dash.no_update, dash.no_update, dash.no_update, dash.no_update, alert, \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

            selected_sentence = list(final_dict_translation['Spanish'].keys())[index_translation]
            correct_sentence = final_dict_translation['English'][selected_sentence]

            # Calcular la similitud semántica utilizando BERT
            student_embedding = model.encode(student_input, convert_to_tensor=True)
            correct_embedding = model.encode(correct_sentence, convert_to_tensor=True)
            similarity_score = util.pytorch_cos_sim(student_embedding, correct_embedding).item() * 100

            # Evaluar la oración del estudiante
            accuracy = similarity_score

            # Obtener feedback y sugerencias específicas usando la API de OpenAI
            messages = [
                {"role": "system", "content": "You are an English tutor"},
                {"role": "user", "content": f"Correct the following sentence: {student_input}. The correct sentence is: {correct_sentence}."}
            ]
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=100
            )
            suggestions = completion.choices[0].message.content

            # Resaltar diferencias entre la respuesta del usuario y la correcta
            highlighted_differences = highlight_differences(student_input, correct_sentence)

            # Guardar las respuestas y detalles
            respuestas_alumno.append(student_input)
            respuestas_correctas_list.append(correct_sentence)
            diferencias_resaltadas_list.append(highlighted_differences)
            similaridad_list.append(f"{similarity_score:.2f}%")
            sugerencias_ia_list.append(suggestions)
            correct_incorrect_list.append("Correcto" if accuracy > 85 else "Incorrecto")

            # Calcular el tiempo tomado para responder la pregunta
            end_time = time.time()
            duration = end_time - start_time_translation
            times_translation.append(duration)
            start_time_translation = end_time

            # Obtener el siguiente índice de la pregunta
            current_index = index_translation
            index_translation += 1

            if current_index + 1 < len(final_dict_translation['Spanish']):
                next_key = list(final_dict_translation['Spanish'].keys())[current_index + 1]
                selected_sentence = next_key

                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       html.H1(f"English Level Quiz"), html.H3(f"Q{index_translation + 1}: {final_dict_translation['Spanish'][selected_sentence]}"), "", "", \
                       {'display': 'block', 'width': '100%', 'height': 100}, dash.no_update, dash.no_update, dash.no_update, dash.no_update, "", \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, ""

            else:
                # Comenzar con las preguntas de alternativas
                question = questions_alternatives[index_alternatives]
                opts = options_alternatives[index_alternatives]
                level = levels_alternatives[index_alternatives]

                # Actualizar los RadioItems para la primera pregunta
                radio_items = dbc.RadioItems(
                    options=[{'label': opt, 'value': i} for i, opt in enumerate(opts)],
                    id='radio-options',
                    inline=False
                )

                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       html.H1(f"English {level} Level Quiz"), html.H3(f"Q{index_alternatives + 1}: {question}"), radio_items, "", {'display': 'none'}, dash.no_update, dash.no_update, dash.no_update, dash.no_update, "", \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

        elif index_alternatives < len(questions_alternatives):
            # Validar si se ha seleccionado una opción
            if selected_option is None:
                alert = dbc.Alert(
                    [
                        html.I(className="bi bi-exclamation-circle-fill me-2"),
                        "No se ha seleccionado respuesta"
                    ], 
                    color="warning", 
                    style={"overflow": "auto", "whiteSpace": "pre-wrap", "fontSize": "larger", "font-family": "Calibri"}
                )
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'display': 'none'},\
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,\
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       dash.no_update, dash.no_update, alert, dash.no_update,dash.no_update, \
                       dash.no_update, dash.no_update, dash.no_update, \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update

            # Almacenar la opción seleccionada en selected_answers
            selected_answers.append(selected_option)

            # Calcular el tiempo tomado para responder la pregunta
            end_time = time.time()
            duration = end_time - start_time_alternatives
            times_alternatives.append(duration)
            start_time_alternatives = end_time

            # Preparar la siguiente pregunta y opciones
            index_alternatives += 1
            if index_alternatives < len(questions_alternatives):
                question = questions_alternatives[index_alternatives]
                opts = options_alternatives[index_alternatives]
                level = levels_alternatives[index_alternatives]

                # Actualizar los RadioItems para la siguiente pregunta
                radio_items = dbc.RadioItems(
                    options=[{'label': opt, 'value': i} for i, opt in enumerate(opts)],
                    id='radio-options',
                    inline=False
                )

                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       html.H1(f"English {level} Level Quiz"), html.H3(f"Q{index_alternatives + 1}: {question}"), radio_items, "", {'display': 'none'}, dash.no_update, dash.no_update, dash.no_update, dash.no_update, "", \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

            else:
                # Mostrar resultados al final
                times = times_alternatives + times_translation
                results_df_alternatives = pd.DataFrame({
                    'Question': questions_alternatives,
                    'Selected Answer': [options_alternatives[i][ans] for i, ans in enumerate(selected_answers)],
                    'Correct Answer': [options_alternatives[i][correct_answers[i]-1] for i in range(len(correct_answers))],
                    'Explanation': explanations,
                    'Correct': ['Yes' if selected_answers[i] == correct_answers[i]-1 else 'No' for i in range(len(selected_answers))]
                })
                results_df_translation = pd.DataFrame({
                    'Oración del Estudiante': respuestas_alumno,
                    'Oración Correcta': respuestas_correctas_list,
                    'Diferencias Resaltadas': diferencias_resaltadas_list,
                    'Similaridad (%)': similaridad_list,
                    'Sugerencias IA': sugerencias_ia_list,
                    'Correcto/Incorrecto': correct_incorrect_list
                })
                results_table_alternatives = dbc.Table.from_dataframe(results_df_alternatives, striped=True, bordered=True, hover=True)
                results_table_translation = dbc.Table.from_dataframe(results_df_translation, striped=True, bordered=True, hover=True)

                # Crear gráfico de barras para respuestas correctas e incorrectas por nivel (alternativas)
                correct_counts_alternatives = results_df_alternatives.groupby(levels_alternatives)['Correct'].apply(lambda x: (x == 'Yes').sum()).reset_index(name='Correct')
                incorrect_counts_alternatives = results_df_alternatives.groupby(levels_alternatives)['Correct'].apply(lambda x: (x == 'No').sum()).reset_index(name='Incorrect')
                bar_df_alternatives = pd.merge(correct_counts_alternatives, incorrect_counts_alternatives, on='index')
                bar_fig_alternatives = px.bar(bar_df_alternatives, x='index', y=['Correct', 'Incorrect'], barmode='group', title='Correct and Incorrect Answers by Level (Alternatives)', color_discrete_sequence=['#007bff','#dc3545'])

                # Crear gráfico de pastel para porcentaje de respuestas correctas vs incorrectas (alternativas)
                total_correct_alternatives = (results_df_alternatives['Correct'] == 'Yes').sum()
                total_incorrect_alternatives = (results_df_alternatives['Correct'] == 'No').sum()
                pie_df_alternatives = pd.DataFrame({
                    'Outcome': ['Correct', 'Incorrect'],
                    'Count': [total_correct_alternatives, total_incorrect_alternatives]
                })
                pie_fig_alternatives = px.pie(pie_df_alternatives, values='Count', names='Outcome', title='Correct vs Incorrect Answers (Alternatives)', color_discrete_sequence=['#dc3545','#007bff'])

                # Crear gráfico de barras para respuestas correctas e incorrectas por nivel (traducción)
                correct_counts_translation = results_df_translation.groupby(results_df_translation['Oración Correcta'].str.split('_').str[0])['Correcto/Incorrecto'].apply(lambda x: (x == 'Correcto').sum()).reset_index(name='Correct')
                incorrect_counts_translation = results_df_translation.groupby(results_df_translation['Oración Correcta'].str.split('_').str[0])['Correcto/Incorrecto'].apply(lambda x: (x == 'Incorrecto').sum()).reset_index(name='Incorrect')
                bar_df_translation = pd.merge(correct_counts_translation, incorrect_counts_translation, on='Oración Correcta')
                bar_fig_translation = px.bar(bar_df_translation, x='Oración Correcta', y=['Correct', 'Incorrect'], barmode='group', title='Correct and Incorrect Answers by Level (Translation)', color_discrete_sequence=['#007bff','#dc3545'])

                # Crear gráfico de pastel para porcentaje de respuestas correctas vs incorrectas (traducción)
                total_correct_translation = (results_df_translation['Correcto/Incorrecto'] == 'Correcto').sum()
                total_incorrect_translation = (results_df_translation['Correcto/Incorrecto'] == 'Incorrecto').sum()
                pie_df_translation = pd.DataFrame({
                    'Outcome': ['Correcto', 'Incorrecto'],
                    'Count': [total_correct_translation, total_incorrect_translation]
                })
                pie_fig_translation = px.pie(pie_df_translation, values='Count', names='Outcome', title='Correct vs Incorrect Answers (Translation)', color_discrete_sequence=['#dc3545','#007bff'])

                # Calcular el promedio de tiempos de respuesta
                avg_time_alternatives = sum(times_alternatives) / len(times_alternatives)
                avg_time_translation = sum(times_translation) / len(times_translation)

                # Crear las tarjetas de tiempo promedio como imágenes
                def create_time_card_image(title, value, file_path):
                    fig, ax = plt.subplots(figsize=(6, 2))  # Aumentar la altura de la figura
                    ax.text(0.5, 0.75, title, ha='center', va='center', fontsize=14)  # Ajustar el título
                    ax.text(0.5, 0.25, value, ha='center', va='center', fontsize=24, weight='bold')  # Ajustar el valor
                    ax.axis('off')
                    fig.savefig(file_path, bbox_inches='tight')
                    plt.close(fig)

                avg_time_card_alternatives_image_path = "avg_time_card_alternatives.png"
                avg_time_card_translation_image_path = "avg_time_card_translation.png"

                create_time_card_image("Average Time per Question (Alternatives)", f"{avg_time_alternatives:.2f} seconds", avg_time_card_alternatives_image_path)
                create_time_card_image("Average Time per Question (Translation)", f"{avg_time_translation:.2f} seconds", avg_time_card_translation_image_path)

                avg_time_card_alternatives = dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Average Time per Question (Alternatives)", className="card-title"),
                            html.P(f"{avg_time_alternatives:.2f} seconds", style={"font-size": "24px", "font-weight": "bold"}, className="card-text")
                        ]
                    )
                )
                avg_time_card_translation = dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Average Time per Question (Translation)", className="card-title"),
                            html.P(f"{avg_time_translation:.2f} seconds", style={"font-size": "24px", "font-weight": "bold"}, className="card-text")
                        ]
                    )
                )

                # Crear el gráfico de líneas para el tiempo de respuesta por pregunta
                time_df = pd.DataFrame({
                    'Pregunta': list(range(1, len(times) + 1)),
                    'Tiempo (s)': times
                }).round({'Tiempo (s)': 2})
                time_fig = px.line(time_df, x='Pregunta', y='Tiempo (s)', title='Time Spent on Each Question')
                time_table = dbc.Table.from_dataframe(time_df, striped=True, bordered=True, hover=True)

                # Guardar las imágenes de los gráficos usando Plotly
                bar_fig_alternatives.write_image("bar_fig_alternatives.png")
                pie_fig_alternatives.write_image("pie_fig_alternatives.png")
                bar_fig_translation.write_image("bar_fig_translation.png")
                pie_fig_translation.write_image("pie_fig_translation.png")
                time_fig.write_image("time_fig.png")

                # # Asegurar que los archivos de imagen se guarden correctamente
                # avg_time_card_alternatives_image_path = "avg_time_card_alternatives.png"
                # avg_time_card_translation_image_path = "avg_time_card_translation.png"

                # Crear las tarjetas de tiempo promedio como imágenes
                fig, ax = plt.subplots(figsize=(6, 1))
                ax.text(0.5, 0.5, f"Average Time per Question (Alternatives): {avg_time_alternatives:.2f} seconds", ha='center', va='center', wrap=True)
                ax.axis('off')
                fig.savefig(avg_time_card_alternatives_image_path, bbox_inches='tight')
                plt.close(fig)

                fig, ax = plt.subplots(figsize=(6, 1))
                ax.text(0.5, 0.5, f"Average Time per Question (Translation): {avg_time_translation:.2f} seconds", ha='center', va='center', wrap=True)
                ax.axis('off')
                fig.savefig(avg_time_card_translation_image_path, bbox_inches='tight')
                plt.close(fig)

                if email_estudiante and nombre_estudiante:
                    try:
                        # Enviar el correo
                        send_email(
                            to_name=nombre_estudiante,
                            to_email=email_estudiante,
                            bar_fig_alternatives="bar_fig_alternatives.png",
                            pie_fig_alternatives="pie_fig_alternatives.png",
                            bar_fig_translation="bar_fig_translation.png",
                            pie_fig_translation="pie_fig_translation.png",
                            time_fig="time_fig.png",
                            avg_time_card_alternatives=avg_time_card_alternatives_image_path,
                            avg_time_card_translation=avg_time_card_translation_image_path,
                            results_df_alternatives=results_df_alternatives,
                            results_df_translation=results_df_translation
                        )
                    except Exception as e:
                        print(f"Error al enviar el correo: {str(e)}")

                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       '', '', '', '', {'display': 'none'}, time_fig, {'display': 'block'}, time_table, {'display': 'block'}, "", \
                       results_table_alternatives, {'display': 'block'}, bar_fig_alternatives, {'display': 'block'}, pie_fig_alternatives, \
                       {'display': 'block'}, avg_time_card_alternatives, {'display': 'block'}, results_table_translation, {'display': 'block'}, \
                       bar_fig_translation, {'display': 'block'}, pie_fig_translation, {'display': 'block'}, avg_time_card_translation, {'display': 'block'}, ''

        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               html.H1(f"English {level} Level Quiz"), html.H3(f"Q{index_alternatives + 1}: {questions_alternatives[index_alternatives]}"), radio_items, "", {'display': 'none'}, \
               dash.no_update, dash.no_update, dash.no_update, dash.no_update, "", \
               dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

if __name__ == "__main__":
    app.run_server(debug=True)
