import cv2
import os
import numpy as np

INPUT_VIDEO = "input.mp4" 
OUTPUT_VOB = "VIDEO_TS/VTS_01_1.VOB"
MAX_FRAMES = 1200 

os.makedirs("VIDEO_TS", exist_ok=True)

if os.path.exists(INPUT_VIDEO):
    cap = cv2.VideoCapture(INPUT_VIDEO)
    print(f"[CONVERTER] найдено видео {INPUT_VIDEO}. конвертируем в цветной формат YUV420...")
else:
    print(f"[CONVERTER] видео не найдено. генерируем цветную тестовую анимацию...")
    cap = None

with open(OUTPUT_VOB, "wb") as f:
    frame_count = 0
    
    if cap is None:
        # генерируем красивую цветную психоделику на 600 кадров
        for t in range(600):
            # создаем цветной кадр
            img = np.zeros((240, 320, 3), dtype=np.uint8)
            cx = int(160 + 60 * np.cos(t * 0.04))
            cy = int(120 + 40 * np.sin(t * 0.06))
            # рисуем цветные круги (Зеленый слоник символично зеленый!)
            cv2.circle(img, (cx, cy), 40, (0, 255, 0), -1)
            cv2.circle(img, (160, 120), int(20 + 10*np.sin(t*0.1)), (0, 120, 255), 3)
            
            # переводим в YUV420 (стандарт сжатия DVD!)
            yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV_I420)
            f.write(yuv.tobytes())
            frame_count += 1
    else:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            frame_resized = cv2.resize(frame, (320, 240))
            # конвертируем кадр в формат YUV I420 (яркость + сжатый цвет)
            yuv = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2YUV_I420)
            
            f.write(yuv.tobytes())
            frame_count += 1
            if frame_count >= MAX_FRAMES: break
        cap.release()

print(f"[CONVERTER] готово! сжато {frame_count} цветных кадров. файл: {OUTPUT_VOB}")
