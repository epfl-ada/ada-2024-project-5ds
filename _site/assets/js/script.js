// Toggle Dropdown Visibility
function toggleDropdown() {
    document.getElementById("dropdown-content").classList.toggle("show");
}

function hideDropdown() {
    document.getElementById("dropdown-content").classList.remove("show");
}

// Show Selected Content
function showContent(sectionId) {
    // Hide all content sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.style.display = 'none');
    
    // Show the selected section
    document.getElementById(sectionId).style.display = 'block';

    // Hide dropdown
    hideDropdown();
}

let isFirstGraph = true;

function switchGraph() {
    // Get graph elements
    const graph1 = document.getElementById('graph1');
    const graph2 = document.getElementById('graph2');
    const graphCaption = document.getElementById('graph-caption');

    // Toggle visibility
    if (isFirstGraph) {
        graph1.style.display = 'none';
        graph2.style.display = 'block';
        graphCaption.innerHTML = `<p>A visualization showing another perspective on genre representation.</p>`;
    } else {
        graph1.style.display = 'block';
        graph2.style.display = 'none';
        graphCaption.innerHTML = `<p>A visualization showing the genre breakdown of movies featuring Oscar-winning actors.</p>`;
    }

    // Toggle graph state
    isFirstGraph = !isFirstGraph;
}
