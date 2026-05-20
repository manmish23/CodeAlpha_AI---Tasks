import tkinter as tk
from tkinter import scrolledtext
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- AUTO DOWNLOAD NLTK DATA --- 
try:
    word_tokenize("test")
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

# --- 1. FAQs WITH MORE KEYWORD VARIATIONS --- 
FAQ_DATA = {
    # College
    "What are the college timings?": "College runs from 9:00 AM to 4:00 PM, Monday to Friday.",
    "College time schedule": "College runs from 9:00 AM to 4:00 PM, Monday to Friday.",
    "How do I apply for admission?": "Visit our website portal and fill Form 16. Last date is July 30th.",
    "Admission process": "Visit our website portal and fill Form 16. Last date is July 30th.",
    "What is the fee structure?": "Annual college fees are 1.2 Lakh for CSE. Hostel extra 80k per year.",
    "How much is college fees?": "Annual college fees are 1.2 Lakh for CSE. Hostel extra 80k per year.",
    "College fees cost": "Annual college fees are 1.2 Lakh for CSE. Hostel extra 80k per year.",
    "Where is the library located?": "Library is in Block B, 2nd floor. Open 8 AM to 8 PM.",
    "Library location": "Library is in Block B, 2nd floor. Open 8 AM to 8 PM.",
    "How to contact placement cell?": "Email placement@college.edu or visit Room 101, Admin Block.",
    "Placement contact": "Email placement@college.edu or visit Room 101, Admin Block.",
    "What documents needed for admission?": "10th/12th marksheets, TC, Migration, Aadhar, 4 photos required.",
    "Documents for admission": "10th/12th marksheets, TC, Migration, Aadhar, 4 photos required.",
    "When will semester exams start?": "Odd sem exams start 1st week of December as per academic calendar.",
    "Exam dates": "Odd sem exams start 1st week of December as per academic calendar.",
    
    # Hostel
    "Is hostel compulsory?": "No, hostel is optional. Day scholars can use college bus service.",
    "Hostel mandatory": "No, hostel is optional. Day scholars can use college bus service.",
    "What are hostel fees?": "Hostel fees are 80,000 per year including food and accommodation.",
    "How much is hostel fees?": "Hostel fees are 80,000 per year including food and accommodation.",
    "Hostel cost": "Hostel fees are 80,000 per year including food and accommodation.",
    "What are hostel timings?": "Hostel in-time is 9:00 PM for all students. Gate closes at 9:30 PM.",
    "What is hostel in time?": "Hostel in-time is 9:00 PM for all students. Gate closes at 9:30 PM.",
    "Hostel gate closing time": "Hostel in-time is 9:00 PM for all students. Gate closes at 9:30 PM.",
    "Is hostel food good?": "Hostel mess provides 4 meals: breakfast, lunch, snacks, dinner. Veg & Non-veg options.",
    "What food is provided in hostel?": "Hostel mess provides 4 meals: breakfast, lunch, snacks, dinner. Veg & Non-veg options.",
    "Situation of food at hostel": "Hostel mess provides 4 meals: breakfast, lunch, snacks, dinner. Veg & Non-veg options. Quality is decent.",
    "Hostel mess food": "Hostel mess provides 4 meals: breakfast, lunch, snacks, dinner. Veg & Non-veg options.",
    "Are hostel rooms AC?": "We have both AC and Non-AC rooms. AC rooms cost 15k extra per year.",
    "Hostel AC rooms": "We have both AC and Non-AC rooms. AC rooms cost 15k extra per year.",
    "How many students per hostel room?": "Standard rooms are 3-sharing. AC rooms are 2-sharing.",
    "Hostel room sharing": "Standard rooms are 3-sharing. AC rooms are 2-sharing.",
    "Is wifi available in hostel?": "Yes, 24/7 high-speed WiFi available in all hostel blocks.",
    "Hostel wifi": "Yes, 24/7 high-speed WiFi available in all hostel blocks.",
    "Can parents visit hostel?": "Yes, parents allowed on Sundays 10 AM to 5 PM with ID proof at warden office.",
    "Parents visiting hostel": "Yes, parents allowed on Sundays 10 AM to 5 PM with ID proof at warden office."
}

faq_questions = list(FAQ_DATA.keys())

# --- 2. PREPROCESS TEXT ---
def preprocess(text):
    text = text.lower()
    tokens = word_tokenize(text)
    keep_words = {'what', 'how', 'when', 'where', 'why', 'much', 'many', 'is', 'are', 'good', 'situation'}
    stop_words = set(stopwords.words('english')) - keep_words
    
    tokens = [word for word in tokens if word not in string.punctuation]
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

processed_faqs = [preprocess(q) for q in faq_questions]

# --- 3. VECTORIZE - sublinear_tf prevents 'hostel' from dominating ---
vectorizer = TfidfVectorizer(ngram_range=(1,3), sublinear_tf=True)
faq_vectors = vectorizer.fit_transform(processed_faqs)

# --- 4. MATCH USER QUESTION ---
def get_response(user_input):
    if not user_input.strip():
        return "Please type a question."
    
    user_processed = preprocess(user_input)
    user_vector = vectorizer.transform([user_processed])
    
    similarities = cosine_similarity(user_vector, faq_vectors)
    best_match_index = similarities.argmax()
    best_score = similarities[0, best_match_index]
    
    if best_score < 0.35:  # Slightly higher threshold
        return "Sorry, I don't know that yet. Ask about college timings, fees, admission, hostel rooms, food, in-time, wifi, etc."
    
    best_faq = faq_questions[best_match_index]
    return FAQ_DATA[best_faq]

# --- 5. CHAT UI ---
def send_message():
    user_text = user_input.get()
    if user_text.strip() == "":
        return
    
    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"You: {user_text}\n")
    
    bot_response = get_response(user_text)
    chat_area.insert(tk.END, f"Bot: {bot_response}\n\n")
    
    chat_area.config(state='disabled')
    chat_area.see(tk.END)
    user_input.delete(0, tk.END)

root = tk.Tk()
root.title("College + Hostel FAQ Chatbot - Task 2")
root.geometry("500x600")

tk.Label(root, text="College & Hostel FAQ Chatbot", font=("Arial", 16, "bold")).pack(pady=10)

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', font=("Arial", 11))
chat_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
chat_area.config(state='normal')
chat_area.insert(tk.END, "Bot: Hi! Ask me about college timings, fees, admission, hostel rooms, food, in-time, wifi, etc.\n\n")
chat_area.config(state='disabled')

user_frame = tk.Frame(root)
user_frame.pack(fill=tk.X, padx=10, pady=10)

user_input = tk.Entry(user_frame, font=("Arial", 11))
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
user_input.bind("<Return>", lambda event: send_message())

send_btn = tk.Button(user_frame, text="Send", command=send_message, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
send_btn.pack(side=tk.RIGHT, padx=(5,0))

tk.Label(root, text="Task 2 - NLP Chatbot using NLTK + Cosine Similarity", font=("Arial", 8)).pack(side=tk.BOTTOM, pady=5)

root.mainloop()