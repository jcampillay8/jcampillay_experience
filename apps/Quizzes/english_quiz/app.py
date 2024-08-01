import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State
from apps.Quizzes.english_quiz.layout import serve_layout
from apps.Quizzes.english_quiz.callback import register_callbacks#, store_student_answer_app
from apps.Quizzes.english_quiz.data import initialize_quiz
from django_plotly_dash import DjangoDash

# Inicializar la aplicación Dash
app = DjangoDash('EnglishQuizApp', external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"], suppress_callback_exceptions=True)


# Establecer el layout de la aplicación
app.layout = serve_layout

# Registrar callbacks
register_callbacks(app)

if __name__ == "__main__":
    initialize_quiz()
    app.run_server(debug=True)