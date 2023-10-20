const vscode = require("vscode");
const path = require("path");
const fs = require("fs");

async function code_companion_query(query) {
  
  const urlQuery = `http://localhost:5000/query?question=${query}`;

  try {
    const response = await fetch(urlQuery);

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.text();
    console.log('Data:', data);
    return data; // Return the response data

  } catch (error) {
    console.error('Error:', error);
    throw error; 
  }
}


function activate(context) {
  let disposable = vscode.commands.registerCommand(
    "extension.startCodeCompanion",
    () => {
      const panel = vscode.window.createWebviewPanel(
        "inputPanel",
        "MS Graph Assistant",
        vscode.ViewColumn.One,
        {
          enableScripts: true,
        }
      );

      const extensionPath = context.extensionPath;
      const styleOnDiskPath = vscode.Uri.joinPath(context.extensionUri, 'style.css');
      const stylePath = panel.webview.asWebviewUri(styleOnDiskPath);
      const scriptOnDiskPath = vscode.Uri.joinPath(context.extensionUri, 'script.js');
      const scriptPath = panel.webview.asWebviewUri(scriptOnDiskPath);
      const imgOnDiskPath = vscode.Uri.joinPath(context.extensionUri, 'resources', 'welcome.png');
      const imgPath = panel.webview.asWebviewUri(imgOnDiskPath);
      
      panel.webview.html = getWebviewContentFromFile(extensionPath, stylePath, scriptPath, imgPath);


      panel.webview.onDidReceiveMessage(
        async (message) => {
          if (message.command === "processInput") {
            const imageUri = vscode.Uri.file(context.asAbsolutePath('resources/question.png'));
            const imageSrc = panel.webview.asWebviewUri(imageUri).toString();
  
            panel.webview.postMessage({command: "inputImg", imgSrc: imageSrc});
            const inputText = message.text;
            //runPythonScript(context, false, inputText, extensionPath, panel);
            const responseimageUri = vscode.Uri.file(context.asAbsolutePath('resources/chatbot.png'));
            const responseimageSrc = panel.webview.asWebviewUri(responseimageUri).toString();
            panel.webview.postMessage({command: "output", imgSrc: responseimageSrc});
            data = await code_companion_query(inputText);
            //const jsonObject = JSON.parse(data);
           // console.log(jsonObject);
            panel.webview.postMessage({command: "output-completed", text: data});
          }
        },
        undefined,
        context.subscriptions
      );
    }
  );

  context.subscriptions.push(disposable);
}


function getWebviewContentFromFile(extensionPath, stylePath, scriptPath) {
  return `
  <html>

  <head>
      <title>Microsoft Graph Assistant</title>
      <link rel="stylesheet" type="text/css" href="${stylePath}">
  </head>

  <body>
    <h1 style="text-align: center;">Microsoft Graph Assistant</h1>
    <div id="bodyContent">
        <div id="outputContainer">
            <!-- Rendered input and "Input processed" lines will appear here -->
        </div>
        <div class="bottom-container">
            <input type="text" id="textInput" placeholder="Enter text here">
            <button id="processButton">Submit</button>
        </div>
    </div>
    <script src="${scriptPath}"></script>
  </body
  </html>
  `
}

module.exports = {
  activate
};
