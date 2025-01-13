import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

st.title("QR Code Generator")
st.title("Enter text/URL to create a QR code")

qrCode = st.text_input("Enter Text/URL:")

if qrCode:
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 10,
        border = 4
    )
    qr.add_data(qrCode)
    qr.make(fit=True)
    img = qr.make_image(fill_color = "black", back_color = "white")

    buffer = BytesIO()
    img.save(buffer, format = "PNG")    
    buffer.seek(0)

    st.image(buffer, caption = "Generated QR Code", use_container_width = True)

    st.download_button(
        label = "Download QR Code",
        data = buffer,
        file_name = "QRCode.png",
        mime = "image/png"
    )

