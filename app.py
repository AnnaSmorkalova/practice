import cv2
import numpy as np

# Глобальные переменные состояния
original_img = None
original_img_backup = None
current_img = None
current_channels = "all"
current_brightness = 0
line_coords = []


def load_image():
    global original_img, original_img_backup, current_img, current_channels, current_brightness, line_coords

    while True:
        path = input("Введите путь к изображению (jpg/png) или 'exit' для выхода: ")
        if path.lower() == 'exit':
            return False

        # Проверка существования файла через попытку открытия
        try:
            with open(path, 'rb') as f:
                pass
        except IOError:
            print("Ошибка: файл не найден! Попробуйте еще раз.")
            continue

        # Проверка расширения файла
        if not (path.lower().endswith('.jpg') or path.lower().endswith('.jpeg') or path.lower().endswith('.png')):
            print("Ошибка: поддерживаются только JPG и PNG файлы! Попробуйте еще раз.")
            continue

        # Загрузка изображения
        img = cv2.imread(path)
        if img is None:
            print("Ошибка: не удалось загрузить изображение! Попробуйте еще раз.")
            continue

        # Инициализация глобальных переменных
        original_img = img.copy()
        original_img_backup = img.copy()
        current_img = img.copy()
        current_channels = "all"
        current_brightness = 0
        line_coords = []
        return True


def use_camera():
    global original_img, original_img_backup, current_img, current_channels, current_brightness, line_coords

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Ошибка: не удалось подключиться к камере!")
        print("Возможные решения:")
        print("1. Проверьте, подключена ли камера")
        print("2. Дайте программе доступ к камере")
        print("3. Перезагрузите компьютер")
        return False

    print("Камера подключена. Нажмите пробел чтобы сделать снимок, ESC для отмены")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: не удалось получить кадр с камеры!")
            cap.release()
            return False

        cv2.imshow('Camera - Space to capture, ESC to cancel', frame)
        key = cv2.waitKey(1)

        if key == 27:  # ESC
            cap.release()
            cv2.destroyAllWindows()
            return False
        elif key == 32:  # Пробел
            original_img = frame.copy()
            original_img_backup = frame.copy()
            current_img = frame.copy()
            current_channels = "all"
            current_brightness = 0
            line_coords = []
            cap.release()
            cv2.destroyAllWindows()
            return True


def apply_all_effects():
    global original_img, current_img, current_channels, current_brightness, line_coords

    if original_img is None:
        return

    temp_img = original_img.copy()

    # Применение яркости
    if current_brightness > 0:
        hsv = cv2.cvtColor(temp_img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, current_brightness)
        v = np.clip(v, 0, 255)
        temp_img = cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)

    # Применение цветовых каналов
    if current_channels != "all":
        if current_channels == "red":
            temp_img[:, :, 0] = 0
            temp_img[:, :, 1] = 0
        elif current_channels == "green":
            temp_img[:, :, 0] = 0
            temp_img[:, :, 2] = 0
        elif current_channels == "blue":
            temp_img[:, :, 1] = 0
            temp_img[:, :, 2] = 0

    # Рисование линий
    for line in line_coords:
        x1, y1, x2, y2, thickness = line
        cv2.line(temp_img, (x1, y1), (x2, y2), (0, 255, 0), thickness)

    current_img = temp_img


def show_channels_menu():
    global current_channels

    print("\nВыберите канал:")
    print("1 - Все каналы (оригинал)")
    print("2 - Красный")
    print("3 - Зеленый")
    print("4 - Синий")

    while True:
        choice = input("Ваш выбор (1-4): ")
        if choice == '1':
            current_channels = "all"
            return True
        elif choice == '2':
            current_channels = "red"
            return True
        elif choice == '3':
            current_channels = "green"
            return True
        elif choice == '4':
            current_channels = "blue"
            return True
        else:
            print("Неверный выбор! Попробуйте еще раз.")


def resize_image():
    global original_img, original_img_backup

    while True:
        try:
            print(f"Текущий размер: {original_img.shape[1]}x{original_img.shape[0]}")
            width = int(input("Введите новую ширину: "))
            height = int(input("Введите новую высоту: "))

            if width <= 0 or height <= 0:
                print("Размеры должны быть положительными числами! Попробуйте еще раз.")
                continue

            original_img = cv2.resize(original_img_backup, (width, height))
            return True
        except ValueError:
            print("Ошибка: введите целые числа! Попробуйте еще раз.")
        except AttributeError:
            print("Ошибка: изображение не загружено! Сначала загрузите изображение.")
            return False


def change_brightness():
    global current_brightness

    while True:
        try:
            print(f"Текущая яркость: {current_brightness}")
            value = int(input("Введите значение яркости (0 до 255): "))

            if value < 0 or value > 255:
                print("Значение должно быть от 0 до 255! Попробуйте еще раз.")
                continue

            current_brightness = value
            return True
        except ValueError:
            print("Ошибка: введите целое число! Попробуйте еще раз.")


def draw_line():
    global line_coords

    while True:
        try:
            print("Введите координаты линии:")
            x1 = int(input("x1: "))
            y1 = int(input("y1: "))
            x2 = int(input("x2: "))
            y2 = int(input("y2: "))
            thickness = int(input("Толщина линии: "))

            line_coords.append((x1, y1, x2, y2, thickness))
            return True
        except ValueError:
            print("Ошибка: введите целые числа! Попробуйте еще раз.")


def save_image():
    global current_img

    if current_img is None:
        print("Ошибка: нет изображения для сохранения!")
        return

    while True:
        path = input("Введите путь для сохранения (например: result.jpg): ")
        if not (path.lower().endswith('.jpg') or path.lower().endswith('.jpeg') or path.lower().endswith('.png')):
            print("Поддерживаются только JPG и PNG файлы! Попробуйте еще раз.")
            continue

        if cv2.imwrite(path, current_img):
            print("Изображение сохранено!")
            break
        else:
            print("Ошибка при сохранении! Попробуйте другой путь.")


def show_image():
    global current_img

    if current_img is None:
        print("Ошибка: нет изображения для отображения!")
        return

    cv2.imshow('Current Image', current_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def reset_changes():
    global original_img, original_img_backup, current_img, current_channels, current_brightness, line_coords

    if original_img_backup is None:
        print("Ошибка: нет исходного изображения!")
        return False

    original_img = original_img_backup.copy()
    current_img = original_img_backup.copy()
    current_channels = "all"
    current_brightness = 0
    line_coords = []
    print("Все изменения сброшены!")
    return True


def process_image():
    while True:
        apply_all_effects()

        print("\n=== Меню обработки ===")
        print("1. Показать цветовые каналы")
        print("2. Изменить размер изображения")
        print("3. Повысить яркость")
        print("4. Нарисовать линию")
        print("5. Показать текущее изображение")
        print("6. Сбросить все изменения")
        print("7. Сохранить изображение")
        print("8. Вернуться в главное меню")

        choice = input("Ваш выбор (1-8): ")

        if choice == '1':
            if show_channels_menu():
                apply_all_effects()
        elif choice == '2':
            if resize_image():
                apply_all_effects()
        elif choice == '3':
            if change_brightness():
                apply_all_effects()
        elif choice == '4':
            if draw_line():
                apply_all_effects()
        elif choice == '5':
            show_image()
        elif choice == '6':
            reset_changes()
            apply_all_effects()
        elif choice == '7':
            save_image()
        elif choice == '8':
            cv2.destroyAllWindows()
            break
        else:
            print("Неверный выбор! Попробуйте еще раз.")


def main():
    while True:
        print("\n=== Главное меню ===")
        print("1. Загрузить изображение из файла")
        print("2. Сделать снимок с камеры")
        print("3. Выход")

        choice = input("Ваш выбор (1-3): ")

        if choice == '1':
            if load_image():
                process_image()
        elif choice == '2':
            if use_camera():
                process_image()
        elif choice == '3':
            print("Выход...")
            break
        else:
            print("Неверный выбор! Попробуйте еще раз.")

if __name__ == "__main__":
    main()