
import dynet as dy
import Saxe
import numpy as np

class MLP:
    """ MLP with 1 hidden Layer """

    def __init__(self, model, input_dim, hidden_dim, output_dim, dropout = 0, softmax=False):

        self.input = input_dim
        self.hidden = hidden_dim
        self.output = output_dim
        self.dropout = dropout
        self.softmax = softmax

        self.WI2H = model.add_parameters((self.hidden,self.input))
        self.bI2H = model.add_parameters((self.hidden), init = dy.ConstInitializer(0))
        self.WH2O = model.add_parameters((self.output,self.hidden))
        self.bH20 = model.add_parameters((self.output), init = dy.ConstInitializer(0))

    def __call__(self, inputs, predict=False):

        WI2H = dy.parameter(self.WI2H)
        bI2H = dy.parameter(self.bI2H)
        WH2O = dy.parameter(self.WH2O)
        bH20 = dy.parameter(self.bH20)

        if (predict):
            hidden = dy.tanh(dy.affine_transform([bI2H,WI2H,inputs]))
        else:
            hidden = dy.dropout(dy.tanh(dy.affine_transform([bI2H,WI2H,inputs])),self.dropout)


        output = dy.affine_transform([bH20,WH2O,hidden])

        if (self.softmax):
            return dy.softmax(output)
        else:
            return output


class Lin_Projection:
    """ Linear projection Layer """

    def __init__(self, model, input_dim,output_dim):

        self.input = input_dim
        self.output = output_dim

        Saxe_initializer = Saxe.Orthogonal()
        self.W = model.add_parameters((self.output,self.input), init=dy.NumpyInitializer(Saxe_initializer(((self.output,self.input)))))
        self.b = model.add_parameters((self.output), init = dy.ConstInitializer(0))


    def __call__(self, inputs):

        W = dy.parameter(self.W)
        b = dy.parameter(self.b)

        output = dy.affine_transform([b,W,inputs])

        return output

    def L2_req_term(self):

        W = dy.parameter(self.W)
        WW = W *dy.transpose(W)
        loss = dy.squared_norm(WW - dy.inputTensor(np.eye(self.output))) / 2
        return loss
