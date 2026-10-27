import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students
@st.cache_resource # heavy models hote h is liye ek baar load ho system mein
def load_dlib_models():
    detector=dlib.get_frontal_face_detector()

    sp=dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())

    facerec=dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector,sp,facerec

def getface_embeddings(image_np):
    detector,sp,facerec= load_dlib_models()
    faces=detector(image_np,1)

    encoding=[]

    for face in faces:
        shape=sp(image_np,face)
        face_descriptor=facerec.compute_face_descriptor(image_np,shape,1)#128 embeddigs
        encoding.append(np.array(face_descriptor))
    return encoding

# @st.cache_resource
# def get_trained_models():
#     x=[]
#     y=[]

#     student_db=get_all_students()
#     if not student_db:
#         return None
#     for student in student_db:
#         embedding=student.get('face_embedding')
#         if embedding:
#             x.append(np.array(embedding))
#             y.append(student.get('student_id'))

#         if len(x)==0:
#             return 0

#         clf=SVC(kernel='linear',probability=True,class_weight='balance')
#         try:
#             clf.fit(x,y)
#         except ValueError:
#             pass
#     return {"clf":clf,"X":x,"Y":y}



@st.cache_resource
def get_trained_models():
    x = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    # Step 1: Collect all available face embeddings and student IDs
    for student in student_db:
        embedding = student.get("face_embedding")

        if embedding is not None and len(embedding) > 0:
            x.append(np.array(embedding, dtype=float))
            y.append(student.get("student_id"))

    # Step 2: Check whether any valid embeddings were found
    if len(x) == 0:
        return None

    # Step 3: Create the classifier
    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    # Step 4: Train only if there are at least two different students
    if len(set(y)) < 2:
        return {
            "clf": None,
            "X": x,
            "Y": y
        }

    # Step 5: Fit the classifier on all collected embeddings
    clf.fit(x, y)

    return {
        "clf": clf,
        "X": x,
        "Y": y
    }



def train_classifier():
    st.cache_resource.clear()#cache invalidating
    model_data=get_trained_models()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings=getface_embeddings(class_image_np)
    detected_student={}

    model_data=get_trained_models()

    if not model_data:
        return detected_student,[],len(encodings)
    clf=model_data['clf']
    x_train=model_data['X']
    y_train=model_data['Y']

    all_students=sorted(list(set(y_train)))

    for encoding in encodings:
        if len(all_students)>=2:
            predicted_id=int(clf.predict([encoding])[0])
        else:
            predicted_id=int(all_students[0])
        student_embedding=x_train[y_train.index(predicted_id)]#same index prr hote h agr meri id 2nd prr h y mein toh x mein embedding usi same index prr hogi.

        best_match_score=np.linalg.norm(student_embedding-encoding)
        resemblance_threshold=0.6
        if best_match_score<=resemblance_threshold:
            detected_student[predicted_id]=True
    return detected_student,all_students,len(encodings)


    
    

