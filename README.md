
## API (Back-End)

```markdown
#  Loja Online — API (Back-End)

Este projeto é a **API principal** de uma loja online, desenvolvida em **Python + Flask**, responsável pelo gerenciamento de pedidos.

---

# API Externa: Fake Store API

Este projeto utiliza a Fake Store API, uma API pública gratuita que fornece dados de produtos fictícios para testes e prototipagem.

    Licença: gratuita, sem necessidade de cadastro.
    -https://fakestoreapi.com/products-
     

# Rotas utilizadas:

    GET https://fakestoreapi.com/products → lista de produtos.

    GET https://fakestoreapi.com/products/:id → detalhes de produto.

# Tecnologias

    Python 3.10

    Flask + Flask-CORS

    SQLite3

    Gunicorn

    Docker

---

##  Funcionalidades
A API implementa um CRUD completo de pedidos com suporte a:
- **POST** `/orders` → criar pedido
- **GET** `/orders` → listar pedidos
- **GET** `/orders/<id>` → consultar pedido específico
- **PUT** `/orders/<id>` → atualizar status do pedido
- **DELETE** `/orders/<id>` → excluir pedido

---

##  Instalação e Execução

### Pré-requisitos
- [Docker](https://www.docker.com/) instalado.
- [Python 3.10+](https://www.python.org/downloads/) (se desejar rodar fora do Docker).

### Passos (via Docker)
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/online-shop.git
   cd online-shop/purchase-api-backend

2. Construa e suba o container:

    docker build -t purchase-api-backend .
    docker run --rm -p 8000:8000 purchase-api-backend


3. A API estará acessível em:

    http://localhost:8000