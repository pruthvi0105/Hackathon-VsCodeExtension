const vscode = acquireVsCodeApi();

document.getElementById("processButton").addEventListener("click", () => {
    console.log("Processed.")
    const inputBotImg = document.createElement('img');
    inputBotImg.classList.add('outputBotImg'); // Apply the 'outputDiv' CSS class
    window.addEventListener('message', event => {
      const message = event.data; // The JSON data our extension sent
      switch (message.command) {
          case 'inputImg':
            inputBotImg.src = message.imgSrc;
            break;
          }
      });
    const inputText = document.getElementById("textInput").value;
    const outputContainer = document.getElementById('outputContainer');
    
    // Create a new div element for the input lines
    if (inputText.trim() !== ""){
      const inputDiv = document.createElement('div');
      inputDiv.classList.add('inputDiv'); // Apply the 'inputDiv' CSS class
      const inputLine = document.createElement('p');
      inputLine.textContent = inputText;

      // Append the lines to the container
      inputDiv.appendChild(inputBotImg);
      inputDiv.appendChild(inputLine);
      outputContainer.appendChild(inputDiv);

      // Clear the input field
      textInput.value = '';

      vscode.postMessage({
          command: "processInput",
          text: inputText,
      });
    }
    else
    {
      console.log("Input is empty");
    }
});


window.addEventListener('message', event => {
  const message = event.data; // The JSON data our extension sent
  switch (message.command) {
      case 'output':
          const outputDiv = document.createElement('div');
          outputDiv.classList.add('outputDiv'); // Apply the 'outputDiv' CSS class
          const outputBotImg = document.createElement('img');
          outputBotImg.classList.add('outputBotImg'); // Apply the 'outputDiv' CSS class
          outputBotImg.src = message.imgSrc;
          const loadingDiv = document.createElement('div');
          loadingDiv.classList.add('dot-flashing');
          loadingDiv.setAttribute('id', 'loading-div');
          // Append the lines to the container
          outputDiv.appendChild(outputBotImg);
          outputDiv.appendChild(loadingDiv);
          outputContainer.appendChild(outputDiv);

          // This logs the received text to the console
          console.log(`Received output: ${message.text}`);
          break;
  }
});

window.addEventListener('message', event => {
  const message = event.data; // The JSON data our extension sent
  switch (message.command) {
      case 'output-completed':
        var loadingDiv = document.getElementById('loading-div');
        var outputDiv = loadingDiv.parentNode;
        loadingDiv.parentNode.removeChild(loadingDiv);
        
        const outputLine = document.createElement('p');
        outputLine.textContent = message.text;
        outputDiv.appendChild(outputLine);
        break;
  }
});