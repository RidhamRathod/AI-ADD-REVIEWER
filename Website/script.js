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

    fetch("http://127.0.0.1:5000/upload", {  // Update if your API is hosted elsewhere
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerHTML = `<p style="color: red;"><strong>Error:</strong> ${data.error}</p>`;
            return;
        }

        // Generate results dynamically
        let resultHTML = `
            <h3 style="text-align: center;">Analysis Results</h3>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 10px; margin-top: 15px;">
        `;

        // Iterate over each result and add it dynamically
        const analysisKeys = [
            "Aesthetic Score", "Color Psychology", "Contrast Analysis", 
            "Brightness Analysis", "Image Blurriness", "Readability", 
            "Sentiment Analysis", "Grammar", "Call To Action"
        ];

        analysisKeys.forEach(key => {
            resultHTML += `
                <div style="width: 80%; max-width: 500px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; text-align: center;">
                    <p><strong>${key}:</strong> ${data.analysis_results[key]}</p>
                </div>
            `;
        });

        resultHTML += `</div>`;

        // Add the final explanation
        resultHTML += `
            <div style="width: 90%; max-width: 600px; margin-top: 20px; padding: 15px; background-color: #f9f9f9; border-left: 5px solid #4CAF50; border-radius: 5px;">
                <h4 style="text-align: center;">Final Explanation</h4>
                <p style="text-align: justify; font-size: 16px;">${data.final_explanation}</p>
            </div>
        `;

        document.getElementById("result").innerHTML = resultHTML;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = "<p style='color: red;'>Error analyzing image.</p>";
    });
}
