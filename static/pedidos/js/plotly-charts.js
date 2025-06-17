// static/pedidos/js/plotly-charts.js

document.addEventListener("DOMContentLoaded", function() {
    const graphDiv = document.getElementById("graph-div");
    if (graphDiv && graphDiv.dataset.graph) {
        const graphData = JSON.parse(graphDiv.dataset.graph);
        Plotly.newPlot('graph-div', graphData.data, graphData.layout || {});
    }
});
