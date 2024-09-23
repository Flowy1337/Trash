/**
 * @file: preload.js
 *
 * Description:
 * This script runs in the context of the renderer process and acts as a bridge
 * between the main process and the renderer. It uses Electron's contextBridge
 * API to securely expose certain functionalities to the renderer.
 *

 */
const { contextBridge, ipcRenderer } = require('electron');

window.addEventListener('DOMContentLoaded', () => {
    contextBridge.exposeInMainWorld('electronAPI', {
        saveCodeToFile: (data) => ipcRenderer.send('save-code-to-file', data),
        receiveCodeSaveStatus: (callback) => ipcRenderer.on('code-save-status', (event, ...args) => callback(...args)),
        createNewView: (viewName) => ipcRenderer.invoke('createNewView', viewName)
    });
});




