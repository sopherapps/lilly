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

- Create a `Lilly` class as a subclass of FastAPI.
  - `Lilly` class should have the following properties set during initialization or else the defaults are applied
    - services_path (an import path as string)
    - settings_path (an import path as string)
  - All routes, actions, repositories and datasources are automatically imported using `importlib.import_module` by concatenating the `services` import path to the respective module e.g. `actions`, `routes` etc.
- in order to make route definition solely dependent on folder structure, we change `@app.get` decorators to `@get`
- `app.get`, `app.post` etc. should throw `NotImplemented` errors (unless this effectively breaks the code. In this case, check the difference between when app.get is used and when router.get is used)
- we will have an attribute in a different module from that where Lilly is defined. It is called `router: APIRouter`. Let the module be called `routing`
- in that same module, there will be functions called `get`, `post`etc) that are just returning router.get, router.post etc.
- When initializing in __init__ of Lilly, we will fetch all services and call `self.include_router(router)`. 
- `router` will be imported dynamically after all the routes in all services are imported.
- `app.mount` should throw an `NotImplemented` error because it will complicate the app structure if used
- Use [CBV](https://fastapi-utils.davidmontague.xyz/user-guide/class-based-views/), but with one with router
as one common router for all services as:
  - we will have an attribute in a different module from that where Lilly is defined. It is called `router: APIRouter`. Let the module be called `routing`
  - `@cbv(router)` will be wrapped to become `@routeset`
  - The `class based views` themselves will be subclasses of `RouteSet`
  - The `RouteSet` class will have a protected method `_do(self, action_cls: Action, *args, **kwargs)` to make a call to any action
  - The `@router.post` or `@router.get` etc. on the class based views methods will all be aliased to their `post`, `get` etc counterparts

## ToDo

- [x] Set up the abstract methods structure
- [x] Set up the CLI to generate an app
- [x] Set up the CLI to generate a service
- [x] Make repository public
- [x] Package it and publish it
- [ ] Add some out-of-the-box base data sources e.g.
  - [ ] SqlAlchemy
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
