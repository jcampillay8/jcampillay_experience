def is_valid_password(password):
    """
    Verifica si la contraseña cumple con los requisitos mínimos de longitud.

    Args:
        password (str): La contraseña a verificar.

    Returns:
        bool: True si la contraseña es válida, False si no lo es.
    """
    return len(password) >= 6



# def is_valid_password(password, min_length=True, has_lowercase=True, has_uppercase=True, has_digit=True):
#     """
#     Verifica si la contraseña cumple con los requisitos mínimos de seguridad.

#     Args:
#         password (str): La contraseña a verificar.
#         min_length (bool): Indica si se debe verificar la longitud mínima de la contraseña.
#         has_lowercase (bool): Indica si se debe verificar si la contraseña contiene letras minúsculas.
#         has_uppercase (bool): Indica si se debe verificar si la contraseña contiene letras mayúsculas.
#         has_digit (bool): Indica si se debe verificar si la contraseña contiene dígitos.

#     Returns:
#         bool: True si la contraseña cumple con todas las verificaciones especificadas, False de lo contrario.
#     """
#     validations = []

#     if min_length:
#         validations.append(len(password) >= 6)

#     if has_lowercase:
#         validations.append(any(char.islower() for char in password))

#     if has_uppercase:
#         validations.append(any(char.isupper() for char in password))

#     if has_digit:
#         validations.append(any(char.isdigit() for char in password))

#     return all(validations), {
#         'min_length': len(password) >= 6,
#         'has_lowercase': any(char.islower() for char in password),
#         'has_uppercase': any(char.isupper() for char in password),
#         'has_digit': any(char.isdigit() for char in password)
#     }
