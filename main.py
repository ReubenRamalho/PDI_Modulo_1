import pathlib
import os
import argparse
import random
from PIL import Image, ImageOps

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

# Função para processar uma única imagem
def process_single_image(image_path, mode, max_angle=15):
    image_path = pathlib.Path(image_path)

    if not image_path.exists():
        print(f"Erro: A imagem '{image_path}' não existe.")
        return

    img = Image.open(image_path)

    if mode == "fliph":
        processed_img = flip_horizontal(img)
    elif mode == "rotation":
        processed_img = random_rotation(img, max_angle)
    else:
        print("Modo inválido. Use 'fliph' ou 'rotation'.")
        return

    # Define o caminho de saída
    suffix = "_flipped" if mode == "fliph" else f"_rotated_{max_angle}"
    processed_image_path = image_path.parent / f"{image_path.stem}{suffix}{image_path.suffix}"
    processed_img.save(processed_image_path)

    print(f"Imagem processada salva em: {processed_image_path}")

# Função para processar um diretório
def process_directory(input_dir, output_dir, mode, max_angle=15):
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
                else:
                    print("Modo inválido. Use 'fliph' ou 'rotation'.")
                    return

                processed_image_path = new_class_dir / f"{image_path.stem}{suffix}{image_path.suffix}"
                processed_img.save(processed_image_path)

    print(f"Novo dataset criado em: {output_dir}")

# Configuração do parser para receber argumentos no terminal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Flip horizontal ou rotação aleatória de imagens",
        usage="%(prog)s mode path [--max_angle {1,5,10,15,25,45,90}] [--output OUTPUT]",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40)  # Ajusta o alinhamento
    )

    # Argumento obrigatório para o modo de funcionamento
    parser.add_argument("mode", choices=["fliph", "rotation"], help="Modo de funcionamento: 'fliph' para flip horizontal ou 'rotation' para rotação aleatória")
    
    # Argumento para o caminho da imagem ou diretório
    parser.add_argument("path", help="Caminho da imagem ou diretório")

    # Argumento opcional para o ângulo máximo (apenas para rotação)
    parser.add_argument("--max_angle", type=int, choices=[1, 5, 10, 15, 25, 45, 90], default=15,
                        help="Ângulo máximo para rotação aleatória (default: 15 graus)")

    # Argumento opcional para o diretório de saída (apenas para o modo 'dir')
    parser.add_argument("--output", default="output_processed", help="Caminho do diretório de saída (apenas para o modo 'dir')")

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
