import os
import fitz  # PyMuPDF
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)
from PIL import Image

TOKEN = "8349740296:AAFSTCraaxpgTA_Us1hD0vLBfwGOPOFO10I"

# User state storage
user_images = {}
user_pdf = {}
pending_add = {}


# -----------------------------
# Handle Photos & Documents
# -----------------------------
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    file = None

    # If sent as PHOTO
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await photo.get_file()

    # If sent as DOCUMENT (image file)
    elif update.message.document:
        document = update.message.document
        if document.mime_type and document.mime_type.startswith("image/"):
            file = await document.get_file()
        else:
            await update.message.reply_text("Please send an image file ❌")
            return
    else:
        return

    # If waiting for insert image
    if user_id in pending_add and pending_add[user_id] == "waiting_for_image":
        file_path = f"{user_id}_insert.jpg"
        await file.download_to_drive(file_path)

        pending_add[user_id] = file_path
        await update.message.reply_text(
            "Image received ✅ Now type: add <page_number>"
        )
        return

    # Otherwise collect images normally
    if user_id not in user_images:
        user_images[user_id] = []

    file_path = f"{user_id}_{len(user_images[user_id])}.jpg"
    await file.download_to_drive(file_path)

    user_images[user_id].append(file_path)

    if len(user_images[user_id]) == 1:
        await update.message.reply_text(
            "Images are being collected 📂\nSend all images, then type 'pdf'."
        )


# -----------------------------
# Handle Text Commands
# -----------------------------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.lower().strip()

    # -------- Generate PDF --------
    if text == "pdf":
        if user_id not in user_images or len(user_images[user_id]) == 0:
            await update.message.reply_text("No images found ❌")
            return

        images = []
        for path in user_images[user_id]:
            img = Image.open(path).convert("RGB")
            images.append(img)

        pdf_path = f"{user_id}_output.pdf"

        images[0].save(
            pdf_path,
            save_all=True,
            append_images=images[1:]
        )

        user_pdf[user_id] = pdf_path
        pending_add[user_id] = "waiting_for_image"

        await update.message.reply_document(open(pdf_path, "rb"))
        await update.message.reply_text(
            "PDF generated ✅\nSend a new image to insert into a page."
        )
        return

    # -------- Insert Image As New Page --------
    if text.startswith("add"):
        if user_id not in user_pdf:
            await update.message.reply_text("Generate PDF first ❌")
            return

        if user_id not in pending_add or not isinstance(pending_add[user_id], str):
            await update.message.reply_text("Send image first ❌")
            return

        try:
            page_number = int(text.split()[1]) - 1
        except:
            await update.message.reply_text("Use format: add 2")
            return

        original_pdf_path = user_pdf[user_id]
        insert_image_path = pending_add[user_id]

        doc = fitz.open(original_pdf_path)

        if page_number < 0 or page_number > len(doc):
            await update.message.reply_text("Invalid page number ❌")
            doc.close()
            return

        # Create temporary PDF from image
        temp_img_pdf = f"{user_id}_imgpage.pdf"
        img = Image.open(insert_image_path).convert("RGB")
        img.save(temp_img_pdf)

        img_doc = fitz.open(temp_img_pdf)

        # Insert image page at position
        doc.insert_pdf(img_doc, start_at=page_number)

        # Safe Save
        temp_final = f"{user_id}_temp.pdf"
        doc.save(temp_final)
        doc.close()
        img_doc.close()

        if os.path.exists(original_pdf_path):
            os.remove(original_pdf_path)

        os.rename(temp_final, original_pdf_path)

        os.remove(temp_img_pdf)

        pending_add[user_id] = "waiting_for_image"

        await update.message.reply_document(open(original_pdf_path, "rb"))
        await update.message.reply_text("Page inserted successfully ✅")
        return


# -----------------------------
# Main
# -----------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.PHOTO | filters.Document.IMAGE,
            handle_media
        )
    )

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Smart PDF Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()