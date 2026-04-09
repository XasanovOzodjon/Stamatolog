from .models import Appointment
import requests


def send_telegram_notification(appointment: Appointment):
    doctor = appointment.doctor
    TOKEN = '8620844916:AAG0r8gpcmvLxZHYAyQ2ASbwt25ndQfijEg'

    if doctor.telegram_id:
        chat_id = doctor.telegram_id

        message = f"""
🩺 <b>Yangi uchrashuv!</b>

👤 <b>Bemor:</b> {appointment.patient_name}
📞 <b>Telefon:</b> {appointment.patient_phone}
📧 <b>Email:</b> {appointment.patient_email or '—'}

📅 <b>Sana:</b> {appointment.date}
⏰ <b>Vaqt:</b> {appointment.time}

🧾 <b>Xizmat:</b> {appointment.service}
📝 <b>Izoh:</b> {appointment.notes or '—'}
"""

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
        )