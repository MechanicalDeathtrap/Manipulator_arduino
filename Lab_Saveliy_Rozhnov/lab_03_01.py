import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

def lab1_image_processing(image_path):
    # 1. Загрузка изображения
    original = cv2.imread(image_path)

    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

    # 2. Размытие (Гауссово размытие)
    blurred = cv2.GaussianBlur(original, (5, 5), 0)
    blurred_rgb = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)

    # 3. Повышение резкости
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened_convolution = cv2.filter2D(original, -1, kernel)
    sharpened_convolution_rgb = cv2.cvtColor(sharpened_convolution, cv2.COLOR_BGR2RGB)
    sharpened_unsharp = cv2.addWeighted(original, 1.5, blurred, -0.5, 0)
    sharpened_unsharp_rgb = cv2.cvtColor(sharpened_unsharp, cv2.COLOR_BGR2RGB)

    # 4. Выделение границ (оператор Собеля)
    sobel_x = cv2.Sobel(original, cv2.CV_64F, 1, 0, ksize=5)
    sobel_y = cv2.Sobel(original, cv2.CV_64F, 0, 1, ksize=5)
    sobel_combined = cv2.magnitude(sobel_x, sobel_y)
    sobel_combined = cv2.convertScaleAbs(sobel_combined)

    # 5. Комбинирование результатов
    combined = cv2.addWeighted(blurred, 0.5, sobel_combined, 0.5, 0)
    combined = cv2.addWeighted(combined, 0.5, sharpened_convolution, 0.5, 0)
    combined_rgb = cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)

    # 6. Отображение результатов
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 3, 1)
    plt.title('Оригинальное изображение')
    plt.imshow(original_rgb)
    plt.axis('off')

    plt.subplot(2, 3, 2)
    plt.title('Гауссово размытие')
    plt.imshow(blurred_rgb)
    plt.axis('off')

    plt.subplot(2, 3, 3)
    plt.title('Повышение резкости (Свертка)')
    plt.imshow(sharpened_convolution_rgb)
    plt.axis('off')

    plt.subplot(2, 3, 4)
    plt.title('Повышение резкости (Маска нерезкости)')
    plt.imshow(sharpened_unsharp_rgb)
    plt.axis('off')

    plt.subplot(2, 3, 5)
    plt.title('Выделение границ (Собель)')
    plt.imshow(sobel_combined, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 3, 6)
    plt.title('Комбинированное изображение')
    plt.imshow(combined_rgb)
    plt.axis('off')

    plt.tight_layout()
    plt.show()

# Пример вызова функции
image_path = "img.png"
lab1_image_processing(image_path)
