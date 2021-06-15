## Интерфейс для создания бита
#### Описание:
Интерфейс включает в себя камеру для отработки трека взгляда в реальном времени и приложение. Пользователь запускает приложение и на экране появляется панель управления. С помощью взгляда осуществляется задание желаемых параметров, после чего сигнал преобразуется в аудиофайл. Пользователь может скачать полученный файл. 
#### Технологии:
* ROS
* Python
* OpenCV

#### Цель проекта:
Реализация интерфейса с функцией Gaze tracking, исследование и применение методов и технологий 

#### Задачи проекта:
* Настройка камеры для трека взгляда
* Дизайн приложения
* Разработка алгоритма генерации бита на основе полученных данных
* Разработка приложения
#### Запуск:
Для запуска приложения следует выполнить несколько шагов:

1) Клонировать проект в локальный репозиторий

2) Запустить файл requirements (для установки необходимых библиотек)

3) Переместить содержимое папки src, (папки gaze_tracker и spoproject) в папку, где распологаются ваши ROS пакеты (это может быть catkin_work_space/src)

4) в папке ~/catkin_work_space/ выполнить команду catkin_make

5) Перейти в папку ~/catkin_work_space/src/spoproject/scripts/

6) Запустить интерфейс из этой папки командой python Interface.py
#### Запуск сайта с документацией:
 https://cdn.rawgit.com/x-sanchez/ROS/main/html/index.html
