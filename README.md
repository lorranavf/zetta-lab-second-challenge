# Zetta Lab
# Repositório referente à solução do Desafio 2.

# Proposta

O desafio corresponde ao desenvolvimento de uma API visando a gestão de tarefas. Neste caso específico as tarefas foram modeladas como pertencentes à um projeto de modo que o usuário possa controlar as tarefas por grupos.

Este projeto foi desenvolvido em linguagem Python e o framework utilizado foi o [fastapi](https://fastapi.tiangolo.com/).

# Infraestrutura e Deploy

Este repositório divide-se em três partes principais: codebase, deploy, docs.

**Codebase**

Comporta o código fonte de desenvolvimento da API e o código de testes.

**Deploy**

Comporta a infraestrutura necessária para a implementação do ambiente de execução da API seja ele desenvolvimento, testes ou produção.

Os requerimentos python <libs> estão sendo gerenciados no arquivo [pyproject.toml](pyproject.toml).

**Docs**

Comporta dois documentos importantes: o diagrama de esquemas do banco de dados e o diagrama de como os serviços foram orquestrados. Como por exemplo a separação do banco de dados, da API e do Proxy Reverso o qual também pode ser utilizado como balanceador de carga.

# Execução

Para executar o projeto é necessário ter o [Docker](https://www.docker.com/) instalado. A fim de facilitar a orquestração dos diferentes ambientes, foi desenvovlido um script [makefile](makefile), portanto, recomenda-se instalar o make.

**Desenvolvimento**

```bash
# acionar
make dev-start

# remover
make dev-rm
```
**Testes**

```bash
make tests
```
**Produção**

```bash
# acionar
make prod-start

# remover
make prod-rm
```

**Acesso**

A aplicação estará disponível no link https://localhost:8000/ e pode ser testada em https://localhost:8000/docs.

### Relativo a variáveis de ambiente

foram disponibilizadas arquivos específicos para ambiente de [desenvolvimento](deploy/variables/reference) e [teste](deploy/variables/test) como referência. Criar o arquivo [prod.env]() para o ambiente de produção caso deseje testá-lo.

### Extras

**Pre-Commit**

Instalar [uv](https://docs.astral.sh/uv/).

```bash
# instalar
make pre-commit-install

# acionar
make pre-commit-run
```

**Limpar arquivos e imagens corrompidos do Docker**

```bash
make clean
```

# Oferecimento

Este projeto foi desenvolvido por Lorrana Flores. Uma proposta da Zetta Lab.
