# PowerShell HTTP File Server (Pure PowerShell)

# Parameters
$port = 8080                             # Port to listen on
$rootPath = (Get-Location).Path          # Root directory for file serving
$rootDrive = [System.IO.Path]::GetPathRoot($rootPath) # Get the root of the current drive

# Start the file server
Write-Output "Starting file server on http://localhost:$port/"
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add("http://*:$port/")
$listener.Start()

try {
    while ($listener.IsListening) {
        # Get incoming request
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response

        # Determine the requested file or directory path
        $requestedPath = $request.Url.AbsolutePath.TrimStart('/')
        if ($requestedPath -eq '') { $requestedPath = '.' }

        $fullPath = Join-Path -Path $rootPath -ChildPath $requestedPath

        # Ensure the path is not outside the allowed root directory
        if ($fullPath -like "$rootDrive*") {
            if (Test-Path -Path $fullPath -PathType Leaf) {
                # Serve the file if it exists
                $fileBytes = [System.IO.File]::ReadAllBytes($fullPath)
                $response.ContentType = "application/octet-stream"
                $response.ContentLength64 = $fileBytes.Length
                $response.OutputStream.Write($fileBytes, 0, $fileBytes.Length)
            } elseif (Test-Path -Path $fullPath -PathType Container) {
                # If it's a directory, list the contents (like Python's http.server)
                $parentPath = if ($requestedPath -eq '.') { '' } else { (Split-Path $requestedPath -Parent) }
                $directories = Get-ChildItem -Path $fullPath | Where-Object { $_.PSIsContainer }
                $files = Get-ChildItem -Path $fullPath | Where-Object { -not $_.PSIsContainer }

                $htmlContent = "<html><body><h1>Directory listing</h1><ul>"

                # "." link: Go up one directory (move one step up)
                if ($requestedPath -ne '.' -and $parentPath) {
                    $htmlContent += "<li><a href='/$parentPath/'>.</a> (Move up)</li>"
                }

                # ".." link: Go to the root directory
                $htmlContent += "<li><a href='/'>/../</a></li>"

                # Display directories
                foreach ($dir in $directories) {
                    $htmlContent += "<li><a href='/$requestedPath/$($dir.Name)/'>$($dir.Name)/</a></li>"
                }

                # Display files
                foreach ($file in $files) {
                    $htmlContent += "<li><a href='/$requestedPath/$($file.Name)'>$($file.Name)</a></li>"
                }

                $htmlContent += "</ul></body></html>"
                $response.ContentType = "text/html"
                $response.ContentLength64 = [System.Text.Encoding]::UTF8.GetByteCount($htmlContent)
                $response.OutputStream.Write([System.Text.Encoding]::UTF8.GetBytes($htmlContent), 0, $htmlContent.Length)
            } else {
                # File or directory not found, send a 404 response
                $response.StatusCode = 404
                $errorMessage = [System.Text.Encoding]::UTF8.GetBytes("404 - File or Directory Not Found")
                $response.OutputStream.Write($errorMessage, 0, $errorMessage.Length)
            }
        } else {
            # If the requested path is outside the root path, send an access denied response
            $response.StatusCode = 403
            $errorMessage = [System.Text.Encoding]::UTF8.GetBytes("403 - Access Denied")
            $response.OutputStream.Write($errorMessage, 0, $errorMessage.Length)
        }

        # Close the response
        $response.OutputStream.Close()
    }
} catch {
    Write-Output "An error occurred: $_"
} finally {
    # Stop the listener when done
    $listener.Stop()
    Write-Output "File server stopped."
}
