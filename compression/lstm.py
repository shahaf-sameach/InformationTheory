from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
import numpy as np
import pickle


def get_train(start,end,step,maxlen):
  sentences = []
  next_chars = []
  for i in range(start, end - maxlen, step):
      sentences.append(text[i: i + maxlen])
      next_chars.append(text[i + maxlen])
  print('nb sequences:', len(sentences))

  print('Vectorization...')
  X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
  y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
  for i, sentence in enumerate(sentences):
      for t, char in enumerate(sentence):
          X[i, t, char_indices[char]] = 1
      y[i, char_indices[next_chars[i]]] = 1
  
  return X,y
  

text = open('dickens.txt',errors='ignore').read()

#text=text[0:6500000]
print('corpus length:', len(text))
chars = set(text)
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))




# cut the text in semi-redundant sequences of maxlen characters
step = 4
maxlen = 30

print('Build model...')
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(maxlen, len(chars))))
model.add(Dropout(0.2))
model.add(LSTM(56, return_sequences=False))
model.add(Dropout(0.2))

model.add(Dense(len(chars)))
model.add(Activation('softmax'))

# build the model: 2 stacked LSTM

print(1)
model.compile(loss='categorical_crossentropy', optimizer='rmsprop',  metrics=["accuracy"])
print(1)
T=[4,2,4/3,1]
for i in range(4):
  print(i)
  start = 0
  for j in  T:
    end=int(len(text)//j)
    X, y = get_train(start, end,step,maxlen)
    model.fit(X, y, batch_size=512, epochs=1)
    start=end


dict_error={}
dict_position={}
for start_index in range(10457476):
    sentence = text[start_index: start_index + maxlen];
    x = np.zeros((1, maxlen, len(char_indices)))
    for t, char in enumerate(sentence):
        x[0, t, char_indices[char]] = 1
    answer = model.predict(x, verbose=0)[0]
    next_index = np.argmax(answer)
    nextChar = indices_char[next_index]
    real_char= text[i+1]
    if nextChar!=real_char :
        dict_position[start_index]=real_char+'_'+nextChar
        if real_char+'_'+nextChar in dict_error:
            dict_error[real_char+'_'+nextChar] +=1
        else:
            dict_error[real_char + '_' + nextChar] = 1

dicts_=[dict_error,dict_position]
with open('dict error','wb') as f:
    pickle.dump(dicts_,f)


model.save('InfoModel.h5')
json_string = model.to_json()
open('my_model_architecture2.json', 'w').write(json_string)
model.save_weights('my_model_weights2.h5')
