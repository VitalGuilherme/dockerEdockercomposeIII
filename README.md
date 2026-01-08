# Nome:
- Diário de tarefas.

# Descrição:
- Guarde todo o seu dia em um back-end fácil e interativo.

# Pré-requesitos
- Docker instalado (Docker compose / Podman compose(Opção open-source))
- Instale o Docker no Desktop e siga o passo a passo na página.
- Mac (https://docs.docker.com/desktop/setup/install/mac-install/)
- Linux (https://docs.docker.com/desktop/setup/install/linux/)
- Windows (https://docs.docker.com/desktop/setup/install/windows-install/)

- Instale Podman compose via terminal
- Mac (brew install podman)
- Linux (sudo apt update && sudo apt install -y podman)
- Windows (choco install podman-cli)

- Python 3.13.3 (Caso queira rodar localmente sem container)

# Clone do repositório GitHub.
- git@github.com:VitalGuilherme/dockerEdockercomposeIII.git

# Rodando o sistema comandos terminal.
- podman machine init (cria uma máquina virtual)
- podman machine star (inicia a máquina virtual)
- podman-compose build (builda o arquivo yaml)
- podman-compose up -d (Sobe o container pra rede)
- podman-compose down (Pausa o container retirando da rede)