from dash import Input, Output, State, callback_context, html
import dash_bootstrap_components as dbc
from apps.Quizzes.english_quiz.data import (
    email_estudiante, nombre_estudiante, get_initial_question, initialize_quiz,
    final_dict_translation, respuestas_alumno, respuestas_correctas_list,
    diferencias_resaltadas_list, similaridad_list, sugerencias_ia_list,
    correct_incorrect_list, times_translation, index_translation, start_time_translation
)
from apps.Quizzes.english_quiz.utils import highlight_differences
from sentence_transformers import SentenceTransformer, util
import time
import os
import environ
from openai import OpenAI

env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(__file__), '../../core/.env'))

client = OpenAI(api_key=env('OPENAI_API_KEY'))
model = SentenceTransformer('all-MiniLM-L6-v2')

def register_callbacks(app):
    @app.callback(
        [Output("quiz-content", "style"),
         Output("start-button", "style"),
         Output("email-input", "style"),
         Output("email-label", "style"),
         Output("nombre-input", "style"),
         Output("nombre-label", "style"),
         Output("question-text", "children")],
        Input("start-button", "n_clicks"),
        State("email-input", "value"),
        State("nombre-input", "value"),
        prevent_initial_call=True
    )
    def show_quiz_content(n_clicks, email_value, nombre_value):
        global email_estudiante, nombre_estudiante

        # Inicializar el quiz antes de obtener la primera pregunta
        initialize_quiz()

        if email_value:
            email_estudiante = email_value
        if nombre_value:
            nombre_estudiante = nombre_value
        
        question, counter = get_initial_question()
        
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, f"Q{counter}: {question}"

# def store_student_answer_app(app):
#     @app.callback(
#         [Output("question-text", "children"),
#          Output("alert-container", "children")],
#         Input("next-button", "n_clicks"),
#         State("student-input", "value"),
#         prevent_initial_call=True
#     )
#     def store_student_answer(n_clicks, student_input):
#         global index_translation, start_time_translation

#         if index_translation < len(final_dict_translation['Spanish']):
#             selected_sentence = list(final_dict_translation['Spanish'].keys())[index_translation]
#             correct_sentence = final_dict_translation['English'][selected_sentence]

#             student_embedding = model.encode(student_input, convert_to_tensor=True)
#             correct_embedding = model.encode(correct_sentence, convert_to_tensor=True)
#             similarity_score = util.pytorch_cos_sim(student_embedding, correct_embedding).item() * 100

#             accuracy = similarity_score

#             messages = [
#                 {"role": "system", "content": "You are an English tutor"},
#                 {"role": "user", "content": f"Correct the following sentence: {student_input}. The correct sentence is: {correct_sentence}."}
#             ]
#             completion = client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=messages,
#                 max_tokens=100
#             )
#             suggestions = completion.choices[0].message.content

#             highlighted_differences = highlight_differences(student_input, correct_sentence)

#             respuestas_alumno.append(student_input)
#             respuestas_correctas_list.append(correct_sentence)
#             diferencias_resaltadas_list.append(highlighted_differences)
#             similaridad_list.append(f"{similarity_score:.2f}%")
#             sugerencias_ia_list.append(suggestions)
#             correct_incorrect_list.append("Correcto" if accuracy > 85 else "Incorrecto")

#             end_time = time.time()
#             duration = end_time - start_time_translation
#             times_translation.append(duration)
#             start_time_translation = end_time

#             index_translation += 1

#             if index_translation < len(final_dict_translation['Spanish']):
#                 next_key = list(final_dict_translation['Spanish'].keys())[index_translation]
#                 next_question = final_dict_translation['Spanish'][next_key]
#                 return f"Q{index_translation + 1}: {next_question}", ""

#             else:
#                 return "", dbc.Alert("All translation questions are completed.", color="success")

#         return dash.no_update, dash.no_update