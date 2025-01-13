import cv2
import numpy as np


def otsu_threshold(image):

    blur = cv2.GaussianBlur(image, (5, 5), 0)
    _, otsu_binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return otsu_binary


def process_image(image_path, output_path):

    # Загрузка изображения
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Не удалось загрузить изображение: {image_path}")

    # Преобразование в градации серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("intermediate_gray.jpg", gray)  # Сохранение промежуточного результата

    # Применение метода Оцу для удаления теней
    binary = otsu_threshold(gray)
    cv2.imwrite("intermediate_binary.jpg", binary)  # Сохранение бинарного изображения

    # Удаление мелких шумов и теней с помощью морфологических операций
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    cleaned_binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite("intermediate_cleaned_binary.jpg", cleaned_binary)  # Сохранение очищенного изображения

    # Дополнительная очистка внутри объектов (расширение)
    dilation_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))  # Ядро для расширения
    dilated_binary = cv2.dilate(cleaned_binary, dilation_kernel, iterations=1)  # Расширение объектов
    cv2.imwrite("intermediate_dilated_binary.jpg", dilated_binary)  # Сохранение расширенного изображения

    # Поиск контуров объектов
    contours, _ = cv2.findContours(dilated_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    object_data = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:  # Исключаем слишком маленькие шумы
            M = cv2.moments(contour)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
            else:
                cx, cy = 0, 0

            object_data.append({
                'contour': contour,
                'area': area,
                'center': (cx, cy)
            })

    # Сортировка объектов по площади
    object_data = sorted(object_data, key=lambda x: x['area'], reverse=True)

    # Рисование контуров и аннотаций
    for idx, obj in enumerate(object_data):
        color = (0, 255, 0)  # Зеленый цвет для всех объектов
        if idx == 0:
            label = f"Largest: {obj['area']:.1f}"
            color = (255, 0, 0)  # Синий для самого большого объекта
        elif idx == len(object_data) - 1:
            label = f"Smallest: {obj['area']:.1f}"
            color = (0, 0, 255)  # Красный для самого маленького объекта
        else:
            label = f"{obj['area']:.1f}"

        cv2.drawContours(image, [obj['contour']], -1, color, 2)
        cx, cy = obj['center']
        cv2.circle(image, (cx, cy), 5, (255, 255, 255), -1)  # Белая точка в центре
        cv2.putText(image, label, (cx + 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Сохранение обработанного изображения
    cv2.imwrite(output_path, image)


# Пример использования
process_image('img.png', 'output_image.jpg')
