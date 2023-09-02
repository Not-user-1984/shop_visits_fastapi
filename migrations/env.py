import os
import sys

sys.path.append(os.path.join(sys.path[0], 'src'))
from db.database import Base, get_async_session
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from src.db.models import *
from src.config import settings


config = context.config
section = config.config_ini_section
config.set_section_option(section, "DATABASE_URL", settings.DATABASE_URL)

config.set_main_option('sqlalchemy.url', str(settings.DATABASE_URL))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def create_context():
    return {
        'metadata': target_metadata,
        'session': get_async_session(),
        'alembic_version': context.get_context().version
    }


def run_migrations_offline():
    context.configure(
        url=str(settings.DATABASE_URL),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        user_module_prefix='src.auth.models',
        include_schemas=True
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)
    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        user_module_prefix='scr.auth.models',
        include_schemas=True
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


fileConfig(config.config_file_name)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
