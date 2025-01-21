import os
from pathlib import Path

class VideoFinder:
    def __init__(self, directory, extensions = [".mp4", ".mov", ".avi", '.mkv']):
        self.directory = Path(directory)
        self.extensions = extensions
        self.video_paths = []

    def find_videos(self):
        self._find_videos_recursive(self.directory)
        return self.video_paths

    def _find_videos_recursive(self, dir_path):
        for entry in dir_path.iterdir():
            if entry.is_file() and entry.suffix.lower() in self.extensions:
                self.video_paths.append(entry)
            elif entry.is_dir():
                self._find_videos_recursive(entry)

# Пример использования
if __name__ == "__main__":
    directory = input('Каталог: ')
    finder = VideoFinder(directory)
    video_paths = finder.find_videos()
    print("Все найденные видеофайлы:")
    for video_path in video_paths:
        print(video_path) 
