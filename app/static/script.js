document.getElementById("address-form").addEventListener("submit", async function (event) {
  event.preventDefault();

  const address = document.getElementById("address").value;
  const resultDiv = document.getElementById("result");

  resultDiv.innerHTML = "<p>Fetching property details...</p>";

  try {
    // Fetch property details
    const propertyResponse = await fetch("/fetch-property", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ address: address })
    });

    const propertyData = await propertyResponse.json();

    if (propertyResponse.status !== 200) {
      resultDiv.innerHTML = `<p style="color:red;">Error: ${propertyData.error}</p>`;
      return;
    }

    // Generate overview of property using LLM
    resultDiv.innerHTML = "<p>Generating summary...</p>";

    const summaryResponse = await fetch("/generate-summary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ property_info: propertyData.details })
    });

    const summaryData = await summaryResponse.json();

    if (summaryResponse.status !== 200) {
      resultDiv.innerHTML = `<p style="color:red;">Error: ${summaryData.error}</p>`;
      return;
    }

    // Display the summary to the page
    resultDiv.innerHTML = `
          <h3>AI-Generated Property Summary</h3>
          <p>${summaryData.summary}</p>
      `;

  } catch (error) {
    resultDiv.innerHTML = `<p style="color:red;">Error fetching data.</p>`;
    console.error(error);
  }
});
