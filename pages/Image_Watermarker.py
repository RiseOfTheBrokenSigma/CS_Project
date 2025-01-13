import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.title("Image Watermarker")
st.write("Upload an image and add text or a logo as a watermark")
uploaded_image = st.file_uploader("Upload an image:", type=["jpg", "png", "jpeg"])

if uploaded_image:
    # Convert image to Pillow object
    img = Image.open(uploaded_image).convert("RGBA")
    watermark_type = st.radio("Choose watermark type:", ["Text", "Logo", "Both"])
    watermark = Image.new("RGBA", img.size, (255, 255, 255, 0))
    font_options = {
        "Arial": "arial.ttf",
        "Courier New": "cour.ttf",
        "Times New Roman": "times.ttf"
    }

    if watermark_type in ["Text", "Both"]:
        text = st.text_input("Enter watermark text:", "Watermark")
        font_size = st.slider("Font size:", 10, 100, 30)
        opacity_text = st.slider("Text opacity:", 0, 255, 128)
        font_file = st.file_uploader("Upload a custom font (TTF):", type=["ttf"])

        # Font selection
        selected_font = st.selectbox("Choose a font:", list(font_options.keys()))
        font_path = font_options[selected_font]
        font = ImageFont.truetype(font_path, font_size)


        # Sliders for text position
        x_text = st.slider("Text Horizontal Position:", 0, img.width, 10)
        y_text = st.slider("Text Vertical Position:", 0, img.height, 10)

        # Draw the text watermark on the overlay
        draw = ImageDraw.Draw(watermark)
        draw.text((x_text, y_text), text, font=font, fill=(255, 255, 255, opacity_text))

    if watermark_type in ["Logo", "Both"]:
        logo_file = st.file_uploader("Upload a logo (PNG with transparency):", type=["png"])
        if logo_file:
            logo = Image.open(logo_file).convert("RGBA")
            logo_size = st.slider("Logo size (% of image width):", 10, 100, 20)
            logo_opacity = st.slider("Logo opacity:", 0, 255, 255)
            logo_width = int(img.width * (logo_size / 100))
            logo.thumbnail((logo_width, logo_width))

            # Sliders for logo position
            x_logo = st.slider("Logo Horizontal Position:", 0, img.width - logo.width, 10)
            y_logo = st.slider("Logo Vertical Position:", 0, img.height - logo.height, 10)
            logo_overlay = Image.new("RGBA", logo.size, (255, 255, 255, 0))

            for x in range(logo.width):
                for y in range(logo.height):
                    r, g, b, a = logo.getpixel((x, y))
                    logo_overlay.putpixel((x, y), (r, g, b, int(a * (logo_opacity / 255))))
            watermark.paste(logo_overlay, (x_logo, y_logo), logo_overlay)

    img = Image.alpha_composite(img, watermark)
    img = img.convert("RGB")

    # Display the watermarked image
    st.image(img, caption="Watermarked Image", use_container_width=True)

    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    st.download_button(
        label= "Download Watermarked Image",
        data = buffer,
        file_name = "watermarked_image.jpg",
        mime = "image/jpeg"
    )
