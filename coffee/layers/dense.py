import numpy as np

from .. import frameworks as T
from .. import activations
from .. import global_vars as u

from .base import Layer




__all__ = ["Dense"]

class Dense(Layer):
    def __init__(self,
                 units,
                 activation=None,
                 use_bias=True,
                 init='glroot_uniform',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 name = None,
                 **kwargs):
        super(Dense, self).__init__(**kwargs)
        if name == None:
            name = 'Dense' + str(u.index)
            self.name = name
            u.index += 1
        else:
            self.name = name
        self.units = units
        self.activation = activaton
        def __call__(self, inputs):
            # set input/output shapes
            self.input_shape = inputs.shape
            self.output_shape = self.get_output_shape_for(self.input_shape)
            self.shape = self.output_shape
            # init the layer
            layer = T.dense(self.input_shape[1],
                            self.output_shape[1],
                            bias=use_bias)
            # grab the all_layers and forward lists and add this layer and the function call with its arguments to the lists
            u.all_layers[self.name] = layer
            # get the layers of all the inputs 
            args = (x.name for x in inputs)
            u.forwards.append((layer,) +  args)
            # depending on the activation add the activation layers as well with their arguments
            act = activations.get(self.activation)
            if act not in ['linear', None]:
                name = self.activation + str(u.activation)
                u.all_layers[name] = act
                args = self.name
                u.forwards.append((act,) + args)
            return self

        def get_output_shape_for(self, input_shape):
            return input_shape[:1] + (self.units,)

