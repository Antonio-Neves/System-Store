## 1. Install NSSM

Extract the downloaded archive and copy the `nssm.exe` executable to an easily accessible folder (e.g. `C:\nssm`).

## 2. Create the Windows Service

Open **Command Prompt as Administrator** and use NSSM to install your script as a Windows service.

Navigate to the folder where `nssm.exe` is located and run:

```bash
nssm install StoreManagementDjango
```

NSSM will open a graphical configuration window. Fill in the following fields:

| **Field** | **Value** |
|-----------|-----------|
| **Path** | The full path to your `.bat` script (e.g. `C:\Projects\Django\start_waitress.bat`) |
| **Startup directory** | The root folder of your Django project (the folder containing `manage.py`) |

After filling in the fields, click **Install Service** to create the service.

## 3. Configure and Start the Service

1. Open the **Windows Services** manager (search for **Services** in the Start menu).
2. Locate the service you created (e.g. `StoreManagementDjango`).
3. Double-click the service and:
   - Set **Startup type** to **Automatic**.
   - Click **Start** to launch the service immediately.

Once configured, your Django application running with Waitress will **start automatically whenever Windows boots**  
and will run in the background without requiring any command prompt windows to remain open.

---

## 1. Instalar o NSSM

   **Extraia:** Descomprima o ficheiro e copie o executável `nssm.exe` para uma pasta de fácil acesso (ex: `C:\nssm`).

## 2. Criar o Serviço do Windows

   Abra o **Prompt de Comando como Administrador** e use o NSSM para instalar o seu *script* como um serviço:

   Navegue até à pasta onde guardou o nssm.exe

`nssm install StoreManagementDjango`

O NSSM irá abrir uma janela gráfica onde você deve configurar o seguinte:

| **Campo** | **O que preencher** |
| --- | --- |
| **Path** | O caminho completo para o seu *script* `.bat` (Ex: `C:\Projetos\Django\iniciar_waitress.bat`) |
| **Startup directory** | O caminho para a pasta onde está o seu `manage.py` (pasta raiz do projeto) |

Depois de preencher e clicar em **"Install Service"**, o serviço será criado.

## 3. Configurar e Iniciar o Serviço

1. Abra o **Gestor de Serviços do Windows** (pesquise por "Services" no menu Iniciar).
2. Procure pelo nome que você deu ao seu serviço (Ex: `NomeDoSeuServicoDjango`).
3. Clique duas vezes nele:
    - Em **"Startup type"** (Tipo de Arranque), selecione **"Automatic"** (Automático).
    - Clique em **"Start"** (Iniciar) para arrancar o servidor imediatamente.

Com isso, o seu servidor Django com Waitress **arrancará automaticamente sempre que o Windows for ligado**  
e correrá em segundo plano sem a necessidade de janelas abertas.
