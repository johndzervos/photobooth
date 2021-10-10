import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton
)

from constants import (
    ICON_BUTTON_HEIGHT,
    ICON_BUTTON_LINE_OFFSET,
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
    record_video,
    send_email_with_attachment,
    take_picture,
    validate_email
)


class App(QMainWindow):

  def __init__(self):
    super().__init__()
    self.title = 'Photobooth App'
    self.latest_files = []
    self.left = 10
    self.top = 10
    self.width = 1010
    self.height = 700
    self.initUI()

  def initUI(self):
    try:
      os.makedirs(FILES_DIR)
    except FileExistsError:
      # directory already exists
      pass

    self.setWindowTitle(self.title)
    self.setGeometry(self.left, self.top, self.width, self.height)

    # Create textbox
    self.textbox = QLineEdit(self)
    self.textbox.move(10, 20)
    self.textbox.resize(275, 30)
    self.textbox.setText("cerigo3@gmail.com")

    self.send_email_button = QPushButton('', self)
    self.send_email_button.setIcon(QIcon('assets/email.svg'))
    self.send_email_button.move(10, 60)

    self.take_picture_button = QPushButton('', self)
    self.take_picture_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.take_picture_button.setIcon(QIcon('assets/photo.svg'))
    self.take_picture_button.move(10, ICON_BUTTON_LINE_OFFSET)

    self.take_pictures_button = QPushButton('', self)
    self.take_pictures_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.take_pictures_button.setIcon(QIcon('assets/photos.svg'))
    self.take_pictures_button.move(80, ICON_BUTTON_LINE_OFFSET)

    self.record_gif_button = QPushButton('', self)
    self.record_gif_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.record_gif_button.setIcon(QIcon('assets/gif.png'))
    self.record_gif_button.move(150, ICON_BUTTON_LINE_OFFSET)

    self.record_video_button = QPushButton('', self)
    self.record_video_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.record_video_button.setIcon(QIcon('assets/video.svg'))
    self.record_video_button.move(220, ICON_BUTTON_LINE_OFFSET)

    self.delete_button = QPushButton('', self)
    self.delete_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.delete_button.setIcon(QIcon('assets/trash.svg'))
    self.delete_button.move(600, 600)
    # TODO: Disable button if there isn't any photo to delete

    self.undo_button = QPushButton('', self)
    self.undo_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.undo_button.setIcon(QIcon('assets/undo.svg'))
    self.undo_button.move(700, 600)
    # TODO: Disable button if there isn't any photo to restore

    self.clear_email_button = QPushButton('', self)
    self.clear_email_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.clear_email_button.setIcon(QIcon('assets/eraser.svg'))
    self.clear_email_button.move(290, 20)

    self.backspace_button = QPushButton('', self)
    self.backspace_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.backspace_button.setIcon(QIcon('assets/arrow-left.svg'))
    self.backspace_button.move(290, 60)

    # TODO: Remove pdf button
    self.pdf_button = QPushButton('PDF', self)
    self.pdf_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.pdf_button.move(800, 600)

    for button in KEYBOARD_LAYOUT:
      self.q_button = QPushButton(button[0], self)
      if button[1] is not None and button[2] is not None:
        self.q_button.resize(button[1], button[2])
      self.q_button.move(button[3], button[4])
      self.q_button.clicked.connect(
          lambda checked, text=button[0]: self.on_click_add_to_email(text)
      )

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
    self.send_email_button.clicked.connect(self.on_click_send_email)
    self.clear_email_button.clicked.connect(self.on_click_clear_email)
    self.backspace_button.clicked.connect(self.on_click_backspace)

    self.pdf_button.clicked.connect(self.on_click_generate_pdf)

    self.take_picture_button.clicked.connect(self.on_click_take_picture)
    self.take_pictures_button.clicked.connect(self.on_click_take_pictures)
    self.record_gif_button.clicked.connect(self.on_click_record_gif)
    self.record_video_button.clicked.connect(self.on_click_record_video)
    self.delete_button.clicked.connect(self.on_click_delete_latest)
    self.undo_button.clicked.connect(self.on_click_undo)

    self.show()

  def on_click_send_email(self):
    textboxValue = self.textbox.text()
    # Defend against empty email
    if len(textboxValue) > 0:
      send_email_with_attachment(textboxValue, self.latest_files)

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

  def on_click_record_video(self):
    # Disable action buttons
    self.disable_action_buttons()
    self.latest_files = [record_video()]
    self.display_latest_file()
    # Re-enable action buttons
    self.enable_action_buttons()

  def enable_action_buttons(self):
    self.take_picture_button.setEnabled(True)
    self.take_pictures_button.setEnabled(True)
    self.record_gif_button.setEnabled(True)
    self.record_video_button.setEnabled(True)
    self.delete_button.setEnabled(True)
    self.undo_button.setEnabled(True)

  def disable_action_buttons(self):
    self.take_picture_button.setEnabled(False)
    self.take_pictures_button.setEnabled(False)
    self.record_gif_button.setEnabled(False)
    self.record_video_button.setEnabled(False)
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

  def on_click_generate_pdf(self):
    generate_pdf(self.textbox.text())

  def display_latest_file(self):
    if len(self.latest_files) > 0:
      extension = self.latest_files[0][-4:]
      if extension == '.jpg':
        self.display_photo(f'{self.latest_files[0]}')
      elif extension == '.gif':
        self.display_gif(f'{self.latest_files[0]}')
      elif extension == '.avi':
        self.display_video(f'{self.latest_files[0]}')
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

  def display_video(self, filename):
    print(filename)
    # TODO Add support for video player


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())
