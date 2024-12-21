
        document.addEventListener('DOMContentLoaded', function() {
            // Seleccionar los contenedores de las gráficas
            const chartElements = document.querySelectorAll('.chart-card');
            
            // Iterar sobre cada contenedor y renderizar la gráfica usando el JSON en data-graph
            chartElements.forEach((element, index) => {
                // Obtener el valor del data-graph
                const graphDataString = element.getAttribute('data-graph');
                
                if (graphDataString) {
                    try {
                        const graphData = JSON.parse(graphDataString);
                        const chartId = 'chart' + (index + 1);  // Esto genera el id adecuado para cada gráfica
                        Plotly.newPlot(chartId, graphData);
                    } catch (error) {
                        console.error('Error al parsear los datos JSON para la gráfica ' + (index + 1), error);
                    }
                } else {
                    console.error('No se encontraron datos para la gráfica ' + (index + 1));
                }
            });
        });
