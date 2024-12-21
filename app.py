from flask import Flask, render_template
from midfielders import cargar_mediocampistas
from defenders import cargar_defensas
from goalkeepers import cargar_porteros
from forwards import cargar_delanteros
from midfielders import graficas_mediocampistas
from goalkeepers import graficas_porteros
from forwards import graficas_delanteros
from general import grafica_general
from defenders import graficas_defensas
import plotly.express as px

# Crear una instancia de Flask
app = Flask(__name__)
archivo_csv = 'datosjugadores.csv'

# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generalstats')
def genstats():
    graphs = grafica_general(archivo_csv)
    return render_template('generalstats.html', graphs=graphs)  

@app.route('/goalkeepers')
def goalkeepers():
    porteros = cargar_porteros(archivo_csv)
    top_5_porteros = porteros[:5]
    return render_template('goalkeepers.html', porteros=top_5_porteros)

@app.route('/goalkeeperstats')
def goalkeepersstats():
    graphs = graficas_porteros(archivo_csv)
    return render_template('goalkeepersstats.html', graphs=graphs)  # Pasamos directamente sin json.dumps

@app.route('/defenders')
def defenders():
    defensas = cargar_defensas(archivo_csv)
    top_5_defensas = defensas[:5]
    return render_template('defenders.html', defensas=top_5_defensas)

@app.route('/defendersstats')
def defendersstats():
    graphs = graficas_defensas(archivo_csv)
    return render_template('defendersstats.html', graphs=graphs)

@app.route('/midfielders')
def midfielders():
    mediocampistas = cargar_mediocampistas(archivo_csv)
    top_5_mediocampistas = mediocampistas[:5]
    return render_template('midfielders.html', mediocampistas=top_5_mediocampistas)

@app.route('/midfieldersstats')
def midfieldersstats():
    graphs = graficas_mediocampistas(archivo_csv)
    return render_template('midfieldersstats.html', graphs=graphs)  # Pasamos directamente sin json.dumps

@app.route('/forwards')
def forwards():
    delanteros = cargar_delanteros(archivo_csv)
    top_5_delanteros = delanteros[:5]
    return render_template('forwards.html',delanteros=top_5_delanteros)

@app.route('/forwardsstats')
def forwardsstats():
    graphs = graficas_delanteros(archivo_csv)
    return render_template('forwardsstats.html', graphs=graphs)

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
