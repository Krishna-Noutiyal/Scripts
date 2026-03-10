param(
    [string]$path = (Get-Location).Path,
    [int]$port = 8080,
    [switch]$ShowHidden
)

# Check for admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: This script requires administrator privileges. Please run as admin." -ForegroundColor Red
    exit 1
}

# Validate path exists
if (-not (Test-Path -Path $path -PathType Container)) {
    Write-Host "ERROR: Path does not exist: $path" -ForegroundColor Red
    exit 1
}

$rootPath = (Resolve-Path -Path $path).Path
Write-Host "Starting file server on http://localhost:$port/" -ForegroundColor Green
Write-Host "Serving files from: $rootPath" -ForegroundColor Cyan
if ($ShowHidden) { Write-Host "Showing hidden files." -ForegroundColor DarkGray }

$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add("http://*:$port/")

try {
    $listener.Start()
    
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response

        $requestedPath = $request.Url.AbsolutePath.TrimStart('/').TrimEnd('/')
        if ($requestedPath -eq '') { $requestedPath = '.' }

        $fullPath = Join-Path -Path $rootPath -ChildPath $requestedPath

        if ((Resolve-Path -Path $fullPath -ErrorAction SilentlyContinue).Path -like "$rootPath*") {
            if (Test-Path -Path $fullPath -PathType Leaf) {
                $fileBytes = [System.IO.File]::ReadAllBytes($fullPath)
                $response.ContentType = "application/octet-stream"
                $response.ContentLength64 = $fileBytes.Length
                $response.OutputStream.Write($fileBytes, 0, $fileBytes.Length)
            }
            elseif (Test-Path -Path $fullPath -PathType Container) {
                # Apply hidden files filter
                if ($ShowHidden) {
                    $items = Get-ChildItem -Path $fullPath -Force
                }
                else {
                    $items = Get-ChildItem -Path $fullPath
                }

                $htmlContent = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Directory: /$requestedPath</title>
    <style>
        :root { --bg: #0d1117; --text: #c9d1d9; --accent: #58a6ff; --card-bg: #161b22; --hover: #21262d; --border: #30363d; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; background-color: var(--bg); color: var(--text); margin: 0; padding: 20px; line-height: 1.5; }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { color: var(--text); border-bottom: 1px solid var(--border); padding-bottom: 15px; font-weight: 600; display: flex; align-items: center; gap: 10px; word-break: break-all; }
        ul { list-style: none; padding: 0; margin: 20px 0; }
        li { background: var(--card-bg); margin-bottom: 8px; border: 1px solid var(--border); border-radius: 6px; transition: all 0.2s ease; }
        li:hover { border-color: var(--accent); background: var(--hover); transform: translateX(2px); }
        a { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; color: var(--text); text-decoration: none; flex-wrap: wrap; gap: 10px; }
        .file-info { display: flex; align-items: center; gap: 10px; font-weight: 500; }
        .file-meta { display: flex; gap: 20px; color: #8b949e; font-size: 0.85em; font-family: Consolas, monospace; }
        .meta-size { width: 80px; text-align: right; }
        .meta-date { width: 140px; text-align: right; }
        .footer { text-align: center; margin-top: 40px; color: #8b949e; font-size: 0.85em; padding-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📁 /$requestedPath</h1>
        <ul>
"@
                if ($requestedPath -ne '.') {
                    $parent = Split-Path $requestedPath -Parent
                    $parentHref = if ($parent) { "/$parent" } else { "/" }
                    $htmlContent += "<li><a href='$parentHref'><span class='file-info'>⬅️ Parent Directory</span></a></li>"
                }
                
                $items | ForEach-Object {
                    $name = $_.Name
                    $href = "/$requestedPath/$name".TrimStart('/')
                    $modTime = $_.LastWriteTime.ToString("yyyy-MM-dd HH:mm")

                    if ($_.PSIsContainer) {
                        $htmlContent += "<li><a href='/$href/'><span class='file-info'>📂 $name/</span><span class='file-meta'><span class='meta-size'>--</span><span class='meta-date'>$modTime</span></span></a></li>"
                    }
                    else {
                        # Format file size dynamically
                        $sizeBytes = $_.Length
                        $sizeStr = if ($sizeBytes -ge 1GB) { "{0:N2} GB" -f ($sizeBytes / 1GB) } 
                        elseif ($sizeBytes -ge 1MB) { "{0:N2} MB" -f ($sizeBytes / 1MB) } 
                        elseif ($sizeBytes -ge 1KB) { "{0:N2} KB" -f ($sizeBytes / 1KB) } 
                        else { "$sizeBytes B" }

                        $htmlContent += "<li><a href='/$href'><span class='file-info'>📄 $name</span><span class='file-meta'><span class='meta-size'>$sizeStr</span><span class='meta-date'>$modTime</span></span></a></li>"
                    }
                }
                $htmlContent += @"
        </ul>
        <div class="footer">Served with ☕ and PowerShell</div>
    </div>
</body>
</html>
"@
                
                $contentBytes = [System.Text.Encoding]::UTF8.GetBytes($htmlContent)
                $response.ContentType = "text/html; charset=utf-8"
                $response.ContentLength64 = $contentBytes.Length
                $response.OutputStream.Write($contentBytes, 0, $contentBytes.Length)
            }
            else {
                $response.StatusCode = 404
                $response.OutputStream.Write([System.Text.Encoding]::UTF8.GetBytes("404 - Not Found"), 0, 16)
            }
        }
        else {
            $response.StatusCode = 403
            $response.OutputStream.Write([System.Text.Encoding]::UTF8.GetBytes("403 - Access Denied"), 0, 18)
        }
        $response.OutputStream.Close()
    }
}
catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
}
finally {
    if ($listener.IsListening) { $listener.Stop() }
    $listener.Dispose()
    Write-Host "File server stopped." -ForegroundColor Yellow
}