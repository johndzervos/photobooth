
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
from PyQt5.QtGui import QIcon, QPixmap
from util import send_email_with_attachment, take_picture


PHOTOS_DIR = 'photos'
LETTER_BUTTON_WIDTH = 30
LETTER_BUTTON_HEIGHT = 30
ICON_BUTTON_WIDTH = 60
ICON_BUTTON_HEIGHT = 60

NUMBER_LINE_HEIGHT = 100
FIRST_LETTER_LINE_HEIGHT = 140
SECOND_LETTER_LINE_HEIGHT = 180
THIRD_LETTER_LINE_HEIGHT = 220
FOURTH_LINE_HEIGHT = 260
ICON_BUTTON_LINE_HEIGHT = 300

N_NUMBER_MULTIPLE_PHOTOS = 4


class App(QMainWindow):

  def __init__(self):
    super().__init__()
    self.title = 'Photobooth App'
    self.latest_photo = ''
    self.latest_photos = []
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

    self.is_in_progress = False

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
    self.take_picture_button.move(10, ICON_BUTTON_LINE_HEIGHT)

    self.take_pictures_button = QPushButton('', self)
    self.take_pictures_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.take_pictures_button.setIcon(QIcon('assets/photos.svg'))
    self.take_pictures_button.move(80, ICON_BUTTON_LINE_HEIGHT)

    self.record_gif_button = QPushButton('', self)
    self.record_gif_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.record_gif_button.setIcon(QIcon('assets/gif.png'))
    self.record_gif_button.move(150, ICON_BUTTON_LINE_HEIGHT)

    self.record_video_button = QPushButton('', self)
    self.record_video_button.resize(ICON_BUTTON_WIDTH, ICON_BUTTON_HEIGHT)
    self.record_video_button.setIcon(QIcon('assets/video.svg'))
    self.record_video_button.move(220, ICON_BUTTON_LINE_HEIGHT)

    self.clear_email_button = QPushButton('X', self)
    self.clear_email_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.clear_email_button.move(290, 20)

    self.backspace_button = QPushButton('<-', self)
    self.backspace_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.backspace_button.move(290, 60)

    # NUMBERS

    self.button_1 = QPushButton('1', self)
    self.button_1.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.button_1.move(10, NUMBER_LINE_HEIGHT)

    self.button_2 = QPushButton('2', self)
    self.button_2.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.button_2.move(45, NUMBER_LINE_HEIGHT)

    self.button_3 = QPushButton('3', self)
    self.button_3.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.button_3.move(80, NUMBER_LINE_HEIGHT)

    self.button_4 = QPushButton('4', self)
    self.button_4.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.button_4.move(115, NUMBER_LINE_HEIGHT)

    self.button_5 = QPushButton('5', self)
    self.button_5.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.button_5.move(150, NUMBER_LINE_HEIGHT)

    self.button_6 = QPushButton('6', self)
    self.button_6.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.button_6.move(185, NUMBER_LINE_HEIGHT)

    self.button_7 = QPushButton('7', self)
    self.button_7.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.button_7.move(220, NUMBER_LINE_HEIGHT)

    self.button_8 = QPushButton('8', self)
    self.button_8.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.button_8.move(255, NUMBER_LINE_HEIGHT)

    self.button_9 = QPushButton('9', self)
    self.button_9.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.button_9.move(290, NUMBER_LINE_HEIGHT)

    self.button_0 = QPushButton('0', self)
    self.button_0.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.button_0.move(325, NUMBER_LINE_HEIGHT)

    # FIRST LINE

    self.q_button = QPushButton('q', self)
    self.q_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.q_button.move(10, FIRST_LETTER_LINE_HEIGHT)

    self.w_button = QPushButton('w', self)
    self.w_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.w_button.move(45, FIRST_LETTER_LINE_HEIGHT)

    self.e_button = QPushButton('e', self)
    self.e_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.e_button.move(80, FIRST_LETTER_LINE_HEIGHT)

    self.r_button = QPushButton('r', self)
    self.r_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.r_button.move(115, FIRST_LETTER_LINE_HEIGHT)

    self.t_button = QPushButton('t', self)
    self.t_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.t_button.move(150, FIRST_LETTER_LINE_HEIGHT)

    self.y_button = QPushButton('y', self)
    self.y_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.y_button.move(185, FIRST_LETTER_LINE_HEIGHT)

    self.u_button = QPushButton('u', self)
    self.u_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.u_button.move(220, FIRST_LETTER_LINE_HEIGHT)

    self.i_button = QPushButton('i', self)
    self.i_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.i_button.move(255, FIRST_LETTER_LINE_HEIGHT)

    self.o_button = QPushButton('o', self)
    self.o_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.o_button.move(290, FIRST_LETTER_LINE_HEIGHT)

    self.p_button = QPushButton('p', self)
    self.p_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.p_button.move(325, FIRST_LETTER_LINE_HEIGHT)

    # SECOND LINE

    self.a_button = QPushButton('a', self)
    self.a_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.a_button.move(10, SECOND_LETTER_LINE_HEIGHT)

    self.s_button = QPushButton('s', self)
    self.s_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.s_button.move(45, SECOND_LETTER_LINE_HEIGHT)

    self.d_button = QPushButton('d', self)
    self.d_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.d_button.move(80, SECOND_LETTER_LINE_HEIGHT)

    self.f_button = QPushButton('f', self)
    self.f_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.f_button.move(115, SECOND_LETTER_LINE_HEIGHT)

    self.g_button = QPushButton('g', self)
    self.g_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.g_button.move(150, SECOND_LETTER_LINE_HEIGHT)

    self.h_button = QPushButton('h', self)
    self.h_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.h_button.move(185, SECOND_LETTER_LINE_HEIGHT)

    self.j_button = QPushButton('j', self)
    self.j_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.j_button.move(220, SECOND_LETTER_LINE_HEIGHT)

    self.k_button = QPushButton('k', self)
    self.k_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.k_button.move(255, SECOND_LETTER_LINE_HEIGHT)

    self.l_button = QPushButton('l', self)
    self.l_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.l_button.move(290, SECOND_LETTER_LINE_HEIGHT)

    # THIRD LINE

    self.z_button = QPushButton('z', self)
    self.z_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.z_button.move(10, THIRD_LETTER_LINE_HEIGHT)

    self.x_button = QPushButton('x', self)
    self.x_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.x_button.move(45, THIRD_LETTER_LINE_HEIGHT)

    self.c_button = QPushButton('c', self)
    self.c_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.c_button.move(80, THIRD_LETTER_LINE_HEIGHT)

    self.v_button = QPushButton('v', self)
    self.v_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.v_button.move(115, THIRD_LETTER_LINE_HEIGHT)

    self.b_button = QPushButton('b', self)
    self.b_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.b_button.move(150, THIRD_LETTER_LINE_HEIGHT)

    self.n_button = QPushButton('n', self)
    self.n_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.n_button.move(185, THIRD_LETTER_LINE_HEIGHT)

    self.m_button = QPushButton('m', self)
    self.m_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.m_button.move(220, THIRD_LETTER_LINE_HEIGHT)

    self.dot_button = QPushButton('.', self)
    self.dot_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.dot_button.move(290, THIRD_LETTER_LINE_HEIGHT)

    self.at_button = QPushButton('@', self)
    self.at_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.at_button.move(325, THIRD_LETTER_LINE_HEIGHT)

    # FOURTH LINE

    self.gmail_button = QPushButton('@gmail.com', self)
    # self.gmail_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.gmail_button.move(10, FOURTH_LINE_HEIGHT)

    self.yahoo_button = QPushButton('@yahoo.com', self)
    # self.yahoo_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.yahoo_button.move(115, FOURTH_LINE_HEIGHT)

    self.hotmail_button = QPushButton('@hotmail.com', self)
    # self.hotmail_button.resize(LETTER_BUTTON_WIDTH, LETTER_BUTTON_HEIGHT)
    self.hotmail_button.move(220, FOURTH_LINE_HEIGHT)

    # Create photo display
    self.photo_display = QLabel(self)
    # Find the most recent photo in the photos directory
    photos = sorted(glob.glob(f"{PHOTOS_DIR}/*.jpg"))
    if len(photos) > 0:
      self.latest_photo = photos[-1]
      self.latest_photos = [photos[-1]]
      self.display_photo(f'{self.latest_photo}')

    # connect buttons to functions
    self.send_email_button.clicked.connect(self.on_click_send_email)
    self.clear_email_button.clicked.connect(self.on_click_clear_email)
    self.backspace_button.clicked.connect(self.on_click_backspace)

    self.take_picture_button.clicked.connect(self.on_click_take_picture)
    self.take_pictures_button.clicked.connect(self.on_click_take_pictures)
    self.record_gif_button.clicked.connect(self.on_click_record_gif)
    self.record_video_button.clicked.connect(self.on_click_record_video)

    self.button_1.clicked.connect(lambda: self.on_click_add_to_email('1'))
    self.button_2.clicked.connect(lambda: self.on_click_add_to_email('2'))
    self.button_3.clicked.connect(lambda: self.on_click_add_to_email('3'))
    self.button_4.clicked.connect(lambda: self.on_click_add_to_email('4'))
    self.button_5.clicked.connect(lambda: self.on_click_add_to_email('5'))
    self.button_6.clicked.connect(lambda: self.on_click_add_to_email('6'))
    self.button_7.clicked.connect(lambda: self.on_click_add_to_email('7'))
    self.button_8.clicked.connect(lambda: self.on_click_add_to_email('8'))
    self.button_9.clicked.connect(lambda: self.on_click_add_to_email('9'))
    self.button_0.clicked.connect(lambda: self.on_click_add_to_email('0'))

    self.q_button.clicked.connect(lambda: self.on_click_add_to_email('q'))
    self.w_button.clicked.connect(lambda: self.on_click_add_to_email('w'))
    self.e_button.clicked.connect(lambda: self.on_click_add_to_email('e'))
    self.r_button.clicked.connect(lambda: self.on_click_add_to_email('r'))
    self.t_button.clicked.connect(lambda: self.on_click_add_to_email('t'))
    self.y_button.clicked.connect(lambda: self.on_click_add_to_email('y'))
    self.u_button.clicked.connect(lambda: self.on_click_add_to_email('u'))
    self.i_button.clicked.connect(lambda: self.on_click_add_to_email('i'))
    self.o_button.clicked.connect(lambda: self.on_click_add_to_email('o'))
    self.p_button.clicked.connect(lambda: self.on_click_add_to_email('p'))

    self.a_button.clicked.connect(lambda: self.on_click_add_to_email('a'))
    self.s_button.clicked.connect(lambda: self.on_click_add_to_email('s'))
    self.d_button.clicked.connect(lambda: self.on_click_add_to_email('d'))
    self.f_button.clicked.connect(lambda: self.on_click_add_to_email('f'))
    self.g_button.clicked.connect(lambda: self.on_click_add_to_email('g'))
    self.h_button.clicked.connect(lambda: self.on_click_add_to_email('h'))
    self.j_button.clicked.connect(lambda: self.on_click_add_to_email('j'))
    self.k_button.clicked.connect(lambda: self.on_click_add_to_email('k'))
    self.l_button.clicked.connect(lambda: self.on_click_add_to_email('l'))

    self.z_button.clicked.connect(lambda: self.on_click_add_to_email('z'))
    self.x_button.clicked.connect(lambda: self.on_click_add_to_email('x'))
    self.c_button.clicked.connect(lambda: self.on_click_add_to_email('c'))
    self.v_button.clicked.connect(lambda: self.on_click_add_to_email('v'))
    self.b_button.clicked.connect(lambda: self.on_click_add_to_email('b'))
    self.n_button.clicked.connect(lambda: self.on_click_add_to_email('n'))
    self.m_button.clicked.connect(lambda: self.on_click_add_to_email('m'))
    self.dot_button.clicked.connect(lambda: self.on_click_add_to_email('.'))
    self.at_button.clicked.connect(lambda: self.on_click_add_to_email('@'))

    self.gmail_button.clicked.connect(
      lambda: self.on_click_add_to_email('@gmail.com')
    )
    self.yahoo_button.clicked.connect(
      lambda: self.on_click_add_to_email('@yahoo.com')
    )
    self.hotmail_button.clicked.connect(
      lambda: self.on_click_add_to_email('@hotmail.com')
    )

    self.show()

  def on_click_send_email(self):
    textboxValue = self.textbox.text()
    # Defend against empty email
    if len(textboxValue) > 0:
      send_email_with_attachment(textboxValue, self.latest_photos)

  def on_click_take_picture(self):
    # Defend against multiple button clicks
    if self.is_in_progress is False:
      self.is_in_progress = True
      photo_taken = take_picture()
      self.latest_photo = photo_taken
      self.latest_photos = [photo_taken]
      self.display_photo(f'{self.latest_photo}')
      self.is_in_progress = False

  def on_click_take_pictures(self):
    # Defend against multiple button clicks
    if self.is_in_progress is False:
      self.is_in_progress = True
      self.latest_photos = [
        take_picture()
        for _ in range(N_NUMBER_MULTIPLE_PHOTOS)
      ]
      self.is_in_progress = False

  def on_click_record_gif(self):
    print("record gif")

  def on_click_record_video(self):
    print("record video")

  def on_click_clear_email(self):
    self.textbox.setText('')

  def on_click_backspace(self):
    self.textbox.setText(f"{self.textbox.text()[:-1]}")

  def on_click_add_to_email(self, string):
    self.textbox.setText(f"{self.textbox.text()}{string}")

  def display_photo(self, filename):
    pixmap = QPixmap(filename)
    self.photo_display.setPixmap(pixmap)
    self.photo_display.move(360, 20)
    self.photo_display.resize(pixmap.width() - 10, pixmap.height())


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())
