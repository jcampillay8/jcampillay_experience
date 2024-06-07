import threading

class EmailThread(threading.Thread):
    """
    Clase para enviar correos electrónicos en un hilo separado.
    """

    def __init__(self, email):
        """
        Inicializa la clase con el correo electrónico a enviar.
        """
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        """
        Envía el correo electrónico.
        """
        self.email.send(fail_silently=False)
