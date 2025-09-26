import face_recognition
import cv2
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser

# Initialize text-to-speech
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load known faces
known_face_encodings = []
known_face_names = []

# Load images and encode
def load_faces():
    image = face_recognition.load_image_file("person1.jpg")
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)
    known_face_names.append("Alice")  # Change to your name

# Voice assistant logic
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        return command.lower()
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."

# Respond to voice commands
def handle_command(command):
    if "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")
    elif "date" in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    else:
        speak("I can’t help with that yet!")

# Main function
def main():
    load_faces()

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Video', frame)

            if name != "Unknown":
                speak(f"Hello, {name}")
                command = listen_command()
                handle_command(command)
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
