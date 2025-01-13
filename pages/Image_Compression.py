import streamlit as st
import numpy as np
from PIL import Image
import io

def compressImage(image, threshold=20000):
    # Convert the image to a matrix of it's pixel values. Each pixel is a 1x3 row matrix
    img_array_color = np.array(image)

    # Separate RGB channels. Corresponds to individual R G and B intensities.
    red_channel = img_array_color[:, :, 0]
    green_channel = img_array_color[:, :, 1]
    blue_channel = img_array_color[:, :, 2]

    # Apply FFT to each channel to convert image into frequency domain
    fft_red = np.fft.fftshift(np.fft.fft2(red_channel))
    fft_green = np.fft.fftshift(np.fft.fft2(green_channel))
    fft_blue = np.fft.fftshift(np.fft.fft2(blue_channel))

    # Values above threshold value are kept, while values below threshold values discarded/rounded to surrounding values
    fft_red[np.abs(fft_red) < threshold] = 0
    fft_green[np.abs(fft_green) < threshold] = 0
    fft_blue[np.abs(fft_blue) < threshold] = 0

    # Apply inverse FFT to each channel, reconstructing the image
    ifft_red = np.abs(np.fft.ifft2(np.fft.ifftshift(fft_red))).astype(np.uint8)
    ifft_green = np.abs(np.fft.ifft2(np.fft.ifftshift(fft_green))).astype(np.uint8)
    ifft_blue = np.abs(np.fft.ifft2(np.fft.ifftshift(fft_blue))).astype(np.uint8)

    # Stack the channels back together to form the reconstructed color image
    reconstructed_img = np.stack((ifft_red, ifft_green, ifft_blue), axis=-1)

    return reconstructed_img

# Streamlit header
st.title("Image Compression")
st.write(
    """

    """
)

# File uploader
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")

    # Display the original image
    st.subheader("Original Image")
    st.image(img, caption="Original Image", use_container_width=True)

    original_file_size = len(uploaded_file.getbuffer())

    # Compression threshold slider
    threshold = st.slider(
        "Compression Threshold",
        min_value=0,
        max_value=100000,
        value=20000,
        step=100,
    )

    # Image compression
    reconstructed_img = compressImage(img, threshold)

    # Display the reconstructed image
    st.subheader("Reconstructed Image")
    st.image(reconstructed_img, caption="Reconstructed Image", use_container_width=True)

    # Save the compressed image to an in-memory buffer to remove the need for writing image to a physical file
    compressed_buffer = io.BytesIO()
    compressed_image = Image.fromarray(reconstructed_img)
    compressed_image.save(compressed_buffer, format = "JPEG", quality = 50)
    # Get compressed file size 
    compressed_file_size = compressed_buffer.tell()
    compressed_buffer.seek(0)



    # Display file sizes and compression ratio
    st.write(f"**Original File Size:** {original_file_size / 1024:.2f} KB")
    st.write(f"**Compressed File Size:** {compressed_file_size / 1024:.2f} KB")
    st.write(f"**Compression Ratio:** {original_file_size / compressed_file_size:.2f}")



    # Download button
    st.download_button(
        label="Download",
        data=compressed_buffer,
        file_name=f"compressed_image.JPEG",
        mime=f"image/jpeg"
    )
