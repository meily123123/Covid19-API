from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from model import *
app = FastAPI()


def get_data():
    try:
        all_data = SessionLocal()
        yield all_data
    finally:
        all_data.close()


@app.get("/")
async def covid_overview_datapage(all_data: Session = Depends(get_data)):
    covid_terbaru = all_data.query(Covid).all()[-1]
    covid_overview = {
        "ok": True,
        "data": {
            "total_positive": covid_terbaru.sum_positif,
            "total_recovered": covid_terbaru.sum_sembuh,
            "total_deaths": covid_terbaru.sum_meninggal,
            "total_active": covid_terbaru.sum_dirawat,
            "new_positive": covid_terbaru.positif,
            "new_recovered": covid_terbaru.sembuh,
            "new_deaths": covid_terbaru.meninggal,
            "new_active": covid_terbaru.dirawat,
        },
        "massage": "Berhasil"
    }
    return covid_overview


@app.get("/yearly/{year}")
async def yearly_datapage(year: str, all_data: Session = Depends(get_data)):
    covid_tahunan = all_data.query(Covid).filter(Covid.date.contains(f"{year}")).all()
    if len(covid_tahunan) == 0:
        covid_tahun = {
            "ok": False,
            "massage": "Invalid"
        }
        return covid_tahun
    covid_tahun = {
        "ok": True,
        "data": {
            "year": year,
            "new_positive": covid_tahunan[-1].sum_positif,
            "new_recovered": covid_tahunan[-1].sum_sembuh,
            "new_deaths": covid_tahunan[-1].sum_meninggal,
            "new_active": covid_tahunan[-1].sum_dirawat,
        },
        "massage": "Berhasil"
    }
    return covid_tahun


@app.get("/monthly/{year}/{month}")
async def monthly_datapage(year: str, month: str, all_data: Session = Depends(get_data)):
    covid_bulanan = all_data.query(Covid).filter(Covid.date.contains(f"{year}-{month}")).all()
    if len(covid_bulanan) == 0:
        covid_bulan = {
            "ok": False,
            "massage": "Invalid"
        }
        return covid_bulan
    covid_bulan = {
        "ok": True,
        "data": {
            "month": f"{year}-{month}",
            "new_positive": covid_bulanan[-1].sum_positif,
            "new_recovered": covid_bulanan[-1].sum_sembuh,
            "new_deaths": covid_bulanan[-1].sum_meninggal,
            "new_active": covid_bulanan[-1].sum_dirawat,
        },
        "massage": "Berhasil"
    }
    return covid_bulan


@app.get("/daily/{year}/{month}/{tanggal}")
async def say_hello(year: str, month: str, tanggal: str, all_data: Session = Depends(get_data)):
    covid_harian = all_data.query(Covid).filter(Covid.date.contains(f"{year}-{month}-{tanggal}")).all()
    if len(covid_harian) == 0:
        covid_hari = {
            "ok": False,
            "massage": "Invalid"
        }
        return covid_hari
    covid_hari = {
        "ok": True,
        "data": {
            "date": covid_harian[-1].date,
            "new_positive": covid_harian[-1].positif,
            "new_recovered": covid_harian[-1].sembuh,
            "new_deaths": covid_harian[-1].meninggal,
            "new_active": covid_harian[-1].dirawat,
        },
        "massage": "Berhasil"
    }
    return covid_hari
