import os
from wsgiref.util import setup_testing_defaults

def custom_middleware(app):
    def wrapped_app(environ, start_response):
        setup_testing_defaults(environ)
        path = environ.get('PATH_INFO', '')
        user_agent = environ.get('HTTP_USER_AGENT', '')

        # Verifica se a requisição é de um navegador
        is_browser = 'Mozilla' in user_agent

        # Redirecionar para index.html na raiz
        if path == '/':
            if is_browser:
                status = '302 Found'
                headers = [('Location', '/index.html')]
                start_response(status, headers)
                return [b'Redirecting to /index.html']
            else:
                # Permite que RaiDrive ou outros clientes continuem
                return app(environ, start_response)

        # Serve index.html diretamente
        elif path == '/index.html':
            try:
                index_path = os.path.join(os.path.dirname(__file__), "index.html")
                with open(index_path, "rb") as f:
                    content = f.read()
                status = '200 OK'
                headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
                start_response(status, headers)
                return [content]
            except FileNotFoundError:
                status = '404 Not Found'
                start_response(status, [('Content-Type', 'text/plain')])
                return [b'File not found']

        # Para qualquer outro caminho, redirecione para index.html se for um navegador
        if is_browser:
            status = '302 Found'
            headers = [('Location', '/index.html')]
            start_response(status, headers)
            return [b'Redirecting to /index.html']

        # Permite que RaiDrive ou outros clientes continuem
        return app(environ, start_response)

    return wrapped_app
