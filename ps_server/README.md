# Localhost File Server Using PowerShell

A lightweight, visually stunning local file server written entirely in PowerShell. This script allows you to instantly serve the contents of any directory over HTTP with a modern, responsive dark theme.

## 🌟 Features

* **Modern Dark UI:** A sleek, CSS-styled directory listing with hover effects and a clean layout.
* **Dynamic File Sizes:** Automatically formats file sizes into readable formats (B, KB, MB, GB).
* **Timestamps:** Displays the "Last Modified" date and time for all files and folders.
* **Hidden Files Toggle:** By default, hidden system files stay hidden. Use a simple switch to reveal them.
* **Zero Dependencies:** Uses built-in .NET classes (`System.Net.HttpListener`). No Node.js, Python, or external installations required.

## ⚠️ Prerequisites

* **Windows OS** with PowerShell 5.1 or newer.
* **Administrator Privileges:** The script must be run as an Administrator to bind to network ports using `HttpListener`.

## 🚀 How to Use

1. Save the script as `server.ps1`.
2. Open PowerShell as an **Administrator**.
3. Navigate to the folder you want to serve (or specify it using the `-path` parameter).
4. Run the script:

    ```powershell
    .\server.ps1

    ```

Open your browser and navigate to `http://localhost:8080/` to view your files.

## ⚙️ Parameters

You can customize the server's behavior using the following parameters:

| Parameter | Default Value | Description |
| --- | --- | --- |
| `-path` | Current Directory | The absolute or relative path to the folder you want to serve. |
| `-port` | `8080` | The port number the server will listen on. |
| `-ShowHidden` | `$false` | A switch that, when included, forces the server to display hidden files and folders. |

### Examples

**Serve a specific directory on a custom port:**

```powershell
.\server.ps1 -path "C:\Users\Public\Documents" -port 9000

```

**Serve the current directory and show hidden files:**

```powershell
.\server.ps1 -ShowHidden

```

## 🛑 Stopping the Server

To stop the server, simply click into the PowerShell window where it is running and press `Ctrl + C`. The script includes a `finally` block that will safely clean up and dispose of the HTTP listener.

---

Would you like me to add a section to this README explaining how to add the script to your system's PATH so you can launch the server from anywhere using a simple command?