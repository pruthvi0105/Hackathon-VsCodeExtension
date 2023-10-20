const vscode = require("vscode");
const path = require("path");
const fs = require("fs");

const { exec } = require("child_process");

function runPythonScript(extensionPath) {
  const scriptPath = path.join(extensionPath, "src/code_companion_server.py");
  const pythonProcess = exec(
    `python ${scriptPath}`,
    (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Python script: ${error}`);
        return;
      }

      console.log(`Python script output: ${stdout}`);
    }
  );

  pythonProcess.stdin.end(); // Close the stdin stream to signal end of input
}

async function init_code_companion(folderpath) {
  // URL for the GET request
  const url = `http://localhost:5000/init?path=${folderpath}`;
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

async function code_companion_query(query) {
  const urlQuery = `http://localhost:5000/query?query=${query}`;

  try {
    const response = await fetch(urlQuery);

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.text();
    console.log("Data:", data);
    return data; // Return the response data
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

function stop_code_companion() {
  // URL for the GET request
  const url = `http://localhost:5000/shutdown`;
  try {
    const response = fetch(url);

    response.catch((error) => {
      return;
    });
    return;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

function activate(context) {
  let disposable = vscode.commands.registerCommand(
    "extension.startCodeCompanion",
    () => {
      const panel = vscode.window.createWebviewPanel(
        "inputPanel",
        "Code Companion",
        vscode.ViewColumn.One,
        {
          enableScripts: true,
        }
      );

      const extensionPath = context.extensionPath;
      const styleOnDiskPath = vscode.Uri.joinPath(
        context.extensionUri,
        "style.css"
      );
      const stylePath = panel.webview.asWebviewUri(styleOnDiskPath);
      const scriptOnDiskPath = vscode.Uri.joinPath(
        context.extensionUri,
        "script.js"
      );
      const scriptPath = panel.webview.asWebviewUri(scriptOnDiskPath);
      const welcomeScriptOnDiskPath = vscode.Uri.joinPath(
        context.extensionUri,
        "welcome.js"
      );
      const welcomeScriptPath = panel.webview.asWebviewUri(
        welcomeScriptOnDiskPath
      );
      const imgOnDiskPath = vscode.Uri.joinPath(
        context.extensionUri,
        "resources",
        "welcome.png"
      );
      const imgPath = panel.webview.asWebviewUri(imgOnDiskPath);
      runPythonScript(extensionPath);
      panel.webview.html = getLoadingPage(stylePath);
      setTimeout(() => {
        panel.webview.html = getWebviewContentForWelcomePage(
          extensionPath,
          stylePath,
          welcomeScriptPath,
          imgPath
        );
      }, 5000);

      panel.webview.onDidReceiveMessage((message) => {
        if (message.command === "selectFolder") {
          vscode.window
            .showOpenDialog({
              canSelectFiles: false,
              canSelectFolders: true,
              canSelectMany: false,
              openLabel: "Select Folder",
            })
            .then((uri) => {
              if (uri && uri.length > 0) {
                const folderPath = uri[0].fsPath;
                panel.webview.postMessage({
                  command: "folderSelected",
                  folderPath,
                });
              }
            });
        }
      });

      panel.webview.onDidReceiveMessage(
        async (message) => {
          if (message.command === "startExtension") {
            vscode.window.showInformationMessage(`Loading Code Companion`);
            const folderpath = message.text;

            await init_code_companion(folderpath);

            panel.webview.html = getWebviewContentFromFile(
              extensionPath,
              stylePath,
              scriptPath,
              imgPath
            );
          }
        },
        undefined,
        context.subscriptions
      );

      panel.webview.onDidReceiveMessage(
        async (message) => {
          if (message.command === "processInput") {
            const imageUri = vscode.Uri.file(
              context.asAbsolutePath("resources/question.png")
            );
            const imageSrc = panel.webview.asWebviewUri(imageUri).toString();

            panel.webview.postMessage({
              command: "inputImg",
              imgSrc: imageSrc,
            });
            const inputText = message.text;
            //runPythonScript(context, false, inputText, extensionPath, panel);
            const responseimageUri = vscode.Uri.file(
              context.asAbsolutePath("resources/chatbot.png")
            );
            const responseimageSrc = panel.webview
              .asWebviewUri(responseimageUri)
              .toString();
            panel.webview.postMessage({
              command: "output",
              imgSrc: responseimageSrc,
            });
            data = await code_companion_query(inputText);
            panel.webview.postMessage({
              command: "output-completed",
              text: data,
            });
          }
        },
        undefined,
        context.subscriptions
      );
    }
  );

  context.subscriptions.push(disposable);
}

function getLoadingPage(stylePath) {
  return `
  <html>
  <head>
      <link rel="stylesheet" type="text/css" href="${stylePath}">
  </head>
  <body style="display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;">
    <div class="loader"></div>
  </body>
  </html>
  `;
}

function getWebviewContentForWelcomePage(
  extensionPath,
  stylePath,
  scriptPath,
  imgPath
) {
  return `
  <html>

  <head>
      <title>Welcome to Code Companion</title>
      <link rel="stylesheet" type="text/css" href="${stylePath}">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
  </head>

  <body>
    <div id="welcomeDiv">
      <img src="${imgPath}" id="welcomeImg"></img>
      <h1 style="text-align: center;">Welcome to Code Companion!</h1>
      <div id ="start-div">
        <div id="folder-input">
          <button id="selectFolderButton"><i class="fa-solid fa-folder-open" style="color: #ffffff;"></i></button>
          <div id="selectedFolderPath">Select a folder to start</div>
        </div>
      <button id="startButton"> Start </button>
      </div>
    </div>
    <script src="${scriptPath}"></script>
  </body
  </html>
  `;
}

function getWebviewContentFromFile(
  extensionPath,
  stylePath,
  scriptPath,
  imgPath
) {
  return `
  <html>

  <head>
      <title>Code Companion</title>
      <link rel="stylesheet" type="text/css" href="${stylePath}">
  </head>

  <body>
    <h1 style="text-align: center;">Code Companion</h1>
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
  `;
}

let isDeactivating = false;
function deactivate() {
  if (isDeactivating) {
    return;
  }

  isDeactivating = true;

  try {
    stop_code_companion();
    console.log("Extension is being deactivated");
  } catch (error) {
    console.error("Error deactivating extension:", error);
  }
}

module.exports = {
  activate,
  deactivate,
};
