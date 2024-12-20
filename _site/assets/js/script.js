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
