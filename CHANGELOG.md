# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.2.0] - 2022-05-06

### Added

- `CreateOneAction` for creating a single item in the respective repository
- `CreateManyAction` for creating multiple item in the respective repository
- `UpdateOneAction` for updating a single item from the respective repository
- `UpdateManyAction` for updating multiple item in the respective repository
- `DeleteOneAction` for deleting a single item from the respective repository
- `DeleteManyAction` for deleting multiple items from the respective repository
- `ReadOneAction` for reading a single item from the respective repository
- `ReadManyAction` for reading many items from the respective repository
- `create_name` route to the stub
- `create_many_name` route to the stub
- `update_name` route to the stub
- `update_many_names` route to the stub
- `update_name_partially` route to the stub
- `read_many_names` route to the stub
- `read_name` route to the stub
- `delete_many_names` route to the stub
- `delete_name` route to the stub

### Changed

- The type of the `record`/`new_record` parameter in all repository major methods that need it has changed from `Any`
  to `BaseModel`.
- The type of the `record`/`new_record` parameter in all action major methods that need it has changed from `Any`
  to `BaseModel`.

### Fixed

- Filtering using text SQL in sqlalchemy was fixed by initially coercing them using `text(string_sql)` and then ensuring
  `update` and `delete` statements use `execution_options.synchronize_session="fetch"`

## [0.1.0] - 2022-05-06

### Added

- `SQLAlchemyRepository` which is a repository that can inherited to make repositories that connect to sqlalchemy
- `example.env` file for setting some environment variables like `TEST_DATABASE_URL` for running tests

### Changed

- The `NamesRepository` class in the sample service is now a subclass of `SQLAlchemyRepository`
- Output type of `DataSource.connect()` to be a `ContextManager`
- Section of "How to Run tests" on README.md now includes copying the `.example.env` file
- The `ci.yml` file in `.github/workflows` folder got a test postgreSQL service for running postgreSQL-related tests

### Fixed

- Hanging of the app when a database other than sqlite was used in tests for `SQLAlchemyRepository`

## [0.0.4] - 2022-04-27

### Added

- `SQLAlchemyDataSource` which is a `DataSource` child class that can be used out-of-the-box to connect to RDBMs via
  sqlalchemy

### Changed

- The `NamesDb` class in the sample service is now a subclass of `SQLAlchemyDataSource`

### Fixed
