const vscode = acquireVsCodeApi();

document.getElementById("startButton").addEventListener("click", () => {
  console.log("Extension Started.")
  const folderPath = document.getElementById('selectedFolderPath').innerText;
  vscode.postMessage({
    command: "startExtension",
    text: folderPath,
  });
});

document.getElementById('selectFolderButton').addEventListener('click', () => {
  vscode.postMessage({ command: 'selectFolder' });
});

window.addEventListener('message', event => {
  const message = event.data;
  if (message.command === 'folderSelected') {
      document.getElementById("startButton").style.display = 'block';
      document.getElementById('selectedFolderPath').innerText = `${message.folderPath}`;
  }
});
