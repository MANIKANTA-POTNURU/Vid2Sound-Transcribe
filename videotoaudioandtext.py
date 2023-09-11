import streamlit as st
import moviepy.editor as mp
import os
import speech_recognition as sr

st.title("Video to Audio")


# Upload a video file
video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mkv"])

if video_file is not None:
    # Display the video
    st.video(video_file)

    if st.button("Convert video to Audio"):
        try:
            # Create a temporary directory for files
            temp_dir = "temp_files"
            os.makedirs(temp_dir, exist_ok=True)

            # Save the uploaded video file in the temporary directory
            video_path = os.path.join(temp_dir, video_file.name)
            with open(video_path, "wb") as video_writer:
                video_writer.write(video_file.read())

            # Convert the video to audio
            video_clip = mp.VideoFileClip(video_path)
            audio_clip = video_clip.audio
            audio_path = os.path.join(temp_dir, "video_audio.wav")
            audio_clip.write_audiofile(audio_path)

            # Recognize speech from the audio using CMU Sphinx
            r = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio_data = r.record(source)
                result = r.recognize_sphinx(audio_data)

            # Display the recognized text
            st.write("Recognized Speech:")
            st.write(result)

            # Provide a download link for the user to download the audio
            st.audio(audio_path)

            # Clean up temporary files
            os.remove(video_path)
            os.remove(audio_path)

            # Add a download button
            st.write("")
            st.write("")
            download_button = st.download_button(
                "Download Audio",
                audio_path,
                key="download_button",
                help="Click to download the audio file.",
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
