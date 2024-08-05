import json
import random
import time
import os
import pandas as pd
import dash_bootstrap_components as dbc

email_estudiante = None
nombre_estudiante = None

# Variables globales para la secuencia del quiz
questions_alternatives = []
options_alternatives = []
levels_alternatives = []
times_alternatives = []
selected_answers = []
correct_answers = []
explanations = []

index_alternatives = 0
index_translation = 0
start_time_alternatives = 0
start_time_translation = 0

# Inicializar listas para las traducciones
respuestas_alumno = []
respuestas_correctas_list = []
diferencias_resaltadas_list = []
similaridad_list = []
sugerencias_ia_list = []
correct_incorrect_list = []
times_translation = []

question_translation = None
opts_translation = None
question_alternatives = None
opts_alternatives = None
radio_items_alternatives = None
final_dict_translation = None

# Definir las rutas de los archivos JSON para las alternativas y traducciones
quiz_paths_alternatives = {
    'A1': 'apps/Quizzes/english_quiz/questions/alternativas/A1_alternatives.json',
    'A2': 'apps/Quizzes/english_quiz/questions/alternativas/A2_alternatives.json',
    'B1': 'apps/Quizzes/english_quiz/questions/alternativas/B1_alternatives.json',
    'B2': 'apps/Quizzes/english_quiz/questions/alternativas/B2_alternatives.json',
    'C1': 'apps/Quizzes/english_quiz/questions/alternativas/C1_alternatives.json',
    'C2': 'apps/Quizzes/english_quiz/questions/alternativas/C2_alternatives.json'
}

quiz_paths_translation = {
    'A1': 'apps/Quizzes/english_quiz/questions/traducciones/A1_translate.json',
    'A2': 'apps/Quizzes/english_quiz/questions/traducciones/A2_translate.json',
    'B1': 'apps/Quizzes/english_quiz/questions/traducciones/B1_translate.json',
    'B2': 'apps/Quizzes/english_quiz/questions/traducciones/B2_translate.json',
    'C1': 'apps/Quizzes/english_quiz/questions/traducciones/C1_translate.json',
    'C2': 'apps/Quizzes/english_quiz/questions/traducciones/C2_translate.json'
}

# Función para leer el archivo JSON y seleccionar preguntas aleatorias
def select_questions(file_path, key_type, num_questions=2):
    with open(file_path, 'r') as file:
        data = json.load(file)
    indices = random.sample(range(len(data[key_type])), num_questions)
    selected_questions = {
        key_type: [data[key_type][i] for i in indices],
        'options': [data['options'][i] for i in indices],
        'ans': [data['ans'][i] for i in indices],
        'explanation': [data['explanation'][i] for i in indices],
        'valores': [data['valores'][i] for i in indices]
    }
    return selected_questions

def initialize_quiz():
    global questions_alternatives, options_alternatives, levels_alternatives, correct_answers, explanations
    global respuestas_alumno, respuestas_correctas_list, diferencias_resaltadas_list, similaridad_list, sugerencias_ia_list, correct_incorrect_list, times_translation
    global index_alternatives, index_translation, start_time_alternatives, start_time_translation
    global question_translation, opts_translation, question_alternatives, opts_alternatives, radio_items_alternatives, final_dict_translation

    # Diccionario final para las traducciones
    final_dict_translation = {'Spanish': {}, 'English': {}, 'Score': {}}

    # Iterar sobre los niveles y seleccionar preguntas para las traducciones
    for level, path in quiz_paths_translation.items():
        with open(path, 'r') as file:
            data = json.load(file)
        indices = random.sample(range(len(data['Spanish'])), 2)
        for i in indices:
            new_key = f"{level}_{i+1}"
            final_dict_translation['Spanish'][new_key] = data['Spanish'][str(i+1)].rstrip('.')
            final_dict_translation['English'][new_key] = data['English'][str(i+1)].rstrip('.')
            final_dict_translation['Score'][new_key] = data['Score'][str(i+1)]

    # Diccionario final para las alternativas
    final_dict_alternatives = {}

    # Iterar sobre los niveles y seleccionar preguntas
    for level, path in quiz_paths_alternatives.items():
        selected_questions = select_questions(path, 'ques')
        final_dict_alternatives[f'{level}_ques'] = selected_questions['ques']
        final_dict_alternatives[f'{level}_options'] = selected_questions['options']
        final_dict_alternatives[f'{level}_ans'] = selected_questions['ans']
        final_dict_alternatives[f'{level}_explanation'] = selected_questions['explanation']
        final_dict_alternatives[f'{level}_valores'] = selected_questions['valores']

    # Crear el DataFrame para las alternativas
    df_alternatives = pd.DataFrame(final_dict_alternatives)

    # Variables globales para el control de la secuencia de preguntas y tiempos
    questions_alternatives = []
    options_alternatives = []
    levels_alternatives = []
    times_alternatives = []
    selected_answers = []
    correct_answers = []
    explanations = []

    for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
        questions_alternatives.extend(df_alternatives[f'{level}_ques'])
        options_alternatives.extend(df_alternatives[f'{level}_options'])
        levels_alternatives.extend([level] * len(df_alternatives[f'{level}_ques']))
        correct_answers.extend(df_alternatives[f'{level}_ans'])
        explanations.extend(df_alternatives[f'{level}_explanation'])

    index_alternatives = 0
    index_translation = 0
    start_time_alternatives = time.time()
    start_time_translation = time.time()

    # Inicializar listas para las traducciones
    respuestas_alumno = []
    respuestas_correctas_list = []
    diferencias_resaltadas_list = []
    similaridad_list = []
    sugerencias_ia_list = []
    correct_incorrect_list = []
    times_translation = []

    # Crear la primera pregunta y opciones para las traducciones
    question_translation = list(final_dict_translation['Spanish'].keys())[index_translation]
    opts_translation = final_dict_translation['Spanish'][question_translation]

    # Crear la primera pregunta y opciones para las alternativas
    question_alternatives = questions_alternatives[index_alternatives]
    opts_alternatives = options_alternatives[index_alternatives]

def get_initial_question():
    global question_translation, index_translation
    question_translation = list(final_dict_translation['Spanish'].keys())[index_translation]
    return final_dict_translation['Spanish'][question_translation], index_translation + 1
