// Toggle Dropdown Visibility
function toggleDropdown() {
    document.getElementById("dropdown-content").classList.toggle("show");
}

// Show Selected Content
function showContent(sectionId) {
    // Hide all content sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.style.display = 'none');
    
    // Show the selected section
    document.getElementById(sectionId).style.display = 'block';
}


function switchGraph() {
    // Get the graph container and caption
    const graphContainer = document.getElementById('graph-container');
    const graphCaption = document.getElementById('graph-caption');

    // Check the current graph and toggle
    if (graphContainer.innerHTML.includes('actors_genres_histo.html')) {
        // Switch to the new graph
        graphContainer.innerHTML = `
            {% include plots/genres_cloud.html %}
            <div id="graph-caption" class="plot-caption">
                <p>A visualization showing another perspective on genre representation.</p>
            </div>
        `;
    } else {
        // Switch back to the original graph
        graphContainer.innerHTML = `
            {% include plots/actors_genres_histo.html %}
            <div id="graph-caption" class="plot-caption">
                <p>A visualization showing the genre breakdown of movies featuring Oscar-winning actors.</p>
            </div>
        `;
    }
}
