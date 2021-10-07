import glob
import smtplib
import ssl
import yaml
import cv2
import time
import os
import shutil
from datetime import datetime
from PIL import Image

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COUNTDOWN_TIMER = int(3)
PHOTOBOOTH_WINDOW_NAME = 'Photobooth'
PHOTOS_DIR = 'photos'
DELETED_DIR = 'deleted'

# Load settings
with open("settings.yaml", 'r') as stream:
  settings = yaml.safe_load(stream)['settings']


def send_email_with_attachment(receiver_email: str, filenames_list: list):
  """
  Sends an email to the provided receiver email,
  with the provided file attached
  """
  sender_email = settings['SENDER_EMAIL']

  # Create a multipart message and set headers
  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = receiver_email
  message["Subject"] = settings['EMAIL_SUBJECT']
  message["Bcc"] = receiver_email  # Recommended for mass emails

  # Add body to email
  message.attach(MIMEText(settings['EMAIL_BODY'], "plain"))

  for filename in filenames_list:
    # Add file as application/octet-stream
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(filename, "rb").read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
        'Content-Disposition',
        'attachment',
        filename=filename
    )
    message.attach(part)

  # Add attachment to message and convert message to string
  message.attach(part)
  text = message.as_string()

  # Try to log in to server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP("smtp.gmail.com", 587) as server:
    # Secure the connection
    server.starttls(context=context)
    server.login(sender_email, settings['SENDER_PASSWORD'])
    server.sendmail(sender_email, receiver_email, text)


def take_picture():
  """
  Opens the camera, displays a countdown and after COUNTDOWN_TIMER seconds,
  the frame is saved in the photos directory.
  """
  # Open the camera
  cap = cv2.VideoCapture(0)
  prev = time.time()
  filename = datetime.now().strftime("%Y%m%d%H%M%S")

  timer = COUNTDOWN_TIMER

  cv2.namedWindow(PHOTOBOOTH_WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
  cv2.setWindowProperty(
      PHOTOBOOTH_WINDOW_NAME,
      cv2.WND_PROP_FULLSCREEN,
      cv2.WINDOW_FULLSCREEN
  )

  while timer >= 0:
    ret, img = cap.read()
    # Mirror image
    img = cv2.flip(img, 1)

    # Display countdown on each frame
    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    cv2.putText(img, str(timer),
                (250, 250), font,
                7, (0, 255, 255),
                4, cv2.LINE_AA)
    cv2.imshow(PHOTOBOOTH_WINDOW_NAME, img)
    cv2.waitKey(125)

    # current time
    cur = time.time()

    # Update and keep track of Countdown
    if cur - prev >= 1:
      prev = cur
      timer = timer - 1

  else:
    ret, img = cap.read()
    # Mirror image
    img = cv2.flip(img, 1)

    # Display the photo
    cv2.imshow(PHOTOBOOTH_WINDOW_NAME, img)

    # time for which image is displayed
    cv2.waitKey(2000)

    # Save the frame
    saved_photo = f'{PHOTOS_DIR}/{filename}.jpg'
    cv2.imwrite(saved_photo, img)

  # close the camera
  cap.release()

  # close all the opened windows
  cv2.destroyAllWindows()
  return saved_photo


def create_gif(photos_list: list):
  filename = datetime.now().strftime("%Y%m%d%H%M%S")
  saved_gif = f'{PHOTOS_DIR}/{filename}.gif'
  img, *imgs = [Image.open(f) for f in photos_list]
  img.save(
      fp=saved_gif,
      format='GIF',
      append_images=imgs,
      save_all=True,
      duration=300,
      loop=0
  )
  return saved_gif


def get_latest_file() -> list:
  # Find the most recent photo in the photos directory
  photos = sorted(glob.glob(f"{PHOTOS_DIR}/*"))
  if len(photos) == 0:
    return []
  return [photos[-1]]


def delete_files(filenames: list):
  try:
    os.makedirs(DELETED_DIR)
  except FileExistsError:
    # directory already exists
    pass
  for file in filenames:
    shutil.move(file, file.replace(f"{PHOTOS_DIR}", f"{DELETED_DIR}"))
