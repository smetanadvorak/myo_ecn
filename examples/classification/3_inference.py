import pickle, time, sys
import numpy as np
import numpy.matlib as npm
from sklearn import svm
import myo
from myo_ecn.listeners              import Buffer, ConnectionChecker
from EMG_Classification             import FeatureExtractor, ClassificationModel

def main():

    # ================== setup myo-python (do not change) =====================
    myo.init(sdk_path='../../myo_sdk') # Compile Python binding to Myo's API
    hub = myo.Hub() # Create a Python instance of MYO API
    if not ConnectionChecker().ok: # Check connection before starting acquisition:
        quit()
    # =========================================================================

    # Parce command line inputs, if any
    input_file = 'models/trained_model.pkl'
    if len(sys.argv) > 1:
        input_file = sys.argv[1]


    # Load pickled feature extractor and classification model
    with open(input_file, 'rb') as file:
        model = pickle.load(file)
   
   
    # Extract variables from pickled object
    mdl = model['svm']
    mu  = model['mu']
    sigma = model['sigma']
    svd_approximation_matrix = model['svd_approximation_matrix']
    feature_extractor = model['feature_extractor']
    gestures = model['gestures']


    # Set up the buffer that will always contain the most up-to-date readings from the MYO
    emg_buffer = Buffer(feature_extractor.winlen)


    # Set up inference
    with hub.run_in_background(emg_buffer.on_event):
        print('You may start performing gestures')
        while hub.running:
            time.sleep(0.050)
            # Skip the rest until enough data for feature extraction is acquired
            if len(emg_buffer.emg_data_queue) < feature_extractor.winlen:
                continue

            # Get latest emg data
            emg = emg_buffer.get_emg_data()
            # Convert to a numpy matrix (an Nx8 matrix, each channel is a column):
            emg = np.array([x[1] for x in emg])
            # Extract features from the emg signal:
            feature_vector = feature_extractor.extract_feature_vector(emg)
            # Transform the vector the same way the training feature matrix was transformed: 
            # 1) Center:
            feature_vector -= mu
            # 2) Normalize: 
            feature_vector = np.divide(feature_vector, sigma)
            # 3) Project using SVD approximation matrix:
            feature_vector = np.matmul(feature_vector, svd_approximation_matrix)
            # Pass features to the classifier, make inference:
            inference = mdl.predict(feature_vector)
            # Implement majority voting here, if needed
        
            # Output inference:
            print('\rRecognized gesture: ', gestures[inference[0]], end='')
        
        
        
if __name__ == '__main__':
    main()