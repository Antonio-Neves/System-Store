
### 1. Instalar o NSSM

   **Extraia:** Descomprima o ficheiro e copie o executável `nssm.exe` para uma pasta de fácil acesso (ex: `C:\nssm`).

### 2. Criar o Serviço do Windows

   Abra o **Prompt de Comando como Administrador** e use o NSSM para instalar o seu *script* como um serviço:

   Navegue até à pasta onde guardou o nssm.exe

`nssm install SystemStoreDjango`

O NSSM irá abrir uma janela gráfica onde você deve configurar o seguinte:

| **Campo** | **O que preencher** |
| --- | --- |
| **Path** | O caminho completo para o seu *script* `.bat` (Ex: `C:\Projetos\Django\iniciar_waitress.bat`) |
| **Startup directory** | O caminho para a pasta onde está o seu `manage.py` (pasta raiz do projeto) |

Depois de preencher e clicar em **"Install Service"**, o serviço será criado.

### 4. Configurar e Iniciar o Serviço

1. Abra o **Gestor de Serviços do Windows** (pesquise por "Services" no menu Iniciar).
2. Procure pelo nome que você deu ao seu serviço (Ex: `NomeDoSeuServicoDjango`).
3. Clique duas vezes nele:
    - Em **"Startup type"** (Tipo de Arranque), selecione **"Automatic"** (Automático).
    - Clique em **"Start"** (Iniciar) para arrancar o servidor imediatamente.

Com isso, o seu servidor Django com Waitress **arrancará automaticamente sempre que o Windows for ligado** e correrá em segundo plano sem a necessidade de janelas abertas.