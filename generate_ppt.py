from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def create_presentation():
    prs = Presentation()
    
    # Define slide layouts
    title_slide_layout = prs.slide_layouts[0]
    bullet_slide_layout = prs.slide_layouts[1]
    
    # SLIDE 1: Title
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Multimodal Biological Rhythm Analysis"
    subtitle.text = "Extracting Respiratory Waveforms from PPG using Deep Learning\n\nProject Progress Report"
    
    # SLIDE 2: Problem Statement
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Problem Statement"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "Continuous respiratory monitoring is challenging:"
    p = tf.add_paragraph()
    p.text = "Direct measurements (capnography, chest bands) are uncomfortable, intrusive, and expensive."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Photoplethysmography (PPG) is widely available via cheap wearables (smartwatches)."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Core Challenge: Can we extract the hidden, low-frequency respiratory rhythm directly from the optical PPG heart-rate signal using Deep Learning?"
    p.level = 1

    # SLIDE 3: Project Goals
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Project Goals & Objectives"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "Our roadmap defines 6 core objectives:"
    tf.add_paragraph().text = "1. Respiration Extraction from PPG (Phase 1)"
    tf.add_paragraph().text = "2. Breathing Rhythm Variability Analysis (Entropy, Fractal Scaling)"
    tf.add_paragraph().text = "3. Cardio-Respiratory Interaction (ECG + Breathing)"
    tf.add_paragraph().text = "4. Stress / Activity Impact on Breathing (using EDA/Accelerometer)"
    tf.add_paragraph().text = "5. Pathological vs Normal Rhythm Classification"
    tf.add_paragraph().text = "6. Mathematical Modeling of Respiratory Rhythm"

    # SLIDE 4: Proposed Solution
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Proposed Solution: Deep CorrEncoder"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "We proposed an advanced Encoder-Decoder Neural Network."
    p = tf.add_paragraph()
    p.text = "Deep Bottleneck Architecture: Compresses the signal to force the network to forget high-frequency heartbeat noise."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Large Receptive Field: Using large kernels (31, 15, 7) and 10-second data windows (3000 samples) to capture the macroscopic 4-6 second breathing cycle."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Decoder: Reconstructs the exact continuous respiration waveform."
    p.level = 1

    # SLIDE 5: Datasets Overview
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Dataset Overview & Purpose"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "We are utilizing multiple multimodal datasets:"
    p = tf.add_paragraph()
    p.text = "CapnoBase (PhysioNet): Our MAIN dataset. High-quality PPG, ECG, and Respiration (CO2). Used for training the model."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "BIDMC (PhysioNet): ICU patient data. Used as an independent validation set to check model generalization."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "WESAD (Kaggle/UCI): Wearable Stress and Affect Detection. Contains EDA and Accelerometer data. Will be used for Objective 4 (Stress/Activity analysis)."
    p.level = 1

    # SLIDE 6: CapnoBase Deep Dive
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Deep Dive: CapnoBase Dataset"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "Technical Details of our primary data source:"
    tf.add_paragraph().text = "Format: Downloaded as .mat (MATLAB) files from PhysioNet."
    tf.add_paragraph().text = "Sampling Rate (fs): Exactly 300 Hz."
    tf.add_paragraph().text = "Extracted Signals:"
    p = tf.add_paragraph()
    p.text = "PPG (pleth): The main input feature."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Respiration (co2): The Ground Truth target we want to predict."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "ECG: Saved for future Heart Rate Variability (HRV) calculations."
    p.level = 1

    # SLIDE 7: How We Cleaned the Data
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Signal Cleaning & Preprocessing"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "Biological signals are extremely noisy. Our Phase 3 pipeline:"
    p = tf.add_paragraph()
    p.text = "Bandpass Filtering: Isolates physiological frequencies. We used 'sosfiltfilt' (Second-Order Sections) which is mathematically stable and prevents NaN explosions."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Frequency Ranges: Respiration (0.1 - 0.5 Hz) and PPG (0.1 - 5.0 Hz)."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Z-Score Normalization: Scales all patient data to Mean=0, Std=1, allowing the Neural Network to focus on wave shapes rather than raw amplitude."
    p.level = 1

    # SLIDE 8: Work Progress
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Overall Work Progress"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "What we have successfully completed so far:"
    tf.add_paragraph().text = "[DONE] PHASE 0: Project Architecture Setup"
    tf.add_paragraph().text = "[DONE] PHASE 1: Dataset Acquisition (CapnoBase)"
    tf.add_paragraph().text = "[DONE] PHASE 2: Data Loading (Custom H5/MAT Extractors)"
    tf.add_paragraph().text = "[DONE] PHASE 3: Signal Preprocessing (Filtering & Norm)"
    tf.add_paragraph().text = "[DONE] PHASE 4: Respiration Reconstruction (Model Training)"
    tf.add_paragraph().text = "[NEXT] PHASE 5 & 6: Mathematical Feature Extraction"

    # SLIDE 9: Step-by-Step Debugging (Part 1)
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Implementation Step 1: The NaN Crash"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "Initial Output: Model training failed instantly with Loss = NaN."
    tf.add_paragraph().text = "What We Did:"
    p = tf.add_paragraph()
    p.text = "We diagnosed that the standard Butterworth filter (b,a format) was mathematically unstable for long biological signals."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "We upgraded the preprocessing module to use 'sos' (Second-Order Sections) format and added explicit np.nan_to_num() handlers."
    p.level = 1
    tf.add_paragraph().text = "Result: The model stopped crashing and the loss began decreasing normally."

    # SLIDE 10: Step-by-Step Debugging (Part 2)
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Implementation Step 2: Architecture Overhaul"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "Initial Output: The predicted wave was highly oscillatory, mimicking the heartbeat instead of respiration."
    tf.add_paragraph().text = "What We Did:"
    p = tf.add_paragraph()
    p.text = "We realized the CorrEncoder was too shallow (kernel size 5) and only had a receptive field of 0.016 seconds."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "We wrote and implemented a Deep Bottleneck Architecture with massive kernels (31, 15, 7) and expanded the input window to 3000 samples (10 seconds)."
    p.level = 1
    tf.add_paragraph().text = "Result: The model stopped tracking high-frequency noise and learned to see the macroscopic trend."

    # SLIDE 11: Step-by-Step Debugging (Part 3)
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Implementation Step 3: Resolving Misalignment"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "Initial Output: The predicted wave lost amplitude and phase-tracking due to temporal misalignment."
    tf.add_paragraph().text = "What We Did:"
    p = tf.add_paragraph()
    p.text = "We discovered the 'Invisible Breathing Bug'—the PPG filter lowcut (0.5Hz) was accidentally deleting the 0.25Hz breathing envelope! We fixed it to 0.1Hz."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "We discovered the data windowing function was processing X and Y independently. A flat signal drop in X caused the lists to misalign, ruining the temporal mapping."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "We rewrote create_windows() to check both signals simultaneously."
    p.level = 1

    # SLIDE 12: Final Result & Success
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Final Result: Phase 1 Success"
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = "After retraining the model on the corrected data pipeline:"
    tf.add_paragraph().text = "Loss Improvement: The training loss dropped significantly from 1.04 down to 0.32 in just 100 epochs."
    tf.add_paragraph().text = "Reconstruction Accuracy: The predicted respiratory waveform (Red) now perfectly tracks the phase, frequency, and full amplitude of the true Capnography wave (Blue)."
    tf.add_paragraph().text = "Conclusion: Objective 1 is complete. The system can successfully extract a slow breathing rhythm from a fast PPG signal."

    # SLIDE 13: End
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    title.text = "Thank You!"
    slide.placeholders[1].text = "Ready for Phase 5: Mathematical Feature Extraction"

    prs.save('Project_Progress_Presentation.pptx')
    print("Presentation generated successfully!")

if __name__ == "__main__":
    create_presentation()
