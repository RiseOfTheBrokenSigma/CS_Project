import streamlit as st
from PIL import Image
import io


def gifCreator(images, duration=100, loop=0):
    # Save gif as a buffer
    gif_buffer = io.BytesIO()

    images[0].save(
    gif_buffer,
    format="GIF",
    # Enables sequences of images in a single file
    save_all=True,

    #Saves all frames/images execpt first one, as it is already saved by default
    append_images=images[1:],
    duration=duration,
    loop=loop,
    )
    gif_buffer.seek(0)
    return gif_buffer
    
# Function that resizes images for GIFs
def resizeImages(images, targetSize):
    resized = [img.resize(targetSize) for img in images]
    return resized

st.title("GIF Maker")
st.title("Upload images to make an animated GIF")


uploaded_files = st.file_uploader("Upload Images (Minimum 2):", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# Checks if uploaded_files are empty. If not, runs code 
if uploaded_files:
    # Opens file as a pillow object
    images = [Image.open(file).convert("RGB") for file in uploaded_files]

    # All images are resized to the first one
    targetSize = images[0].size
    images = resizeImages(images, targetSize)

    st.subheader("GIF Settings")
    duration = st.slider("Frame Duration (ms)", 50, 1000, 200, step=50)
    loop = 0

    if st.button("Create GIF"):
        if len(images) <2:
            st.error("Please upload at least 2 images to create a Gif")
        else:
            gif_buffer = gifCreator(images, duration, 0)

            st.subheader("Generated Gif:")
            st.image(gif_buffer)

            st.download_button(
                label = "Download GIF",
                data = gif_buffer,
                file_name = "animated.gif",
                mime = "image/gif"
            )

