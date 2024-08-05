import dash_bootstrap_components as dbc
from dash import html, dcc
from apps.Quizzes.english_quiz.data import initialize_quiz, question_translation, opts_translation, index_translation

def serve_layout():
    initialize_quiz()
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
                        html.Div(id="question-container", className="my-4", children=html.H3(f"Q{index_translation + 1}: {opts_translation}")),
                        dcc.Textarea(id='student-input', style={'display': 'block', 'width': '100%', 'height': 100}),
                        dbc.Button("Next", id="next-button", color="primary", className="me-2"),
                        html.Div(id="alert-container"),
                    ])
                ], width=10),  # Contenedor principal
                dbc.Col(width=1)  # Columna a la derecha
            ])
        ],
        fluid=True
    )
