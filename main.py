import pathlib
import argparse
import random
from PIL import Image

# Implementação manual do flip horizontal
def flip_horizontal(image):
    """
    Realiza o flip horizontal de uma imagem manualmente.
    """
    width, height = image.size
    flipped_image = Image.new(image.mode, (width, height))  # Cria uma nova imagem com o mesmo tamanho e modo

    for x in range(width):
        for y in range(height):
            original_pixel = image.getpixel((x, y))
            flipped_image.putpixel((width - 1 - x, y), original_pixel)

    return flipped_image

# Função para rotação aleatória
def random_rotation(image, max_angle):
    """
    Aplica uma rotação aleatória entre 0 e max_angle graus.
    Preenche os pixels indefinidos com RGB=(0,0,0).
    """
    angle = random.uniform(0, max_angle)  # Gera um ângulo aleatório entre 0 e max_angle
    return image.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(0, 0, 0))

# Função para zoom aleatório
def random_zoom(image, max_zoom):
    """
    Aplica um zoom aleatório entre 0% e max_zoom%.
    A imagem final é cortada para manter as dimensões originais.
    """
    width, height = image.size
    zoom_factor = random.uniform(1.0, 1 + max_zoom / 100)  # Fator de zoom entre 1.0 e (1 + max_zoom%)

    # Calcula o novo tamanho da imagem ampliada
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)

    # Redimensiona a imagem para o novo tamanho maior
    zoomed_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Calcula as coordenadas para o corte central mantendo o tamanho original
    left = (new_width - width) // 2
    top = (new_height - height) // 2
    right = left + width
    bottom = top + height

    # Corta a imagem para o tamanho original
    cropped_image = zoomed_image.crop((left, top, right, bottom))

    return cropped_image

# Função para processar uma única imagem
def process_single_image(image_path, mode, max_angle=15, max_zoom=20):
    image_path = pathlib.Path(image_path)

    if not image_path.exists():
        print(f"Erro: A imagem '{image_path}' não existe.")
        return

    img = Image.open(image_path)

    if mode == "fliph":
        processed_img = flip_horizontal(img)
        suffix = "_flipped"
    elif mode == "rotation":
        processed_img = random_rotation(img, max_angle)
        suffix = f"_rotated_{max_angle}"
    elif mode == "zoom":
        processed_img = random_zoom(img, max_zoom)
        suffix = f"_zoomed_{max_zoom}"
    else:
        print("Modo inválido. Use 'fliph', 'rotation' ou 'zoom'.")
        return

    # Define o caminho de saída
    processed_image_path = image_path.parent / f"{image_path.stem}{suffix}{image_path.suffix}"
    processed_img.save(processed_image_path)

    print(f"Imagem processada salva em: {processed_image_path}")

# Função para processar um diretório
def process_directory(input_dir, output_dir, mode, max_angle=15, max_zoom=20):
    input_dir = pathlib.Path(input_dir)
    output_dir = pathlib.Path(output_dir)

    if not input_dir.exists():
        print(f"Erro: O diretório '{input_dir}' não existe.")
        return

    for class_dir in input_dir.iterdir():
        if class_dir.is_dir():
            new_class_dir = output_dir / class_dir.name
            new_class_dir.mkdir(parents=True, exist_ok=True)

            for image_path in class_dir.glob('*.jpg'):
                img = Image.open(image_path)

                # Salva a imagem original
                original_image_path = new_class_dir / image_path.name
                img.save(original_image_path)

                # Processa a imagem de acordo com o modo
                if mode == "fliph":
                    processed_img = flip_horizontal(img)
                    suffix = "_flipped"
                elif mode == "rotation":
                    processed_img = random_rotation(img, max_angle)
                    suffix = f"_rotated_{max_angle}"
                elif mode == "zoom":
                    processed_img = random_zoom(img, max_zoom)
                    suffix = f"_zoomed_{max_zoom}"
                else:
                    print("Modo inválido. Use 'fliph', 'rotation' ou 'zoom'.")
                    return

                processed_image_path = new_class_dir / f"{image_path.stem}{suffix}{image_path.suffix}"
                processed_img.save(processed_image_path)

    print(f"Novo dataset criado em: {output_dir}")

# Configuração do parser para receber argumentos no terminal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Flip horizontal, rotação ou zoom aleatório em imagens",
        usage="%(prog)s mode path [--max_angle {1,5,10,15,25,45,90}] [--max_zoom {5,10,20,40,80}] [--output OUTPUT]",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40)
    )

    # Argumento obrigatório para o modo de funcionamento
    parser.add_argument("mode", choices=["fliph", "rotation", "zoom"], help="Modo: 'fliph' para flip horizontal, 'rotation' para rotação aleatória ou 'zoom' para zoom aleatório")
    
    # Argumento para o caminho da imagem ou diretório
    parser.add_argument("path", help="Caminho da imagem ou diretório")

    # Argumento opcional para o ângulo máximo (apenas para rotação)
    parser.add_argument("--max_angle", type=int, choices=[1, 5, 10, 15, 25, 45, 90], default=15,
                        help="Ângulo máximo para rotação aleatória (default: 15 graus)")
    
    # Argumento opcional para o zoom máximo (somente para zoom)
    parser.add_argument("--max_zoom", type=int, choices=[5, 10, 20, 40, 80], default=20,
                        help="Porcentagem máxima para zoom aleatório (default: 20%%)")

    # Argumento opcional para o diretório de saída (apenas se path for um diretório)
    parser.add_argument("--output", default="output_processed", help="Caminho do diretório de saída (apenas se path for um diretório)")

    args = parser.parse_args()

    # Decide qual função executar com base no modo escolhido
    if args.mode == "fliph":
        if pathlib.Path(args.path).is_file():
            process_single_image(args.path, mode="fliph")
        elif pathlib.Path(args.path).is_dir():
            process_directory(args.path, args.output, mode="fliph")
        else:
            print(f"Erro: O caminho '{args.path}' não existe.")

    elif args.mode == "rotation":
        if pathlib.Path(args.path).is_file():
            process_single_image(args.path, mode="rotation", max_angle=args.max_angle)
        elif pathlib.Path(args.path).is_dir():
            process_directory(args.path, args.output, mode="rotation", max_angle=args.max_angle)
        else:
            print(f"Erro: O caminho '{args.path}' não existe.")

    elif args.mode == "zoom":
        if pathlib.Path(args.path).is_file():
            process_single_image(args.path, mode="zoom", max_zoom=args.max_zoom)
        elif pathlib.Path(args.path).is_dir():
            process_directory(args.path, args.output, mode="zoom", max_zoom=args.max_zoom)
        else:
            print(f"Erro: O caminho '{args.path}' não existe.")
