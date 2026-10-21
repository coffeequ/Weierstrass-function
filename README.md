# Weierstrass Function Visualization / Визуализация функции Вейерштрасса

# RU
Минимальный Manim-проект для создания анимации о функции Вейерштрасса:

```math
W(x)=\sum_{n=0}^{\infty} a^n\cos(b^n\pi x)
```

В анимации показываются формула, основные свойства функции и приближение к выбранной точке графика, чтобы продемонстрировать фрактальную структуру.

## Состав проекта

- `main.py` - основная сцена `DrawFunction`.
- `manim.cfg` - настройки Manim: вертикальный формат `1080x1920`, черный фон, частота кадров.
- `.gitignore` - исключает сгенерированные видео, изображения, папку `media` и кеш Python.
- `Video/` - папка для готовых или промежуточных видеоматериалов, если используется локально.

## Зависимости

Нужны Python, Manim и NumPy:

```bash
pip install manim numpy
```

Для корректной работы Manim также должны быть установлены системные зависимости Manim: LaTeX, FFmpeg и библиотеки рендеринга. Подробности зависят от операционной системы.

## Запуск

Из корня проекта:

```bash
manim -pqh main.py DrawFunction
```

Где:

- `-p` - открыть результат после рендера;
- `-q h` - качество `high`;
- `main.py` - файл со сценой;
- `DrawFunction` - имя класса сцены.

Для быстрого тестового рендера можно использовать:

```bash
manim -pql main.py DrawFunction
```

## Настройка сцены

Основные параметры находятся в начале метода `construct` в `main.py`:

- `a = 0.5`, `b = 13` - параметры функции Вейерштрасса;
- `x0 = 0.52` - точка фокусировки;
- `max_terms` - число членов ряда для аппроксимации;
- `graph_samples` - количество точек графика;
- `max_x_stretch`, `second_x_stretch` - уровни горизонтального масштабирования при приближении.

Частота кадров в коде задается строкой:

```python
config.frame_rate = 60
```

Она переопределяет значение из `manim.cfg`.

# EN
# Weierstrass Function Visualization

A minimal Manim project for creating an animation of the Weierstrass function:

```math
W(x)=\sum_{n=0}^{\infty} a^n\cos(b^n\pi x)
```

The animation presents the formula, the function's key properties, and a zoom-in on a selected point of the graph to demonstrate its fractal structure.

## Project Structure

- `main.py` — the main `DrawFunction` scene.
- `manim.cfg` — Manim configuration: vertical format (`1080x1920`), black background, and frame rate.
- `.gitignore` — excludes generated videos, images, the `media` directory, and Python cache files.
- `Video/` — directory for finished or intermediate video files, if used locally.

## Dependencies

Python, Manim, and NumPy are required:

```bash
pip install manim numpy
```

For Manim to work correctly, its system dependencies must also be installed, including LaTeX, FFmpeg, and rendering libraries. The exact requirements depend on the operating system.

## Running the Project

Run the following command from the project root directory:

```bash
manim -pqh main.py DrawFunction
```

Where:

- `-p` — preview the result after rendering;
- `-q h` — use `high` quality;
- `main.py` — the file containing the scene;
- `DrawFunction` — the name of the scene class.

For a quick test render, use:

```bash
manim -pql main.py DrawFunction
```

## Scene Configuration

The main parameters are defined at the beginning of the `construct` method in `main.py`:

- `a = 0.5`, `b = 13` — parameters of the Weierstrass function;
- `x0 = 0.52` — the focal point;
- `max_terms` — the number of series terms used for approximation;
- `graph_samples` — the number of graph sample points;
- `max_x_stretch`, `second_x_stretch` — horizontal zoom levels used during the zoom-in animation.

The frame rate is set in the code using:

```python
config.frame_rate = 60
```

This overrides the value specified in `manim.cfg`.

## Output

After rendering, Manim saves the video in the `media/` directory. This directory is not tracked by Git because it contains generated files.

## Результат

После рендера Manim сохраняет видео в папке `media/`. Эта папка не отслеживается Git, так как содержит генерируемые файлы.
