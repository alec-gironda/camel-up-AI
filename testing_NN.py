class TraditionalModel:
    '''

    '''

    #need to put the argparse stuff in this init and in the compilation
    def __init__(self,x_train,y_train,x_test,y_test,validation_method):

        #more arguments in here
        self.compiled_model = self.compile_model()

        self.x_train = np.asarray(x_train)
        self.y_train = np.asarray(y_train)

        self.validation_method = validation_method


        #should only be getting validation data if that is the validation method of choice
        self.validation_x = np.asarray(x_test[len(x_test)//2:])
        self.x_test = np.asarray(x_test[:len(x_test)//2])

        self.validation_y = np.asarray(y_test[len(y_test)//2:])
        self.y_test = np.asarray(y_test[:len(y_test)//2])

    #need to put more arguments in here
    def compile_model(self):

        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(1000,activation = tf.nn.relu))
        model.add(tf.keras.layers.Dense(2,activation= tf.nn.relu))

        optim = tf.keras.optimizers.Adam(learning_rate = 0.001)

        model.compile(optimizer=optim,loss='mean_squared_error',metrics=[tf.keras.metrics.RootMeanSquaredError(),tf.keras.metrics.MeanAbsoluteError()])

        return model

class Train:
    '''

    fit the model to training data

    '''

    def __init__(self,model):
        self.model = model
        self.compiled_model = model.compiled_model
        self.trained_model = self.fit_model(self.compiled_model,self.model)

    def fit_model(self,compiled_model,model):

        earlystopping = tf.keras.callbacks.EarlyStopping(monitor ="val_loss", mode ="min", patience = 20,restore_best_weights = True)

        compiled_model.fit(model.x_train,model.y_train,epochs=100,validation_data = (model.validation_x,model.validation_y),callbacks = [earlystopping])

        return compiled_model

class Evaluate:

    '''

    '''

    def __init__(self,compiled_model,trained_model):
        self.compiled_model = compiled_model
        self.trained_model = trained_model

        statistics = self.get_statistics(self.compiled_model,
                                            self.trained_model)
        self.val_loss = statistics[0]
        self.val_acc = statistics[1]

    def get_statistics(self,compiled_model,trained_model):
        val_loss, val_rmse, val_mae = trained_model.evaluate(compiled_model.x_test,
                                                   compiled_model.y_test)
        return [val_loss, val_rmse, val_mae]

if __name__ == "__main__":

    #
