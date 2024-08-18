### Introduction to MedScan
- **MedScan Overview**: 
  - An innovative educational platform designed to assist medical students.
  - Focuses on detecting and analyzing brain diseases through CT scans.
  - Provides a mentoring system that guides students in identifying brain disorders.

### Training the Model
- **Model Training with YOLOv5**:
  - Utilized the **Brain Tumor Detection Dataset** containing high-quality MRI images.
  - **Dataset Details**:
    - 5,249 MRI images, annotated with bounding boxes for four classes of brain tumors.
    - Classes include: Glioma, Meningioma, No Tumor, Pituitary.
    - Dataset split into training and validation sets.
    - Images come from different MRI angles (sagittal, axial, coronal) to ensure model robustness.
  - **Training Breakdown**:
    - Training Set: Glioma (1,153), Meningioma (1,449), No Tumor (711), Pituitary (1,424).
    - Validation Set: Glioma (136), Meningioma (140), No Tumor (100), Pituitary (136).

### User Interaction with MedScan
- **User Engagement**:
  - **Upload Brain CT Scan**: Users upload their brain CT scan for analysis.
  - **Manual Annotation**: Users can draw a bounding box around the area they suspect has a disease.
  - **Bounding Box Comparison**: MedScan compares user-drawn boxes with the model’s detection.

### Educational Report Generation
- **Model Analysis**:
  - MedScan interprets the user’s input and provides feedback on the correctness of their bounding box.
  - Offers a detailed report analyzing the user's interpretation.
  
- **Educational Component**:
  - MedScan then dives into educating the user about the specific brain disease detected.
  - Implements RAG (Retrieval-Augmented Generation) to fetch the latest articles from PubMed.
  - **What is PubMed?**: A free resource developed and maintained by the National Center for Biotechnology Information (NCBI), it comprises over 30 million citations for biomedical literature.
  - Combines insights from these articles to create a cohesive educational report.

### Data Storage and Future Reference
- **Storing Reports in MongoDB**:
  - All reports, including user’s bounding box, correct box, interpretations, and MedScan’s feedback, are stored in MongoDB.
  - Allows users to revisit and reflect on their past assessments, providing a continuous learning experience.

### Conclusion
- **MedScan’s Mission**:
  - To mentor medical students by offering hands-on experience with brain disease detection.
  - Fosters a deeper understanding of brain disorders through practical analysis and educational content.

