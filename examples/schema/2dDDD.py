from datetime import datetime
from sqlalchemy import Table, Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///2dDDD.db'
db = SQLAlchemy(app)


class System_Description(db.Model):
    __tablename__ = 'system_description'
    id = Column(db.Integer, primary_key=True)
    info = Column(db.Text)
    n_slip_system = Column(db.Integer)
    relaxation_time = Column(db.Float)
    total_time = Column(db.Float)

    geometry = relationship("Geometry",
                                    uselist=False,
                                    back_populates="system_description")
    material_properties = relationship("Material_Properties",
                                    uselist=False,
                                    back_populates="system_description")
    loading_condition= relationship("Loading_Condition",
                                    uselist=False,
                                    back_populates="system_description")
    slip_system = relationship("Slip_System",
                                    back_populates="system_description")

class Material_Properties(db.Model):
    __tablename__ = 'material_properties'
    id = Column(db.Integer, primary_key=True)
    system_description_id = Column(db.Integer, ForeignKey('system_description.id'))
    burgers_vector = Column(db.Float)
    drag_coefficient = Column(db.Float)
    poisson_ratio = Column(db.Float)
    young_modulus = Column(db.Float)

    system_description = relationship("System_Description", back_populates="material_properties")

class Geometry(db.Model):
    __tablename__ = 'square_geometry'
    id = Column(db.Integer, primary_key=True)
    x0 = Column(db.Float)
    x1 = Column(db.Float)
    y0 = Column(db.Float)
    y1 = Column(db.Float)
    system_description_id = Column(db.Integer, ForeignKey('system_description.id'))

    system_description = relationship("System_Description", back_populates="square_geometry")

class Loading_Condition(db.Model):
    __tablename__ = 'loading_condition'
    id = Column(db.Integer, primary_key=True)
    f_external = Column(db.Float)
    system_description_id = Column(db.Integer, ForeignKey('system_description.id'))

    system_description = relationship("System_Description", back_populates="loading_condition")

class Slip_System(db.Model):
    __tablename__ = 'slip_system'
    id = Column(db.Integer, primary_key=True)
    system_description_id = Column(db.Integer, ForeignKey("system_description.id"))
    n_slip_plane = Column(db.Integer)

    slip_plane = relationship("Slip_Plane", back_populates="slip_system")
    system_description = relationship("System_Description", back_populates="slip_system")

class Slip_Plane(db.Model):
    __tablename__ = 'slip_plane'
    id = Column(db.Integer, primary_key=True)
    slip_system_id = Column(db.Integer, ForeignKey("slip_system.id"))
    angle = Column(db.Float)
    length = Column(db.Float)
    x0 = Column(db.Float)
    y0 = Column(db.Float)

    slip_system = relationship("Slip_System", back_populates="slip_plane")

class Simulation_Single_Step(db.Model):
    __tablename__ = 'simulation_single_step'
    id = Column(db.Integer(), primary_key=True)
    density = Column(db.Numeric)
    plastic_strain = Column(db.Numeric)
    strain = Column(db.Numeric)
    stress = Column(db.Numeric)
    temperature = Column(db.Numeric(12, 2))
    system_description_id = Column(db.Integer(), ForeignKey("system_description.id"))


    system_description = relationship("System_Description",
                              back_populates="simulation_single_step"
                              )

db.create_all()

if __name__ == "__main__":
    app.run()
