"""Backend module"""

import cv2
import numpy as np
from typing import Tuple

def load_image(file_path: str) -> np.ndarray:
    """
    Загрузка изображения с указанного пути.
    :param file_path: путь к файлу изображения
    :return: изображение в формате numpy array
    """
    img = cv2.imread(file_path)
    if img is None:
        raise ValueError("Не удалось загрузить изображение")
    return img

def capture_from_webcam() -> np.ndarray:
    """
    Захват изображения с веб-камеры.
    :return: изображение в формате numpy array
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise ValueError("Не удалось подключиться к веб-камере")
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError("Не удалось захватить изображение с веб-камеры")
    return frame

def show_channel(img: np.ndarray, channel: str) -> np.ndarray:
    """
    Показ выбранного цветового канала изображения.
    :param img: исходное изображение
    :param channel: цветовой канал ("red", "green", "blue")
    :return: изображение с выделенным цветовым каналом
    """
    if channel == "red":
        return img[:, :, 2]
    elif channel == "green":
        return img[:, :, 1]
    elif channel == "blue":
        return img[:, :, 0]
    else:
        raise ValueError("Неверный канал. Выберите 'red', 'green' или 'blue'.")

def apply_gaussian_blur(img: np.ndarray, kernel_size: int) -> np.ndarray:
    """
    Применение размытия по Гауссу к изображению.
    :param img: исходное изображение
    :param kernel_size: размер ядра (должен быть нечетным числом)
    :return: размытое изображение
    """
    if kernel_size % 2 == 0:
        raise ValueError("Размер ядра должен быть нечетным числом")
    blurred_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    return blurred_img

def convert_to_gray(img: np.ndarray) -> np.ndarray:
    """
    Конвертация изображения в оттенки серого.
    :param img: исходное изображение
    :return: изображение в оттенках серого
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img

def draw_line(img: np.ndarray, start_point: Tuple[int, int], end_point: Tuple[int, int], thickness: int) -> np.ndarray:
    """
    Рисование линии на изображении.
    :param img: исходное изображение
    :param start_point: координаты начала линии (x1, y1)
    :param end_point: координаты конца линии (x2, y2)
    :param thickness: толщина линии
    :return: изображение с нарисованной линией
    """
    img_with_line = img.copy()
    color = (0, 255, 0)  # Зеленый цвет
    cv2.line(img_with_line, start_point, end_point, color, thickness)
    return img_with_line
