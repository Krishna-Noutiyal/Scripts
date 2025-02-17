# Localhost File Server Using PowerShell
This PowerShell script creates a server on localhost port 8080 by default. The script creates a file server that can be used to download files just like the `http.server` in python.
> The script is going to host the server and list all the folders and file in the current working directory

## Running the script
To run the script navigate to the script folder and run this command on the terminal
> **Run as Administrator**
```

powershell -f ps_server.ps1

```
## Can't Run Script on the System
If Windows doesn't allow  you to run scripts on your system you will have to set the execution policy in your system. Open Powershell with Administrative privileges and run this command :
```

Set-ExecutionPolicy RemoteSigned

```

## Needed Feature
- [ ] Automatically ask for Administrative Privileges
- [ ] Proper directory navigation buttons on Web Page
