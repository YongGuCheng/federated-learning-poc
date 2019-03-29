import numpy as np

from commons.operations_utils.functions import get_encrypted_number, encrypt_vector, sum_encrypted_vectors, \
    get_serialized_encrypted_value


class LinearRegression:
    """Runs linear regression with local data or by gradient steps,
    where gradient can be passed in.

    Using public key can encrypt locally computed gradients.
    """

    def __init__(self, name, X, y, pubkey=None):
        self.name = name
        self.pubkey = pubkey
        self.X, self.y = X, y
        self.weights = np.zeros(X.shape[1])

    def set_weights(self, weights):
        self.weights = weights

    def fit(self, n_iter, eta=0.01):
        """Linear regression for n_iter"""
        for _ in range(n_iter):
            gradient = self.compute_gradient()
            self.gradient_step(gradient, eta)

    def gradient_step(self, gradient, eta=0.01):
        """Update the model with the given gradient"""
        self.weights -= eta * gradient

    def compute_gradient(self):
        """Compute the gradient of the current model using the training set
        """
        delta = self.predict(self.X) - self.y
        return delta.dot(self.X) / len(self.X)

    def predict(self, X):
        """Score test data"""
        return X.dot(self.weights)

    def encrypted_gradient(self):
        """Compute and encrypt gradient."""
        gradient = self.compute_gradient()
        #return gradient.tolist()
        return encrypt_vector(self.pubkey, gradient)


    # def process(self):
        # encrypt_aggr
        # encrypt_aggr = [get_encrypted_number(self.pubkey, encrypt_value['ciphertext'], encrypt_value['exponent']) for
        #                encrypt_value in encrypted_model['values']]
        # return [get_serialized_gradient(value) for value in self.encrypted_gradient(encrypt_aggr)]

    def process(self):
        #return self.encrypted_gradient()
        return [get_serialized_encrypted_value(value) for value in self.encrypted_gradient()]