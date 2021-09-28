
import sys
import os
import glob
from PyQt5.QtWidgets import (
  QApplication,
  QPushButton,
  QLineEdit,
  QMainWindow,
  QLabel,
)
from PyQt5.QtGui import QPixmap
from util import send_email_with_attachment, take_picture


PHOTOS_DIR = 'photos'


class App(QMainWindow):

  def __init__(self):
    super().__init__()
    self.title = 'Photobooth App'
    self.latest_photo = ''
    self.left = 10
    self.top = 10
    self.width = 1000
    self.height = 700
    self.initUI()
  
  def initUI(self):
    try:
      os.makedirs(PHOTOS_DIR)
    except FileExistsError:
      # directory already exists
      pass

    self.setWindowTitle(self.title)
    self.setGeometry(self.left, self.top, self.width, self.height)

    # Create textbox
    self.textbox = QLineEdit(self)
    self.textbox.move(20, 20)
    self.textbox.resize(280,30)
    self.textbox.setText("cerigo3@gmail.com") 
    
    # Create buttons
    self.send_email_button = QPushButton('Send email', self)
    self.send_email_button.move(20, 80)

    self.take_picture_button = QPushButton('Take a picture', self)
    self.take_picture_button.move(20, 120)

    # Create photo display
    self.photo_display = QLabel(self)
    # Find the most recent photo in the photos directory
    photos = sorted(glob.glob(f"{PHOTOS_DIR}/*.jpg"))
    if len(photos) > 0:
      self.latest_photo = photos[-1]
      self.display_photo(f'{self.latest_photo}')
    
    # connect buttons to functions
    self.send_email_button.clicked.connect(self.on_click_send_email)
    self.take_picture_button.clicked.connect(self.on_click_take_picture)
    self.show()
  
  def on_click_send_email(self):
    textboxValue = self.textbox.text()
    send_email_with_attachment(textboxValue, self.latest_photo)
  
  def on_click_take_picture(self):
    self.latest_photo = take_picture()
    self.display_photo(f'{self.latest_photo}')

  def display_photo(self, filename):
    pixmap = QPixmap(filename)
    self.photo_display.setPixmap(pixmap)
    self.photo_display.move(350, 20)
    self.photo_display.resize(pixmap.width(),pixmap.height())

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())