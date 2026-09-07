from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


app = FastAPI(
    title="Railway Station Management System",
    description="Информационная система железнодорожной станции",
    version="1.0.0",
)

DATABASE_URL = "sqlite:///railway_station.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
)

Base = declarative_base()

def is_empty(value):
    return value is None or (isinstance(value, str) and not value.strip())
class Station(Base):
    __tablename__ = "stations"

    id = Column(
        Integer,
        primary_key=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    city = Column(
        String,
        nullable=False,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
        }

class Train(Base):
    __tablename__ = "trains"

    id = Column(
        Integer,
        primary_key=True,
    )

    number = Column(
        String,
        nullable=False,
    )

    departure_station = Column(
        String,
        nullable=False,
    )

    arrival_station = Column(
        String,
        nullable=False,
    )

    price = Column(
        Float,
        nullable=False,
    )

    schedules = relationship(
        "Schedule",
        back_populates="train",
    )

    tickets = relationship(
        "Ticket",
        back_populates="train",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "departure_station": self.departure_station,
            "arrival_station": self.arrival_station,
            "price": self.price,
        }
        
class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(
        Integer,
        primary_key=True,
    )

    full_name = Column(
        String,
        nullable=False,
    )

    passport = Column(
        String,
        nullable=False,
    )

    tickets = relationship(
        "Ticket",
        back_populates="passenger",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "passport": self.passport,
        }
        
class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(
        Integer,
        primary_key=True,
    )

    train_id = Column(
        Integer,
        ForeignKey("trains.id"),
    )

    departure_time = Column(
        String,
        nullable=False,
    )

    arrival_time = Column(
        String,
        nullable=False,
    )

    trip_date = Column(
        String,
        nullable=False,
    )

    train = relationship(
        "Train",
        back_populates="schedules",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "train_id": self.train_id,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "trip_date": self.trip_date,
        }
        
class Ticket(Base):
    __tablename__ = "tickets"

    __table_args__ = (
        UniqueConstraint("train_id", "seat_number", name="unique_train_seat"),
    )

    id = Column(
        Integer,
        primary_key=True,
    )

    passenger_id = Column(
        Integer,
        ForeignKey("passengers.id"),
    )

    train_id = Column(
        Integer,
        ForeignKey("trains.id"),
    )

    seat_number = Column(
        String,
        nullable=False,
    )

    purchase_date = Column(
        DateTime,
        default=datetime.utcnow,
    )

    passenger = relationship(
        "Passenger",
        back_populates="tickets",
    )

    train = relationship(
        "Train",
        back_populates="tickets",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "passenger_id": self.passenger_id,
            "train_id": self.train_id,
            "seat_number": self.seat_number,
            "purchase_date": str(self.purchase_date),
        }
        
Base.metadata.create_all(
    bind=engine,
)

@app.get("/api/stations")
def get_stations():
    session = SessionLocal()

    stations = session.query(
        Station
    ).all()

    result = [
        station.to_dict()
        for station in stations
    ]

    session.close()

    return result


@app.post("/api/stations")
def add_station(
    name: str,
    city: str,
):
    if is_empty(name) or is_empty(city):
        return {"message": "Все поля должны быть заполнены"}

    session = SessionLocal()

    station = Station(
        name=name.strip(),
        city=city.strip(),
    )

    session.add(station)

    session.commit()

    session.close()

    return {
        "message": "Station added"
    }


@app.delete("/api/stations/{station_id}")
def delete_station(
    station_id: int,
):
    session = SessionLocal()

    station = session.query(
        Station
    ).filter(
        Station.id == station_id
    ).first()

    if not station:
        session.close()

        return {
            "message": "Station not found"
        }

    session.delete(station)

    session.commit()

    session.close()

    return {
        "message": "Station deleted"
    }
    
@app.get("/api/trains")
def get_trains():
    session = SessionLocal()

    trains = session.query(
        Train
    ).all()

    result = [
        train.to_dict()
        for train in trains
    ]

    session.close()

    return result


@app.post("/api/trains")
def add_train(
    number: str,
    departure_station: str,
    arrival_station: str,
    price: float,
):
    if (is_empty(number) or is_empty(departure_station) or
            is_empty(arrival_station) or price is None or price <= 0):
        return {"message": "Все поля должны быть заполнены корректно"}

    session = SessionLocal()

    train = Train(
        number=number.strip(),
        departure_station=departure_station.strip(),
        arrival_station=arrival_station.strip(),
        price=price,
    )

    session.add(train)

    session.commit()

    session.close()

    return {
        "message": "Train added"
    }


@app.delete("/api/trains/{train_id}")
def delete_train(
    train_id: int,
):
    session = SessionLocal()

    train = session.query(
        Train
    ).filter(
        Train.id == train_id
    ).first()

    if not train:
        session.close()

        return {
            "message": "Train not found"
        }

    session.delete(train)

    session.commit()

    session.close()

    return {
        "message": "Train deleted"
    }
    
@app.get("/api/passengers")
def get_passengers():
    session = SessionLocal()

    passengers = session.query(
        Passenger
    ).all()

    result = [
        passenger.to_dict()
        for passenger in passengers
    ]

    session.close()

    return result


@app.post("/api/passengers")
def add_passenger(
    full_name: str,
    passport: str,
):
    if is_empty(full_name) or is_empty(passport):
        return {"message": "Все поля должны быть заполнены"}

    session = SessionLocal()

    passenger = Passenger(
        full_name=full_name.strip(),
        passport=passport.strip(),
    )

    session.add(passenger)

    session.commit()

    session.close()

    return {
        "message": "Passenger added"
    }


@app.delete("/api/passengers/{passenger_id}")
def delete_passenger(
    passenger_id: int,
):
    session = SessionLocal()

    passenger = session.query(
        Passenger
    ).filter(
        Passenger.id == passenger_id
    ).first()

    if not passenger:
        session.close()

        return {
            "message": "Passenger not found"
        }

    session.delete(passenger)

    session.commit()

    session.close()

    return {
        "message": "Passenger deleted"
    }
    
@app.get("/api/schedules")
def get_schedules():
    session = SessionLocal()

    schedules = session.query(
        Schedule
    ).all()

    result = [
        schedule.to_dict()
        for schedule in schedules
    ]

    session.close()

    return result


@app.post("/api/schedules")
def add_schedule(
    train_id: int,
    departure_time: str,
    arrival_time: str,
    trip_date: str,
):
    if is_empty(departure_time) or is_empty(arrival_time) or is_empty(trip_date):
        return {"message": "Все поля должны быть заполнены"}

    session = SessionLocal()

    schedule = Schedule(
        train_id=train_id,
        departure_time=departure_time,
        arrival_time=arrival_time,
        trip_date=trip_date,
    )

    session.add(schedule)

    session.commit()

    session.close()

    return {
        "message": "Schedule added"
    }


@app.delete("/api/schedules/{schedule_id}")
def delete_schedule(
    schedule_id: int,
):
    session = SessionLocal()

    schedule = session.query(
        Schedule
    ).filter(
        Schedule.id == schedule_id
    ).first()

    if not schedule:
        session.close()

        return {
            "message": "Schedule not found"
        }

    session.delete(schedule)

    session.commit()

    session.close()

    return {
        "message": "Schedule deleted"
    }
    
@app.get("/api/tickets")
def get_tickets():
    session = SessionLocal()

    tickets = session.query(
        Ticket
    ).all()

    result = [
        ticket.to_dict()
        for ticket in tickets
    ]

    session.close()

    return result


@app.post("/api/tickets")
def buy_ticket(
    passenger_id: int,
    train_id: int,
    seat_number: str,
):
    if is_empty(seat_number):
        return {"message": "Все поля должны быть заполнены"}

    session = SessionLocal()

    occupied_seat = session.query(Ticket).filter(
        Ticket.train_id == train_id,
        Ticket.seat_number == seat_number.strip()
    ).first()

    if occupied_seat:
        session.close()
        return {"message": "Место занято"}

    ticket = Ticket(
        passenger_id=passenger_id,
        train_id=train_id,
        seat_number=seat_number.strip(),
    )

    session.add(ticket)

    session.commit()

    session.close()

    return {
        "message": "Ticket purchased"
    }


@app.delete("/api/tickets/{ticket_id}")
def delete_ticket(
    ticket_id: int,
):
    session = SessionLocal()

    ticket = session.query(
        Ticket
    ).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        session.close()

        return {
            "message": "Ticket not found"
        }

    session.delete(ticket)

    session.commit()

    session.close()

    return {
        "message": "Ticket deleted"
    }
    
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>
🚆 Railway Station Management System
</title>

<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
rel="stylesheet"
>

<style>

body{
    background:linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
    min-height:100vh;
    color:white;
}

.navbar{
    background:#020617;
}

.card{
    border:none;
    border-radius:20px;
    box-shadow:0 10px 30px rgba(0,0,0,.3);
}

.section{
    display:none;
}

.section.active{
    display:block;
}

.table{
    color:black;
}

.stat-card{
    transition:.3s;
}

.stat-card:hover{
    transform:translateY(-5px);
}

.btn-menu{
    width:100%;
    margin-bottom:10px;
}

.sidebar{
    min-height:85vh;
}

</style>

</head>

<body>

<nav class="navbar navbar-dark">
<div class="container-fluid">

<span class="navbar-brand mb-0 h1">
🚆 Railway Station Management System
</span>

</div>
</nav>

<div class="container-fluid mt-4">

<div class="row">

<div class="col-md-3">

<div class="card sidebar">

<div class="card-body">

<h4 class="text-dark">
Меню
</h4>

<button
class="btn btn-primary btn-menu"
onclick="showSection('dashboard')"
>
📊 Обзор
</button>

<button
class="btn btn-success btn-menu"
onclick="showSection('stations')"
>
🚉 Станции
</button>

<button
class="btn btn-info btn-menu"
onclick="showSection('trains')"
>
🚄 Поезда
</button>

<button
class="btn btn-warning btn-menu"
onclick="showSection('passengers')"
>
👤 Пассажиры
</button>

<button
class="btn btn-secondary btn-menu"
onclick="showSection('schedules')"
>
📅 Расписание
</button>

<button
class="btn btn-danger btn-menu"
onclick="showSection('tickets')"
>
🎫 Билеты
</button>

</div>

</div>

</div>

<div class="col-md-9">

<div
id="dashboard"
class="section active"
>

<h2 class="mb-4">
📊 Обзор системы
</h2>

<div class="row">

<div class="col-md-4">

<div class="card stat-card">

<div class="card-body text-center">

<h1 id="stations-count">
0
</h1>

<h5>
Станций
</h5>

</div>

</div>

</div>

<div class="col-md-4">

<div class="card stat-card">

<div class="card-body text-center">

<h1 id="trains-count">
0
</h1>

<h5>
Поездов
</h5>

</div>

</div>

</div>

<div class="col-md-4">

<div class="card stat-card">

<div class="card-body text-center">

<h1 id="tickets-count">
0
</h1>

<h5>
Билетов
</h5>

</div>

</div>

</div>

</div>

</div>

<div
id="stations"
class="section"
>

<div class="card">

<div class="card-body">

<h3>
🚉 Станции
</h3>

<div class="row">

<div class="col-md-5">

<input
id="station-name"
class="form-control mb-2"
placeholder="Название станции"
>

<input
id="station-city"
class="form-control mb-2"
placeholder="Город"
>

<button
class="btn btn-success"
onclick="addStation()"
>
Добавить
</button>

</div>

</div>

<hr>

<table class="table table-striped">

<thead>

<tr>
<th>ID</th>
<th>Название</th>
<th>Город</th>
</tr>

</thead>

<tbody id="stations-table">

</tbody>

</table>

</div>

</div>

</div>

<div
id="trains"
class="section"
>

<div class="card">

<div class="card-body">

<h3>
🚄 Поезда
</h3>

<div class="row">

<div class="col-md-6">

<input
id="train-number"
class="form-control mb-2"
placeholder="Номер поезда"
>

<input
id="train-from"
class="form-control mb-2"
placeholder="Откуда"
>

<input
id="train-to"
class="form-control mb-2"
placeholder="Куда"
>

<input
id="train-price"
class="form-control mb-2"
placeholder="Цена"
type="number"
>

<button
class="btn btn-success"
onclick="addTrain()"
>
Добавить поезд
</button>

</div>

</div>

<hr>

<table class="table table-striped">

<thead>

<tr>
<th>ID</th>
<th>Номер</th>
<th>Откуда</th>
<th>Куда</th>
<th>Цена</th>
</tr>

</thead>

<tbody id="trains-table">

</tbody>

</table>

</div>

</div>

</div>
<div
id="passengers"
class="section"
>

<div class="card">

<div class="card-body">

<h3>
👤 Пассажиры
</h3>

<input
id="passenger-name"
class="form-control mb-2"
placeholder="ФИО"
>

<input
id="passenger-passport"
class="form-control mb-2"
placeholder="Паспорт"
>

<button
class="btn btn-success"
onclick="addPassenger()"
>
Добавить пассажира
</button>

<hr>

<table class="table table-striped">

<thead>
<tr>
<th>ID</th>
<th>ФИО</th>
<th>Паспорт</th>
</tr>
</thead>

<tbody id="passengers-table">

</tbody>

</table>

</div>

</div>

</div>


<div
id="schedules"
class="section"
>

<div class="card">

<div class="card-body">

<h3>
📅 Расписание
</h3>

<input
id="schedule-train"
class="form-control mb-2"
placeholder="ID поезда"
>

<input
id="schedule-date"
class="form-control mb-2"
placeholder="Дата"
>

<input
id="schedule-departure"
class="form-control mb-2"
placeholder="Время отправления"
>

<input
id="schedule-arrival"
class="form-control mb-2"
placeholder="Время прибытия"
>

<button
class="btn btn-success"
onclick="addSchedule()"
>
Добавить расписание
</button>

<hr>

<table class="table table-striped">

<thead>
<tr>
<th>ID</th>
<th>Поезд</th>
<th>Дата</th>
<th>Отправление</th>
<th>Прибытие</th>
</tr>
</thead>

<tbody id="schedules-table">

</tbody>

</table>

</div>

</div>

</div>


<div
id="tickets"
class="section"
>

<div class="card">

<div class="card-body">

<h3>
🎫 Билеты
</h3>

<input
id="ticket-passenger"
class="form-control mb-2"
placeholder="ID пассажира"
>

<input
id="ticket-train"
class="form-control mb-2"
placeholder="ID поезда"
>

<input
id="ticket-seat"
class="form-control mb-2"
placeholder="Место"
>

<button
class="btn btn-success"
onclick="buyTicket()"
>
Купить билет
</button>

<hr>

<table class="table table-striped">

<thead>
<tr>
<th>ID</th>
<th>Пассажир</th>
<th>Поезд</th>
<th>Место</th>
</tr>
</thead>

<tbody id="tickets-table">

</tbody>

</table>

</div>

</div>

</div>

</div>

</div>

</div>

<script>

function showSection(id){

document
.querySelectorAll(".section")
.forEach(
section =>
section.classList.remove("active")
);

document
.getElementById(id)
.classList.add("active");

}

async function loadStats(){

const stations =
await fetch("/api/stations")
.then(r=>r.json());

const trains =
await fetch("/api/trains")
.then(r=>r.json());

const tickets =
await fetch("/api/tickets")
.then(r=>r.json());

document
.getElementById("stations-count")
.innerText =
stations.length;

document
.getElementById("trains-count")
.innerText =
trains.length;

document
.getElementById("tickets-count")
.innerText =
tickets.length;

}

async function loadStations(){

const data =
await fetch("/api/stations")
.then(r=>r.json());

let html = "";

data.forEach(item=>{

html += `
<tr>
<td>${item.id}</td>
<td>${item.name}</td>
<td>${item.city}</td>
</tr>
`;

});

document
.getElementById("stations-table")
.innerHTML = html;

}

async function loadTrains(){

const data =
await fetch("/api/trains")
.then(r=>r.json());

let html = "";

data.forEach(item=>{

html += `
<tr>
<td>${item.id}</td>
<td>${item.number}</td>
<td>${item.departure_station}</td>
<td>${item.arrival_station}</td>
<td>${item.price}</td>
</tr>
`;

});

document
.getElementById("trains-table")
.innerHTML = html;

}

async function loadPassengers(){

const data =
await fetch("/api/passengers")
.then(r=>r.json());

let html = "";

data.forEach(item=>{

html += `
<tr>
<td>${item.id}</td>
<td>${item.full_name}</td>
<td>${item.passport}</td>
</tr>
`;

});

document
.getElementById("passengers-table")
.innerHTML = html;

}

async function loadSchedules(){

const data =
await fetch("/api/schedules")
.then(r=>r.json());

let html = "";

data.forEach(item=>{

html += `
<tr>
<td>${item.id}</td>
<td>${item.train_id}</td>
<td>${item.trip_date}</td>
<td>${item.departure_time}</td>
<td>${item.arrival_time}</td>
</tr>
`;

});

document
.getElementById("schedules-table")
.innerHTML = html;

}

async function loadTickets(){

const data =
await fetch("/api/tickets")
.then(r=>r.json());

let html = "";

data.forEach(item=>{

html += `
<tr>
<td>${item.id}</td>
<td>${item.passenger_id}</td>
<td>${item.train_id}</td>
<td>${item.seat_number}</td>
</tr>
`;

});

document
.getElementById("tickets-table")
.innerHTML = html;

}
function validateFields(fields){
    return fields.every(value => value.trim() !== "");
}

async function addStation(){

const name =
document.getElementById(
"station-name"
).value.trim();

const city =
document.getElementById(
"station-city"
).value.trim();

if(!name || !city){
alert("Заполните все поля!");
return;
}

await fetch(
`/api/stations?name=${encodeURIComponent(name)}&city=${encodeURIComponent(city)}`,
{
method:"POST"
}
);

loadStations();
loadStats();

}

async function addTrain(){

const number =
document.getElementById(
"train-number"
).value.trim();

const from =
document.getElementById(
"train-from"
).value.trim();

const to =
document.getElementById(
"train-to"
).value.trim();

const price =
document.getElementById(
"train-price"
).value;

if(!number || !from || !to || !price){
alert("Заполните все поля!");
return;
}

await fetch(
`/api/trains?number=${encodeURIComponent(number)}&departure_station=${encodeURIComponent(from)}&arrival_station=${encodeURIComponent(to)}&price=${price}`,
{
method:"POST"
}
);

loadTrains();
loadStats();

}

async function addPassenger(){

const name =
document.getElementById(
"passenger-name"
).value.trim();

const passport =
document.getElementById(
"passenger-passport"
).value.trim();

if(!name || !passport){
alert("Заполните все поля!");
return;
}

await fetch(
`/api/passengers?full_name=${encodeURIComponent(name)}&passport=${encodeURIComponent(passport)}`,
{
method:"POST"
}
);

loadPassengers();

}

async function addSchedule(){

const trainId =
document.getElementById(
"schedule-train"
).value.trim();

const date =
document.getElementById(
"schedule-date"
).value.trim();

const departure =
document.getElementById(
"schedule-departure"
).value.trim();

const arrival =
document.getElementById(
"schedule-arrival"
).value.trim();

if(!trainId || !date || !departure || !arrival){
alert("Заполните все поля!");
return;
}

await fetch(
`/api/schedules?train_id=${trainId}&departure_time=${departure}&arrival_time=${arrival}&trip_date=${date}`,
{
method:"POST"
}
);

loadSchedules();

}

async function buyTicket(){

const passenger =
document.getElementById(
"ticket-passenger"
).value.trim();

const train =
document.getElementById(
"ticket-train"
).value.trim();

const seat =
document.getElementById(
"ticket-seat"
).value.trim();

if(!passenger || !train || !seat){
alert("Заполните все поля!");
return;
}

const response = await fetch(
`/api/tickets?passenger_id=${encodeURIComponent(passenger)}&train_id=${encodeURIComponent(train)}&seat_number=${encodeURIComponent(seat)}`,
{
method:"POST"
}
);

const result = await response.json();

if(result.message === "Место занято"){
alert("Место занято!");
return;
}

loadTickets();
loadStats();

}


loadStats();
loadStations();
loadTrains();
loadPassengers();
loadSchedules();
loadTickets();

</script>

</body>
</html>
"""
@app.get(
    "/",
    response_class=HTMLResponse,
)
def home():
    return HTML_PAGE 