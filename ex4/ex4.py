import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat

data = loadmat('ex3data1.mat')
print (data)

X = data['X']
y = data['y']

from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse = False)
y_processed = encoder.fit_transform(y)
print (y_processed.shape)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def forward_propagate(X, theta1, theta2):
    m = X.shape[0]

    a1 = np.insert(X, 0, values=np.ones(m), axis=1)
    z2 = a1 * theta1.T
    a2 = np.insert(z2, 0, values=np.ones(m), axis=1)
    z3 = a2 * theta2.T
    h = sigmoid(z3)

    return a1, z2, a2, z3, h


def cost(params, input_size, hidden_layer_size, num_labels, X, y, learning_rate):
    m = X.shape[0]
    X = np.matrix(X)
    y = np.matrix(y)

    theta1 = np.matrix(np.reshape(params[:hidden_layer_size * (input_size + 1)], (hidden_layer_size, (input_size + 1))))
    theta2 = np.matrix(np.reshape(params[hidden_layer_size*(input_size + 1):],
                                  (num_labels, (hidden_layer_size + 1))))

    a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)

    J = 0
    # loop in range of labels of output, J is bigger
    for i in range(num_labels):
        J += 1/m * np.sum(np.multiply(-y[:, i], np.log(h[:, i])) - np.multiply((1 - y[:, i]), np.log(1 - h[:, i])))

    # loop in range of number of inputs, J is smaller
    # for i in range(m):
    #     J += np.sum(np.multiply(-y[i, :], np.log(h[i, :])) - np.multiply((1 - y[i, :]), np.log(1-h[i, :])))
    # J = J/m

    return J


input_size = 400
hidden_layer_size = 25
num_labels = 10
learning_rate = 1

params = (np.random.random(size=hidden_layer_size * (input_size + 1) + num_labels * (hidden_layer_size + 1)) - 0.5) * 0.25

m = X.shape[0]
X = np.matrix(X)
y = np.matrix(y)

theta1 = np.matrix(np.reshape(params[:hidden_layer_size * (input_size + 1)], (hidden_layer_size, (input_size + 1))))
theta2 = np.matrix(np.reshape(params[hidden_layer_size * (input_size + 1):],
                              (num_labels, (hidden_layer_size + 1))))

J = cost(params, input_size, hidden_layer_size, num_labels, X, y_processed, learning_rate)

print(J)

regularization = (float(learning_rate) / (2 * m)) * (np.sum(np.power(theta1[:, 1:], 2)) + np.sum(np.power(theta2[:, 1:], 2)))

J = J + regularization

print(J)