import boto3


def recognize(picture):
        rekognition = boto3.client('rekognition', region_name='us-west-2')    
        res =   rekognition.detect_faces(Image={'Bytes':picture}, Attributes=['ALL'])
        return  res

def get_emotion_type(emotion_vector):
    most_probable_emotion = None
    temp_conf = 0
    for emotion in emotion_vector['Emotions']:
        if emotion['Confidence'] > temp_conf:
            most_probable_emotion = emotion['Type']
            temp_conf = emotion['Confidence'] 
    return most_probable_emotion


def get_vector_from_face(face):
    vector = {
    "age_range_low": face['AgeRange']['Low'],
    "age_range_high": face['AgeRange']['High'],
    "smile": face['Smile']['Value'],
    "gender": face['Gender']['Value'],
    "emotion": get_emotion_type(face)
    }
    return vector

def get_all_vectors(rekognition_response):
    faces_vectors = []
    for face in rekognition_response['FaceDetails']:
        faces_vectors.append(get_vector_from_face(face))
    return faces_vectors


def run_rekognition(picture):
    rekognition_response = recognize(picture)
    return   get_all_vectors(rekognition_response)