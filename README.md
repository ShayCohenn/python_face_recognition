# Face Recognition Using Python
******Using this program requires a webcam******

This is a basic face recognition program using python and a few packages: <br>
• kivy - For the GUI,<br>
• opencv - For the face recognition part<br>

This program uses opencv and the uploaded images to predict who is the person in the frame<br>
Note that the more images the program gets the more accurate its prediction

## Intallation:
clone the repo
```
git clone https://github.com/ShayCohenn/python_face_recognition.git
```
cd into the folder
```
cd python_face_recognition
```
create virtual enviroment
```
python -m virtualenv env
```
activate virtual enviroment
```
.\env\Scripts\activate
```
install the dependencies
```
pip install -r requirements.txt
```
run the program
```
python ./main.py
```

## Usage:
• Register button is for creating images, <br>
• Login button is for the prediction
<img src="screenshots\screenshot1.png"><hr>
<img src="screenshots\screenshot2.png"><hr>
• Enter your name in the text box<br>
• Start The Camera - It takes 1 image per second (can be ajusted in face_rec.py line 11)
```python
    capture_interval = 1  # Set the capture interval to 1 second
```
• To Close The Camera Press "q" (Can be ajusted in face_rec.py line 36)
```python
       if key == ord('q'):
```
• Save Images To Transfer The Images To The Faces Folder<br>
<img src="screenshots/screenshot3.png" heigh="100px" width="100px">