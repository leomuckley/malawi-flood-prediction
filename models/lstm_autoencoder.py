#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 22:28:27 2020

@author: leo
"""


import tensorflow as tf
import matplotlib.pyplot as plt

class LSTMAutoencoder():
    
    def __init__(self, epochs, batch_size, loss, metric, callbacks):
        self.num_time_steps = 30
        self.num_temporal_feats = 10
        self.epochs = epochs
        self.batch = batch_size
        self.loss = loss
        self.metric = metric
        self.model = None
        self.history = None
        self.es = callbacks
        
    def fit(self, X, y, X_val, y_val):       
        temporal_input = tf.keras.Input(shape=(self.num_time_steps, self.num_temporal_feats), name="temporal")
        lstm_1 = tf.keras.layers.LSTM(32, return_sequences=True, kernel_initializer='glorot_normal')(temporal_input)
        lstm_2 = tf.keras.layers.LSTM(16, return_sequences=True, kernel_initializer='glorot_normal')(lstm_1)
        lstm_3 = tf.keras.layers.LSTM(1, kernel_initializer='glorot_normal')(lstm_2)
        repeat_1 = tf.keras.layers.RepeatVector(32)(lstm_3)
        lstm_4 = tf.keras.layers.LSTM(16, return_sequences=True, kernel_initializer='glorot_normal')(repeat_1)
        lstm_5 = tf.keras.layers.LSTM(32, kernel_initializer='glorot_normal')(lstm_4) 
        dense_1 = tf.keras.layers.Dense(1)(lstm_5)        
        self.model = tf.keras.Model(inputs=temporal_input, outputs=dense_1)
        self.model.compile(optimizer='adam', loss=self.loss, metrics=[self.metric])
        self.history = self.model.fit(X, y, epochs=self.epochs, batch_size=self.batch, validation_data=(X_val, y_val), callbacks=[self.es])
        
        return self.history
    
    def predict(self, X_test):
        return self.model.predict(X_test, batch_size=self.batch)
           
    def save(self, filename):
        return self.model.save(filename)
   
    def return_history(self):
        return self.history


        
