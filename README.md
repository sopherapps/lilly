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
git clone git@github.com:sopherapps/lilly.git && cd lilly
```

- Create a test postgres database if you have not yet

```shell
sudo -su postgres
createdb <test_db_name>
exit
```

- Copy the `.example.env` file to `.env`

```shell
cp .example.env .env
```

- Update the `TEST_DATABASE_URL` to the URL of your test postgres database in the `.env` file
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
python -m unittest
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
existing code.

The `DataSource`s can be found in the `datasources.py` module. Customize them accordingly following the guidance of the
already existing code.

The `Repository`s can be found in the `respositories.py` module. Customize them accordingly following the guidance of
the already existing code.

The `RouteSet`s can be found in the `routes.py` module. Customize them accordingly following the guidance of the already
existing code.

The `DataModel` DTOs can be found in the `dtos.py` module. Customize them accordingly following the guidance of the
already existing code.

### Data Sources

To create a new data source, one needs to subclass the `DataSource` class and override the `connect(self)` method.

```python
from typing import ContextManager
from lilly.datasources import DataSource


class SampleConnectionContextManager:
  def __init__(self, connection):
    self.connection = connection

  def __enter__(self):
    return self.connection

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.connection.close()


class SampleDataSource(DataSource):
  def connect(self) -> ContextManager:
    # do some stuff and return a context manager for a connection
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
from sqlalchemy import Column, Integer, String
from lilly.repositories import Repository
from lilly.datasources import SQLAlchemyDataSource, DataSource
from lilly.conf import settings

Base = declarative_base()


class UserModel(Base):
  """The database model for users"""
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  email = Column(String)


class UsersRepository(Repository):
  """Repository for saving and retrieving users"""
  _users_db = SQLAlchemyDataSource(db_uri=settings.DATABASE_URL, declarative_meta=Base)

  # -- other important methods need to be overridden also. I have excluded them for brevity.

  @property
  def _datasource(self) -> DataSource:
    return self._users_db
```

### Repositories

To create a new repository, one needs to subclass the `Repository` class and override all the following methods:

- `_get_one(self, datasource_connection: Any, record_id: Any, **kwargs) -> Any` method to get one record of
  id `record_id`
- `_get_many(self, datasource_connection: Any, skip: int, limit: int, filters: Dict[Any, Any], **kwargs) -> List[Any]`
  method to get many records that fulfil the `filters`
- `_create_one(self, datasource_connection: Any, record: BaseModel, **kwargs) -> Any` method to create one record
- `_create_many(self, datasource_connection: Any, record: List[BaseModel], **kwargs) -> List[Any]` method to create many
  records
- `_update_one(self, datasource_connection: Any, record_id: Any, new_record: BaseModel, **kwargs) -> Any` method to
  update one record of id `record_id`
- `_update_many(self, datasource_connection: Any, new_record: BaseModel, filters: Dict[Any, Any], **kwargs) -> Any`
  method to update many records that fulfil the `filters`
- `_remove_one(self, datasource_connection: Any, record_id: Any, **kwargs) -> Any` method to remove one record of
  id `record_id`
- `_remove_many(self, datasource_connection: Any, filters: Dict[Any, Any], **kwargs) -> Any` method to remove many
  records that fulfil the `filters`
- `_datasource(self) -> DataSource` an @property-decorated method to return the DataSource whose `connect()` method is
    to be called in any of the other methods to get its instance.
- `_to_output_dto(self, record: Any) -> BaseModel` method which converts any record from the data source raw to DTO
    for the public methods

A good example is how we implemented the `SQLAlchemyRepository`. Feel free to look at it.

To make life easier for the developer, we have created a few off-the-shelf `Repository` subclasses with most of those methods implemented.
They just need to be inherited and a few abstract methods filled with one-liners (or slightly more than one-liners if you wish).

These include:

#### 1. SQLAlchemyRepository

This connects to any relational database e.g. MySQL, PostgreSQL, Sqlite etc. using [SQLAlchemy](https://www.sqlalchemy.org/)
via the `SQLAlchemyDataSource` data source class.

Here is a sample of its usage:

```python
from typing import Type

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeMeta, declarative_base


from lilly.repositories import SQLAlchemyRepository
from lilly.datasources import SQLAlchemyDataSource
from lilly.conf import settings

from .dtos import NameRecordDTO # a subclass of pydantic.BaseModel that is a Data Transfer Object for Name types

Base = declarative_base()


class Name(Base):
    __tablename__ = "names"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)


class NamesRepository(SQLAlchemyRepository):
    """Repository for saving and retrieving random names"""
    _names_db = SQLAlchemyDataSource(declarative_meta=Base, db_uri=settings.DATABASE_URL)

    @property
    def _model_cls(self) -> Type[DeclarativeMeta]:
        return Name

    @property
    def _dto_cls(self) -> Type[BaseModel]:
      return NameRecordDTO

    @property
    def _datasource(self) -> SQLAlchemyDataSource:
      return self._names_db

# The NamesRepository can then be instantiated in the `Actions` subclasses

```

### Actions

To create a new action, one needs to subclass the `Action` class and override the `run()` method.

For instance:

```python
import random
import string

from pydantic import BaseModel

from lilly.actions import Action

from .repositories import NamesRepository  # A Repository for names
from .dto import NameCreationRequestDTO # The Data Transfer Object to used when creating a name


class GenerateRandomName(Action):
  """
  Generates a random string and persists it in the data source
  """
  _vowels = "aeiou"
  _consonants = "".join(set(string.ascii_lowercase) - set("aeiou"))
  _name_repository = NamesRepository()

  def __init__(self, length: int = 7):
    self._length = length

  def run(self) -> BaseModel:
    """Actual method that is run"""
    name = self._generate_random_word()
    return self._name_repository.create_one(NameCreationRequestDTO(title=name))

  def _generate_random_word(self):
    """Generates a random word"""
    word = ""
    for i in range(self._length):
      if i % 2 == 0:
        word += random.choice(self._consonants)
      else:
        word += random.choice(self._vowels)
    return word

# The GenerateRandomName action is then used in a route as self._do(GenerateRandomName, length=9)
```

To make life easier for the developer, we have developed a few Actions that can be inherited and used easily. They
include:

#### 1. CreateOneAction

This is a CRUD action that creates a single item in the repository. Here is a sample of how it is used.

```python
from lilly.actions import CreateOneAction
from lilly.repositories import Repository


# inherit the CreateOneAction and implement its _repository @property method
class CreateOneName(CreateOneAction):
  """Create a single Name record in the repository"""

  @property
  def _repository(self) -> Repository:
    return  # your repository

# then use it in your routes like self._do(CreateOneName, data_dto)
```

#### 2. CreateManyAction

This is a CRUD action that creates multiple items in the repository at one go. Here is a sample of how it is used.

```python
from lilly.actions import CreateManyAction
from lilly.repositories import Repository


# inherit the CreateManyAction and implement its _repository @property method
class CreateManyNames(CreateManyAction):
  @property
  def _repository(self) -> Repository:
    return  # your repository

# then use it in your routes like self._do(CreateManyNames, data_dtos)
```

#### 3. ReadOneAction

This is a CRUD action that reads a single item from the repository. Here is a sample of how it is used.

```python
from lilly.actions import ReadOneAction
from lilly.repositories import Repository


# inherit the ReadOneAction and implement its _repository @property method
class ReadOneName(ReadOneAction):
  @property
  def _repository(self) -> Repository:
    return  # your repository

# then use it in your routes like self._do(ReadOneName, record_id)
```

#### 4. ReadManyAction

This is a CRUD action that reads multiple items in the repository at one go basing on a number of filters and pagination
controls. Here is a sample of how it is used.

```python
from lilly.actions import ReadManyAction
from lilly.repositories import Repository


# inherit the ReadManyAction and implement its _repository @property method
class ReadManyNames(ReadManyAction):
  @property
  def _repository(self) -> Repository:
    return  # your repository

# then use it in your routes like self._do(ReadManyNames, "id > 8 AND title LIKE "%doe", skip=1, limit=10, address="Kampala")
# To read all names that:
#  - have an id greater than 8
#  - and title ending with 'doe'
#  - as well having the address for that name equal to "Kampala"
#  - but skipping the first item in that collection
#  - and returning not more than ten records
```

#### 5. UpdateOneAction

This is a CRUD action that updates a single item in the repository. Here is a sample of how it is used.

```python
from lilly.actions import UpdateOneAction
from lilly.repositories import Repository


# inherit the UpdateOneAction and implement its _repository @property method
class UpdateOneName(UpdateOneAction):
  @property
  def _repository(self) -> Repository:
    return  # your repository

# then use it in your routes like self._do(UpdateOneName, record_id, new_data_dto)
```

#### 6. UpdateManyAction

This is a CRUD action that updates multiple items in the repository at one go basing on a number of filters supplied.
Here is a sample of how it is used.

```python
from lilly.actions import UpdateManyAction
from lilly.repositories import Repository


# inherit the UpdateManyAction and implement its _repository @property method
class UpdateManyNames(UpdateManyAction):
  @property
  def _repository(self) -> Repository:
    return  # your repository

# then use it in your routes like self._do(UpdateManyNames, new_data_dto, "id > 8 AND title LIKE "%doe", address="Kampala")
# To update all names to resemble new_data_dto for all names that:
#  - have an id greater than 8
#  - and title ending with 'doe'
#  - as well having the address for that name equal to "Kampala"
```

#### 7. DeleteOneAction

This is a CRUD action that deletes a single item in the repository. Here is a sample of how it is used.

```python
from lilly.actions import DeleteOneAction
from lilly.repositories import Repository


# inherit the DeleteOneAction and implement its _repository @property method
class DeleteOneName(DeleteOneAction):
  @property
  def _repository(self) -> Repository:
    return  # your repository

# then use it in your routes like self._do(DeleteOneName, record_id)
```

#### 6. UpdateManyAction

This is a CRUD action that deletes multiple items in the repository at one go basing on a number of filters supplied.
Here is a sample of how it is used.

```python
from lilly.actions import DeleteManyAction
from lilly.repositories import Repository


# inherit the DeleteManyAction and implement its _repository @property method
class DeleteManyNames(DeleteManyAction):
  @property
  def _repository(self) -> Repository:
    return  # your repository

# then use it in your routes like self._do(DeleteManyNames, "id > 8 AND title LIKE "%doe", address="Kampala")
# To delete all names that:
#  - have an id greater than 8
#  - and title ending with 'doe'
#  - as well having the address for that name equal to "Kampala"
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
  - `create_one(self, record: BaseModel, **kwargs) -> Any` method to create one record
  - `create_many(self, records: List[BaseModel], **kwargs) -> List[Any]` method to create many records
  - `update_one(self, record_id: Any, new_record: Any, **kwargs) -> Any` method to update one record of id `record_id`
  - `update_many(self, new_record: BaseModel, filters: Dict[Any, Any], **kwargs) -> Any` method to update many records
    that fulfil the `filters`
  - `remove_one(self, record_id: Any, **kwargs) -> Any` method to remove one record of id `record_id`
  - `remove_many(self, filters: Dict[Any, Any], **kwargs) -> Any` method to remove many records that fulfil
    the `filters`
- `Repository` subclasses should also have the following methods overridden:
  - `_get_one(self, datasource_connection: Any, record_id: Any, **kwargs) -> Any` method to get one record of
    id `record_id`
  - `_get_many(self, datasource_connection: Any, skip: int, limit: int, filters: Dict[Any, Any], **kwargs) -> List[Any]`
    method to get many records that fulfil the `filters`
  - `_create_one(self, datasource_connection: Any, record: BaseModel, **kwargs) -> Any` method to create one record
  - `_create_many(self, datasource_connection: Any, record: List[BaseModel], **kwargs) -> List[Any]` method to create
    many records
  - `_update_one(self, datasource_connection: Any, record_id: Any, new_record: BaseModel, **kwargs) -> Any` method to
    update one record of id `record_id`
  - `_update_many(self, datasource_connection: Any, new_record: BaseModel, filters: Dict[Any, Any], **kwargs) -> Any`
    method to update many records that fulfil the `filters`
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
- The `connect()` method of the `DataSource` class should return a `ContextManager` wrapped around the connection itself
  so as to allow for any clean up tasks to be done in the `__exit__()` method of that ContextManager after each
  connection is ready to be dropped. The `__enter__` method of the ContextManager needs to return the actual connection
  object.

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
  - [x] SqlAlchemyRepository (RDBM e.g. PostgreSQL, MySQL etc.)
  - [x] SQLAlchemyRepository hangs when postgres is used (try running tests)
  - [ ] RedisRepository
  - [ ] MemcachedRepository
  - [ ] RESTAPIRepository
  - [ ] GraphQLRepository
  - [ ] RabbitMQRepository
  - [ ] ActiveMQRepository
  - [ ] WebsocketsRepository
  - [ ] KafkaRepository
  - [ ] MongodbRepository
  - [ ] CouchbaseRepository
  - [ ] DiskCacheRepository
- [x] Add some out-of-the-box base actions e.g.
  - [x] CreateOneAction
  - [x] CreateManyAction
  - [x] UpdateOneAction
  - [x] UpdateManyAction
  - [x] ReadOneAction
  - [x] ReadManyAction
  - [x] DeleteOneAction
  - [x] DeleteManyAction
- [ ] Add some out-of-the-box base route sets
  - [ ] CRUDRouteSet
  - [ ] WebsocketRouteSet
  - [ ] GraphQLRoute
- [ ] Add example code in examples folder
  - [ ] Todolist (CRUDRouteSet, SqlAlchemyRepo)
  - [ ] RandomQuotes (WebsocketRouteSet, MongodbRepo) (quotes got from the Bible)
  - [ ] Clock (WebsocketRouteSet, WebsocketsRepo)
- [ ] Set up automatic documentation
- [x] Set up CI via Github actions
- [ ] Set up CD via Github actions
- [ ] Write about it in hashnode or Medium or both

## Inspiration

- The idea to create **lilly** came after looking at what the [Loopback](https://loopback.io/) team did
  with [Loopback4](https://loopback.io/doc/en/lb4)

## ChangeLog

For the changes across versions, look at the [CHANGELOG.md](./CHANGELOG.md)

## License

Copyright (c) 2022 [Martin Ahindura](https://github.com/Tinitto) Licensed under the [MIT License](./LICENSE)
