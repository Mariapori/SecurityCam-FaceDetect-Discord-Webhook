from datetime import datetime
from time import time
import cv2
import discord
video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
timeLock = time()
while True:
    _, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        if time() >= timeLock:
            timeLock = time() + 60 #1 min
            filename = f"tunkeilija-{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.png"
            cv2.imwrite(filename, frame)
            webhook = discord.SyncWebhook.from_url("your_webhook_url")
            embed = discord.Embed(title="Tunkeilija!", description="Kasvot havaittu! :warning:")
            file = discord.File(filename, filename="image.png")
            embed.set_image(url="attachment://image.png")
            webhook.send(file=file,embed=embed)

    cv2.imshow("Mariaporin turvakamera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()