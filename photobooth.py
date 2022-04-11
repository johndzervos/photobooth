#!/usr/bin/env python3

import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QMovie, QPixmap, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QWidget,
)

from constants import (
    ICON_BUTTON_HEIGHT,
    ICON_BUTTON_ROW_OFFSET,
    ICON_BUTTON_WIDTH,
    KEYBOARD_LAYOUT,
    LETTER_BUTTON_HEIGHT,
    LETTER_BUTTON_WIDTH,
    N_NUMBER_MULTIPLE_PHOTOS
)
from util import (
    DELETED_DIR,
    FILES_DIR,
    create_gif,
    generate_pdf,
    get_latest_file,
    move_files,
    send_email_with_attachment,
    take_picture,
    validate_email
)


DEFAULT_EMAIL = "cerigo3@gmail.com"
WINDOW_X_OFFSET = 10
WINDOW_Y_OFFSET = 10
WINDOW_WIDTH = 1010
WINDOW_HEIGHT = 500

class EmailWindow(QWidget):

  def __init__(self, latest_files):
    QWidget.__init__(self)
    self.setWindowTitle('Send email')
    self.latest_files = latest_files
    super(EmailWindow, self).__init__()

    self.initUI()
  
  def initUI(self):
    self.setGeometry(WINDOW_X_OFFSET, WINDOW_Y_OFFSET, WINDOW_WIDTH, WINDOW_HEIGHT)
    self.setWindowTitle('Send email')
    # Create textbox
    self.textbox = QLineEdit(self)
    self.textbox.move(10, 20)
    self.textbox.resize(275, 30)
    self.textbox.setText(DEFAULT_EMAIL)

    self.clear_email_button = QPushButton('', self)
    self.clear_email_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.clear_email_button.setIcon(QIcon('assets/eraser.svg'))
    self.clear_email_button.move(290, 20)

    self.backspace_button = QPushButton('', self)
    self.backspace_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.backspace_button.setIcon(QIcon('assets/arrow-left.svg'))
    self.backspace_button.move(710, 110)

    self.send_email_button = QPushButton('', self)
    self.send_email_button.setIcon(QIcon('assets/email.svg'))
    self.send_email_button.move(10, 60)

    # Connect buttons to functions
    self.send_email_button.clicked.connect(self.on_click_send_email)
    self.clear_email_button.clicked.connect(self.on_click_clear_email)
    self.backspace_button.clicked.connect(self.on_click_backspace)

    for button in KEYBOARD_LAYOUT:
      self.q_button = QPushButton(button[0], self)
      if button[1] is not None and button[2] is not None:
        self.q_button.resize(button[1], button[2])
      self.q_button.move(button[3], button[4])
      self.q_button.clicked.connect(
          lambda checked, text=button[0]: self.on_click_add_to_email(text)
      )

  def on_click_send_email(self):
    textboxValue = self.textbox.text()
    # Defend against empty email
    if len(textboxValue) > 0:
      send_email_with_attachment(textboxValue, self.latest_files)
      self.close()

  def on_click_clear_email(self):
    self.textbox.setText('')
    self.clear_email_button.setEnabled(False)
    self.backspace_button.setEnabled(False)
    self.send_email_button.setEnabled(False)

  def on_click_backspace(self):
    self.textbox.setText(f"{self.textbox.text()[:-1]}")
    if len(self.textbox.text()) == 0:
      self.clear_email_button.setEnabled(False)
      self.backspace_button.setEnabled(False)
    self.send_email_button.setEnabled(validate_email(self.textbox.text()))

  def on_click_add_to_email(self, string):
    self.textbox.setText(f"{self.textbox.text()}{string}")
    self.clear_email_button.setEnabled(True)
    self.backspace_button.setEnabled(True)
    self.send_email_button.setEnabled(validate_email(self.textbox.text()))


class MainWindow(QMainWindow):
  switch_window = QtCore.pyqtSignal(list)

  def open_email_modal(self):
    self.switch_window.emit(self.latest_files)

  def __init__(self):
    super().__init__()
    self.latest_files = []
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Photobooth App')
    self.setGeometry(WINDOW_X_OFFSET, WINDOW_Y_OFFSET, WINDOW_WIDTH, WINDOW_HEIGHT)

    self.take_picture_button = QPushButton('', self)
    self.take_picture_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.take_picture_button.setIcon(QIcon('assets/photo.svg'))
    self.take_picture_button.move(15, 15)

    self.take_picture_label = QLabel(self)
    self.take_picture_label.setText("1 picture")
    self.take_picture_label.adjustSize()
    self.take_picture_label.move(90, 35)

    self.take_pictures_button = QPushButton('', self)
    self.take_pictures_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.take_pictures_button.setIcon(QIcon('assets/photos.svg'))
    self.take_pictures_button.move(15, 85)

    self.take_pictures_label = QLabel(self)
    self.take_pictures_label.setText("4 pictures")
    self.take_pictures_label.adjustSize()
    self.take_pictures_label.move(90, 105)

    self.record_gif_button = QPushButton('', self)
    self.record_gif_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.record_gif_button.setIcon(QIcon('assets/gif.png'))
    self.record_gif_button.move(15, 155)

    self.record_gif_label = QLabel(self)
    self.record_gif_label.setText("4 pictures -> GIF")
    self.record_gif_label.adjustSize()
    self.record_gif_label.move(90, 175)

    self.open_email_modal_button = QPushButton('', self)
    self.open_email_modal_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.open_email_modal_button.setIcon(QIcon('assets/email.svg'))
    self.open_email_modal_button.move(15, 225)

    self.open_email_modal_label = QLabel(self)
    self.open_email_modal_label.setText("Send email")
    self.open_email_modal_label.adjustSize()
    self.open_email_modal_label.move(90, 245)

    self.delete_button = QPushButton('', self)
    self.delete_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.delete_button.setIcon(QIcon('assets/trash.svg'))
    self.delete_button.move(15, 295)
    # TODO: Disable button if there isn't any photo to delete

    self.delete_label = QLabel(self)
    self.delete_label.setText("Delete")
    self.delete_label.adjustSize()
    self.delete_label.move(90, 315)

    self.undo_button = QPushButton('', self)
    self.undo_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.undo_button.setIcon(QIcon('assets/undo.svg'))
    self.undo_button.move(15, 365)
    # TODO: Disable button if there isn't any photo to restore

    self.restore_label = QLabel(self)
    self.restore_label.setText("Restore")
    self.restore_label.adjustSize()
    self.restore_label.move(90, 385)

    # TODO: Remove pdf button
    self.pdf_button = QPushButton('PDF', self)
    self.pdf_button.resize(30, 30)
    self.pdf_button.move(15, 435)

    # Create photo displays
    self.photo_display = QLabel(self)
    self.photo_display1 = QLabel(self)
    self.photo_display2 = QLabel(self)
    self.photo_display3 = QLabel(self)

    self.photo_display.move(360, 20)
    self.photo_display1.move(680, 20)
    self.photo_display2.move(360, 260)
    self.photo_display3.move(680, 260)

    self.latest_files = get_latest_file(FILES_DIR, False)
    self.display_latest_file()

    # Connect buttons to functions
    self.open_email_modal_button.clicked.connect(self.open_email_modal)

    self.pdf_button.clicked.connect(self.on_click_generate_pdf)

    self.take_picture_button.clicked.connect(self.on_click_take_picture)
    self.take_pictures_button.clicked.connect(self.on_click_take_pictures)
    self.record_gif_button.clicked.connect(self.on_click_record_gif)
    self.delete_button.clicked.connect(self.on_click_delete_latest)
    self.undo_button.clicked.connect(self.on_click_undo)

    self.show()

  def on_click_take_picture(self):
    # Disable action buttons
    self.disable_action_buttons()
    photo_taken = take_picture()
    self.latest_files = [photo_taken]
    self.display_photo(f'{photo_taken}')
    # Re-enable action buttons
    self.enable_action_buttons()

  def on_click_take_pictures(self):
    # Disable action buttons
    self.disable_action_buttons()
    photos_taken = [
        take_picture()
        for _ in range(N_NUMBER_MULTIPLE_PHOTOS)
    ]
    self.latest_files = photos_taken
    self.display_photos(photos_taken)
    # Re-enable action buttons
    self.enable_action_buttons()

  def on_click_record_gif(self):
    # Disable action buttons
    self.disable_action_buttons()
    self.latest_files = [
        take_picture()
        for _ in range(N_NUMBER_MULTIPLE_PHOTOS)
    ]
    self.latest_files = [create_gif(self.latest_files)]
    self.display_gif(f'{self.latest_files[0]}')
    # Re-enable action buttons
    self.enable_action_buttons()

  def enable_action_buttons(self):
    self.take_picture_button.setEnabled(True)
    self.take_pictures_button.setEnabled(True)
    self.record_gif_button.setEnabled(True)
    self.delete_button.setEnabled(True)
    self.undo_button.setEnabled(True)

  def disable_action_buttons(self):
    self.take_picture_button.setEnabled(False)
    self.take_pictures_button.setEnabled(False)
    self.record_gif_button.setEnabled(False)
    self.delete_button.setEnabled(False)
    self.undo_button.setEnabled(False)

  def on_click_delete_latest(self):
    # Disable action buttons
    self.disable_action_buttons()
    move_files(self.latest_files, FILES_DIR, DELETED_DIR)
    self.latest_files = get_latest_file(FILES_DIR, False)
    self.display_latest_file()
    # Re-enable action buttons
    self.enable_action_buttons()

  def on_click_undo(self):
    # Disable action buttons
    self.disable_action_buttons()
    restored_file = get_latest_file(DELETED_DIR, True)
    if len(restored_file) > 0:
      self.latest_files = restored_file
      move_files(self.latest_files, DELETED_DIR, FILES_DIR)
      self.latest_files[0] = self.latest_files[0]\
                                 .replace(DELETED_DIR, FILES_DIR)
      self.display_latest_file()
    # Re-enable action buttons
    self.enable_action_buttons()

  def on_click_generate_pdf(self):
    generate_pdf(self.textbox.text())

  def display_latest_file(self):
    if len(self.latest_files) > 0:
      extension = self.latest_files[0][-4:]
      if extension == '.jpg':
        self.display_photo(f'{self.latest_files[0]}')
      elif extension == '.gif':
        self.display_gif(f'{self.latest_files[0]}')
      else:
        print(f"unknown format: {extension}")
    else:
      self.photo_display.clear()
      self.photo_display1.clear()
      self.photo_display2.clear()
      self.photo_display3.clear()

  def display_photo(self, filename):
    pixmap = QPixmap(filename)
    self.photo_display.setPixmap(pixmap)
    self.photo_display.resize(pixmap.width(), pixmap.height())
    self.photo_display1.clear()
    self.photo_display2.clear()
    self.photo_display3.clear()

  def create_scaled_pixmap(self, filename):
    return QPixmap(filename).scaled(
        320,
        240,
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation
    )

  def display_photos(self, filenames: list):
    """
    filenames is expected to have a maximum length of 4
    """
    displays = [
        self.photo_display,
        self.photo_display1,
        self.photo_display2,
        self.photo_display3,
    ]
    for display, filename in zip(displays, filenames):
      display.resize(320, 240)
      pixmap = self.create_scaled_pixmap(filename)
      display.setPixmap(pixmap)

  def display_gif(self, filename):
    pixmap = QPixmap(filename)
    self.photo_display.resize(pixmap.width() - 10, pixmap.height())
    self.movie = QMovie(filename)
    self.photo_display.setMovie(self.movie)
    self.movie.start()
    self.photo_display1.clear()
    self.photo_display2.clear()
    self.photo_display3.clear()


class Controller:

  def __init__(self):
    pass

  def show_main(self):
    self.window = MainWindow()
    self.window.switch_window.connect(self.show_email_window)
    self.window.show()

  def show_email_window(self, latest_files):
    self.email_window = EmailWindow(latest_files)
    self.email_window.show()


def main():
  try:
    os.makedirs(FILES_DIR)
  except FileExistsError:
    # directory already exists
    pass

  app = QApplication(sys.argv)
  controller = Controller()
  controller.show_main()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
