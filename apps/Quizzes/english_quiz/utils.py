from difflib import ndiff
from dash import html

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
