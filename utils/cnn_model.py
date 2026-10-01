# utils/cnn_model.py

import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

# ----------------- PYTORCH CNN ARCHITECTURE ----------------- #
if HAS_TORCH:
    class SkinCNN(nn.Module):
        """
        A 3-layer Convolutional Neural Network for dermatological skin type and concern classification.
        Can be trained on dermoscopic image repositories like HAM10000.
        """
        def __init__(self, num_classes=4):
            super(SkinCNN, self).__init__()
            self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
            self.bn1 = nn.BatchNorm2d(32)
            self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
            self.bn2 = nn.BatchNorm2d(64)
            self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
            self.bn3 = nn.BatchNorm2d(128)
            self.pool = nn.MaxPool2d(2, 2)
            self.fc1 = nn.Linear(128 * 16 * 16, 512)
            self.dropout = nn.Dropout(0.5)
            self.fc2 = nn.Linear(512, num_classes)
            
        def forward(self, x):
            x = self.pool(F.relu(self.bn1(self.conv1(x))))
            x = self.pool(F.relu(self.bn2(self.conv2(x))))
            x = self.pool(F.relu(self.bn3(self.conv3(x))))
            x = x.view(-1, 128 * 16 * 16)
            x = F.relu(self.fc1(x))
            x = self.dropout(x)
            x = self.fc2(x)
            return x
else:
    class SkinCNN:
        def __init__(self, num_classes=4):
            pass
        def forward(self, x):
            return x


# ----------------- REAL-TIME CONVOLUTION ENGINE ----------------- #
# 3x3 Laplacian Kernel for fine edge/wrinkle detection
_LAPLACIAN_KERNEL = ImageFilter.Kernel(
    (3, 3),
    [-1, -1, -1,
     -1,  8, -1,
     -1, -1, -1],
    scale=1,
    offset=0
)

def convolve_image_edges(img_gray):
    """
    Performs 2D convolution edge extraction using a Laplacian kernel.
    """
    return img_gray.filter(_LAPLACIAN_KERNEL)


def analyze_skin_image(image_file):
    """
    Reads an uploaded face or skin photo, processes it with 2D convolutions,
    analyzes color spectrum distributions, generates a visual heatmap scan,
    and returns predicted skin diagnostics. Optimized for ultra-fast response.
    """
    # 1. Load image and normalize size to 256x256 for fast convolution & HUD generation
    img_orig = Image.open(image_file).convert("RGB")
    img_resized = img_orig.resize((256, 256), Image.Resampling.BILINEAR)
    
    img_arr = np.array(img_resized)
    r_chan = img_arr[:, :, 0].astype(float)
    g_chan = img_arr[:, :, 1].astype(float)
    b_chan = img_arr[:, :, 2].astype(float)
    
    # 2. Extract Skin Features via Convolution & HSV Analysis
    red_ratio = r_chan / (g_chan + b_chan + 1.0)
    redness_mask = red_ratio > 1.25
    redness_score = float(np.mean(redness_mask) * 100 * 4.0)
    redness_score = min(max(redness_score, 10.0), 95.0)
    
    luminance = 0.299 * r_chan + 0.587 * g_chan + 0.114 * b_chan
    oiliness_mask = luminance > 215
    oiliness_score = float(np.mean(oiliness_mask) * 100 * 6.0)
    oiliness_score = min(max(oiliness_score, 8.0), 98.0)
    
    img_gray = ImageOps.grayscale(img_resized)
    img_edges = convolve_image_edges(img_gray)
    edges_arr = np.array(img_edges)
    
    texture_mask = edges_arr > 45
    texture_score = float(np.mean(texture_mask) * 100 * 8.0)
    texture_score = min(max(texture_score, 12.0), 92.0)
    
    # 3. Create Custom HUD Heatmap Visualization
    h_arr = np.zeros_like(img_arr, dtype=np.int32)
    h_arr[redness_mask] += [235, 50, 50]       # Pink-Red highlight
    h_arr[oiliness_mask] += [235, 180, 50]     # Golden yellow shine highlight
    h_arr[texture_mask] += [50, 180, 235]      # Cyan line highlight
    
    h_arr = np.clip(h_arr, 0, 255).astype(np.uint8)
    h_img = Image.fromarray(h_arr)
    
    scanned_overlay = Image.blend(img_resized, h_img, alpha=0.45)
    enhancer = ImageEnhance.Contrast(scanned_overlay)
    scanned_overlay = enhancer.enhance(1.15)
    
    # 4. Skin Diagnostic Classification Rules
    if oiliness_score > 55:
        skin_type = "Oily"
    elif oiliness_score < 18 and texture_score > 50:
        skin_type = "Dry"
    elif oiliness_score > 30 and texture_score > 35:
        skin_type = "Combination"
    elif redness_score > 40:
        skin_type = "Sensitive"
    else:
        skin_type = "Combination"
        
    # Concern heuristics
    if redness_score > 50:
        concern = "Sensitive Skin" if skin_type == "Sensitive" else "Acne"
    elif texture_score > 60:
        concern = "Aging" if skin_type == "Dry" else "Open Pores"
    elif oiliness_score > 65:
        concern = "Acne"
    elif texture_score > 45:
        concern = "Flaky Skin" if skin_type == "Dry" else "Pigmentation"
    else:
        concern = "Tan" if skin_type == "Oily" else "Dryness"
        
    diagnostics = {
        "skin_type": skin_type,
        "concern": concern,
        "scores": {
            "sebum": oiliness_score,
            "texture": texture_score,
            "redness": redness_score
        }
    }
    
    return scanned_overlay, diagnostics


def analyze_hair_image(image_file):
    """
    Reads an uploaded hair/scalp photo, processes it with 2D convolutions,
    generates a visual heatmap scan, and returns predicted hair diagnostics.
    """
    img_orig = Image.open(image_file).convert("RGB")
    img_resized = img_orig.resize((256, 256), Image.Resampling.BILINEAR)
    
    img_arr = np.array(img_resized)
    r_chan = img_arr[:, :, 0].astype(float)
    g_chan = img_arr[:, :, 1].astype(float)
    b_chan = img_arr[:, :, 2].astype(float)
    
    luminance = 0.299 * r_chan + 0.587 * g_chan + 0.114 * b_chan
    oiliness_mask = luminance > 200
    oiliness_score = float(np.mean(oiliness_mask) * 100 * 5.0)
    oiliness_score = min(max(oiliness_score, 10.0), 95.0)
    
    img_gray = ImageOps.grayscale(img_resized)
    img_edges = convolve_image_edges(img_gray)
    edges_arr = np.array(img_edges)
    
    density_mask = edges_arr > 50
    density_score = float(np.mean(density_mask) * 100 * 7.0)
    density_score = min(max(density_score, 15.0), 85.0)
    
    red_ratio = r_chan / (g_chan + b_chan + 1.0)
    redness_mask = red_ratio > 1.3
    redness_score = float(np.mean(redness_mask) * 100 * 3.0)
    redness_score = min(max(redness_score, 5.0), 90.0)
    
    h_arr = np.zeros_like(img_arr, dtype=np.int32)
    h_arr[oiliness_mask] += [235, 180, 50]  # Sebum yellow
    h_arr[density_mask] += [50, 180, 235]   # Density blue
    h_arr[redness_mask] += [235, 50, 50]    # Scalp redness
    h_arr = np.clip(h_arr, 0, 255).astype(np.uint8)
    
    h_img = Image.fromarray(h_arr)
    scanned_overlay = Image.blend(img_resized, h_img, alpha=0.45)
    enhancer = ImageEnhance.Contrast(scanned_overlay)
    scanned_overlay = enhancer.enhance(1.2)
    
    hair_type = "Straight"
    if oiliness_score > 60:
        hair_type = "Oily"
    elif oiliness_score < 30:
        hair_type = "Dry"
        
    concern = "Hair Fall"
    if redness_score > 40:
        concern = "Dandruff"
    elif density_score < 40:
        concern = "Hair Fall"
    elif oiliness_score > 65:
        concern = "Oily Scalp"
    elif oiliness_score < 25:
        concern = "Frizz"
    else:
        concern = "Hair Fall"
        
    diagnostics = {
        "hair_type": hair_type,
        "concern": concern,
        "scores": {
            "sebum": oiliness_score,
            "density": density_score,
            "irritation": redness_score
        }
    }
    
    return scanned_overlay, diagnostics


def analyze_makeup_image(image_file):
    """
    Reads an uploaded face photo, processes it with 2D convolutions to detect
    contrast and features, generates a visual heatmap scan, and returns 
    predicted makeup style diagnostics.
    """
    img_orig = Image.open(image_file).convert("RGB")
    img_resized = img_orig.resize((256, 256), Image.Resampling.BILINEAR)
    
    img_arr = np.array(img_resized)
    r_chan = img_arr[:, :, 0].astype(float)
    g_chan = img_arr[:, :, 1].astype(float)
    b_chan = img_arr[:, :, 2].astype(float)
    
    undertone_ratio = r_chan / (b_chan + 1.0)
    warm_mask = undertone_ratio > 1.2
    warmth_score = float(np.mean(warm_mask) * 100 * 2.5)
    warmth_score = min(max(warmth_score, 10.0), 90.0)
    
    img_gray = ImageOps.grayscale(img_resized)
    img_edges = convolve_image_edges(img_gray)
    edges_arr = np.array(img_edges)
    
    contrast_mask = edges_arr > 60
    contrast_score = float(np.mean(contrast_mask) * 100 * 5.0)
    contrast_score = min(max(contrast_score, 15.0), 85.0)
    
    smoothness_mask = edges_arr < 25
    smoothness_score = float(np.mean(smoothness_mask) * 100)
    smoothness_score = min(max(smoothness_score, 20.0), 95.0)
    
    h_arr = np.zeros_like(img_arr, dtype=np.int32)
    h_arr[warm_mask] += [235, 120, 50]       # Warmth (Orange/Coral)
    h_arr[contrast_mask] += [180, 50, 235]   # Contrast (Purple/Magenta)
    h_arr[smoothness_mask] += [50, 235, 180] # Smoothness (Mint/Teal)
    h_arr = np.clip(h_arr, 0, 255).astype(np.uint8)
    
    h_img = Image.fromarray(h_arr)
    scanned_overlay = Image.blend(img_resized, h_img, alpha=0.35)
    enhancer = ImageEnhance.Contrast(scanned_overlay)
    scanned_overlay = enhancer.enhance(1.25)
    
    skin_type = "Combination"
    if smoothness_score < 40 and warmth_score > 60:
        skin_type = "Sensitive"
    elif warmth_score > 50:
        skin_type = "Oily"
    elif smoothness_score > 70:
        skin_type = "Dry"
        
    style = "Daily Makeup"
    if contrast_score > 60:
        style = "Glam Makeup"
    elif contrast_score > 40 and smoothness_score > 70:
        style = "Bridal Makeup"
    elif warmth_score > 60:
        style = "Glowing Skin"
    elif smoothness_score > 80:
        style = "Natural Look"
    else:
        style = "Daily Makeup"
        
    undertone = "Neutral"
    if warmth_score > 65:
        undertone = "Warm"
    elif warmth_score < 35:
        undertone = "Cool"
        
    avg_luminance = float(np.mean(0.299 * r_chan + 0.587 * g_chan + 0.114 * b_chan))
    if avg_luminance > 180:
        skin_tone = "Fair"
    elif avg_luminance > 130:
        skin_tone = "Light"
    elif avg_luminance > 90:
        skin_tone = "Medium"
    elif avg_luminance > 50:
        skin_tone = "Tan"
    else:
        skin_tone = "Deep"
    
    diagnostics = {
        "skin_type": skin_type,
        "concern": style,
        "skin_tone": skin_tone,
        "undertone": undertone,
        "scores": {
            "warmth": warmth_score,
            "contrast": contrast_score,
            "smoothness": smoothness_score
        }
    }
    
    return scanned_overlay, diagnostics
