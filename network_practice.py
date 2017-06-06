# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Thomax Young)s
"""

import numpy as np
import random

class Network(object):
    def __init__(self,sizes):
        self.num_layers=len(sizes)
        self.sizes=sizes
        self.biases=[np.random.randn(y,1) for y in sizes[1:]]
        self.weights=[np.random.randn(y,x)
                        for x,y in zip(sizes[:-1], sizes[1:])]
        
    
    def show(self):
        print('the sizes are %s'%self.sizes)
        print('the biases are %s'%self.biases)
        print('the weights are %s'%self.weights)

   
    def feedforward(self, a):
        for b,w in zip(self.biases, self.weights):
           '''
           debug code
          
          
           print('the input is %s'%a)
           print('the weights are%s'%w)
           print('the biases are%s'%b)
            '''
           #might need to transpose b
           #the reason you got the wrong anser is that you did not specific 
           #in_put's dimention it is  (n,) by defalt if you define it as 
           #input=np.array([1,2]). you should hve (n,1)
           #so either you use i=np.array([[1],[2]]),or i.reshape(2,1)
           #becareful with this
           a=sigmoid(np.dot(w, a)+b)
           #a=sigmoid(np.dot(w, a).transpose()+b)
        return a
    
    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        if test_data: 
            n_test=len(test_data)
        n=len(training_data)
        for j in xrange(epochs):
            random.shuffle(training_data)
            mini_batches=[training_data[k:k+mini_batch_size]
                        for k in xrange(0,n, mini_batch_size)]
            for mini_batche in mini_batches:
                self.update_mini_batch(mini_batche, eta)
            if test_data:
                print('epoch {0}:{1}/{2}'.format(
                        j,self.evaluate(test_data),n_test))
            else:
                print('epoch {0} complete'.format(j))
            
    def update_mini_batch(self,mini_batch, eta):
        nbla_b=[np.zeros(b.shape) for b in self.biases]
        nbla_w=[np.zeros(w.shape) for w in self.weights]
        for x,y in mini_batch:
            delta_nbla_b, delta_nbla_w=self.backprop(x,y)
            nbla_b=[nb+dnb for nb,dnb in zip(nbla_b, delta_nbla_b)]
            nbla_w=[nw+dnw for nw,dnw in zip(nbla_w, delta_nbla_w)]
        self.weights=[w-(eta/len(mini_batch))*nw
                      for w,nw in zip(self.weights, nbla_w)]
        self.biases=[b-(eta/len(mini_batch))*nb
                     for b,nb in zip(self.biases, nbla_b)]

    def backprop(self, x, y):
            """Return a tuple ``(nabla_b, nabla_w)`` representing the
            gradient for the cost function C_x.  ``nabla_b`` and
            ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
            to ``self.biases`` and ``self.weights``."""
            nabla_b = [np.zeros(b.shape) for b in self.biases]
            nabla_w = [np.zeros(w.shape) for w in self.weights]
            # feedforward
            activation = x
            activations = [x] # list to store all the activations, layer by layer
            zs = [] # list to store all the z vectors, layer by layer
            for b, w in zip(self.biases, self.weights):
                z = np.dot(w, activation)+b
                zs.append(z)
                activation = sigmoid(z)
                activations.append(activation)
            # backward pass
            delta = self.cost_derivative(activations[-1], y) * \
                sigmoid_prime(zs[-1])
            nabla_b[-1] = delta
            nabla_w[-1] = np.dot(delta, activations[-2].transpose())
            # Note that the variable l in the loop below is used a little
            # differently to the notation in Chapter 2 of the book.  Here,
            # l = 1 means the last layer of neurons, l = 2 is the
            # second-last layer, and so on.  It's a renumbering of the
            # scheme in the book, used here to take advantage of the fact
            # that Python can use negative indices in lists.
            for l in xrange(2, self.num_layers):
                z = zs[-l]
                sp = sigmoid_prime(z)
                delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
                nabla_b[-l] = delta
                nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
            return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        return (output_activations-y)

#aware the indentation that if you need a function global, you make it no indentation
    #### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))
    

        
            
         
            
    