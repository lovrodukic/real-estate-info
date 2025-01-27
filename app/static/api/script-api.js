document.getElementById("address-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const address = document.getElementById("address").value;
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "<p>Fetching property details...</p>";

    try {
      // Fetch property details
      const propertyResponse = await fetch("/api/fetch-property", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address: address })
      });

      const propertyData = await propertyResponse.json();

      if (propertyResponse.status !== 200) {
        resultDiv.innerHTML = `
          <p style="color:red;">Error: ${propertyData.error}</p>
        `;
        return;
      }

      // Display the JSON to the page
      resultDiv.innerHTML = `
          <h3>Response:</h3>
          <pre>${JSON.stringify(propertyData, null, 2)}</pre>
      `;

    } catch (error) {
      resultDiv.innerHTML = `<p style="color:red;">Error fetching data.</p>`;
      console.error(error);
    }
  });
