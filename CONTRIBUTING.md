## шо ты маленький привет

здарова, спасибо что хочешь помочь проекту.

## что за проект

это coreDVD, проект который эмулирует DVD-плеер со своим процессором (pulse) и сторонним (z80), видео проигрывается через ffmpeg, а графический интерфейс приложения SFML.

## как же помочь проекту?

### баги и идеи
- создай [Issue](https://github.com/pristochelovek097/project-coredvd/issues) с описанием
- используй метки: `bug`, `enhancement`, `good first issue`

### код
1. форкни репо
2. создай ветку: `git checkout -b feature/что-то-крутое`
3. сделай изменения
4. запушь и открой pull requests

### документация
- исправь опечатки в README
- добавь примеры использования
- напиши туториал по прошивкам

## сборка

**линукс:**
```bash
sudo apt install libsfml-dev libavformat-dev libavcodec-dev libswscale-dev libavutil-dev
# если хочешь чтобы у тебя ракета была а не код
g++ src/main.cpp -o coredvd \
    -lsfml-graphics -lsfml-window -lsfml-system \
    -lavformat -lavcodec -lswscale -lavutil -lpthread \
    -std=c++17 -O3 -march=native -mtune=native \
    -flto=auto -fomit-frame-pointer -pipe \
    -Wl,--as-needed -Wl,--gc-sections

# просто скомпилировать
g++ src/main.cpp -o coredvd \
    -lsfml-graphics -lsfml-window -lsfml-system \
    -lavformat -lavcodec -lswscale -lavutil -lpthread \
    -std=c++17 -O2 -pipe

# дебаг
g++ src/main.cpp -o coredvd \
    -lsfml-graphics -lsfml-window -lsfml-system \
    -lavformat -lavcodec -lswscale -lavutil -lpthread \
    -std=c++17 -g -O0 -DDEBUG -Wall -Wextra
```

**винда:**

```bash
# 1. установка Chocolatey
winget install Chocolatey.Chocolatey

# 2. установка MinGW (g++)
choco install mingw -y

# 3. установка FFmpeg
winget install Gyan.FFmpeg.Essentials

# 4. установка vcpkg
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat

# 5. установка SFML через vcpkg
.\vcpkg install sfml:x64-windows

# 6. интеграция vcpkg
.\vcpkg integrate install

# 7. возвращаемся в папку проекта
cd ..

# если хочешь чтобы у тебя ракета была а не код
g++ src/main.cpp -o coredvd \
    -lsfml-graphics -lsfml-window -lsfml-system \
    -lavformat -lavcodec -lswscale -lavutil -lpthread \
    -std=c++17 -O3 -march=native -mtune=native \
    -flto=auto -fomit-frame-pointer -pipe \
    -Wl,--as-needed -Wl,--gc-sections

# просто скомпилировать
g++ src/main.cpp -o coredvd \
    -lsfml-graphics -lsfml-window -lsfml-system \
    -lavformat -lavcodec -lswscale -lavutil -lpthread \
    -std=c++17 -O2 -pipe

# дебаг
g++ src/main.cpp -o coredvd \
    -lsfml-graphics -lsfml-window -lsfml-system \
    -lavformat -lavcodec -lswscale -lavutil -lpthread \
    -std=c++17 -g -O0 -DDEBUG -Wall -Wextra
```

## стиль кода

- один файл -`src/main.cpp` (модульность - можно)
- отступы - 4 пробела
- имена переменных - `snake_case`
- комментарии на русском или английском

## контакты

- телеграм: @pristochelovek097
- иссуес на гитхабе

---

спасибо, что залетел. любая помощь принимается с любовью. 

```text
____________$$$$$$$$______$$$$$$$$$
__________$$$$$$$$$$$$__$$$$$$$__$$$$
_________$$$$$$$$$$$$$$$$$$$$$$$$__$$$
_________$$$$$$$$$$$$$$$$$$$$$$$$__$$$
_________$$$$$$$$$$$$$$$$$$$$$$$$__$$$
__________$$$$$$$$$$$$$$$$$$$$$$__$$$
____________$$$$$$$$$$$$$$$$$$$$$$$
_______________$$$$$$$$$$$$$$$$$
_________________$$$$$$$$$$$$$
____________________$$$$$$$
______________________$$$
_______________________$
```

сам печатал >3
