import sys, os
import numpy as np
import numpy.matlib as npm
from sklearn import svm
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


    # Get to the dataset folder, figure out which classes are present in the training dataset
    # by reading the subfolders' names:
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



    # =======   Data normalisation and dimensionality reduction   ========
    # Center feature matrix:
    mu = feature_matrix.mean(axis=0)
    feature_matrix = feature_matrix - npm.repmat(mu, feature_matrix.shape[0], 1)
    # Normalise:
    sigma = feature_matrix.std(axis=0)
    feature_matrix = np.divide(feature_matrix, npm.repmat(sigma, feature_matrix.shape[0], 1))

    # Reduce the dimensionality of the normalised feature matrix using SVD, retaining n% of the data's variance:
    u, s, vh = np.linalg.svd(feature_matrix)    # Get SVD of feature matrix
    s = pow(s,2)                                # Get its eigen values
    s = np.cumsum(s)/np.sum(s)                  # Normalise the sum of variances
    retained_variance = 0.75                    # How much of the original variance to retain in the approximation
    n_components = np.nonzero( s > retained_variance )[0][0] + 1
    feature_matrix_approx = np.matmul(feature_matrix, vh[:,:n_components]) #Approximate the feature matrix: Fapprox = F * Vappox



    # =======   Train a classifier   ========
    mdl = svm.SVC(gamma='auto', C=10)
    mdl.fit(feature_matrix_approx, labels)
    print('SVM classifier trained!')

    # Check inference on the training set:
    labels_res = mdl.predict(feature_matrix_approx)

    # Calculate and report the confusion matrix on the training set:
    conf_mat = np.zeros((len(gestures), len(gestures)), dtype=np.int)
    for i in range(len(labels)):
        conf_mat[labels[i], labels_res[i]] += 1
    
    print('Confusion matrix on training set:\n', conf_mat)



    # =======   Save results   ========
    # Save the classification model and feature extractor to a file to use for inference later:
    svd_approximation_matrix = vh[:,:n_components]
    filename = output_file + '.pkl'
    saved_model = {'svm':mdl, 'mu':mu, 'sigma':sigma, \
                   'svd_approximation_matrix':svd_approximation_matrix, \
                   'n_components':n_components, 'feature_extractor':extractor, \
                   'gestures':gestures}
               
    with open(filename, 'wb') as file:
        pickle.dump(saved_model, file)
	
	
	
	
if __name__ == '__main__':
    main()