from django.shortcuts import render
from .forms import ChatBotForm
import tensorflow as tf
import numpy as np
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import random
import string


def chatbot(request):
    form=ChatBotForm()
    if request.method=='POST':
        form=ChatBotForm(request.POST)
        response=None
        if form.is_valid():
            question=form.cleaned_data.get('question')
            with open('myapp/data.json','r') as f:
                file=json.load(f)
            tokenizer=tf.keras.preprocessing.text.tokenizer_from_json(file)
            model=load_model('myapp/chatterbot.h5')
            classes = np.loadtxt('myapp/classes.txt', dtype=str)

            # Create a new label encoder and set its classes
            le = LabelEncoder()
            le.classes_ = classes
            le.classes_
            input_shape=6
            with open('myapp/responses.json','r') as f:
                responses=json.load(f)
            text_p=[]
            prediction_input=question
            
        #     removing punt and converting to lower_case
            prediction_input=[letters.lower() for letters in prediction_input if letters not in string.punctuation]
            prediction_input=''.join(prediction_input)
            text_p.append(prediction_input)
            
        #     tokenizing and padding
            prediction_input=tokenizer.texts_to_sequences(text_p)
            prediction_input=np.array(prediction_input).reshape(-1)
            prediction_input=pad_sequences([prediction_input],input_shape)
            
        #     getting output from model

            output=model.predict(prediction_input)
            output=output.argmax()
            
        #     finding the right tag and predicting 
            response_tag=le.inverse_transform([output])[0]
            response=random.choice(responses[response_tag])

            if response:
                return render(request,'myapp/chatbot.html',{'form':form,'response':response})        

        return render(request,'myapp/chatbot.html',{'form':form})
    return render(request,'myapp/chatbot.html',{'form':form})