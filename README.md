# Railtech-server
## Setup instructions (windows)
### 1. Create virtual environment
To config this, you have to create the virtual env first using
```Powershell
python -m venv .env
```

### 2. Run the virtual environment
```Powershell
.\.env\Scripts\Activate.ps1 
```
If you see a `(.env)` at the start of your powershell terminal then it means this works

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
You are done with installation!
---
Note: If you want to remove execution policy for this scope (reversing what you did earlier)
```
Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser
```