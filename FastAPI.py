from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime
#app = FastAPI()
#engine = create_engine('mysql+pymysql://root:root@localhost:3306/patients')
app = FastAPI()

# Configuração do banco de dados MySQL
engine = create_engine('mysql+pymysql://root:root@localhost:3306/patients', pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos das entidades
class Patient(Base):
    __tablename__ = 'patient'

    PatientID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(255))
    LastName = Column(String(255))
    vaccines = relationship('Vaccine', back_populates='patient')


class Vaccine(Base):
    __tablename__ = 'vaccine'

    VaccineID = Column(Integer, primary_key=True, index=True)
    PatientID = Column(Integer, ForeignKey('patient.PatientID'))
    VaccineName = Column(String(255))
    DoseDate = Column(DateTime)
    DoseNumber = Column(Integer)
    VaccineType = Column(String(255))
    doses = relationship('Dose', back_populates='vaccine')
    patient = relationship('Patient', back_populates='vaccines')


class Dose(Base):
    __tablename__ = 'dose'

    DoseID = Column(Integer, primary_key=True, index=True)
    VaccineID = Column(Integer, ForeignKey('vaccine.VaccineID'))
    TypeDose = Column(String(255))
    DoseDate = Column(DateTime)
    DoseNumber = Column(Integer)
    ApplicationType = Column(String(255))
    vaccine = relationship('Vaccine', back_populates='doses')


Base.metadata.create_all(bind=engine)

def get_patient_with_vaccines(patient_id: int, db: Session):
    patient = db.query(Patient).filter(Patient.PatientID == patient_id).first()
    if patient:
        return patient
    return None


def get_vaccine_with_doses(vaccine_id: int, db: Session):
    vaccine = db.query(Vaccine).filter(Vaccine.VaccineID == vaccine_id).first()
    if vaccine:
        return vaccine
    return None


# Rota
@app.post("/api/Paciente")
def create_patient(name: str, last_name: str):
    db = SessionLocal()
    patient = Patient(Name=name, LastName=last_name)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    db.close()
    return patient


@app.get("/api/Paciente")
def read_patients():
    db = SessionLocal()
    patients = db.query(Patient).all()
    db.close()
    return patients


@app.get("/api/Paciente/{patient_id}")
def read_patient(patient_id: int):
    db = SessionLocal()
    patient = get_patient_with_vaccines(patient_id, db)
    db.close()
    if patient:
        return patient
    raise HTTPException(status_code=404, detail="Paciente não encontrado")


@app.put("/api/Paciente/{patient_id}")
def update_patient(patient_id: int, name: str, last_name: str):
    db = SessionLocal()
    patient = get_patient_with_vaccines(patient_id, db)
    if patient:
        patient.Name = name
        patient.LastName = last_name
        db.commit()
        db.close()
        return patient
    db.close()
    raise HTTPException(status_code=404, detail="Paciente não encontrado")


@app.delete("/api/Paciente/{patient_id}")
def delete_patient(patient_id: int):
    db = SessionLocal()
    patient = get_patient_with_vaccines(patient_id, db)
    if patient:
        db.delete(patient)
        db.commit()
        db.close()
        return JSONResponse(content={"message": "Paciente deletado com sucesso"})
    db.close()
    raise HTTPException(status_code=404, detail="Paciente não encontrado")


@app.post("/api/Vacina")
def create_vaccine(patient_id: int, vaccine_name: str, dose_date: str, dose_number: int, vaccine_type: str):
    db = SessionLocal()
    vaccine = Vaccine(PatientID=patient_id, VaccineName=vaccine_name, DoseDate=dose_date, DoseNumber=dose_number, VaccineType=vaccine_type)
    db.add(vaccine)
    db.commit()
    db.refresh(vaccine)
    db.close()
    return vaccine


@app.get("/api/Vacina")
def read_vaccines():
    db = SessionLocal()
    vaccines = db.query(Vaccine).all()
    db.close()
    return vaccines


@app.get("/api/Vacina/{vaccine_id}")
def read_vaccine(vaccine_id: int):
    db = SessionLocal()
    vaccine = get_vaccine_with_doses(vaccine_id, db)
    db.close()
    if vaccine:
        return vaccine
    raise HTTPException(status_code=404, detail="Vacina não encontrada")


@app.put("/api/Vacina/{vaccine_id}")
def update_vaccine(vaccine_id: int, patient_id: int, vaccine_name: str, dose_date: str, dose_number: int, vaccine_type: str):
    db = SessionLocal()
    vaccine = get_vaccine_with_doses(vaccine_id, db)
    if vaccine:
        vaccine.PatientID = patient_id
        vaccine.VaccineName = vaccine_name
        vaccine.DoseDate = dose_date
        vaccine.DoseNumber = dose_number
        vaccine.VaccineType = vaccine_type
        db.commit()
        db.close()
        return vaccine
    db.close()
    raise HTTPException(status_code=404, detail="Vacina não encontrada")


@app.delete("/api/Vacina/{vaccine_id}")
def delete_vaccine(vaccine_id: int):
    db = SessionLocal()
    vaccine = get_vaccine_with_doses(vaccine_id, db)
    if vaccine:
        db.delete(vaccine)
        db.commit()
        db.close()
        return JSONResponse(content={"message": "Vacina deletada com sucesso"})
    db.close()
    raise HTTPException(status_code=404, detail="Vacina não encontrada")


@app.post("/api/Dose")
def create_dose(vaccine_id: int, type_dose: str, dose_date: str, dose_number: int, application_type: str):
    db = SessionLocal()
    dose = Dose(VaccineID=vaccine_id, TypeDose=type_dose, DoseDate=dose_date, DoseNumber=dose_number, ApplicationType=application_type)
    db.add(dose)
    db.commit()
    db.refresh(dose)
    db.close()
    return dose


@app.get("/api/Dose")
def read_doses():
    db = SessionLocal()
    doses = db.query(Dose).all()
    db.close()
    return doses


@app.get("/api/Dose/{dose_id}")
def read_dose(dose_id: int):
    db = SessionLocal()
    dose = db.query(Dose).filter(Dose.DoseID == dose_id).first()
    db.close()
    if dose:
        return dose
    raise HTTPException(status_code=404, detail="Dose não encontrada")


@app.put("/api/Dose/{dose_id}")
def update_dose(dose_id: int, vaccine_id: int, type_dose: str, dose_date: str, dose_number: int, application_type: str):
    db = SessionLocal()
    dose = db.query(Dose).filter(Dose.DoseID == dose_id).first()
    if dose:
        dose.VaccineID = vaccine_id
        dose.TypeDose = type_dose
        dose.DoseDate = dose_date
        dose.DoseNumber = dose_number
        dose.ApplicationType = application_type
        db.commit()
        db.close()
        return dose
    db.close()
    raise HTTPException(status_code=404, detail="Dose não encontrada")