# Railtech-server

This is the server for the android app as listed here: https://github.com/Scxr-ch/Realtech

Note: that the server might not load as render takes a while to load the website if you access it for the first time in a long time)

## What is this prototype about?
This prototype was made for a competition called: **Singapore RailTech Grand Challenge (SGRTGC) 2024 - Open Innovation Challenge**

This competition is where participants develop innovative ideas and solutions to tackle real-world rail engineering problems faced during day-to-day operations and maintenance in the railway industry. The objective of the challenge is to find solutions to improve productivity, safety and/or enhance environmental sustainability, with incorporation of digitalisation where possible.
The problem statement for this year’s Open Innovation Challenge is “How might we monitor the movement of working personnel in the rail track system in real-time?”

As a group, our solution was to develop an Android app that utilises Received Signal Strength Indicator (RSSI) to estimate the distance from an Access Point (AP), followed by trilateration between three Wi-Fi Access Points with known coordinates to determine the precise location of workers on the tracks. This leverages on existing infrastructure instead of a solution that requires the setting of one’s own anchor points. This is more focused on underground systems as above ground systems would use GPS.

All the calculation has been done in here, all the android app does is to send the data from the Wi-Fi scan.
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

When you are editing any tailwind classes, run this command (in another terminal after running `python index.py` to run the flask server):3
```Powershell
npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch
```
this should start running a script and whenever you edit any tailwind classes in the html files it will generate the corresponding css for those classes in another file so that tailwind like does its job :D

> Note: Whenever you have a html file that uses tailwind classes make sure to put a link to the output.css file at the end of the `<head>` html tag as shown below
> ```html
> <link href="../static/output.css" rel="stylesheet">
>```
