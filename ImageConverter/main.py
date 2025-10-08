from abc import ABC, abstractmethod
from PIL import Image


class AImageConverter(ABC):

    @abstractmethod
    def create(self, source_path: str): pass

class PngToJpgConverter(AImageConverter):

    def create(self, source_path: str):
        target_path = source_path.split('.')[0] + '_convert_image.jpg'
        with Image.open(source_path) as img:
            rgb_img = img.convert('RGB')
        return rgb_img.save(target_path)

class JpgToPngConverter(AImageConverter):

    def create(self, source_path: str):
        target_path = source_path.split('.')[0] + '_convert_image.png'
        with Image.open(source_path) as img:
            rgb_img = img.convert('RGB')
        return rgb_img.save(target_path)

class AConverterCreator(ABC):

    @abstractmethod
    def create_converter(self) -> AImageConverter: pass


class PngToJpgConverterCreator(AConverterCreator):

    def create_converter(self) -> AImageConverter:
        return PngToJpgConverter()


class JpgToPngConverterCreator(AConverterCreator):

    def create_converter(self) -> AImageConverter:
        return JpgToPngConverter()

def main():
    convectors = {
        'png': JpgToPngConverterCreator(),
        'jpg': PngToJpgConverterCreator()
    }
    name_convectors = ', '.join(list(convectors.keys()))
    source_path = input("Введите путь к исходному файлу: ").strip()
    format_output = input(f"Введите необходимый формат({name_convectors}): ").strip()

    format_image = format_output.lower()
    if format_image in convectors.keys():
        convector = convectors[format_image].create_converter()
    else:
        print(f'Такого формата пока нет >>> {format_image}')
        return None

    convector.create(source_path)

if __name__ == '__main__':
    main()
