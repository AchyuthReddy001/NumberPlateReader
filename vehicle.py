import pandas as pd
import numpy as np
import itertools
import keras
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.models import Sequential
from keras import optimizers
from keras.preprocessing import image
from keras.layers import Dropout, Flatten, Dense
from keras import applications
from keras.utils.np_utils import to_categorical
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import math
import datetime
import time

# Default dimensions we found online
img_width, img_height = 224, 224

# Create a bottleneck file
top_model_weights_path = "bottleneck_fc_model.h5"
# loading up our datasets
train_data_dir = "D:\\FinalProject\\Data\\train"
validation_data_dir = "D:\\FinalProject\\Data\\validate"
test_data_dir = "D:\\FinalProject\\Data\\test"
# number of epochs to train top model
epochs = 7  # this has been changed after multiple model run
# batch size used by flow_from_directory and predict_generator
batch_size = 50


#Loading vgg16 model
vgg16 = applications.VGG16(include_top=False, weights="imagenet")
datagen = ImageDataGenerator(rescale=1. / 255)
#needed to create the bottleneck .npy files

'''
# __this can take an hour and half to run so only run it once.
# once the npy files have been created, no need to run again. Convert this cell to a code cell to run.__
start = datetime.datetime.now()

generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode=None,
    shuffle=False)

nb_train_samples = len(generator.filenames)
num_classes = len(generator.class_indices)

predict_size_train = int(math.ceil(nb_train_samples / batch_size))

bottleneck_features_train = vgg16.predict_generator(generator, predict_size_train)

np.save('bottleneck_features_train.npy', bottleneck_features_train)
end = datetime.datetime.now()
elapsed = end - start
print('Time: ', elapsed)

'''

# training data
generator_top = datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle = False)

nb_train_samples = len(generator_top.filenames)
num_classes = len(generator_top.class_indices)

# load the bottleneck features saved earlier
train_data = np.load('bottleneck_features_train.npy')

# get the class labels for the training data, in the original order
train_labels = generator_top.classes

# convert the training labels to categorical vectors
train_labels = to_categorical(train_labels, num_classes=num_classes)


#valid
# training data
generator_top = datagen.flow_from_directory(
    test_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle = False)

nb_train_samples = len(generator_top.filenames)
num_classes = len(generator_top.class_indices)

# load the bottleneck features saved earlier
validation_data = np.load("bottleneck_features_train.npy")

# get the class labels for the training data, in the original order
validation_labels = generator_top.classes

# convert the training labels to categorical vectors
validation_labels = to_categorical(validation_labels, num_classes=num_classes)

#test
# training data
generator_top = datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle = False)

nb_train_samples = len(generator_top.filenames)
num_classes = len(generator_top.class_indices)

# load the bottleneck features saved earlier
test_data = np.load("bottleneck_features_train.npy")

# get the class labels for the training data, in the original order
test_labels = generator_top.classes

# convert the training labels to categorical vectors
test_labels = to_categorical(test_labels, num_classes=num_classes)


#model
start = datetime.datetime.now()
model = Sequential()
model.add(Flatten(input_shape=train_data.shape[1:]))
model.add(Dense(100, activation=keras.layers.LeakyReLU(alpha=0.3)))
model.add(Dropout(0.5))
model.add(Dense(50, activation=keras.layers.LeakyReLU(alpha=0.3)))
model.add(Dropout(0.3))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy',
   optimizer=optimizers.RMSprop(lr=1e-4),
   metrics=['acc'])
history = model.fit(train_data, train_labels,
   epochs=7,
   batch_size=batch_size,
   validation_data=(validation_data, validation_labels))
model.save_weights(top_model_weights_path)
(eval_loss, eval_accuracy) = model.evaluate(validation_data, validation_labels, batch_size=batch_size,     verbose=1)

print('[INFO] accuracy: {:.2f}%'.format(eval_accuracy * 100))
print('[INFO] Loss: {}'.format(eval_loss))
end= datetime.datetime.now()
elapsed= end-start
print ('Time: ', elapsed)

model.evaluate(test_data,test_labels)

def read_image(file_path):
   print("[INFO] loading and preprocessing image…")
   image = load_img(file_path, target_size=(224, 224))
   image = img_to_array(image)
   image = np.expand_dims(image, axis=0)
   image /= 255.
   return image
def test_single_image(path):
  veh = ['bike', 'bus', 'car', 'lorry']
  images = read_image(path)
  #print("Hello")
  time.sleep(.5)
  bt_prediction = vgg16.predict(images)
  preds = model.predict_proba(bt_prediction)

  for idx, veh, x in zip(range(0,4), veh , preds[0]):
   print('ID: {}, Label: {} {}%'.format(idx, veh, round(x*100,2) ))
  #print('Final Decision:')
  time.sleep(.5)

  for x in range(3):
  # print('.'*(x+1))
   time.sleep(.2)
  class_predicted = model.predict_classes(bt_prediction)
  class_dictionary = generator_top.class_indices
  inv_map = {v: k for k, v in class_dictionary.items()}
  #print('ID: {}, Label: {}'.format(class_predicted[0],  inv_map[class_predicted[0]]))
  print('Final Decision:',inv_map[class_predicted[0]])
  return inv_map[class_predicted[0]]
#path = "F:/M.Tech-Project/Final_prjt-2020-1/LicPlateImages/correct_pred/2.png"
#test_single_image(path)
