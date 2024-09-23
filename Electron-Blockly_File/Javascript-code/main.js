/**
 * @file
 * This file is the main process of the Electron application. It initializes the app,
 * manages inter-process communication (IPC) between the renderer and the main process,
 * and handles file operations, including saving, reading, and modifying files.
 * It also provides functionality to run external scripts, such as the 'blockify' script.
 * The file handles:
 * - Initializes the Electron BrowserWindow and loads the renderer (index.html).
 * - Handles file I/O operations like reading, writing, and modifying Python files.
 * - Interacts with the renderer process via IPC (save, read, start script commands).
 * - Clears cache, cookies, and storage data before launching the main window.

 * The file is automatically executed when the Electron application starts. It sets up
 * the main process and connects the back-end functionality to the front-end interface.
 */


import { app, BrowserWindow, ipcMain, dialog, session } from 'electron';
import path from 'path';
import fs from 'fs';
import readline from 'readline';
import { promises as gf } from 'fs';

const filePathTraining = './generatedCode/Error.py';
const filePaths = [];
import { exec } from 'child_process';

let currentPath = filePathTraining;
/**
 * Must be called at the beginning of the Electron process
 * Creates the initial view and loads the index.html file
 */
function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false, // Consider enabling context isolation in production for security reasons
        },
    });

    win.loadFile('./renderer/index.html');
}
/**
 * Give path to desired directory and delete all files included
 * Is used everytime we start the project to ensure the generatedCode folder won't store redundant files

 */
async function deleteDirContent(directory) {
    try {
        const files = await gf.readdir(directory);  // Get list of files/directories inside the directory

        for (const file of files) {
            const filePath = path.join(directory, file);
            const stat = await gf.lstat(filePath);  // Get file/directory status (to check if it's a directory)

            if (stat.isDirectory()) {
                await gf.rmdir(filePath, { recursive: true });  // Remove directory and its contents
            } else {
                await gf.unlink(filePath);  // Remove file
            }
        }
        console.log(`All contents deleted from ${directory}`);
    } catch (err) {
        console.error(`Error while deleting contents of ${directory}.`, err);
    }
}

app.whenReady().then(() => {
    // Clear cache, cookies, storage, and other session data before creating the window
    const ses = session.defaultSession;

    // Clear cache
    ses.clearCache().then(() => {
        console.log('Cache cleared');
    });

    // Clear cookies
    ses.clearStorageData({ storages: ['cookies'] }).then(() => {
        console.log('Cookies cleared');
    });

    // Clear local storage, session storage, indexedDB, and other storage data
    ses.clearStorageData({
        storages: ['localstorage', 'sessions', 'indexdb', 'websql', 'serviceworkers', 'cachestorage'],
    }).then(() => {
        console.log('All session storage data cleared');

        // Now create the window
        createWindow();
        const filePath = path.join('./projectsrc/projectskeleton.py');
        console.log("READING FILE");

        fs.readFile(filePath, 'utf-8', (err, data) => {
            console.log("reading...");
            if (err) {
                console.error('Failed to load file:', err);
                return;
            }


        });
    }).catch(err => {
        console.error('Error clearing storage data:', err);
        // Still create the window even if there was an error clearing data
        createWindow();
    });


});
/**
 * Inserts a comment at a specified line in a file.
 * The comment will be in the format `#viewName+\n#viewName-` where `viewName` is provided as a parameter.
 *
 * @param {string} filePath - The path to the file where the comment will be inserted.
 * @param {string} viewName - The name to be used in the comment (used to generate `#viewName+` and `#viewName-`).
 * @param {number} lineIndex - The index at which the comment should be inserted. The index should be 0-based.
 *
 * @throws {Error} If there's an issue reading or writing to the file.
 * @throws {RangeError} If the lineIndex is out of bounds of the file's total lines.
 *
 * @example
 * // Inserts a comment in the file at line 5:
 * insertCommentAtLine('/path/to/file.txt', 'MyView', 5);
 */
function insertCommentAtLine(filePath, viewName, lineIndex) {
    try {
        // Read the current content of the file
        let content = fs.readFileSync(filePath, 'utf8');

        // Split the content into an array of lines
        let lines = content.split('\n');

        // Create the comment to be inserted
        const comment = `#${viewName}+\n#${viewName}-`;

        // Insert the comment at the specified line index
        if (lineIndex >= 0 && lineIndex <= lines.length) {
            lines.splice(lineIndex, 0, comment);  // Insert the comment at the given index
        } else {
            console.error("Line index out of bounds");
            return;
        }

        // Join the lines back together and write the modified content back to the file
        const updatedContent = lines.join('\n');
        fs.writeFileSync(filePath, updatedContent, 'utf8');

        console.log(`Comment successfully inserted at line ${lineIndex}`);
    } catch (err) {
        console.error('Error while modifying the file:', err);
    }
}


/**
 * Saves the given code to the current file path.
 *
 * @param {Electron.IpcMainEvent} event - The IPC event.
 * @param {string} code - The code content to be saved to the file.
 */
ipcMain.on('save-code-to-file', async (event, code) => {
    fs.writeFileSync(currentPath, code);
});

/**
 * Saves each code block in `codeArray` to corresponding files in `filePaths`.
 * If the path or file is undefined, the operation for that index is skipped.
 *
 * @param {Electron.IpcMainEvent} event - The IPC event.
 * @param {string[]} codeArray - Array of code blocks to be saved.
 */
ipcMain.on('save-block-to-file', async (event, codeArray) => {
    for (let i = 0; i < currentPath.length; i++) {
        if (currentPath[i] === undefined || filePaths[i] === undefined) {
            console.log(`Skipping save for index ${i} due to undefined path or file.`);
            continue;
        }

        try {
            console.log("Saving " + codeArray[i] + " to " + filePaths[i]);
            fs.writeFileSync(filePaths[i], codeArray[i]);
        } catch (error) {
            console.error(`Error saving file at ${filePaths[i]}: ${error.message}`);
        }
    }
});

/**
 * Reads the content of `output.json` and sends it back via the IPC event.
 *
 * @param {Electron.IpcMainEvent} event - The IPC event.
 */
ipcMain.on('read-outputjson', async (event) => {
    const functionNamesContent = fs.readFileSync('./output.json', 'utf8');
    const functionNamesJson = JSON.parse(functionNamesContent);
    console.log("Are in server now");
    event.sender.send('response-outputjson', functionNamesJson);
});

/**
 * Reads the lines of a specified file and logs each line.
 *
 * @param {Electron.IpcMainEvent} event - The IPC event.
 */
ipcMain.on('read-file', (event) => {
    const filePath = 'projectsrc/CodeToBlockDemo.py';
    const readInterface = readline.createInterface({
        input: fs.createReadStream(filePath),
        output: process.stdout,
        console: false,
    });

    readInterface.on('line', (line) => {
        console.log('Reading ..' + line);
    });
});

/**
 * Changes the current file path based on the selected view index.
 *
 * @param {Electron.IpcMainEvent} event - The IPC event.
 * @param {number} view - The index of the view to change to.
 */
ipcMain.on('change-view-option', (event, view) => {
    currentPath = filePaths[view];
    console.log('Current Path is:', currentPath);
});

/**
 * Creates a new Python file for the given view name and sends confirmation.
 *
 * @param {Electron.IpcMainEvent} event - The IPC event.
 * @param {string} viewName - The name of the view to create a file for.
 * @param {number} index - The index at which to add the view.
 */
ipcMain.on('create-new-view', (event, viewName, index) => {
    const filePath = `./generatedCode/${viewName}.py`;
    filePaths.push(filePath);
    fs.writeFileSync(filePath, '', 'utf8');
    event.sender.send('new-view-created', { message: `File created: ${viewName}`, viewName: viewName });
});

/**
 * Creates a new Python file and inserts a comment in a skeleton Python file at the specified index.
 *
 * @param {Electron.IpcMainEvent} event - The IPC event.
 * @param {string} viewName - The name of the view.
 * @param {number} index - The line index to insert the comment.
 */
ipcMain.on('create-new-view-with-index', (event, viewName, index) => {
    const filePath = `./generatedCode/${viewName}.py`;
    filePaths.push(filePath);
    fs.writeFileSync(filePath, '', 'utf8');
    const filePath2 = './projectsrc/projectskeleton.py';
    insertCommentAtLine(filePath2, viewName, index);
    event.sender.send('new-view-created', { message: `File created: ${viewName}`, viewName: viewName });
});

/**
 * Writes the updated code to the destination file.
 *
 * @param {Electron.IpcMainEvent} event - The IPC event.
 * @param {string} updatedCode - The updated code to save.
 * @param {string} destPath - The destination file path to save the code.
 */
ipcMain.on('submit-changes', (event, updatedCode, destPath) => {
    console.log(updatedCode);
    fs.writeFileSync(destPath, updatedCode, 'utf8');
});

/**
 * Opens a file dialog, deletes the content of the `generatedCode` directory,
 * writes the selected file to the project source, and runs the 'blockify' script.
 *
 * @param {Electron.IpcMainEvent} event - The IPC event.
 * @param {number} cheatCount - The count passed to the 'blockify' script.
 */
ipcMain.on('start-script', async (event, cheatCount) => {

    try {
        const { filePath } = await dialog.showSaveDialog({
            buttonLabel: 'Select file',
            filters: [{ name: 'Python Files', extensions: ['py'] }]
        });

        if (!filePath) {
            throw new Error('No file selected');
        }

        const sourceFile = fs.readFileSync(filePath, 'utf8');
        //const generatedCodePath = '../generatedCode';
        //await deleteDirContent(generatedCodePath);
        fs.writeFileSync('./projectsrc/projectsrc.py', sourceFile);

        exec('npm run blockify ' + cheatCount, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing blockify: ${error}`);
                event.sender.send('script-error', `Error: ${stderr}`);
            } else {
                console.log('Script executed successfully:', stdout);
                event.sender.send('load-blocks', filePath);
            }
        });

    } catch (error) {
        console.error(`Caught error: ${error.message}`);
        event.sender.send('script-error', error.message);
    }
});

ipcMain.on('open-Doc', async (event, cheatCount) => {




        exec('npm run docs ' + cheatCount, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error opening docs: ${error}`);
                event.sender.send('script-error', `Error: ${stderr}`);
            }
        });


});

/**
 * Quits the app when all windows are closed (except on macOS).
 */
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

/**
 * Reopens the app when activated, specifically for macOS.
 */
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
