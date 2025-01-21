from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import os
from video_finder import VideoFinder
import math

def get_filename_without_extension(file_path):
    # Получаем имя файла (без пути) и расширение
    filename_with_extension = os.path.basename(file_path)
    
    # Разделяем имя файла и расширение
    name, extension = os.path.splitext(filename_with_extension)
    
    # Возвращаем только имя файла без расширения
    return name

def last_directory(path):
    return os.path.basename(os.path.dirname(path))

class TimeConverter:
    def to_hours_minutes_and_seconds(self, total_seconds):
        hours = total_seconds // 3600
        remaining_seconds = total_seconds % 3600
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        return hours, minutes, seconds

class VideoToGifsConverter:
    def __init__(self, input_filepath, output_directory, gif_seconds_limit = 60, fps = 15, resized = 0.5, resize_algorithm = 'fast_bilinear', loop=1):
        self.input_filepath = input_filepath
        self.output_directory = output_directory
        self.fps = fps
        self.resized = resized
        self.resize_algorithm = resize_algorithm
        self.loop = loop
        self.resize_method = 1
        self.gif_seconds_limit = int(gif_seconds_limit)
    
    def convert(self):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        #target_resolution – Set to (desired_width, desired_height) to have ffmpeg resize the frames before returning them. This is much faster than streaming in high-res and then resizing. If either dimension is None, the frames are resized by keeping the existing aspect ratio.
        #resize_algorithm – The algorithm used for resizing. Default: “bicubic”, other popular options include “bilinear” and “fast_bilinear”. 
        clip = VideoFileClip(self.input_filepath, resize_algorithm=self.resize_algorithm)
        if self.resized != 1 and self.resize_method == 1:
            clip = VideoFileClip(self.input_filepath, resize_algorithm=self.resize_algorithm, target_resolution=(math.floor(clip.w * self.resized), math.floor(clip.h * self.resized)))
        total_seconds = int(clip.duration)
        time_converter = TimeConverter()
        duration_hours, duration_minutes, duration_seconds = time_converter.to_hours_minutes_and_seconds(clip.duration)
        for start_time in range(0, total_seconds, self.gif_seconds_limit):
            end_time = min(start_time + self.gif_seconds_limit, total_seconds)
            subclip = clip.subclipped(start_time, end_time)
            if self.resized != 1 and self.resize_method == 2:
                subclip = subclip.resized(self.resized)
            start_time_hours, start_time_minutes, start_time_seconds = time_converter.to_hours_minutes_and_seconds(start_time)
            end_time_hours, end_time_minutes, end_time_seconds = time_converter.to_hours_minutes_and_seconds(end_time)
            if start_time_hours < 10:
                start_time_hours = '0' + str(start_time_hours)
            if start_time_minutes < 10:
                start_time_minutes = '0' + str(start_time_minutes)
            if start_time_seconds < 10:
                start_time_seconds = '0' + str(start_time_seconds)
            if end_time_hours < 10:
                end_time_hours = '0' + str(end_time_hours)
            if end_time_minutes < 10:
                end_time_minutes = '0' + str(end_time_minutes)
            if end_time_seconds < 10:
                end_time_seconds = '0' + str(end_time_seconds)
            if duration_hours > 0:
                gif_filename = str(start_time_hours) + ':' + str(start_time_minutes) + ':' + str(start_time_seconds)
                gif_filename += '_to_'
                gif_filename += str(end_time_hours) + ':' + str(end_time_minutes) + ':' + str(end_time_seconds)
            else:
                gif_filename = str(start_time_minutes) + ':' + str(start_time_seconds)
                gif_filename += '_to_'
                gif_filename += str(end_time_minutes) + ':' + str(end_time_seconds)
            gif_filename += '.gif'
            gif_filepath = os.path.join(self.output_directory, gif_filename)
            
            subclip.write_gif(gif_filepath, fps=self.fps, loop=self.loop)
            print(f"Created {gif_filepath}")

# Пример использования
if __name__ == "__main__":
    video_file = input('Укажите название файла или каталога: ')
    output_directory = input('Укажите куда сохранять гифки: ')
    gif_seconds_limit = input('Укажите продолжительность одной гифки в секундах: ')
    fps = input('Укажите количество кадров в секунду: ')
    resized = input('Укажите насколько разрешение гифки нужно уменьшить (0.1 - самое маленькое разрешение, 1 - оригинальное разрешение): ')
    loop = input('Зацикливать гифки (y - да, n - нет)? ')
    if video_file == False or video_file.strip() == '' or video_file == None:
        video_file = os.getcwd()
    if output_directory == False or output_directory.strip() == '' or output_directory == None:
        output_directory = os.getcwd() + '/gifs'
    if video_file == output_directory:
        output_directory += '/gifs'
    if gif_seconds_limit == False or gif_seconds_limit.strip() == '' or gif_seconds_limit == None:
        gif_seconds_limit = 60
    if fps == False or fps.strip() == '' or fps == None:
        fps = 15
    if resized == False or resized.strip() == '' or resized == None:
        resized = 0.5
    if loop == False or loop.strip() == '' or loop == None:
        loop = 1
    elif loop.lower() == 'y':
        loop = 1
    elif loop.lower() == 'n':
        loop = 0
    else:
        loop = 1
    if os.path.isdir(video_file):
        video_paths = VideoFinder(video_file).find_videos()
        for video_file in video_paths:
            new_output_directory = output_directory + '/' + last_directory(video_file)
            gifsConverter = VideoToGifsConverter(video_file, new_output_directory + '/' + get_filename_without_extension(video_file), gif_seconds_limit, int(fps), float(resized), 'fast_bilinear', loop)
            gifsConverter.convert()
    elif os.path.isfile(video_file):
            gifsConverter = VideoToGifsConverter(video_file, output_directory + '/' + get_filename_without_extension(video_file), gif_seconds_limit, int(fps), float(resized), 'fast_bilinear', loop)
            gifsConverter.convert()     
    else:
        print('Нету такого файла или каталога.')
