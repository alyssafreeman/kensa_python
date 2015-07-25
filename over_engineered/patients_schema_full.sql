-- General patient info
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
    _id             integer primary key autoincrement not null,
    patient_id      text not null references patient(patient_id),
    visit_date      date not null references visit(visit_date),
    case_status     text not null references visit(case_status),
    overweight      integer not null,      
    obese           integer not null,
    hypertension    integer not null,
    cad             integer not null,
    chf             integer not null,
    hyperlipidemia  integer not null,
    prediabetes     integer not null,
    diabetes        integer not null,
    asthma          integer not null,
    copd            integer not null,
    depression      integer not null,
    nicotine_use    integer not null,
    unique(patient_id, visit_date) on conflict replace
);

-- Weight Management
create table weight_management (
    _id                         integer primary key autoincrement not null,
    patient_id                  text not null references patient(patient_id),
    visit_date                  date not null references visit(visit_date),
    height_measured             integer, 
    height_baseline             integer,
    waist_measured              integer,
    waist_baseline              integer,
    waist_progress              integer,
    waist_goal                  integer,
    waist_date_goal_achieved    date,
    waist_progress_notes        text,
    weight_measured             integer,
    weight_baseline             integer,
    weight_progress             integer,
    weight_goal                 integer,
    weight_date_goal_achieved   date,
    weight_progress_notes       text,
    bmi_measured                integer,
    bmi_baseline                integer,
    bmi_progress                integer,
    bmi_date_goal_achieved      date,
    bmi_progress_notes          text
);

-- Blood Pressure Control
create table blood_pressure_control (
    _id                             integer primary key autoincrement not null,
    patient_id                      text not null references patient(patient_id),
    visit_date                      date not null references visit(visit_date),
    systolic_measured               integer, 
    systolic_baseline               integer,
    systolic_progress               integer,
    systolic_goal                   integer,
    systolic_date_goal_achieved     date,
    systolic_progress_notes         text,
    diastolic_measured              integer, 
    diastolic_baseline              integer,
    diastolic_progress              integer,
    diastolic_goal                  integer,
    diastolic_date_goal_achieved    date,
    diastolic_progress_notes        text
);

-- Lipid Management
create table lipid_management (
    _id                       integer primary key autoincrement not null,
    patient_id                text not null references patient(patient_id),
    visit_date                date not null references visit(visit_date),
    tc_measured               integer, 
    tc_baseline               integer,
    tc_progress               integer,
    tc_date_goal_achieved     date,
    tc_progress_notes         text,
    ldl_measured              integer, 
    ldl_baseline              integer,
    ldl_progress              integer,
    ldl_goal                  integer,
    ldl_date_goal_achieved    date,
    ldl_progress_notes        text,
    hdl_measured              integer, 
    hdl_baseline              integer,
    hdl_progress              integer,
    hdl_goal                  integer,
    hdl_date_goal_achieved    date,
    hdl_progress_notes        text,
    tgs_measured              integer, 
    tgs_baseline              integer,
    tgs_progress              integer,
    tgs_date_goal_achieved    date,
    tgs_progress_notes        text
);

-- Diabetes
create table diabetes (
    _id                         integer primary key autoincrement not null,
    patient_id                  text not null references patient(patient_id),
    visit_date                  date not null references visit(visit_date),
    fbg_measured                integer, 
    fbg_baseline                integer,
    fbg_progress                integer,
    fbg_date_goal_achieved      date,
    fbg_progress_notes          text,
    hb_measured                 integer, 
    hb_baseline                 integer,
    hb_progress                 integer,
    hb_goal                     integer,
    hb_date_goal_achieved       date,
    hb_progress_notes           text,
    retinal_measured            text, 
    retinal_baseline            text,
    retinal_progress            integer,
    retinal_goal                text,
    retinal_date_goal_achieved  date,
    retinal_progress_notes      text,
    renal_measured              text, 
    renal_baseline              text,
    renal_progress              integer,
    renal_goal                  text,
    renal_date_goal_achieved    date,
    renal_progress_notes        text,
    foot_measured               text, 
    foot_baseline               text,
    foot_progress               integer,
    foot_goal                   text,
    foot_date_goal_achieved     date,
    foot_progress_notes         text
);


-- Compliance
create table compliance (
    _id                         integer primary key autoincrement not null,
    patient_id                  text not null references patient(patient_id),
    visit_date                  date not null references visit(visit_date),
    meds_measured               text,
    meds_baseline               text,
    meds_progress               integer, 
    meds_date_goal_achieved     date,
    meds_progress_notes         text,
    diet_measured               text,
    diet_baseline               text,
    diet_progress               integer, 
    diet_date_goal_achieved     date,
    diet_progress_notes         text,
    exercise_measured           text,
    exercise_baseline           text,
    exercise_progress           integer, 
    exercise_date_goal_achieved date,
    exercise_progress_notes     text,
    nicotine_measured           text,
    nicotine_baseline           text,
    nicotine_progress           integer, 
    nicotine_goal               text,
    nicotine_date_goal_achieved date,
    nicotine_progress_notes     text
);
