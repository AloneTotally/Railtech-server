# Railtech-server
## Setup instructions (windows)
### 1. Create virtual environment
To config this, you have to create the virtual env first using
```Powershell
python -m venv venv
```

### 2. Run the virtual environment
```Powershell
.\venv\Scripts\Activate.ps1 
```
If you see a `(venv)` at the start of your powershell terminal then it means this works

#### If step 2 fails:
If the error message says "execution of scripts is disabled on this system", make another terminal window, run the following:
```Powershell
Get-ExecutionPolicy -List
```
If you see something like the following, (where `CurrentUser` or `LocalMachine` is NOT `remoteSigned`), that means that this is the problem. We will fix this in the next step.
```plaintext
        Scope ExecutionPolicy
        ----- ---------------
MachinePolicy       Undefined
   UserPolicy       Undefined
      Process       Undefined
  CurrentUser       Undefined
 LocalMachine       Undefined
```
Run the following to change the execution policy:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
It is complete :D now you can try to run **step 2**.

### 3. Installing all requirements
```Powershell
pip install -r requirements.txt
```
You are done with installation! (For python)

---
Note: If you want to remove execution policy for this scope (reversing what you did earlier)
```
Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser
```

### 1. Installing things for js

This just installs the dependencies required for the html side of things
```Powershell
npm install
```
If it says that html doesnt work go install nodejs [here](https://nodejs.org/en/download/prebuilt-installer).

### 2. Start the Tailwind CLI build process

When you are editing any tailwind classes, run this command (in another terminal after running `python index.py` to run the flask server):
```Powershell
npx tailwindcss -i ./static/input.css -o ./static/output.css --watch
```
this should start running a script and whenever you edit any tailwind classes in the html files it will generate the corresponding css for those classes in another file so that tailwind like does its job :D

> Note: Whenever you have a html file that uses tailwind classes make sure to put a link to the output.css file at the end of the `<head>` html tag as shown below
> ```html
> <link href="../static/output.css" rel="stylesheet">
>```