# Lilly

Lilly is fast service-oriented and layered Python 3.6+ web framework built on top of [FastAPI](https://fastapi.tiangolo.com/)
It is enforces a certain way of creating FastApi applications that is much easier to reason about.
Since it is based on FastAPI, it is modern, fast (high performance), and works well with Python type hints.

## Purpose

Lilly signifies peaceful beauty. _Lilly_ is thus an opinionated framework that ensures clean beautiful
code structure that scales well for large projects and large teams.

- It just adds more opinionated structure to the already beautiful [FastAPI](https://fastapi.tiangolo.com/).
- It ensures that when someone is building a web application basing on Lilly, they don't need to think about the structure.
- The developer should just know that it is a service-oriented architecture with each service having a layered architecture
that ensures layers don't know what the other layer is doing.

## Key Features

On top of the [key features of FastAPI](https://fastapi.tiangolo.com/) which include:

- Fast. It is based on FastApi
- Intuitive: Great editor support. Completion everywhere. Less time debugging.
- Easy: Designed to be easy to use and learn. Less time reading docs.
- Short: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
- Robust: Get production-ready code. With automatic interactive documentation.
- Standards-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as
  Swagger) and JSON Schema.

It also:

- Enforces a separation of concerns between service to service
- Enforces a separation of concerns within the service between presentation, business, persistence, and data_source
  layers

## Quick Start

- Ensure you have [Python 3.7](https://www.python.org/downloads/release/python-370/) or +3.7 installed
- Create a new folder for your application

```shell
mkdir lilly_sample && cd lilly_sample
```

- Create the virtual environment and activate it

```shell
python3 -m venv env
source env/bin/activate
```

- Install lilly

```shell
pip install lilly
```

- Create your first application based off the framework

```shell
python -m lilly create-app
```

This will create the following folder structure with some fully functional sample code

```shell
.
  ├── main.py
  ├──  settings.py
  └── services
      ├──  __init__.py
      └── hello
          ├── __init__.py
          ├── actions.py
          ├── datasources.py
          ├── dtos.py
          ├── repositories.py
          └── routes.py
```

- Install uvicorn and run the app

```shell
pip install uvicorn
uvicorn main:app --reload
```

- View the OpenAPI docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

- For you to add another service in the services folder, run the command:

```shell
python -m lilly create-service <service-name>
```

e.g.

```shell
python -m lilly create-service blog
```

- For more information about the commands, just run the `help` commands

```shell
python -m lilly --help
python -m lilly create-app --help
python -m lilly create-service --help
```

## How to Run tests

- Clone the repository

```shell
git clone git@github.com:sopherapps/lilly.git 
```

- Create virtual environment for Python 3.7 and above and activate it

```shell
python3 -m venv env
source env/bin/activate
```

- Install requirements

```shell
pip install -r requirements.txt
```

- Run the test command

```shell
python -m unittest  discover -s test
```

## Usage

Lilly can be used easily in your app.

To create a new app, we use the command:

```shell
python -m lilly create-app <app-name>
```

To add another service in the service folder, we use the command:

```shell
python -m lilly create-service <service-name>
```

These two commands create a starting point with a sample fully-functional web app whose docs can be found at
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) when the app is run locally with the command.

```shell
uvicorn main:app --reload
```

The two `create` commands typically create a service folder with the follwoing structure

```shell
      └── <service-name>
          ├── __init__.py
          ├── actions.py
          ├── datasources.py
          ├── dtos.py
          ├── repositories.py
          └── routes.py
```

The `Action`s can be found in the `actions.py` module. Customize them accordingly following the guidance of the already
existing code. The `DataSource`s can be found in the `datasources.py` module. Customize them accordingly following the
guidance of the already existing code. The `Repository`s can be found in the `respositories.py` module. Customize them
accordingly following the guidance of the already existing code. The `RouteSet`s can be found in the `routes.py` module.
Customize them accordingly following the guidance of the already existing code. The `DataModel` DTOs can be found in
the `dtos.py` module. Customize them accordingly following the guidance of the already existing code.

### Data Sources

To create a new data source, one needs to subclass the `DataSource` class and override the `connect(self)` method.

```python
from typing import Any
from lilly.datasources import DataSource


class SampleDataSource(DataSource):
  def connect(self) -> Any:
    # do some stuff and return a connection
    pass
```

To make life easier for the developer, we have created a few DataSources that can be used or overridden. They include:

#### 1. SQLAlchemyDataSource

This connects to any relational database e.g. MySQL, PostgreSQL, Sqlite etc.
using [SQLAlchemy](https://www.sqlalchemy.org/)
It can be used in a repository as in this example:

```python
from typing import Any
from sqlalchemy.orm import declarative_base
from lilly.repositories import Repository
from lilly.datasources import SQLAlchemyDataSource, DataSource
from lilly.conf import settings

Base = declarative_base()


class NamesRepository(Repository):
  """Repository for saving and retrieving random names"""
  _names_db = SQLAlchemyDataSource(db_uri=settings.DATABASE_URL, declarative_meta=Base)

  # -- other important methods need to be overridden also. I have excluded them for brevity.

  @property
  def _datasource(self) -> DataSource:
    return self._names_db
```

## Design

### Requirements

The following features are required.

#### Configuration

- All services are put in the `services` folder whose import path is passed as a parameter to the `Lilly` instance
  during initialization.
  (Default: folder called `services` on root of project)
- All settings are put as constants in the `settings` python module whose import path is passed to `Lilly` instance at
  initialization.
  (Default: `settings.py` on the root of project)

#### Base Structures

- All services must have the following modules or packages:
  - `routes` (if a package is used, all `RouteSet` subclasses must be imported into the `routes.__init__` module)
  - `actions`
  - `repositories`
  - `datasources`
  - `dtos`
- Just like [FastAPI Class-based views (CBV)](https://fastapi-utils.davidmontague.xyz/user-guide/class-based-views/)
  routes, Lilly routes (which are technically methods of the Service subclass) should have the `post,get,put,patch...`
  decorators. The format is exactly as it is in FastAPI. In addition, dependencies can be shared across multiple
  endpoints of the same service thanks to `FastApi CBV`.
- `RouteSet` is the base class of all Routes. It should have the following methods overridden:
  - `_do(self, actionCls: Type[Action], *args, **kwargs)` which internally initializes the actionCls and calls `run()`
    on it
- `Action` subclasses should have an overridden `run(self) -> Any` method
  - The `run(self)` method should be able to access any repositories by directly importing any it needs
- `Repository` subclasses should have public:
  - `get_one(self, record_id: Any, **kwargs) -> Any` method to get one record of id `record_id`
  - `get_many(self, skip: int, limit: int, filters: Dict[Any, Any], **kwargs) -> List[Any]` method to get many records
    that fulfil the `filters`
  - `create_one(self, record: Any, **kwargs) -> Any` method to create one record
  - `create_many(self, record: List[Any], **kwargs) -> List[Any]` method to create many records
  - `update_one(self, record_id: Any, new_record: Any, **kwargs) -> Any` method to update one record of id `record_id`
  - `update_many(self, new_record: Any, filters: Dict[Any, Any], **kwargs) -> Any` method to update many records that
    fulfil the `filters`
  - `remove_one(self, record_id: Any, **kwargs) -> Any` method to remove one record of id `record_id`
  - `remove_many(self, filters: Dict[Any, Any], **kwargs) -> Any` method to remove many records that fulfil
    the `filters`
- `Repository` subclasses should also have the following methods overridden:
  - `_get_one(self, datasource_connection: Any, record_id: Any, **kwargs) -> Any` method to get one record of
    id `record_id`
  - `_get_many(self, datasource_connection: Any, skip: int, limit: int, filters: Dict[Any, Any], **kwargs) -> List[Any]`
    method to get many records that fulfil the `filters`
  - `_create_one(self, datasource_connection: Any, record: Any, **kwargs) -> Any` method to create one record
  - `_create_many(self, datasource_connection: Any, record: List[Any], **kwargs) -> List[Any]` method to create many
    records
  - `_update_one(self, datasource_connection: Any, record_id: Any, new_record: Any, **kwargs) -> Any` method to update
    one record of id `record_id`
  - `_update_many(self, datasource_connection: Any, new_record: Any, filters: Dict[Any, Any], **kwargs) -> Any` method
    to update many records that fulfil the `filters`
  - `_remove_one(self, datasource_connection: Any, record_id: Any, **kwargs) -> Any` method to remove one record of
    id `record_id`
  - `_remove_many(self, datasource_connection: Any, filters: Dict[Any, Any], **kwargs) -> Any` method to remove many
    records that fulfil the `filters`
  - `_datasource(self) -> DataSource` an @property-decorated method to return the DataSource whose `connect()` method is
    to be called in any of the other methods to get its instance.
  - `_to_output_dto(self, record: Any) -> BaseModel` method which converts any record from the data source raw to DTO
    for the public methods
- `DataSource` subclasses should have an overridden `connect(self)` method
- `dtos` (Data Transfer Object classes) are subclasses of the `pydantic.BaseModel` which are to be used to move data
  across the layers
- Any setting added to the gazetted settings file can be accessed via `lilly.conf.settings.<setting_name>`
  e.g. `lilly.conf.settings.APP_SETTING`

#### Running

- The `Lilly` instance should be run the same way as FastAPI instances are run e.g.

```shell
uvicorn main:app # for app defined in the main.py module
```
### Implementation Ideas

- The application is an instance of the `Lilly` class which is a subclass of the `FastAPI` class.
- To create a `Lilly` instance, we need to pass in the following parameters:
  - services_path (an import path as string, default is "services")
  - settings_path (an import path as string, default is "settings")
- During `Lilly` initialization, all routes are automatically imported using `importlib.import_module` by concatenating
  the `<services_path>.<service_name>.routes` e.g. `services.hello.routes`.
- In order to make route definition solely dependent on folder structure, we change `@app.get` decorators to `@get`
- `app.get`, `app.post` etc. should throw `NotImplementedError` errors
- The whole app has one instance of the `router: APIRouter`. It is defined in the `routing` module.
- In that same `routing` module, `router.get`, `router.post`, `router.delete`, `router.put`, `router.patch`
  , `router.head`, `router.options` are all aliased by their post-period `suffixes` e.g. `get`, `post` etc.
- When initializing in __init__ of Lilly, we fetch the routes in all services then call `self.include_router(router)`.
- `app.mount` should throw an `NotImplementedError` error because it complicates the app structure if used to mount
  other applications, considering the fact that all routes share one `router` instance.
- In order to have a protected method `_do()` to call an action within the routers, we use class-based views
  from [fastapi-utils CBV](https://fastapi-utils.davidmontague.xyz/user-guide/class-based-views/).
- All these class based views will be subclasses of `RouteSet` which has an overridable protected
  method `_do(self, action_cls: Action, *args, **kwargs)` to make a call to any action
- All these class based views will have a decorator `@routeset` which is an alias of `@cbv(router)` where `router` is
  the router common to all routes
- All the routes in the app have one router so their endpoints need to be different and explicit since no mounting will
  be allowed

## ToDo

- [x] Set up the abstract methods structure
- [x] Set up the CLI to generate an app
- [x] Set up the CLI to generate a service
- [x] Make repository public
- [x] Package it and publish it
- [ ] Add some out-of-the-box base data sources e.g.
  - [x] SqlAlchemy
  - [ ] Redis
  - [ ] Memcached
  - [ ] RESTAPI
  - [ ] GraphQL
  - [ ] RabbitMQ
  - [ ] ActiveMQ
  - [ ] Websockets
  - [ ] Kafka
  - [ ] Mongodb
  - [ ] Couchbase
  - [ ] DiskCache
- [ ] Add some out-of-the-box base repositories e.g. 
  - [ ] SqlAlchemyRepo (RDBM e.g. PostgreSQL, MySQL etc.)
  - [ ] RedisRepo
  - [ ] MemcachedRepo
  - [ ] RESTAPIRepo
  - [ ] GraphQLRepo
  - [ ] RabbitMQRepo
  - [ ] ActiveMQRepo
  - [ ] WebsocketsRepo
  - [ ] KafkaRepo
  - [ ] MongodbRepo
  - [ ] CouchbaseRepo
  - [ ] DiskCacheRepo
- [ ] Add some out-of-the-box base actions e.g.
  - [ ] CreateOneAction
  - [ ] CreateManyAction
  - [ ] UpdateOneAction
  - [ ] UpdateManyAction
  - [ ] ReadOneAction
  - [ ] ReadManyAction
  - [ ] DeleteOneAction
  - [ ] DeleteManyAction
- [ ] Add some out-of-the-box base route sets
  - [ ] CRUDRouteSet
  - [ ] WebsocketRouteSet
  - [ ] GraphQLRoute
- [ ] Add example code in examples folder
  - [ ] Todolist (CRUDRouteSet, SqlAlchemyRepo)
  - [ ] RandomQuotes (WebsocketRouteSet, MongodbRepo) (quotes got from the Bible)
  - [ ] Clock (WebsocketRouteSet, WebsocketsRepo)
- [ ] Set up automatic documentation
- [ ] Set up CI via Github actions
- [ ] Set up CD via Github actions
- [ ] Write about it in hashnode or Medium or both

## Inspiration

- The idea to create **lilly** came after looking at what the [Loopback](https://loopback.io/) team did
  with [Loopback4](https://loopback.io/doc/en/lb4)

## License

Copyright (c) 2022 [Martin Ahindura](https://github.com/Tinitto) Licensed under the [MIT License](./LICENSE)
