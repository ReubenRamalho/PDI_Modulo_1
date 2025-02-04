# Sistema de Manipulação de Imagens (smi)

Este script em Python permite realizar operações de processamento de imagens, incluindo **flip horizontal**, **rotação aleatória** e **zoom aleatório**. O script suporta tanto o processamento de imagens individuais quanto de diretórios inteiros.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `Pillow`
  - `matplotlib`

Instale as dependências usando:

```bash
pip install Pillow matplotlib
```

## Uso

O script pode ser executado via linha de comando:

```bash
python smi.py <modo> <caminho> [opções]
```

### Argumentos Obrigatórios
- `modo`: Define o tipo de processamento.
  - `fliph`: Flip horizontal.
  - `rotation`: Rotação aleatória.
  - `zoom`: Zoom aleatório.

- `caminho`: Caminho para a imagem ou diretório de imagens.

### Opções
- `--max_angle`: Define o ângulo máximo para rotação aleatória. Valores permitidos: 1, 5, 10, 15, 25, 45, 90 (padrão: 15).
- `--max_zoom`: Define a porcentagem máxima para zoom aleatório. Valores permitidos: 5, 10, 20, 40, 80 (padrão: 20).
- `--output`: Caminho para o diretório de saída ao processar diretórios (padrão: `output_processed`).
- `--show`: Exibe a imagem original e a processada (apenas para imagens individuais).

## Exemplos de Uso

### 1. Flip Horizontal em uma Imagem Individual
```bash
python smi.py fliph caminho/para/imagem.jpg --show
```

### 2. Rotação Aleatória com Ângulo Máximo de 45º
```bash
python smi.py rotation caminho/para/imagem.jpg --max_angle 45 --show
```

### 3. Zoom Aleatório em um Diretório de Imagens
```bash
python smi.py zoom caminho/para/diretorio --max_zoom 40 --output imagens_processadas
```

## Funcionalidades

- **Flip Horizontal:** Implementado pixel a pixel.
- **Rotação Aleatória:** Rotação com preenchimento de fundo preto.
- **Zoom Aleatório:** Zoom com corte central para manter o tamanho original.
- **Exibição Comparativa:** Mostra a imagem original e a processada lado a lado com `--show`.

## Estrutura de Saída

Para diretórios, o script cria uma estrutura semelhante à original dentro do diretório de saída, contendo as imagens originais e processadas.

## Erros Comuns
- **"O caminho não existe"**: Verifique se o caminho está correto.
- **"Modo inválido"**: Use apenas os modos permitidos (`fliph`, `rotation`, `zoom`).

## Licença
Este script é fornecido para fins educacionais e de experimentação.

