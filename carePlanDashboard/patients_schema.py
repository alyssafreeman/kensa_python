"""-- General patient info
create table patient (
    _id             integer primary key autoincrement not null,
    patient_id      integer not null unique,
    first_name      text,
    last_name       text,
    gender          text,
    age             text,
    relationship    text,
    first_appt_date date
);

-- General visit info
create table visit ( 
    _id                     integer primary key autoincrement not null,
    patient_id              text not null references patient(patient_id),
    visit_date              date not null unique,
    recent_visit            integer not null,
    next_appt_date          date,
    pcp_name                text,
    case_status             text,
    health_risk_assessment  integer,
    biometrics              integer,
    coach_initials          text,
    comments                text
);

-- Diagnosis/Risk Factor - Clinical Risk Category
create table diagnosis (
    _id                 integer primary key autoincrement not null,
    patient_id          text not null references patient(patient_id),
    visit_date          date not null references visit(visit_date),
    recent_visit        text not null references visit(recent_visit),
    case_status         text not null references visit(case_status),
    overweight          integer not null,      
    obese               integer not null,
    hypertension        integer not null,
    cad                 integer not null,
    chf                 integer not null,
    hyperlipidemia      integer not null,
    prediabetes         integer not null,
    diabetes            integer not null,
    asthma              integer not null,
    copd                integer not null,
    depression          integer not null,
    nicotine_use        integer not null,
    waist_progress      integer,
    weight_progress     integer,
    bmi_progress        integer,
    systolic_progress   integer,
    diastolic_progress  integer,
    tc_progress         integer,
    ldl_progress        integer,
    hdl_progress        integer,
    tgs_progress        integer,
    fbg_progress        integer,
    hb_progress         integer,
    retinal_progress    integer,
    renal_progress      integer,
    foot_progress       integer,
    meds_progress       integer,
    diet_progress       integer,
    exercise_progress   integer,
    nicotine_progress   integer,
    unique(patient_id, visit_date) on conflict replace
);

-- Results based Incentive pProgram
create table incentive_program (
    _id                     integer primary key autoincrement not null,
    patient_id              text not null references patient(patient_id),
    visit_date              date not null references visit(visit_date),
    recent_visit            text not null references visit(recent_visit),
    first_name              text not null references patient(first_name),
    last_name               text not null references patient(last_name),
    blood_pressure_control  integer,
    ldl_cholesterol         integer,
    tobacco_use             integer,
    bmi                     integer,
    total                   integer
);"""
