# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Thomax Young)s
"""

import network_practice
net=network_practice.Network([784, 30, 10])
net.SGD(training_data, 30, 10, 3.0, test_data=test_data)