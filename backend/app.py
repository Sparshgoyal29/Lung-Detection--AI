from flask import Flask, render_template, request, send_file, redirect
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import sqlite3
from pdf_generator import create_pdf

app = Flask(__name__)

# Load trained AI model
model = tf.keras.models.load_model("lung_model.h5")

# Upload folder
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Patient Details
    name = request.form["name"]
    age = request.form["age"]
    gender = request.form["gender"]
    phone = request.form["phone"]

    # Check uploaded file
    if "file" not in request.files:
        return "No file uploaded"

    file = request.files["file"]

    # Save image
    filename = file.filename

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    # Load image

    img = image.load_img(filepath)

    width, height = img.size

    if width < 200 or height < 200:
        return """
        Invalid Image.
        Please upload a valid Chest X-Ray image.
        """

    img = image.load_img(
        filepath,
        target_size=(150, 150)
    )

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # AI Prediction
    prediction = model.predict(img_array)

    raw_prediction = float(prediction[0][0])

    if 0.40 < raw_prediction < 0.60:
        return """
        Uncertain Prediction.
        Please upload a clear Chest X-Ray image.
        """

    if prediction[0][0] > 0.5:
        result = "PNEUMONIA DETECTED"
        confidence = round(
            float(prediction[0][0]) * 100,
            2
        )
    else:
        result = "NORMAL"
        confidence = round(
            (1 - float(prediction[0][0])) * 100,
            2
        )
    # Generate PDF Report

    pdf_name = f"{name}_Report.pdf"

    create_pdf(
        pdf_name,
        name,
        age,
        gender,
        phone,
        result,
        confidence
    )
    # Save Patient Record

    conn = sqlite3.connect("hospital.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO patients
    (name, age, gender, phone, result, confidence)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        name,
        age,
        gender,
        phone,
        result,
        str(confidence)
    ))

    conn.commit()
    conn.close()

    # Show Report Page

    return render_template(
        "report.html",
        name=name,
        age=age,
        gender=gender,
        phone=phone,
        result=result,
        confidence=confidence,
        filename=filename
    )


@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("hospital.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patients"
    )

    patients = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        patients=patients
    )

@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("hospital.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/download/<name>")
def download(name):

    pdf_file = f"{name}_Report.pdf"

    return send_file(
        pdf_file,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)