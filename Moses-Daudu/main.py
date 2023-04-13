import face_recognition
import os
folder_name = 'vids'  
result_folder = 'result'
initial_image_folder = 'initial_images'
final_image_folder = 'unique_images'

# create a list of face encodings for all images in the folder
face_encodings = []
for filename in os.listdir(initial_image_folder):
    image_path = os.path.join(initial_image_folder, filename)
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)
    if len(encoding) > 0:
        face_encodings.append(encoding[0])

# create a list of duplicate face encodings
duplicate_encodings = []
for i, encoding in enumerate(face_encodings):
    for j in range(i+1, len(face_encodings)):
        distance = face_recognition.face_distance([encoding], face_encodings[j])
        if distance < 0.6:  # threshold for similarity
            duplicate_encodings.append(j)

# remove duplicate images
for i in sorted(set(duplicate_encodings), reverse=True):
    filename = os.listdir(initial_image_folder)[i]
    image_path = os.path.join(initial_image_folder, filename)
    os.remove(image_path)
    print(f'Deleted {filename} because it is a duplicate face.')