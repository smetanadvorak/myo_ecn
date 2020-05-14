import numpy as np
import numpy.matlib as npm
from sklearn import svm

class FeatureExtractor():
    def __init__(self, winlen=50, overlap=25):
        self.features = [self.mav]
        if winlen <= overlap:
            raise ValueError('Feature extractor initialisation: overlap should be smaller that window length.')
        self.winlen = winlen
        self.overlap = overlap
    
    def extract_feature_matrix(self, sig):
        feature_matrix = np.zeros((0, len(self.features) * sig.shape[1]))
        labels = []
        win_start   = [s for s in range(0, sig.shape[0], self.winlen-self.overlap) if s+self.winlen < sig.shape[0]]
        win_end     = [s + self.winlen for s in win_start]
        for (s,e) in zip(win_start, win_end):
            feature_vector = self.extract_feature_vector(sig[s:e,:])
            feature_matrix = np.vstack((feature_matrix, feature_vector))
        return feature_matrix
    
    def extract_feature_vector(self, sig):
        feat_vec = np.zeros((1,0))
        for feature in self.features:
            res = feature(sig)
            feat_vec = np.hstack((feat_vec, res))
        return feat_vec
    
    # Functions that extract features
    def mav(self, sig):
        res = abs(sig).mean(axis=0)
        return res[np.newaxis, :]
  
""" 
    def new_feature(self, sig):
        ...    
    Define functions that extract features here, add them to the features list in __init__()
    Feature should take the signal as np.matrix(len, nchan) and return a row vector np.matrix(1,nchan)
"""      




class ClassificationModel:
    def __init__(self):
        pass
        
    def fit(self, feature_matrix, labels, retained_variance = 0.75, classifier = None):
        feature_matrix = self.fit_normalise(feature_matrix)
        feature_matrix = self.fit_reduce_dimensionality(feature_matrix, retained_variance)
        
        if classifier is None:
            self.classifier = svm.SVC(gamma='auto', C=10)
        else:
            self.classifier = classifier
        
        self.classifier.fit(feature_matrix, labels)
        print('Classifier trained!')
        
        # Check inference on the training set:
        labels_res = self.classifier.predict(feature_matrix)

        # Calculate and report the confusion matrix on the training set:
        conf_mat = np.zeros((max(labels)+1, max(labels)+1), dtype=np.int)
        for i in range(len(labels)):
            conf_mat[labels[i], labels_res[i]] += 1
        print('Confusion matrix on training set:\n', conf_mat)
        
    def fit_normalise(self, feature_matrix):
        self.mu = feature_matrix.mean(axis=0)
        feature_matrix = feature_matrix - npm.repmat(self.mu, feature_matrix.shape[0], 1)

        self.sigma = feature_matrix.std(axis=0)
        feature_matrix = np.divide(feature_matrix, npm.repmat(self.sigma, feature_matrix.shape[0], 1))
        return feature_matrix
    
    def fit_reduce_dimensionality(self, feature_matrix, retained_variance):
        u, s, vh = np.linalg.svd(feature_matrix)    # Get SVD of feature matrix
        s = pow(s,2)                                # Get its eigen values
        s = np.cumsum(s)/np.sum(s)                  # Normalise the sum of variances
        n_components = np.nonzero( s > retained_variance )[0][0] + 1  # How much of the original variance to retain in the approximation
        self.v_approx = vh[:,:n_components]
        feature_matrix = np.matmul(feature_matrix, self.v_approx) #Approximate the feature matrix: Fapprox = F * Vappox
        return feature_matrix
    
    def predict(self, feature_matrix):
        # Normalize the input
        feature_matrix = feature_matrix - npm.repmat(self.mu, feature_matrix.shape[0], 1)
        feature_matrix = np.divide(feature_matrix, npm.repmat(self.sigma, feature_matrix.shape[0], 1))
        # Project to lower-dimensional space:
        feature_matrix = np.matmul(feature_matrix, self.v_approx)
        
        return self.classifier.predict(feature_matrix)
