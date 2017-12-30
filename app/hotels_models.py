# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, text


metadata = MetaData()


t_bookings = Table(
    'bookings', metadata,
    Column('booking_id', Integer, nullable=False, server_default=text("nextval('hotels.bookings_booking_id_seq'::regclass)")),
    Column('client_name', String(254)),
    Column('hotel_name', String(254)),
    Column('arrival', String(254)),
    Column('departure', String(254)),
    Column('datetime', DateTime),
    schema='hotels'
)
