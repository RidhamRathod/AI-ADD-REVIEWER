function uploadImage() {
    let fileInput = document.getElementById("imageInput");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select an image first!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    // Show loading message
    document.getElementById("result").innerHTML = "<p>Analyzing image, please wait...</p>";

    fetch("http://127.0.0.1:5000/upload", {  // Update this if your API is hosted elsewhere
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerHTML = `<p style="color: red;"><strong>Error:</strong> ${data.error}</p>`;
            return;
        }

        let resultText = `
            <h3>Analysis Results:</h3>
            <p><strong>Aesthetic Score:</strong> ${data["Aesthetic Score"]}</p>
            <p><strong>Color Psychology:</strong> ${data["Color Psychology"]}</p>
            <p><strong>Contrast Analysis:</strong> ${data["Contrast Analysis"]}</p>
            <p><strong>Brightness Analysis:</strong> ${data["Brightness Analysis"]}</p>
            <p><strong>Image Blurriness:</strong> ${data["Image Blurriness"]}</p>
        `;
        document.getElementById("result").innerHTML = resultText;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = "<p style='color: red;'>Error analyzing image.</p>";
    });
}
