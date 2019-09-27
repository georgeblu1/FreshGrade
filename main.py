from PySide2.QtWidgets import (QApplication, QDialog, QGraphicsScene, QLabel,
                               QPushButton, QVBoxLayout, QGraphicsView)
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl, QObject, Slot
from PySide2.QtGui import QImage, QPixmap
import cv2
import sys
import time

# import model

app = QApplication([])
# view = QQuickView()
# view.setResizeMode(QQuickView.SizeRootObjectToView)
# url = QUrl("view.qml")

# view.setSource(url)
# view.show()
# app.exec_()

vs = cv2.VideoCapture(0)

scene = QGraphicsScene()

# view = QGraphicsView(scene)
# view.show()

image_label = QLabel()
# image_label.show()


@Slot()
def fresh_button_clicked():
    print("Button clicked, Hello!")


fresh = QPushButton("Fresh")
fresh.clicked.connect(fresh_button_clicked)
# fresh.show()

dialog = QDialog()
layout = QVBoxLayout()

layout.addWidget(image_label)
layout.addWidget(fresh)
dialog.setLayout(layout)
dialog.show()

# scene.addWidget(fresh)
# scene.addWidget(image_label)
# image_label.show()

while True:
    ok, frame = vs.read()
    height, width, channel = frame.shape

    # pred = model.predict_fruit_class(frame)
    # TODO: show pred to user

    if cv2.waitKey(27) & 0xFF == ord('q'):
        break
    time.sleep(0.02)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    bytesperline = 3 * width
    image = QImage(rgb_frame.data, width, height, bytesperline, QImage.Format_RGB888)

    pixmap = QPixmap(image)

    image_label.setPixmap(pixmap)
