
Based on the project on-api we are gonna try to create a new api module
please visit those pages to get more details about the arcitechture:
    - https://fastapi.tiangolo.com/tutorial/bigger-applications/
    - https://github.com/ycd/manage-fastapi
    
this is a good practices for structuring a FastAPI project

your_project
├── __init__.py
├── main.py
├── core
│   ├── models
│   │   ├── database.py
│   │   └── __init__.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── schema.py
│   └── settings.py
├── tests
│   ├── __init__.py
│   └── v1
│       ├── __init__.py
│       └── test_v1.py
└── v1
    ├── api.py
    ├── endpoints
    │   ├── endpoint.py
    │   └── __init__.py
    └── __init__.py 
By using __init__ everywhere, we can access the variables from the all over the app, just like Django.

Let's the folders into parts:

Core
models
database.py
schemas
users.py
something.py
settings.py
tests
v1
v2
Models
It is for your database models, by doing this you can import the same database session or object from v1 and v2.

Schemas
Schemas are your Pydantic models, we call it schemas because it is actually used for creating OpenAPI schemas since FastAPI is based on OpenAPI specification we use schemas everywhere, from Swagger generation to endpoint's expected request body.

settings.py
It is for Pydantic's Settings Management which is extremely useful, you can use the same variables without redeclaring it, to see how it could be useful for you check out our documentation for Settings and Environment Variables

Tests
It is good to have your tests inside your backend folder.

APIs
Create them independently by APIRouter, instead of gathering all your APIs inside one file.

## Notes
You can use absolute import for all your importing since we are using __init__ everywhere, see Python's packaging docs.

So assume you are trying to import v1's endpoint.py from v2, you can simply do

from my_project.v1.endpoints.endpoint import something

## IPFS
we should eventually consider migrating to our own hosted node as down trafic could increase our costs 
https://medium.com/ethereum-developers/how-to-host-your-ipfs-files-online-forever-f0c56b9b5398

to access files on the local test node: http://localhost:8080/ipfs/<HASH>

to run a local node of ipfs (needed to run the tests) follow the following tutorial:
https://medium.com/python-pandemonium/getting-started-with-python-and-ipfs-94d14fdffd10

## Troubleshooting

### Environment installation

#### error with crypto
if you have the following error

`cannot import name 'scrypt' from 'Crypto.Protocol.KDF'`

in your poetry shell do the following

```
pip uninstall pycrypto
pip uninstall pycryptodome
pip install pycryptodome
```

#### error with ipfs deamon version

if you have the following error

`ipfshttpclient.exceptions.VersionMismatch: Unsupported daemon version '0.12.1' (not in range: 0.5.0 ≤ … < 0.9.0)`

open this file in an editor: 

`.venv/lib/python3.9/site-packages/ipfshttpclient/client/__init__.py`

then modify the max supported version in line 24 to

`VERSION_MAXIMUM   = "0.13.0"`

## Modifying the Database structure

While SQLAlchemy directly supports emitting CREATE and DROP statements for schema constructs, the ability to alter those constructs, usually via the ALTER statement as well as other database-specific constructs, is outside of the scope of SQLAlchemy itself.

The SQLAlchemy project offers the Alembic migration tool for this purpose. Alembic features a highly customizable environment and a minimalistic usage pattern, supporting such features as transactional DDL, automatic generation of “candidate” migrations, an “offline” mode which generates SQL scripts, and support for branch resolution.

By modifying the DB structure in the metadata of the declarative_base, it is possible to ask Alembic to detect automatically the changes using the following command:

```
$ alembic revision --autogenerate -m "My message"`
```

This will create a new revision file inside the alembic/version folder which will contain some header information, identifiers for the current revision, `upgrade`, and a `downgrade` revision in case you need to revert the changes. Both revision needs to be carefully checked so that the automatically detected modifications are the desired ones. The migration hasn’t actually run yet, of course. This is done by running

```
$ alembic upgrade head
```

Alembic details that all of the following changes are detected properly by the Autogenerate command:

* Table additions, removals.
* Column additions, removals.
* Change of nullable status on columns.
* Basic changes in indexes and explicitly-named unique constraints
* Basic changes in foreign key constraints

For other changes, please refer to https://alembic.sqlalchemy.org/en/latest/autogenerate.html to see in which case it can be detected and used.

A more detailed explanation can be found here https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script and usueful alembic commands at https://alembic.sqlalchemy.org/en/latest/api/commands.html

