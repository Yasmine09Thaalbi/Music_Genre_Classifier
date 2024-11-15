import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("/kaggle/input/mydatasetkaggle/features_30_sec.csv")

X = df[['chroma_stft_mean', 'chroma_stft_var', 'rms_mean', 'rms_var', 
        'spectral_centroid_mean', 'spectral_centroid_var', 
        'spectral_bandwidth_mean', 'spectral_bandwidth_var']].values


y = df['filename'].apply(lambda x: x.split('.')[0]).values  


label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)


X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)


svm_model = SVC(kernel='rbf', probability=True) 
svm_model.fit(X_train, y_train)

train_accuracy = svm_model.score(X_train, y_train)
print("Training Accuracy:", train_accuracy)


y_pred = svm_model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_,zero_division=1))


joblib.dump(svm_model, "svm_model.pkl")
print("done")
