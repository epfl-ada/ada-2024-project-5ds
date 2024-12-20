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

// Import parameters from JSON
const parameters = await fetch('/ada-2024-project-5ds/assets/mad_lab_parameters.json').then(res => res.json());
const { svm, preprocessing } = parameters;


// Scale numerical values
function scale(value, mean, scale) {
    return (value - mean) / scale;
}

// Preprocess user input
function preprocessInput(titleLength, category, boxOffice, runtime) {
    const categoryMapping = preprocessing.categories;
    const scalingParams = preprocessing.scaling;

    const genreEncoded = categoryMapping[category];
    const scaledBoxOffice = scale(boxOffice, scalingParams.mean[0], scalingParams.scale[0]);
    const scaledRuntime = scale(runtime, scalingParams.mean[1], scalingParams.scale[1]);

    return [titleLength, genreEncoded, scaledBoxOffice, scaledRuntime];
}

function rbfKernel(supportVector, inputVector, gamma) {
    let squaredDistance = 0;
    for (let i = 0; i < supportVector.length; i++) {
        squaredDistance += Math.pow(supportVector[i] - inputVector[i], 2);
    }
    return Math.exp(-gamma * squaredDistance);
}

function predict(inputVector) {
    const { support_vectors, dual_coefficients, intercept, gamma } = svm;

    let decisionValue = intercept[0];

    for (let i = 0; i < support_vectors.length; i++) {
        const kernelValue = rbfKernel(support_vectors[i], inputVector, gamma);
        decisionValue += dual_coefficients[0][i] * kernelValue;
    }

    return decisionValue >= 0 ? 'Likely to Win' : 'Unlikely to Win';
}

function handlePrediction() {
    // Get user inputs
    console.log('Handling prediction');

    const titleLength = parseFloat(document.getElementById('title-length').value);
    const category = document.getElementById('categories').value;
    const boxOffice = parseFloat(document.getElementById('box-office').value);
    const runtime = parseFloat(document.getElementById('runtime').value);

    // Preprocess input
    const inputVector = preprocessInput(titleLength, category, boxOffice, runtime);

    // Predict
    const prediction = predict(inputVector);

    // Display result
    document.getElementById('prediction-result').innerHTML = `
        <h3>Prediction Result:</h3>
        <p><strong>Prediction:</strong> ${prediction}</p>
    `;
}

