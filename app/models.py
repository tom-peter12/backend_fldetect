# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.expression import text
# from sqlalchemy.sql.sqltypes import TIMESTAMP

# from .database import Base

# class User(Base):
#     __tablename__ = "users"
#     user_id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, nullable=False, unique=True, index=True)
#     # username = Column(String, unique=True, index=True)
#     password = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True),
#                         nullable=False, server_default=text('now()'))
#     # last_login = Column(TIMESTAMP(timezone=True), nullable=False)

#     # devices = relationship("UserDevice", back_populates="user")

# class Device(Base):
#     __tablename__ = 'devices'

#     device_id = Column(Integer, primary_key=True, index=True)
#     device_name = Column(String)
#     device_type = Column(String)
#     created_at = Column(TIMESTAMP(timezone=True),
#                         nullable=False, server_default=text('now()'))

#     users = relationship("UserDevice", back_populates="device")


# class UserDevice(Base):
#     __tablename__ = 'user_devices'

#     user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
#     device_id = Column(Integer, ForeignKey('devices.device_id'), primary_key=True)
#     is_active = Column(Boolean, default=True)

#     user = relationship("User", back_populates="devices")
#     device = relationship("Device", back_populates="users")


# # class FederatedTask(Base):
# #     __tablename__ = 'federated_tasks'

# #     task_id = Column(Integer, primary_key=True, index=True)
# #     task_name = Column(String)
# #     task_status = Column(String)
# #     created_at = Column(TIMESTAMP(timezone=True),
# #                         nullable=False, server_default=text('now()'))


# # class DeviceTask(Base):
# #     __tablename__ = 'device_tasks'
# #     device_id = Column(Integer, ForeignKey('devices.device_id'), primary_key=True)
# #     task_id = Column(Integer, ForeignKey('federated_tasks.task_id'), primary_key=True)
# #     status = Column(String)
# #     updated_at = Column(TIMESTAMP(timezone=True))


from sqlalchemy import Column, Integer, String, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base 

# class User(Base):
#     __tablename__ = "users"
#     user_id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)

#     # device_id = Column(Integer, primary_key=True, index=True)
#     device_name = Column(String)
#     device_type = Column(String)
#     device_os = Column(Integer)
#     device_mem = Column(String)
#     # created_at = Column(TIMESTAMP(timezone=True),
#     #                     nullable=False, server_default=text('now()'))


from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    device_unique_id = Column(String, nullable=False, unique=True)
    device_name = Column(String)
    device_type = Column(String)
    device_os = Column(Integer)
    device_mem = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    client_weights = Column(JSON, nullable=False)

class The_Model(Base):
    __tablename__ = "the_model"
    id = Column(Integer, primary_key=True, index=True)
    model = Column(JSON, nullable=False)


class Aggregated_Model(Base):
    __tablename__ = "aggregated_weights"
    id = Column(Integer, primary_key=True, index=True)
    aggregated_weight = Column(JSON, nullable=False)

