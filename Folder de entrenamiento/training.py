import random
import json
import pickle
import numpy as np
#from keras.optimizers import SGD
from keras.optimizers import Adam

import nltk
from nltk.stem import WordNetLemmatizer #Para pasar las palabras a su forma raíz

#Para crear la red neuronal
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
#from keras.optimizers import sgd_experimental

lemmatizer = WordNetLemmatizer()

intents = json.loads(open(R'C:\Users\PC\Desktop\Proyecto IA\Folder de entrenamiento\leng.json').read())

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '¿', '.', ',']

#Clasifica los patrones y las categorías
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

#Pasa la información a unos y ceros según las palabras presentes en cada categoría para hacer el entrenamiento
training = []
output_empty = [0]*len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
random.shuffle(training)
training = np.array(training) 
print(training) 


# Reparte los datos para pasarlos a la red
train_x = list(training[:,0])
train_y = list(training[:,1])

# Import additional layers and regularizers
from keras.layers import LeakyReLU
from keras.regularizers import l2

# Creamos la red neuronal con mejoras
model = Sequential()

# Input layer
model.add(Dense(512, input_shape=(len(train_x[0]),), activation='linear', kernel_regularizer=l2(0.01)))
model.add(LeakyReLU(alpha=0.05))
model.add(Dropout(0.5))

# Hidden layers
model.add(Dense(512, activation='linear', kernel_regularizer=l2(0.01)))
model.add(LeakyReLU(alpha=0.05))
model.add(Dropout(0.5))

model.add(Dense(256, activation='linear', kernel_regularizer=l2(0.01)))
model.add(LeakyReLU(alpha=0.05))
model.add(Dropout(0.5))

# Output layer
model.add(Dense(len(train_y[0]), activation='softmax'))

# Creamos el optimizador y lo compilamos
opt = Adam(learning_rate=0.001)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])


#Entrenamos el modelo y lo guardamos
train_process = model.fit(np.array(train_x), np.array(train_y), epochs=20000, batch_size=256, verbose=1)
model.save(r"C:\Users\PC\Desktop\Proyecto IA\Folder de entrenamiento\chatbot_model.h5", train_process)