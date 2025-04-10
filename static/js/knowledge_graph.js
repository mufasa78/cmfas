/**
 * Knowledge Graph visualization using D3.js
 */

let graphSimulation = null;
let graphSvg = null;
let graphNodes = [];
let graphLinks = [];
let graphWidth = 1000;
let graphHeight = 600;

/**
 * Initializes the knowledge graph visualization
 * @param {string} elementId - DOM element ID for the graph
 */
function initKnowledgeGraph(elementId) {
    const container = document.getElementById(elementId);
    if (!container) return;
    
    // Clear existing graph
    container.innerHTML = '';
    
    // Set dimensions
    graphWidth = container.clientWidth;
    graphHeight = 600;
    
    // Create SVG element
    graphSvg = d3.select(container).append('svg')
        .attr('width', graphWidth)
        .attr('height', graphHeight)
        .attr('class', 'knowledge-graph');
    
    // Add zoom functionality
    const zoom = d3.zoom()
        .scaleExtent([0.1, 4])
        .on('zoom', (event) => {
            graphSvg.select('g').attr('transform', event.transform);
        });
    
    graphSvg.call(zoom);
    
    // Create a container group for all graph elements
    graphSvg.append('g');
    
    // Add loading indicator
    graphSvg.append('text')
        .attr('x', graphWidth / 2)
        .attr('y', graphHeight / 2)
        .attr('text-anchor', 'middle')
        .attr('class', 'loading-text')
        .text('Loading Knowledge Graph...');
    
    // Load graph data
    let dataUrl = '/api/knowledge-graph';
    
    // Check for material or prescription filter
    const materialId = new URLSearchParams(window.location.search).get('material_id');
    const prescriptionId = new URLSearchParams(window.location.search).get('prescription_id');
    
    if (materialId) {
        dataUrl += `?material_id=${materialId}`;
    } else if (prescriptionId) {
        dataUrl += `?prescription_id=${prescriptionId}`;
    }
    
    fetchGraphData(dataUrl);
}

/**
 * Fetches graph data from API and renders the graph
 * @param {string} url - API endpoint URL
 */
function fetchGraphData(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Remove loading indicator
            graphSvg.select('.loading-text').remove();
            
            if (data.nodes.length === 0) {
                // Show no data message
                graphSvg.append('text')
                    .attr('x', graphWidth / 2)
                    .attr('y', graphHeight / 2)
                    .attr('text-anchor', 'middle')
                    .attr('fill', '#ccc')
                    .text('No graph data available');
                return;
            }
            
            // Store nodes and links
            graphNodes = data.nodes;
            graphLinks = data.links;
            
            // Render graph
            renderGraph();
        })
        .catch(error => {
            console.error('Error fetching graph data:', error);
            
            // Remove loading indicator and show error
            graphSvg.select('.loading-text').remove();
            graphSvg.append('text')
                .attr('x', graphWidth / 2)
                .attr('y', graphHeight / 2)
                .attr('text-anchor', 'middle')
                .attr('fill', '#f56c6c')
                .text('Error loading knowledge graph data');
        });
}

/**
 * Renders the knowledge graph with nodes and links
 */
function renderGraph() {
    // Create the simulation
    graphSimulation = d3.forceSimulation(graphNodes)
        .force('link', d3.forceLink(graphLinks).id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(graphWidth / 2, graphHeight / 2))
        .force('collision', d3.forceCollide().radius(60));
    
    const container = graphSvg.select('g');
    
    // Create links
    const link = container.selectAll('.link')
        .data(graphLinks)
        .enter()
        .append('line')
        .attr('class', 'link')
        .attr('stroke', d => getLinkColor(d.type))
        .attr('stroke-width', 1.5)
        .attr('stroke-opacity', 0.6);
    
    // Create nodes
    const node = container.selectAll('.node')
        .data(graphNodes)
        .enter()
        .append('g')
        .attr('class', 'node')
        .call(d3.drag()
            .on('start', dragStarted)
            .on('drag', dragged)
            .on('end', dragEnded));
    
    // Add node circles
    node.append('circle')
        .attr('r', d => getNodeRadius(d))
        .attr('fill', d => getNodeColor(d.type))
        .attr('stroke', '#fff')
        .attr('stroke-width', 1.5);
    
    // Add node labels
    node.append('text')
        .attr('dy', 4)
        .attr('text-anchor', 'middle')
        .text(d => d.name)
        .attr('fill', '#fff')
        .attr('font-size', '10px');
    
    // Add tooltips
    node.append('title')
        .text(d => getNodeTooltip(d));
    
    // Update positions on tick
    graphSimulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        
        node
            .attr('transform', d => `translate(${d.x},${d.y})`);
    });
    
    // Add legend
    addGraphLegend();
}

/**
 * Adds a legend to the graph
 */
function addGraphLegend() {
    const legend = graphSvg.append('g')
        .attr('class', 'legend')
        .attr('transform', 'translate(20, 20)');
    
    // Material node
    legend.append('circle')
        .attr('cx', 10)
        .attr('cy', 10)
        .attr('r', 8)
        .attr('fill', getNodeColor('material'));
    
    legend.append('text')
        .attr('x', 25)
        .attr('y', 15)
        .text('Medicinal Material')
        .attr('fill', '#ccc')
        .attr('font-size', '12px');
    
    // Prescription node
    legend.append('circle')
        .attr('cx', 10)
        .attr('cy', 40)
        .attr('r', 8)
        .attr('fill', getNodeColor('prescription'));
    
    legend.append('text')
        .attr('x', 25)
        .attr('y', 45)
        .text('Prescription')
        .attr('fill', '#ccc')
        .attr('font-size', '12px');
    
    // Contains link
    legend.append('line')
        .attr('x1', 0)
        .attr('y1', 70)
        .attr('x2', 20)
        .attr('y2', 70)
        .attr('stroke', getLinkColor('contains'))
        .attr('stroke-width', 1.5);
    
    legend.append('text')
        .attr('x', 25)
        .attr('y', 75)
        .text('Contains')
        .attr('fill', '#ccc')
        .attr('font-size', '12px');
    
    // Interaction link
    legend.append('line')
        .attr('x1', 0)
        .attr('y1', 100)
        .attr('x2', 20)
        .attr('y2', 100)
        .attr('stroke', getLinkColor('synergistic'))
        .attr('stroke-width', 1.5);
    
    legend.append('text')
        .attr('x', 25)
        .attr('y', 105)
        .text('Interaction')
        .attr('fill', '#ccc')
        .attr('font-size', '12px');
}

/**
 * Returns the appropriate color for a node based on its type
 * @param {string} type - Node type (material or prescription)
 * @returns {string} - Color code
 */
function getNodeColor(type) {
    switch (type) {
        case 'material':
            return '#5470c6';
        case 'prescription':
            return '#91cc75';
        default:
            return '#909399';
    }
}

/**
 * Returns the appropriate color for a link based on its type
 * @param {string} type - Link type
 * @returns {string} - Color code
 */
function getLinkColor(type) {
    switch (type) {
        case 'contains':
            return '#909399';
        case 'synergistic':
            return '#67c23a';
        case 'antagonistic':
            return '#f56c6c';
        default:
            return '#e6a23c';
    }
}

/**
 * Returns the radius for a node based on its type and properties
 * @param {Object} node - Node data
 * @returns {number} - Radius value
 */
function getNodeRadius(node) {
    return node.type === 'material' ? 10 : 15;
}

/**
 * Generates tooltip text for a node
 * @param {Object} node - Node data
 * @returns {string} - Tooltip text
 */
function getNodeTooltip(node) {
    if (node.type === 'material') {
        return `${node.name}\nProperty: ${node.property || 'N/A'}\nFlavor: ${node.flavor || 'N/A'}\nMeridian: ${node.meridian || 'N/A'}`;
    } else {
        return `${node.name}\nEfficacy: ${node.efficacy || 'N/A'}`;
    }
}

/**
 * Handles start of node dragging
 * @param {Event} event - Drag event
 */
function dragStarted(event) {
    if (!event.active) graphSimulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
}

/**
 * Handles node dragging
 * @param {Event} event - Drag event
 */
function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
}

/**
 * Handles end of node dragging
 * @param {Event} event - Drag event
 */
function dragEnded(event) {
    if (!event.active) graphSimulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
}

/**
 * Filters the graph to show only nodes related to a specific material
 * @param {number} materialId - ID of the material to filter by
 */
function filterByMaterial(materialId) {
    // Redirect to knowledge graph with material filter
    window.location.href = `/knowledge-graph?material_id=${materialId}`;
}

/**
 * Filters the graph to show only nodes related to a specific prescription
 * @param {number} prescriptionId - ID of the prescription to filter by
 */
function filterByPrescription(prescriptionId) {
    // Redirect to knowledge graph with prescription filter
    window.location.href = `/knowledge-graph?prescription_id=${prescriptionId}`;
}

/**
 * Resets the graph to show all nodes
 */
function resetGraph() {
    // Redirect to knowledge graph without filters
    window.location.href = '/knowledge-graph';
}

// Initialize knowledge graph when page loads
document.addEventListener('DOMContentLoaded', function() {
    const graphContainer = document.getElementById('knowledge-graph');
    if (graphContainer) {
        initKnowledgeGraph('knowledge-graph');
        
        // Add event listener for window resize
        window.addEventListener('resize', () => {
            graphWidth = graphContainer.clientWidth;
            if (graphSvg) {
                graphSvg.attr('width', graphWidth);
                
                // Update center force if simulation exists
                if (graphSimulation) {
                    graphSimulation.force('center', d3.forceCenter(graphWidth / 2, graphHeight / 2));
                    graphSimulation.alpha(0.3).restart();
                }
            }
        });
    }
});
