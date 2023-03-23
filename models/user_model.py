from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean,Float,Text
from sqlalchemy import func
from db.config import Base



class PhoneModel(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey('rolls.id',),nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)


class WorkersModel(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True)
    roll_id = Column(Integer, ForeignKey('rolls.id',), nullable=False)
    name = Column(String, nullable=False)
    phone_id = Column(Integer,ForeignKey('phones.id',),nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    token = Column(String, unique=True, nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)


class TitleModel(Base):
    __tablename__ = "rolls"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)


class PartnerModel(Base):
    __tablename__ = "partners"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    balance = Column(Integer,nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    phone_id = Column(Integer, ForeignKey('phones.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('workers.id', ondelete="CASCADE"), nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)

class TaminotModel(Base):
    __tablename__ = "taminot"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer,nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey('workers.id', ondelete="CASCADE"), nullable=False)
    partner_id = Column(Integer, ForeignKey('partners.id', ondelete="CASCADE"), nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)


class StoreModel(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    long = Column(Float, nullable=False)
    lat = Column(Float,nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey('workers.id', ondelete="CASCADE"), nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)

class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer,nullable=False)
    trade_price = Column(Integer,nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey('workers.id', ondelete="CASCADE"), nullable=False)
    partner_id = Column(Integer, ForeignKey('partners.id', ondelete="CASCADE"), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id', ondelete="CASCADE"), nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)


class CustomerModel(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    roll_id = Column(Integer, ForeignKey('rolls.id', ondelete="CASCADE"), nullable=False)
    phone_id = Column(Integer, ForeignKey('phones.id', ondelete="CASCADE"), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id', ondelete="CASCADE"), nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete="CASCADE"), nullable=False)
    phone_id = Column(Integer, ForeignKey('phones.id', ondelete="CASCADE"), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id', ondelete="CASCADE"), nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)

class SaleModel(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete="CASCADE"), nullable=False)
    phone_id = Column(Integer, ForeignKey('phones.id', ondelete="CASCADE"), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id', ondelete="CASCADE"), nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)


class ProfitModel(Base):
    __tablename__ = "profits"
    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('workers.id', ondelete="CASCADE"), nullable=False)
    comment = Column(Text,nullable=True)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)

class ExpenseModel(Base):
    __tablename__ = "expense"
    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('workers.id', ondelete="CASCADE"), nullable=False)
    comment = Column(Text,nullable=True)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)


