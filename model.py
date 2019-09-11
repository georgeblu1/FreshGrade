from PySide2.QtWidgets import (QApplication, QDialog, QGraphicsScene,
                               QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
                               QGraphicsView, QFrame)
from PySide2.QtCore import QUrl, QObject, Slot
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtQuick import QQuickView
from keras.models import Sequential, load_model
from keras.preprocessing import image
from threading import Thread
import copy
import cv2
import cv2
import numpy as np
import sys
import time


if __name__ == '__main__':
    app = QApplication([])
    image_label = QLabel()


    @Slot()
    def fresh_button_clicked():
        print("Button clicked, Hello!")


    fresh_apple = QPushButton("Fresh Apple")
    fresh_apple.clicked.connect(fresh_button_clicked)

    fresh_orange = QPushButton("Fresh Orange")
    fresh_orange.clicked.connect(fresh_button_clicked)

    rotten_apple = QPushButton("Rotten Apple")
    rotten_apple.clicked.connect(fresh_button_clicked)

    rotten_orange = QPushButton("Rotten Orange")
    rotten_orange.clicked.connect(fresh_button_clicked)

    buttons_layout = QHBoxLayout()
    buttons_layout.addWidget(fresh_apple)
    buttons_layout.addWidget(rotten_apple)
    buttons_layout.addWidget(fresh_orange)
    buttons_layout.addWidget(rotten_orange)
    buttons_frame = QFrame()
    buttons_frame.setLayout(buttons_layout)

    pred_label = QLabel()

    dialog = QDialog()
    layout = QVBoxLayout()

    layout.addWidget(image_label)
    layout.addWidget(buttons_frame)
    layout.addWidget(pred_label)
    dialog.setLayout(layout)
    dialog.show()

    def main_loop():
        """Loading models and prediction need to be on the same thread."""
        PATH_TO_TRAINED_MODEL_FILE = 'fruit_classify_model.h5'
        size = 512

        trained_model_path = PATH_TO_TRAINED_MODEL_FILE
        trained_model = load_model(trained_model_path)
        class_dict = np.load('class_dict.npy', allow_pickle=True).item()


        def predict_fruit_class(image_path, trained_model=trained_model, class_dict=class_dict):
            """
            Perform class prediction on input image and print predicted class.

            Args:
                image_path(str): Absolute Path to test image
                trained_model(object): trained model from load_model()
                class_dict(dict): python dict of all image classes.

            Returns:
                Probability of predictions for each class.
            """
            # x = image.load_img(image_path, target_size=(size,size))
            x = image.img_to_array(cv2.resize(image_path, (size,size)))
            x = np.expand_dims(x, axis=0)
            prediction_class = trained_model.predict_classes(x, batch_size=1)
            #prediction_probs = trained_model.predict_proba(x, batch_size=1)
            #print('probs:',prediction_probs)
            #print('class_index:',prediction_class[0])
            for key, value in class_dict.items():
                if value == prediction_class.item():
                    return key
            return None

        vs = cv2.VideoCapture(2)
        while vs.isOpened():
            ok, frame = vs.read()
            height, width, channel = frame.shape

            # increase brightness
            # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # hsv[:,:,2] += 10
            # frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

            pred = predict_fruit_class(frame)
            pred_label.setText("Prediction: " + pred)

            if cv2.waitKey(27) & 0xFF == ord('q'):
                break
            time.sleep(0.03)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bytesperline = 3 * width
            qimage = QImage(rgb_frame.data, width, height, bytesperline, QImage.Format_RGB888)
            pixmap = QPixmap(qimage)
            image_label.setPixmap(pixmap)

    thread = Thread(target=main_loop)
    thread.start()

    app.exec_()
