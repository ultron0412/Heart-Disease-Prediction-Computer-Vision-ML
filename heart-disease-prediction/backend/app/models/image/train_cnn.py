"""
ECG Image CNN Training (Medical-Grade)

- Transfer Learning: MobileNetV2
- ECG-aware preprocessing
- Class imbalance handling
- Partial fine-tuning
- AUC + Accuracy metrics
"""

from pathlib import Path
import numpy as np

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import AUC

from sklearn.utils.class_weight import compute_class_weight

# =========================================================
# 1. Resolve Project Paths (SAFE & PORTABLE)
# =========================================================
BASE_DIR = Path(__file__).resolve().parents[4]

TRAIN_DIR = BASE_DIR / "data" / "images" / "train"
TEST_DIR = BASE_DIR / "data" / "images" / "test"
MODEL_DIR = BASE_DIR / "models" / "image"
MODEL_PATH = MODEL_DIR / "heart_cnn.keras"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16

# =========================================================
# 2. Data Preprocessing (ECG-SPECIFIC)
# =========================================================
"""
Why preprocess_input?
- Matches ImageNet feature scale
- Essential for transfer learning
"""

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=5,        # ECGs should not rotate much
    zoom_range=0.05,
    width_shift_range=0.02,
    height_shift_range=0.02
)

test_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

train_data = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=True
)

test_data = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=False
)

# =========================================================
# 3. Handle Class Imbalance (CRITICAL FOR MEDICAL DATA)
# =========================================================
labels = train_data.classes

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(labels),
    y=labels
)

class_weights = dict(enumerate(class_weights))
print("⚖️ Class weights:", class_weights)

# =========================================================
# 4. Base CNN Model (TRANSFER LEARNING)
# =========================================================
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# =========================================================
# 5. Partial Fine-Tuning (MEDICAL BEST PRACTICE)
# =========================================================
"""
- Freeze early layers (generic features)
- Fine-tune last 50 layers (ECG adaptation)
"""

for layer in base_model.layers[:-50]:
    layer.trainable = False
for layer in base_model.layers[-50:]:
    layer.trainable = True

# =========================================================
# 6. ECG-Specific Classification Head
# =========================================================
x = base_model.output
x = GlobalAveragePooling2D()(x)

x = Dense(256, activation="relu")(x)
x = Dropout(0.5)(x)

x = Dense(64, activation="relu")(x)
x = Dropout(0.3)(x)

output = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base_model.input, outputs=output)

# =========================================================
# 7. Compile Model (MEDICAL METRICS)
# =========================================================
model.compile(
    optimizer=Adam(learning_rate=5e-6),
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        AUC(name="auc")
    ]
)

model.summary()

# =========================================================
# 8. Callbacks (STABILITY & GENERALIZATION)
# =========================================================
early_stop = EarlyStopping(
    monitor="val_auc",
    mode="max",
    patience=4,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.3,
    patience=3,
    min_lr=1e-6
)

# =========================================================
# 9. Train Model
# =========================================================
model.fit(
    train_data,
    epochs=30,
    validation_data=test_data,
    callbacks=[early_stop, reduce_lr],
    class_weight=class_weights
)

# =========================================================
# 10. Save Model (NEW KERAS FORMAT)
# =========================================================
MODEL_DIR.mkdir(parents=True, exist_ok=True)
model.save(MODEL_PATH)

print(f"✅ Medical-grade ECG CNN saved at: {MODEL_PATH}")
