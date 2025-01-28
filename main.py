import pathlib
import os
import argparse
from PIL import Image

# Implementação manual do flip horizontal
def flip_horizontal(image):
    """
    Realiza o flip horizontal de uma imagem manualmente.
    """
    width, height = image.size
    flipped_image = Image.new(image.mode, (width, height))  # Cria uma nova imagem com o mesmo tamanho e modo
    
    # Preenche a nova imagem com pixels da imagem original em ordem invertida horizontalmente
    for x in range(width):
        for y in range(height):
            original_pixel = image.getpixel((x, y))
            flipped_image.putpixel((width - 1 - x, y), original_pixel)
    
    return flipped_image

# Função para processar uma única imagem
def process_single_image(image_path):
    image_path = pathlib.Path(image_path)  # Converte para Path se for string

    if not image_path.exists():
        print(f"Erro: A imagem '{image_path}' não existe.")
        return
    
    # Abre a imagem original
    img = Image.open(image_path)

    # Cria a versão flipada
    flipped_img = flip_horizontal(img)

    # Define o caminho de saída (salva no mesmo local com "_flipped" no nome)
    flipped_image_path = image_path.parent / f"{image_path.stem}_flipped{image_path.suffix}"
    flipped_img.save(flipped_image_path)

    print(f"Imagem flipada salva em: {flipped_image_path}")

# Função para processar e salvar imagens dentro de um diretório
def process_directory(input_dir, output_dir):
    input_dir = pathlib.Path(input_dir)
    output_dir = pathlib.Path(output_dir)
    
    if not input_dir.exists():
        print(f"Erro: O diretório '{input_dir}' não existe.")
        return

    for class_dir in input_dir.iterdir():
        if class_dir.is_dir():
            # Cria a mesma estrutura de diretório no novo dataset
            new_class_dir = output_dir / class_dir.name
            new_class_dir.mkdir(parents=True, exist_ok=True)

            for image_path in class_dir.glob('*.jpg'):
                # Abre a imagem original
                img = Image.open(image_path)

                # Salva a imagem original
                original_image_path = new_class_dir / image_path.name
                img.save(original_image_path)

                # Cria a versão flipada horizontalmente usando a implementação manual
                flipped_img = flip_horizontal(img)

                # Salva a imagem flipada
                flipped_image_path = new_class_dir / f"{image_path.stem}_flipped{image_path.suffix}"
                flipped_img.save(flipped_image_path)

    print(f"Novo dataset criado em: {output_dir}")

# Configuração do parser para receber argumentos no terminal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flip horizontal de imagens")

    # Argumento para o modo de funcionamento
    parser.add_argument("mode", choices=["single", "dir"], help="Modo de funcionamento: 'single' para uma imagem ou 'dir' para um diretório")

    # Argumento para o caminho da imagem ou do diretório
    parser.add_argument("path", help="Caminho da imagem ou diretório")

    # Argumento opcional para o diretório de saída no modo 'dir'
    parser.add_argument("--output", default="output_flipped", help="Caminho do diretório de saída (apenas para o modo 'dir')")

    args = parser.parse_args()

    # Decide qual função executar com base no modo escolhido
    if args.mode == "single":
        process_single_image(args.path)
    elif args.mode == "dir":
        process_directory(args.path, args.output)
