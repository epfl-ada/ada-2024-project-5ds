

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

async function handlePrediction() {
    // Get user inputs
    const title = document.getElementById('movie-title').value.trim();
    const titleLength = title.length; // Calculate title length
    const category = document.getElementById('categories').value;
    const boxOffice = parseFloat(document.getElementById('box-office').value);
    const runtime = parseFloat(document.getElementById('runtime').value);

    // Preprocess input
    const inputVector = preprocessInput(titleLength, category, boxOffice, runtime);

    // Predict
    const prediction = predict(inputVector);

    // Generate movie description
    const description = `
        <p><strong>Movie Title:</strong> "${title}"</p>
        <p><strong>Title Length:</strong> ${titleLength} characters</p>
        <p><strong>Movie Genre:</strong> ${category}</p>
        <p><strong>Box Office Revenue:</strong> $${boxOffice}M</p>
        <p><strong>Runtime:</strong> ${runtime} minutes</p>
    `;

    // Display result
    document.getElementById('prediction-result').innerHTML = `
        <h3>Prediction Result:</h3>
        ${description}
        <p><strong>Prediction:</strong> ${prediction}</p>
        <p><strong>Explanation:</strong> Based on the provided details, the movie is ${
            prediction === 'Likely to Win' ? 'likely to win' : 'unlikely to win'
        } an Oscar. Factors such as title, genre, runtime, and box office revenue were considered.</p>
    `;
}



