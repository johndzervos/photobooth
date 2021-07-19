# Photobooth
A script to create a photobooth app. Is using cv to get the camera input, display countdown and then capture an image. User has the option to send the captured image to his/her personal email.

## Installation
Works with python 3.8.10.
To install dependencies:
```
pip install requirements.txt
```

## How to use
Copy the contents of `settings.example.yaml` to `settings.yaml` and adjust the content to your settings.
The photobooth app is called with:
```
python photobooth.py
```
This will spawn a winow. The window has:
* A 'Take picture' button: Which opens the camera and takes a picture after 3 seconds
* An input field: Where the user is prompted to add his/her email
* A 'Send email' button: Which sends the displayed image to the provided email
* A display area: Where the most recent photo is displayed