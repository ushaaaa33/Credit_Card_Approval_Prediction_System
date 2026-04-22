import numpy as np
from collections import Counter

def gini_index(y):
    
    counts = Counter(y)
    impurity = 1
    for label in counts:
        prob = counts[label] / len(y)
        impurity -= prob ** 2
    return impurity

def split_dataset(X, y, feature_index, threshold):
    
    left_idx = X[:, feature_index] <= threshold       # Find indices where condition is True
    right_idx = X[:, feature_index] > threshold       # Find indices where condition is False
    return X[left_idx], X[right_idx], y[left_idx], y[right_idx]

def best_split(X, y):

    best_feature, best_threshold, best_gain = None, None, -1
    parent_impurity = gini_index(y)  
    
    n_features = X.shape[1]     # get total no. of couls 
    
    for feature in range(n_features):
        thresholds = np.unique(X[:, feature])    #get all unique values in that column
        
        for threshold in thresholds:   # find every values as  a potential split point
            X_left, X_right, y_left, y_right = split_dataset(X, y, feature, threshold)
            
            if len(y_left) == 0 or len(y_right) == 0:
                continue
            
            # Calculate Weighted Impurity of children
            child_impurity = (len(y_left) / len(y)) * gini_index(y_left) + \
                           (len(y_right) / len(y)) * gini_index(y_right)
            info_gain = parent_impurity - child_impurity
            
            # If this is the best gain we've seen, save these parameters
            if info_gain > best_gain:
                best_gain, best_feature, best_threshold = info_gain, feature, threshold
    
    return best_feature, best_threshold, best_gain

class Node:
    
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

class DecisionTreeClassifierCustom:
    
    def __init__(self, max_depth=10, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None
        self.node_count = 0

    def build_tree(self, X, y, depth=0):
       
        n_samples, n_features = X.shape
        num_labels = len(np.unique(y))
        
        self.node_count += 1    # track how many nodes we have created
        if self.node_count % 100 == 0:
            print(f"  Building tree... {self.node_count} nodes created", end='\r')
        
        # Stopping criteria
        if depth >= self.max_depth or num_labels == 1 or n_samples < self.min_samples_split:
            return Node(value=Counter(y).most_common(1)[0][0])  # return most frequent clas
        
        feature, threshold, gain = best_split(X, y)
        
        if gain == -1:    # If no split improves the model, make it a leaf
            return Node(value=Counter(y).most_common(1)[0][0])
        
        X_left, X_right, y_left, y_right = split_dataset(X, y, feature, threshold)     # Recursively build the Left and Right branche
        left = self.build_tree(X_left, y_left, depth + 1)
        right = self.build_tree(X_right, y_right, depth + 1)
        
        return Node(feature, threshold, left, right)

    def fit(self, X, y):
       
        self.node_count = 0
        self.root = self.build_tree(X, y)
        print(f"\n  Total nodes created: {self.node_count}")
        return self

    def _predict(self, x, node):
        
        if node.value is not None:    # If we hit a leaf, return the decision
            return node.value
        
        # Otherwise, check the condition and go deeper
        if x[node.feature] <= node.threshold:
            return self._predict(x, node.left)
        return self._predict(x, node.right)

    def predict(self, X):
        return np.array([self._predict(x, self.root) for x in X])