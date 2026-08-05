const startScan = async () => {
  if (!file) {
    alert("Please select a file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/analysis/malware",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Scan failed");
    }

    console.log("Malware Analysis:", data);

    alert(
      `Result: ${data.analysis.prediction}\n` +
      `Risk: ${data.analysis.risk}\n` +
      `Confidence: ${data.analysis.confidence}%`
    );

  } catch (error) {
    console.error(error);
    alert("Unable to analyze the file. Make sure the backend is running.");
  }
};
