import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# Step 1: Load the CSV file
df = pd.read_csv("/kaggle/input/mydatasetkaggle/features_30_sec.csv")

# Step 2: Prepare features (X) and target labels (y)
# X will be the columns with features like chroma_stft_mean, rms_mean, etc.
X = df[['chroma_stft_mean', 'chroma_stft_var', 'rms_mean', 'rms_var', 
        'spectral_centroid_mean', 'spectral_centroid_var', 
        'spectral_bandwidth_mean', 'spectral_bandwidth_var']].values

# y will be the genre (extracted from filename column)
y = df['filename'].apply(lambda x: x.split('.')[0]).values  # Assuming the  genre is in the filename before the extension

# Step 3: Label encode the genre labels (since SVM needs numerical labels)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Step 4: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Step 5: Train the SVM model
svm_model = SVC(kernel='rbf', probability=True)  # Linear kernel for simplicity
svm_model.fit(X_train, y_train)

train_accuracy = svm_model.score(X_train, y_train)
print("Training Accuracy:", train_accuracy)

# Step 6: Evaluate the model
y_pred = svm_model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_,zero_division=1))

# Step 7: Save the trained model to a file (binary format)
joblib.dump(svm_model, "svm_model.pkl")
print("done")
