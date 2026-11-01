import numpy as np

def softmax(x):
    x = np.asarray(x, dtype=float)
    e = np.exp(x - x.max())          # subtract max: avoids overflow
    return e / e.sum()

def predict(features, weights):
    return int(np.argmax(softmax(np.asarray(weights) @ np.asarray(features))))
