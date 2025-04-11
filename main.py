from tkinter import *
from tkinter import messagebox
import numpy as np
import nltk
import re
from nltk.corpus import stopwords
from gensim.models.keyedvectors import KeyedVectors
from keras.models import load_model
import keras.backend as K

from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import messagebox, filedialog


import speech_recognition as sr

import googletrans
from googletrans import Translator

from gtts import gTTS



nltk.download('stopwords')
nltk.download('punkt')

#Load models globally
try:
    word2vec_model = KeyedVectors.load_word2vec_format("word2vecmodel.bin", binary=True)
except FileNotFoundError:
    print("word2vec model file not found!")

try:
    lstm_model = load_model("final_lstm.h5")
    lstm_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
except FileNotFoundError:
    print("LSTM model file not found!")

def inputtext(text):
    stop_words = set(stopwords.words('english'))
    text = re.sub("[^A-Za-z]", " ", text)
    text = text.lower()
    filtered_sentence = [w for w in text.split() if w not in stop_words]
    return filtered_sentence

def getvector(essays, model, numberfeature):
    essay_vecs = np.zeros((len(essays), numberfeature), dtype="float32")
    for c, essay in enumerate(essays):
        vec = np.zeros((numberfeature,), dtype="float32")
        noOfWords = 0.
        for word in essay:
            if word in model.index_to_key:
                vec = np.add(vec, model[word])
                noOfWords += 1
        if noOfWords > 0:
            vec = np.divide(vec, noOfWords)
        essay_vecs[c] = vec
    return essay_vecs

def converttoverctor(text):
    numberfeature = 300
    clean_test_essays = [inputtext(text)]
    testdatavector = getvector(clean_test_essays, word2vec_model, numberfeature)
    testdatavector = np.reshape(testdatavector,(testdatavector.shape[0], 1, testdatavector.shape[1]))

    predictionvalue = lstm_model.predict(testdatavector)
    return round(predictionvalue[0][0])

def text_score(text):
    K.clear_session()
    if not text or len(text) < 20:
        raise ValueError("Text is too short or missing.")
    
    score = converttoverctor(text)
    return score


def on_predict():
    text = text_area.get("1.0", END).strip()
    if len(text) < 20:
        messagebox.showerror("Error", "Text is too short. Please enter at least 20 characters.")
        return
    
    try:
        score = text_score(text)
        result_label.config(text=f"Predicted Score: {score}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


framebg = "#161d3f"
bodybg = "#84a1e8"

root = Tk()
root.title("Essay Score Prediction")
root.geometry("1030x570+290+140")
root.resizable(False, False)
root.config(bg="#bf5d43")





# Translation Functions

def trans_text():
    text1_ = text_area.get(1.0, END)
    translated_text = translate(text1_, combo1.get(), combo.get())
    text_area2.delete(1.0, END)
    text_area2.insert(END, translated_text)
    
def translate(text_, trans_from, trans_to):
    t1 = Translator()
    trans_text = t1.translate(text_, src=trans_from, dest=trans_to)
    return trans_text.text





    

# Icon
image_icon = PhotoImage(file="Images/icon.png")
root.iconphoto(False, image_icon)

# Top Frame
Top_frame = Frame(root, bg="#321246", width=1100, height=100)
Top_frame.place(x=0, y=0)
Logo = PhotoImage(file="Images/logo.png")
Label(root, image=Logo, bg="#321246").place(x=40, y=15)
Label(Top_frame, text="Essay Predict", font="arial 20 bold", bg="#321246", fg="#fff").place(x=190, y=40)

# Text Area
text_area = Text(root, font="Robote 15", bg="#cbe7c2", relief=GROOVE, wrap=WORD)
text_area.place(x=40, y=140, width=600, height=200)


# Language Comboboxes
language = googletrans.LANGUAGES
languageV = list(language.values())

combo1 = ttk.Combobox(root, values=languageV, font="Roboto 10", state="r", width=10)
combo1.place(x=200, y=100)
combo1.set("ENGLISH")

combo = ttk.Combobox(root, values=languageV, font="Roboto 10", state="r", width=10)
combo.place(x=330, y=100)
combo.set("ENGLISH")

text_area2 = Text(root, font="Robote 15", bg="#e5eec1", relief=GROOVE, wrap=WORD)
text_area2.place(x=40, y=360, width=600, height=200)


# Buttons
imageicon = PhotoImage(file="Images/Predict.png")
btn = Button(root, compound=LEFT, image=imageicon, bd=0, bg="#bf5d43", font="arial 14 bold",command=on_predict)
btn.place(x=700, y=200)



transimage = PhotoImage(file="Images/translate.png")
trans_button = Button(root, image=transimage, bg="#bf5d43", bd=0, command=trans_text)  # type: ignore
trans_button.place(x=880, y=207)


result_label = Label(root, text="Predicted Score: ")
result_label.place(x=700,y=300)

root.mainloop()
