# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, text


metadata = MetaData()


t_bookings = Table(
    'bookings', metadata,
    Column('booking_id', Integer, nullable=False, server_default=text("nextval('flights.bookings_booking_id_seq'::regclass)")),
    Column('client_name', String(254)),
    Column('fly_number', String(254)),
    Column('from_', String(254)),
    Column('to_', String(254)),
    Column('datetime', DateTime),
    schema='flights'
)
