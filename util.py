import asyncio
import glob
import os
import shutil
import smtplib
import re
import ssl
import time
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

import cv2
import yaml
from PIL import Image

COUNTDOWN_TIMER = int(3)
RECORDING_TIME = int(5)
PHOTOBOOTH_WINDOW_NAME = 'Photobooth'
FILES_DIR = 'files'
DELETED_DIR = 'deleted'
PDF_DIR = 'assets/pdf/'
PDF_TEMPLATE = 'template.html'
CSS_FILE = 'pdf_styling.css'

EMAILS_FILE = "emails.txt"
DEFAULT_EMAIL = "cerigo3@gmail.com"

# Load settings
with open("settings.yaml", 'r') as stream:
  settings = yaml.safe_load(stream)['settings']


def get_filename():
  return datetime.now().strftime("%Y%m%d%H%M%S")


def validate_email(email):
  pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
  return re.match(pattern, email) is not None

def fire_and_forget(f):
  def wrapped(*args, **kwargs):
    return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)

  return wrapped

@fire_and_forget
def send_email_with_attachment(receiver_email: str, filenames_list: list):
  """
  Sends an email to the provided receiver email,
  with the provided files attached
  """
  print("Trying to send email...")
  sender_email = settings['SENDER_EMAIL']

  # Create pdf and include it in the attachments
  saved_pdf = generate_pdf(receiver_email)
  filenames_list.append(saved_pdf)

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
    save_email_to_file(receiver_email)
  print("Email sent!")

def save_email_to_file(email):
  file_object = open(EMAILS_FILE, 'a')
  file_object.write(f"{email}\n")
  file_object.close()

def take_picture() -> str:
  """
  Opens the camera, displays a countdown and after COUNTDOWN_TIMER seconds,
  the frame is saved in the files directory.
  """
  filename = get_filename()
  saved_photo = f'{FILES_DIR}/{filename}.jpg'
  # Open the camera
  cap = cv2.VideoCapture(0)

  prev = time.time()
  timer = COUNTDOWN_TIMER

  cv2.namedWindow(PHOTOBOOTH_WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
  cv2.setWindowProperty(
      PHOTOBOOTH_WINDOW_NAME,
      cv2.WND_PROP_FULLSCREEN,
      cv2.WINDOW_FULLSCREEN
  )

  while timer >= 0:
    _, img = cap.read()
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
    _, img = cap.read()
    # Mirror image
    img = cv2.flip(img, 1)

    # Display the photo
    cv2.imshow(PHOTOBOOTH_WINDOW_NAME, img)

    # time for which image is displayed
    cv2.waitKey(2000)

    # Save the frame
    cv2.imwrite(saved_photo, img)

  # close the camera
  cap.release()

  # close all the opened windows
  cv2.destroyAllWindows()
  return saved_photo


def create_gif(photos_list: list) -> str:
  filename = get_filename()
  saved_gif = f'{FILES_DIR}/{filename}.gif'
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


def get_latest_file(directory: str, reverse: bool) -> list:
  """
  Find the most recent file in the provided directory, exclude pdfs
  """
  photos = sorted([
      filename for filename in glob.glob(f'{directory}/*.*')
      if not filename.endswith('.pdf')
  ], reverse=reverse)
  if len(photos) == 0:
    return []
  return [photos[-1]]


def move_files(filenames: list, source_dir: str, dest_dir: str):
  """
  Move the files from the source directory to the destination directory
  """
  try:
    os.makedirs(dest_dir)
  except FileExistsError:
    # directory already exists
    pass
  for file in filenames:
    shutil.move(file, file.replace(source_dir, dest_dir))


def generate_pdf(email: str):
  """
  Generate pdf to be included as an attachment to the email.
  The template is used, placed in pdf dir
  """
  filename = get_filename()
  saved_pdf = f'{FILES_DIR}/{filename}.pdf'

  env = Environment(loader=FileSystemLoader('.'))
  # TODO: Improve the styling of the template
  this_folder = os.path.dirname(os.path.abspath(__file__))
  template = env.get_template(f"{PDF_DIR}{PDF_TEMPLATE}")
  template_vars = {
      'event': settings['EVENT_NAME'],
      'date': settings['EVENT_DATE'],
      'place': settings['EVENT_PLACE'],
      'url': settings['EVENT_WEBSITE'],
      'receiver_name': email.split('@')[0],
      'body': settings['PDF_MESSAGE'],
      'signature': settings['PDF_SIGNATURE'],
      'top_image_path': f'file://{this_folder}/assets/pdf/{settings["PDF_TOP_IMG"]}',
      'bottom_image_path': f'file://{this_folder}/assets/pdf/{settings["PDF_BOTTOM_IMG"]}',
      'main_image_path': f'file://{this_folder}/assets/pdf/{settings["PDF_MAIN_IMG"]}',
  }
  html_out = template.render(template_vars)
  css = CSS(f"{PDF_DIR}{CSS_FILE}")
  HTML(string=html_out).write_pdf(saved_pdf, stylesheets=[css])
  return saved_pdf

def retrieve_latest_email():
  try:
    with open(EMAILS_FILE, 'r') as f:
      return f.readlines()[-1].strip()
  except FileNotFoundError:
    return DEFAULT_EMAIL