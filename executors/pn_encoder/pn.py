import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.python.framework.errors_impl import NotFoundError


def conv_bn(x, filters):
    x = layers.Conv1D(filters, kernel_size=1, padding='valid')(x)
    x = layers.BatchNormalization(momentum=0.0)(x)
    return layers.Activation('relu')(x)


def dense_bn(x, filters):
    x = layers.Dense(filters)(x)
    x = layers.BatchNormalization(momentum=0.0)(x)
    return layers.Activation('relu')(x)


def tnet(inputs, num_features):
    class OrthogonalRegularizer(keras.regularizers.Regularizer):
        def __init__(self, num_features_, l2reg=0.001):
            self.num_features = num_features_
            self.l2reg = l2reg
            self.eye = tf.eye(self.num_features)

        def __call__(self, x):
            x = tf.reshape(x, (-1, self.num_features, self.num_features))
            xxt = tf.tensordot(x, x, axes=(2, 2))
            xxt = tf.reshape(xxt, (-1, self.num_features, self.num_features))
            return tf.reduce_sum(self.l2reg * tf.square(xxt - self.eye))

        def get_config(self):
            return {'num_features': self.num_features,
                    'l2reg': self.l2reg,
                    'eye': self.eye.numpy()}

    # Initialize bias as the identity matrix
    bias = keras.initializers.Constant(np.eye(num_features).flatten())
    reg = OrthogonalRegularizer(num_features)

    x = conv_bn(inputs, 32)
    x = conv_bn(x, 64)
    x = conv_bn(x, 512)
    x = layers.GlobalMaxPooling1D()(x)
    x = dense_bn(x, 256)
    x = dense_bn(x, 128)
    x = layers.Dense(
        num_features * num_features,
        kernel_initializer='zeros',
        bias_initializer=bias,
        activity_regularizer=reg,
    )(x)
    feat_T = layers.Reshape((num_features, num_features))(x)
    # Apply affine transformation to input features
    return layers.Dot(axes=(2, 1))([inputs, feat_T])


def get_model(num_class, num_point=2048, hard_label=True):
    inputs = keras.Input(shape=(num_point, 3))

    x = tnet(inputs, 3)
    x = conv_bn(x, 32)
    x = conv_bn(x, 32)
    x = tnet(x, 32)
    x = conv_bn(x, 32)
    x = conv_bn(x, 64)
    x = layers.GlobalMaxPooling1D()(x)
    x = dense_bn(x, 128)
    x = layers.Dropout(0.3)(x)

    outputs = layers.Dense(num_class, activation='softmax' if hard_label else 'sigmoid')(x)

    return keras.Model(inputs=inputs, outputs=outputs, name='pointnet')


def get_bottleneck_model(ckpt_path):
    model = get_model(1)
    intermediate_layer_model = keras.Model(inputs=model.input,
                                           outputs=[model.get_layer(f'dense_{j}').output for j in range(1, 7)])

    intermediate_layer_model.load_weights(ckpt_path)
    return intermediate_layer_model


def train_model(train_dataset, ckpt_path, num_class, num_epoch, hard_label=True):
    model = get_model(num_class, hard_label=hard_label)
    try:
        model.load_weights(ckpt_path)
    except NotFoundError:
        pass  #: first time, pass intentionally

    if hard_label:
        model.compile(
            loss='categorical_crossentropy',
            optimizer=keras.optimizers.Adagrad(learning_rate=0.001),
            metrics=['accuracy', 'AUC'],
        )
    else:
        model.compile(
            loss='binary_crossentropy',
            optimizer=keras.optimizers.Adagrad(learning_rate=0.001),
            metrics=['accuracy', 'AUC'],
        )

    model.fit(train_dataset, epochs=num_epoch)
    model.save_weights(ckpt_path)
