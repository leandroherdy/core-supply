# Juntos Somos+

## Descrição

Esta API foi desenvolvida para processar dados de clientes em formato CSV e JSON, aplicando regras de classificação com base na região e características do usuário. A API fornece uma lista dos usuários elegíveis de acordo com sua região e tipo de classificação. Além disso, oferece funcionalidades de paginação para facilitar a navegação entre os registros.

## Recebimento de Dados de Clientes
O sistema processa informações de clientes fornecidas por empresas participantes. Esses dados são enviados em dois formatos principais: CSV e JSON.

### Exemplo de Arquivo CSV:
```
gender,name.title,name.first,name.last,location.street,location.city,location.state,location.postcode,location.coordinates.latitude,location.coordinates.longitude,location.timezone.offset,location.timezone.description,email,dob.date,dob.age,registered.date,registered.age,phone,cell,picture.large,picture.medium,picture.thumbnail
male,mr,joselino,alves,2095 rua espirito santo ,são josé de ribamar,paraná,96895,-35.8687,-131.8801,-10:00,Hawaii,joselino.alves@example.com,1996-01-09T02:53:34Z,22,2014-02-09T19:19:32Z,4,(97) 0412-1519,(94) 6270-3362,https://randomuser.me/api/portraits/men/75.jpg,https://randomuser.me/api/portraits/med/men/75.jpg,https://randomuser.me/api/portraits/thumb/men/75.jpg
```
### Exemplo de Arquivo JSON:
```
{
  "gender": "male",
  "name": {
    "title": "mr",
    "first": "antonelo",
    "last": "da conceição"
  },
  "location": {
    "street": "8986 rua rui barbosa ",
    "city": "santo andré",
    "state": "alagoas",
    "postcode": 40751,
    "coordinates": {
      "latitude": "-69.8704",
      "longitude": "-165.9545"
    },
    "timezone": {
      "offset": "+1:00",
      "description": "Brussels, Copenhagen, Madrid, Paris"
    }
  },
  "email": "antonelo.daconceição@example.com",
  "dob": {
    "date": "1956-02-12T10:38:37Z",
    "age": 62
  },
  "registered": {
    "date": "2005-12-05T15:22:53Z",
    "age": 13
  },
  "phone": "(85) 8747-8125",
  "cell": "(87) 2414-0993",
  "picture": {
    "large": "https://randomuser.me/api/portraits/men/8.jpg",
    "medium": "https://randomuser.me/api/portraits/med/men/8.jpg",
    "thumbnail": "https://randomuser.me/api/portraits/thumb/men/8.jpg"
  }
}
```

## Regras de Negócio

Para organizar e analisar os dados recebidos, implementamos regras de negócio baseadas nas cinco regiões do Brasil:

  1. Norte
  2. Nordeste
  3. Centro-Oeste
  4. Sudeste
  5. Sul

O sistema processa os dados recebidos para associá-los corretamente às regiões e garantir que estejam prontos para serem consultados e manipulados conforme necessário.
Essas regras são fundamentais para alinhar os dados com os requisitos internos e otimizar o processo de análise de clientes.

### Classificação por Região:

A classificação do usuário depende da sua localização geográfica. A API utiliza uma série de limites geográficos (bounding box) para determinar se o usuário se encaixa em uma das categorias de classificação (ESPECIAL, NORMAL, TRABALHOSO).

- **ESPECIAL**

```
minlon: -2.196998
minlat -46.361899
maxlon: -15.411580
maxlat: -34.276938
```
```
minlon: -19.766959
minlat -52.997614
maxlon: -23.966413
maxlat: -44.428305
```

- **NORMAL**

```
minlon: -26.155681
minlat -54.777426
maxlon: -34.016466
maxlat: -46.603598
```

- **TRABALHOSO:** Qualquer outro usuário que não se encaixa nas regras acima.

### Transformação dos dados:

1. Telefone: Os números de telefone devem ser convertidos para o formato internacional [E.164](https://en.wikipedia.org/wiki/E.164).
2. Nacionalidade Padrão: O campo `nationality` é inserido automaticamente com o valor padrão `BR`, já que todos os clientes cadastrados são do Brasil.
3. Gênero: O campo `gender` deve ser alterado para o formato `M` ou `F`, conforme necessário.
4. Remoção de Idade: O campo `age` de `dob` e `registered` é removido.
5. Estrutura Simplificada: A estrutura dos dados é reorganizada para melhorar a legibilidade, utilizando arrays para telephoneNumbers e mobileNumbers, por exemplo.

## Endpoints
### 1. Carregar Dados de Clientes
  * **Método:** GET
  * **URL:** /load-data/

### Descrição
Este endpoint é utilizado para carregar os dados de entrada a partir dos arquivos **CSV** e **JSON** disponibilizados via URL.

* #### Parâmetros de URL:
  * URL para o arquivo CSV contendo os dados dos clientes.
  * URL para o arquivo JSON contendo os dados dos clientes.

### Autenticação
Este endpoint requer autenticação via **Token**. O token deve ser enviado no cabeçalho da requisição.

### Exemplo de Requisição
```
curl -X GET "http://127.0.0.1:8000/load-data/" \
  -H "Authorization: Bearer <seu_access_token_aqui>"
```
* #### Resposta:

  * **Código de Status:** 200 OK

  * **Corpo da resposta:** Lista paginada de usuários, contendo metadados de paginação.

```
{
  "pageNumber": 1,
  "pageSize": 10,
  "totalCount": 1000,
  "previousPage": null,
  "nextPage": "http://127.0.0.1:8000/api/v1/clients/https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv/?page=2&page_size=10",
  "users": [
      {
          "type": "laborious",
          "gender": "f",
          "name": {
              "title": "mrs",
              "first": "ione",
              "last": "da costa"
          },
          "location": {
              "region": "norte",
              "street": "8614 avenida vinícius de morais",
              "city": "ponta grossa",
              "state": "rondônia",
              "postcode": 97701,
              "coordinates": {
                  "latitude": -76.3253,
                  "longitude": 137.9437
              },
              "timezone": {
                  "offset": "-1:00",
                  "description": "Azores, Cape Verde Islands"
              }
          },
          "email": "ione.dacosta@example.com",
          "birthday": "1968-01-24T18:03:23Z",
          "registered": "2004-01-23T23:54:33Z",
          "telephoneNumbers": [
              "+550154155648"
          ],
          "mobileNumbers": [
              "+551082645550"
          ],
          "picture": {
              "large": "https://randomuser.me/api/portraits/women/46.jpg",
              "medium": "https://randomuser.me/api/portraits/med/women/46.jpg",
              "thumbnail": "https://randomuser.me/api/portraits/thumb/women/46.jpg"
          },
          "nationality": "BR"
      },
      ...
  ]
}
```

  * **Código de Status:** 401 Unauthorized (se o token for inválido ou não fornecido)

```
{
  "detail": "Authentication credentials were not provided."
}
```

## Execução

### Requisitos
* Python 3.12
* Poetry 1.8.4
* Docker 4.36.0

### Instalação
1. Clone o repositório:
```
git clone git@github.com:leandroherdy/core-supply.git
cd core-supply
```
2. Instale as dependências utilizando o Poetry:
```
make install
```
3. Suba as dependências (por exemplo, banco de dados) utilizando Docker Compose:
```
make up-dependencies-only
```
4. Inicie o servidor:

```
make run-server
```

## Testes
1. Execute os testes com o comando:
```
make test
```
2. Execute os testes validate.sh com o comando:
```
make test-sh
```

## Considerações Finais
