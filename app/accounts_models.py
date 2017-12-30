# coding: utf-8
from sqlalchemy import Column, Integer, MetaData, String, Table, text


metadata = MetaData()


t_user_account = Table(
    'user_account', metadata,
    Column('id', Integer, nullable=False, server_default=text("nextval('accounts.user_account_id_seq'::regclass)")),
    Column('name', String(254)),
    Column('amount', Integer),
    schema='accounts'
)
