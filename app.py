from flask import Flask, render_template, request
from Calculo_iva_a_pagar import calcular_iva_archivos
import webbrowser
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_files', methods=['POST'])
def process_files():
    # Get the path to the selected folder from the form data
    folder_path = request.form.get('folder_path')
    folder_path = os.path.abspath(folder_path)

    # Call the calcular_iva_archivos function to process the files
    resultados = calcular_iva_archivos(ruta_archivo=folder_path)

    # Pass the results to a new HTML template for displaying the output
    return render_template('results.html', resultados=resultados)


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')


if __name__ == "__main__":
    # the command you want
    open_browser()
    app.run(port=5000)
