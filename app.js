async function uploadImage() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image file first.");
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {  
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('result').innerHTML = `
                <h3>Prediction: ${data.prediction}</h3>
                <p>Precautions: ${data.precautions}</p>
            `;
        } else {
            document.getElementById('result').innerHTML = `<p>Error: Unable to fetch prediction.</p>`;
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById('result').innerHTML = `<p>Error: Something went wrong!</p>`;
    }
}