import os
from django.shortcuts import render
import joblib

# Load model and vectorizer once
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'diagnosis', 'ml', 'text_diagnosis_model.pkl')
VEC_PATH = os.path.join(BASE_DIR, 'diagnosis', 'ml', 'text_vectorizer.pkl')
from django.contrib.auth.decorators import login_required
from .models import DiagnosisHistory
from .models import ChatMessage
import time

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)

REMEDY_LOOKUP = {
    "Malaria": "Stay hydrated, take antimalarial medication as prescribed. See a doctor if fever persists.",
    "Typhoid": "Complete your antibiotics, eat soft food, and avoid public contact. See a doctor for follow-up tests.",
    "Common Cold": "Rest, drink fluids, use warm steam. No need for antibiotics unless it worsens.",
    "Psoriasis": "Use moisturizers and medicated creams. Consider seeing a dermatologist.",
    "Diabetes": "Monitor your blood sugar, follow a low-carb diet, and consult an endocrinologist regularly.",
    "Migraine": "Avoid triggers, stay in a quiet dark room, take prescribed medication.",
    "Dengue": "Stay hydrated, rest well. Seek emergency care if bleeding or severe weakness occurs.",
    # Add more as needed...
}

REMEDY_DATA = {
    "Malaria": {
        "remedy": "Take antimalarial medication as prescribed. Stay hydrated and rest. Seek medical attention if symptoms persist.",
        "explanation": "Malaria is caused by parasites transmitted through mosquito bites. Common symptoms include fever, chills, and headache."
    },
    "Psoriasis": {
        "remedy": "Use topical treatments and moisturizers. Avoid triggers like stress and cold weather.",
        "explanation": "Psoriasis is a chronic autoimmune condition that causes skin cells to build up rapidly, forming scales and red patches."
    },
    "Hypertension": {
        "remedy": "Reduce salt intake, exercise regularly, and take prescribed medication. Monitor your blood pressure regularly.",
        "explanation": "Hypertension, or high blood pressure, can lead to heart disease if untreated. It's often symptomless but dangerous over time."
    },
    # Add more...
}




@login_required
def symptom_checker(request):
    user_input = request.POST.get('symptoms')
    predictions = []

    if user_input:
        vect_input = vectorizer.transform([user_input])
        time.sleep(2)
        label = model.predict(vect_input)[0]
        prob = model.predict_proba(vect_input).max() * 100

        extra = REMEDY_DATA.get(label, {
            "remedy": "No remedy information available.",
            "explanation": "No additional explanation available for this diagnosis."
        })

        bot_response = f"{label} ({round(prob, 2)}% confidence)\n\n{extra['explanation']}\n\nSuggested Remedy: {extra['remedy']}"

        # Save to DB
        ChatMessage.objects.create(
            user=request.user,
            message=user_input,
            response=bot_response
        )

    # Fetch full chat history
    chat_history = ChatMessage.objects.filter(user=request.user)

    return render(request, 'diagnosis/diagnosis_form.html', {
        'chat_history': chat_history
    })



@login_required
def diagnosis_history(request):
    history = DiagnosisHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'diagnosis/history.html', {'history': history})