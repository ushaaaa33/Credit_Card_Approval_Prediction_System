import numpy as np
import pandas as pd
import joblib
from model import DecisionTreeClassifierCustom

if __name__ == "__main__":
    print("=" * 60)
    print("🎓 Training Custom Decision Tree Model")
    print("=" * 60)
    
    try:
        # Load dataset
        print("📂 Loading dataset...")
        df = pd.read_csv("Balanced_Credit_Card_Dataset.csv")
        print(f"✓ Loaded {len(df)} records")
        
        # Use a SMALLER sample for faster training
        # For testing, use 5000 samples. For production, use more.
        SAMPLE_SIZE = 5000
        if len(df) > SAMPLE_SIZE:
            df = df.sample(n=SAMPLE_SIZE, random_state=42)
            print(f"📊 Using sample of {SAMPLE_SIZE} records for faster training")
        
        # Prepare features and target
        # Drop index column if it exists
        if 'index' in df.columns:
            df = df.drop(columns=['index'])
        
        X = df.drop(columns=["CREDIT_CARD_APPROVAL_STATUS"]).values
        y = df["CREDIT_CARD_APPROVAL_STATUS"].values
        
        print(f"✓ Features shape: {X.shape}")
        print(f"✓ Target shape: {y.shape}")
        
        # Split data
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"✓ Training set: {len(X_train)} samples")
        print(f"✓ Test set: {len(X_test)} samples")
        
        # Train model with LIMITED DEPTH for faster training
        print("\n🤖 Training model (this may take 1-2 minutes)...")
        clf = DecisionTreeClassifierCustom(max_depth=5, min_samples_split=10)
        clf.fit(X_train, y_train)
        print("✓ Model trained successfully!")
        
        # Evaluate
        print("\n📊 Evaluating model...")
        y_pred = clf.predict(X_test)
        accuracy = np.sum(y_pred == y_test) / len(y_test)
        print(f"✓ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        # Save model
        print("\n💾 Saving model...")
        joblib.dump(clf, "custom_decision_tree.pkl")
        print("✓ Model saved as 'custom_decision_tree.pkl'")
        
        print("\n" + "=" * 60)
        print("✅ Training Complete!")
        print("=" * 60)
        print("\n🚀 You can now run: python app.py")
        
    except FileNotFoundError:
        print("❌ Error: Merged_Dataset.csv not found!")
        print("Please make sure the dataset file exists in the current directory.")
    except Exception as e:
        print(f"❌ Error during training: {e}")
        import traceback
        traceback.print_exc()