from sqlalchemy import Column, String, BigInteger
from database_generate import *


class Covid(Base):
    __tablename__ = "covid_harian_tb"
    date = Column(String, primary_key=True)
    meninggal = Column(BigInteger)
    sembuh = Column(BigInteger)
    positif = Column(BigInteger)
    dirawat = Column(BigInteger)
    sum_meninggal = Column(BigInteger)
    sum_sembuh = Column(BigInteger)
    sum_positif = Column(BigInteger)
    sum_dirawat = Column(BigInteger)


Base.metadata.create_all(bind=engine)
