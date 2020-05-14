import sys, os
import numpy as np
import pickle
from EMG_Classification import FeatureExtractor, ClassificationModel

def main():
    # Parce command line inputs, if any
    data_folder = 'data'
    output_file = 'models/trained_model'
    if len(sys.argv) > 1:
        data_folder = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    
    # =======       Setup        ========
    # Setup the windowing parameters and feature extractor:
    extractor = FeatureExtractor(winlen=100, overlap=75)

    # Define feature matrix and label vector:
    n_features = len(extractor.features)
    n_channels = 8;
    feature_matrix  = np.zeros((0, n_features * n_channels))
    labels = []

    # Get to the dataset folder, figure out which classes are present 
    # in the training dataset by reading the subfolders' names:
    os.chdir(data_folder)
    gestures = dict(enumerate(sorted([c for c in os.listdir() if os.path.isdir(c)])))



    # =======   Extract feature matrix   ========
    # For each class (i.e. gesture) ...
    for (g, gesture) in gestures.items():
        os.chdir(gesture)
        # ... access all trials (repetitions of this gesture) ...
        trials = sorted([t for t in os.listdir() if os.path.isfile(t)])
        for trial in trials:
            # ... load EMG data from the .csv file ...
            emg = np.loadtxt(trial, delimiter=', ')
            # ... extract features and concatenate to the feature matrix ...
            to_add = extractor.extract_feature_matrix(emg)
            feature_matrix  = np.vstack((feature_matrix, to_add))
            # ... and concatenate the class' labels to the labels vector.
            labels         += [g] * to_add.shape[0]
        os.chdir('..')
    # Get back to the original folder
    os.chdir('..')



    # ======= Fit classification model =======
    mdl = ClassificationModel()
    mdl.fit(feature_matrix, labels)



    # =======   Save results   ========
    # Save the classification model and feature extractor to a file to use for inference later:
    filename = output_file + '.pkl'
    saved_model = {'feature_extractor':extractor, 'mdl':mdl, 'gestures':gestures}
               
    with open(filename, 'wb') as file:
        pickle.dump(saved_model, file)
	
	
if __name__ == '__main__':
    main()