from keras.preprocessing import image
from keras.models import Sequential, load_model
import numpy as np
import cv2

# GLOBALS
PATH_TO_TRAINED_MODEL_FILE = 'fruit_classify_model.h5'
size = 512

def predict_fruit_class(frame, trained_model, class_dict):
    """
    Perform class prediction on input image and print predicted class.

    Args:
        image_path(str): Absolute Path to test image
        trained_model(object): trained model from load_model()
        class_dict(dict): python dict of all image classes.

    Returns:
        Probability of predictions for each class.
    """
    #x = image.load_img(frame, target_size=(size,size))
    x = image.img_to_array(cv2.resize(frame, (size,size)))
    x = np.expand_dims(x, axis=0)
    prediction_class = trained_model.predict_classes(x, batch_size=1)
    prediction_probs = trained_model.predict_proba(x, batch_size=1)
    #print('probs:',prediction_probs)
    #print('class_index:',prediction_class[0])
    for key, value in class_dict.items():
        if value == prediction_class.item():
            return key
    return None
		
trained_model_path = PATH_TO_TRAINED_MODEL_FILE
trained_model = load_model(trained_model_path)
class_dict = np.load('class_dict.npy', allow_pickle=True).item()

vs = cv2.VideoCapture(0)
ok, frame = vs.read()
while vs.isOpened():
	ok, frame = vs.read()
	cv2.imshow('my webcam', frame)
	print(predict_fruit_class(frame,trained_model,class_dict))
	if cv2.waitKey(1) == 27: 
		break  # esc to quit
cv2.destroyAllWindows()