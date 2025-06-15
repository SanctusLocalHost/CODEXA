# CODEXA

# Gerador de QR Codes em Lotes - CODEXA

CODEXA é uma ferramenta desenvolvida em Python para gerar QR Codes a partir de URLs, com a funcionalidade de adicionar sua logomarca personalizada ao centro do QR Code. 

Seu principal diferencial é a capacidade de gerar QR Codes em lotes (infinitos) a partir da importação de arquivos Excel (.xlsx, .xls) ou CSV (.csv).

## Preview
Dark Mode
![Image](https://github.com/user-attachments/assets/e7f75446-2b5b-4b35-a3ef-c0ecbfc78d03)

Light Mode
![Image](https://github.com/user-attachments/assets/7d972cf6-8047-459e-8efa-28f249e451ee)

Log Terminal Mode
![Image](https://github.com/user-attachments/assets/62ef02ed-70de-4d10-a97f-cbd1617f2a0f)

## Funcionalidades Principais

*   **Geração Individual:** Crie QR Codes únicos rapidamente.
*   **Geração em Lote:** Importe arquivos Excel ou CSV para gerar múltiplos QR Codes de uma vez.
*   **Logomarca Personalizada:** Adicione sua própria logo no centro dos QR Codes gerados.
*   **Nomenclatura Customizável:** Adicione prefixos aos nomes dos arquivos gerados em lote.
*   **Terminal de Log Integrado:** Acompanhe o processo e possíveis avisos (acessível via `Ctrl+T`).
*   **Opções de Saída:** Escolha o formato (PNG, JPG/JPEG) e o tamanho da imagem.
*   **Organização Automática:** Os QR Codes são salvos em subpastas dedicadas.
*   **Offline:** Funciona sem necessidade de conexão com a internet.
*   **Multiplataforma:** Compatível com Windows, macOS e Linux.

## Requisitos

*   Python 3.x
*   As seguintes bibliotecas Python são necessárias:
    ```bash
    pip install customtkinter qrcode[pil] Pillow pandas openpyxl
    ```

## Como Usar

1.  Certifique-se de que todas as dependências listadas acima estão instaladas.
2.  Execute o script Python:
    ```bash
    python nome_do_seu_script.py
    ```
    (Substitua `nome_do_seu_script.py` pelo nome real do arquivo, ex: `codexa_qr_generator.py`)

### Interface Principal

A interface é dividida em:

*   **Modo Único:** Para gerar um QR Code por vez.
*   **Modo Macro (Lote):** Para gerar múltiplos QR Codes a partir de um arquivo.

### Modo Único

1.  **URL/Link:** Insira a URL para a qual o QR Code deve apontar.
2.  **Nome do arquivo:** Defina o nome do arquivo de saída (sem a extensão).
3.  **Opções (Opcional):**
    *   **Selecionar Logo:** Escolha uma imagem para ser o logo no centro do QR Code.
    *   **Formato de saída:** PNG (padrão), JPEG, JPG.
    *   **Diretório de Saída:** Escolha onde salvar o QR Code (por padrão, uma subpasta em seu diretório de usuário).
    *   **Tamanho Imagem (px):** Defina a resolução da imagem do QR Code.
4.  Clique em **Gerar QR**.

### Modo Macro (Geração em Lote)

1.  **Importar CSV/Excel:** Selecione seu arquivo de dados (.csv, .xlsx, .xls).
    *   **Estrutura do Arquivo de Entrada (Excel/CSV):**
        *   A **primeira linha** deve ser o cabeçalho (nomes das colunas).
        *   Os **dados para os QR Codes começam a partir da segunda linha**.
        *   **Coluna de Links:** Uma coluna deve conter as URLs/links (o programa tenta detectar automaticamente colunas com nomes como "url", "link", etc.).
        *   **Coluna de Nomes:** Outra coluna deve conter os nomes base para os arquivos de QR Code gerados (o programa tenta detectar colunas como "nome", "título", "identificador", etc.).
        *   **Exemplo de estrutura:**
            | Link_Site        | Nome_Identificador |
            |------------------|--------------------|
            | https://site1.com| ProdutoA           |
            | https://site2.com| ServicoB           |
            | ...              | ...                |
2.  **Prefixo para os arquivos (Opcional):** Adicione um prefixo que será inserido antes do nome de cada arquivo gerado (ex: `QR_Empresa_` resultaria em `QR_Empresa_ProdutoA.png`).
3.  **Opções (Opcional):**
    *   **Selecionar Logo:** Escolha uma imagem para ser o logo.
    *   **Formato de saída:** PNG (padrão), JPEG, JPG.
    *   **Diretório de Saída:** Escolha a pasta base para salvar os QR Codes (serão salvos em uma subpasta).
    *   **Tamanho Imagem (px):** Defina a resolução.
4.  Clique em **Iniciar** para começar a geração em lote.
    *   Uma barra de progresso e mensagens no terminal de log (se aberto) indicarão o andamento.

## Outras Funcionalidades

*   **Terminal de Log:** Pressione `Ctrl+T` para abrir/fechar um console de log dentro da aplicação, útil para acompanhar detalhes do processo.
*   **Modo Dark/Light:** Um seletor na barra lateral permite alternar entre o tema escuro (Dark) e claro (Light).
*   **Atualizações / Sobre:** Botões na barra lateral para visualizar o histórico de versões e informações sobre o CODEXA.

## Autor

*   Breno_Santos

## Versão do Script

*   1.2.8
