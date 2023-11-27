from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import datetime

app = FastAPI()

# Configuração do banco de dados PostgreSQL
engine = create_engine('mysql+pymysql://root:root@localhost:3306/patients', pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos de entidades
class Patient(Base):
    __tablename__ = 'Patient'

    patient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)


class Vaccine(Base):
    __tablename__ = 'Vaccine'

    vaccine_id = Column(Integer, primary_key=True, index=True)
    vaccine_name = Column(String)
    dose_date = Column(DateTime)
    dose_number = Column(Integer)
    vaccine_type = Column(String)
    patient_id = Column(Integer, ForeignKey('Patient.patient_id', ondelete='CASCADE'))


class Dose(Base):
    __tablename__ = 'Dose'

    dose_id = Column(Integer, primary_key=True, index=True)
    type_dose = Column(String)
    dose_date = Column(DateTime)
    dose_number = Column(Integer)
    application_type = Column(String)
    vaccine_id = Column(Integer, ForeignKey('Vaccine.vaccine_id', ondelete='CASCADE'))


Base.metadata.create_all(bind=engine)

# Rotas para Pacientes
@app.post("/patients")
def create_patient(name: str, last_name: str):
    patient = Patient(name=name, last_name=last_name)
    session.add(patient)
    session.commit()
    return JSONResponse(content={'id': patient.patient_id, 'name': patient.name, 'last_name': patient.last_name})

@app.get("/patients")
def get_patients():
    patients = session.query(Patient).all()
    patients_list = [{'id': patient.patient_id, 'name': patient.name, 'last_name': patient.last_name} for patient in patients]
    return JSONResponse(content=patients_list)

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
    return JSONResponse(content={'id': patient.patient_id, 'name': patient.name, 'last_name': patient.last_name})

@app.put("/patients")
def update_patient(patient_id: int, name: str, last_name: str):
    patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
    patient.name = name
    patient.last_name = last_name
    session.commit()
    return JSONResponse(content={'id': patient.patient_id, 'name': patient.name, 'last_name': patient.last_name})

@app.delete("/patients")
def delete_patient(patient_id: int):
    patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
    session.delete(patient)
    session.commit()
    return JSONResponse(content={'message': 'Paciente deletado'})


# Rotas para Vacinas
@app.post("/vaccines")
def create_vaccine(vaccine_name: str, dose_number: int, vaccine_type: str, patient_id: int):
    vaccine = Vaccine(vaccine_name=vaccine_name, dose_date=datetime.datetime.now(), dose_number=dose_number, vaccine_type=vaccine_type, patient_id=patient_id)
    session.add(vaccine)
    session.commit()
    return JSONResponse(content={'id': vaccine.vaccine_id, 'name': vaccine.vaccine_name, 'dose_date': str(vaccine.dose_date), 'dose_number': vaccine.dose_number, 'vaccine_type': vaccine.vaccine_type, 'patient_id': vaccine.patient_id})

@app.get("/vaccines")
def get_vaccines():
    vaccines = session.query(Vaccine).all()
    vaccines_list = [{'id': vaccine.vaccine_id, 'name': vaccine.vaccine_name, 'dose_date': str(vaccine.dose_date), 'dose_number': vaccine.dose_number, 'vaccine_type': vaccine.vaccine_type, 'patient_id': vaccine.patient_id} for vaccine in vaccines]
    return JSONResponse(content=vaccines_list)

@app.get("/vaccines/{vaccine_id}")
def get_vaccine(vaccine_id: int):
    vaccine = session.query(Vaccine).filter(Vaccine.vaccine_id == vaccine_id).first()
    return JSONResponse(content={'id': vaccine.vaccine_id, 'name': vaccine.vaccine_name, 'dose_date': str(vaccine.dose_date), 'dose_number': vaccine.dose_number, 'vaccine_type': vaccine.vaccine_type, 'patient_id': vaccine.patient_id})

@app.put("/vaccines")
def update_vaccine(vaccine_id: int, vaccine_name: str, dose_number: int, vaccine_type: str, patient_id: int):
    vaccine = session.query(Vaccine).filter(Vaccine.vaccine_id == vaccine_id).first()
    vaccine.vaccine_name = vaccine_name
    vaccine.dose_number = dose_number
    vaccine.vaccine_type = vaccine_type
    vaccine.patient_id = patient_id
    session.commit()
    return JSONResponse(content={'id': vaccine.vaccine_id, 'name': vaccine.vaccine_name, 'dose_date': str(vaccine.dose_date), 'dose_number': vaccine.dose_number, 'vaccine_type': vaccine.vaccine_type, 'patient_id': vaccine.patient_id})

@app.delete("/vaccines")
def delete_vaccine(vaccine_id: int):
    vaccine = session.query(Vaccine).filter(Vaccine.vaccine_id == vaccine_id).first()
    session.delete(vaccine)
    session.commit()
    return JSONResponse(content={'message': 'Vacina deletada'})


# Rotas para Doses
@app.post("/doses")
def create_dose(type_dose: str, dose_number: int, application_type: str, vaccine_id: int):
    dose = Dose(type_dose=type_dose, dose_date=datetime.datetime.now(), dose_number=dose_number, application_type=application_type, vaccine_id=vaccine_id)
    session.add(dose)
    session.commit()
    return JSONResponse(content={'id': dose.dose_id, 'type_dose': dose.type_dose, 'dose_date': str(dose.dose_date), 'dose_number': dose.dose_number, 'application_type': dose.application_type, 'vaccine_id': dose.vaccine_id})

@app.get("/doses")
def get_doses():
    doses = session.query(Dose).all()
    doses_list = [{'id': dose.dose_id, 'type_dose': dose.type_dose, 'dose_date': str(dose.dose_date), 'dose_number': dose.dose_number, 'application_type': dose.application_type, 'vaccine_id': dose.vaccine_id} for dose in doses]
    return JSONResponse(content=doses_list)

@app.get("/doses/{dose_id}")
def get_dose(dose_id: int):
    dose = session.query(Dose).filter(Dose.dose_id == dose_id).first()
    return JSONResponse(content={'id': dose.dose_id, 'type_dose': dose.type_dose, 'dose_date': str(dose.dose_date), 'dose_number': dose.dose_number, 'application_type': dose.application_type, 'vaccine_id': dose.vaccine_id})

@app.put("/doses")
def update_dose(dose_id: int, type_dose: str, dose_number: int, application_type: str, vaccine_id: int):
    dose = session.query(Dose).filter(Dose.dose_id == dose_id).first()
    dose.type_dose = type_dose
    dose.dose_number = dose_number
    dose.application_type = application_type
    dose.vaccine_id = vaccine_id
    session.commit()
    return JSONResponse(content={'id': dose.dose_id, 'type_dose': dose.type_dose, 'dose_date': str(dose.dose_date), 'dose_number': dose.dose_number, 'application_type': dose.application_type, 'vaccine_id': dose.vaccine_id})

@app.delete("/doses")
def delete_dose(dose_id: int):
    dose = session.query(Dose).filter(Dose.dose_id == dose_id).first()
    session.delete(dose)
    session.commit()
    return JSONResponse(content={'message': 'Dose deletada'})


# Rota para Pacientes, Vacinas e Doses
@app.get("/pacientsAndVaccinesAndDoses/{patient_id}")
def get_pacientsAndVaccinesAndDoses(patient_id: int):
    patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()
    vaccines = session.query(Vaccine).filter(Vaccine.patient_id == patient.patient_id).all()
    vaccines_list = []

    for vaccine in vaccines:
        doses = session.query(Dose).filter(Dose.vaccine_id == vaccine.vaccine_id).all()
        doses_list = []

        for dose in doses:
            doses_list.append({'id': dose.dose_id, 'type_dose': dose.type_dose, 'dose_date': str(dose.dose_date), 'dose_number': dose.dose_number, 'application_type': dose.application_type, 'vaccine_id': dose.vaccine_id})

        vaccines_list.append({'id': vaccine.vaccine_id, 'name': vaccine.vaccine_name, 'dose_date': str(vaccine.dose_date), 'dose_number': vaccine.dose_number, 'vaccine_type': vaccine.vaccine_type, 'patient_id': vaccine.patient_id, 'doses': doses_list})

    return JSONResponse(content={'id': patient.patient_id, 'name': patient.name, 'last_name': patient.last_name, 'vaccines': vaccines_list})

@app.get("/vaccinesAndDoses/{vaccine_id}")
def get_vaccinesAndDoses(vaccine_id: int):
    vaccine = session.query(Vaccine).filter(Vaccine.vaccine_id == vaccine_id).first()
    doses = session.query(Dose).filter(Dose.vaccine_id == vaccine.vaccine_id).all()
    doses_list = []

    for dose in doses:
        doses_list.append({'id': dose.dose_id, 'type_dose': dose.type_dose, 'dose_date': str(dose.dose_date), 'dose_number': dose.dose_number, 'application_type': dose.application_type, 'vaccine_id': dose.vaccine_id})

    return JSONResponse(content={'id': vaccine.vaccine_id, 'name': vaccine.vaccine_name, 'dose_date': str(vaccine.dose_date), 'dose_number': vaccine.dose_number, 'vaccine_type': vaccine.vaccine_type, 'patient_id': vaccine.patient_id, 'doses': doses_list})
