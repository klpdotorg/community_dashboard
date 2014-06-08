-- Table: myapp_document
-- DROP TABLE myapp_document;

CREATE TABLE myapp_document
(
  id serial NOT NULL,
  docfile character varying(100) NOT NULL,
  CONSTRAINT myapp_document_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE myapp_document
  OWNER TO postgres;

-- Table: tb_fc
-- DROP TABLE tb_fc;

CREATE TABLE tb_fc
(
  id serial NOT NULL,
  name character(120) NOT NULL,
  CONSTRAINT pk_tb_fc PRIMARY KEY (id),
  CONSTRAINT "UQ_TB_FC_FC_NAME" UNIQUE (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tb_fc
  OWNER TO postgres;

-- Table: tb_district
-- DROP TABLE tb_district;

CREATE TABLE tb_district
(
  id serial NOT NULL,
  district_name character(50),
  CONSTRAINT pk_tb_district PRIMARY KEY (id),
  CONSTRAINT "UQ_TB_DISTRICT_DIST_NAME" UNIQUE (district_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tb_district
  OWNER TO postgres;
  
-- Table: tb_block
-- DROP TABLE tb_block;

CREATE TABLE tb_block
(
  id serial NOT NULL,
  block_name character(120),
  district_id serial NOT NULL,
  CONSTRAINT pk_tb_block PRIMARY KEY (id),
  CONSTRAINT fk_district_id FOREIGN KEY (district_id)
      REFERENCES tb_district (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "UQ_TB_BLOCK_BLOCK_DIST" UNIQUE (block_name, district_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tb_block
  OWNER TO postgres;

-- Table: tb_cluster
-- DROP TABLE tb_cluster;

CREATE TABLE tb_cluster
(
  id serial NOT NULL,
  cluster_name character(150),
  block_id serial NOT NULL,
  CONSTRAINT pk_tb_cluster PRIMARY KEY (id),
  CONSTRAINT fk_block_id FOREIGN KEY (block_id)
      REFERENCES tb_block (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "UQ_TB_CLUSTER_CLUSTER_BLOCK" UNIQUE (cluster_name, block_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tb_cluster
  OWNER TO postgres;


-- Table: tb_school
-- DROP TABLE tb_school;

CREATE TABLE tb_school
(
  id serial NOT NULL,
  school_name character(500),
  cluster_id serial NOT NULL,
  klp_id numeric(15,0),
  CONSTRAINT pk_tb_school PRIMARY KEY (id),
  CONSTRAINT fk_cluster_id FOREIGN KEY (cluster_id)
      REFERENCES tb_cluster (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT "UQ_TB_SCHOOL_SCHOOL_CLUSTER" UNIQUE (school_name, cluster_id, klp_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tb_school
  OWNER TO postgres;


-- Table: tb_visit_details

-- DROP TABLE tb_visit_details;

CREATE TABLE tb_visit_details
(
  id serial NOT NULL,
  month smallint,
  day smallint,
  year integer,
  fc_id serial NOT NULL,
  other_visit character varying(500),
  school_id serial NOT NULL,
  CONSTRAINT pk_tb_visit_details PRIMARY KEY (id),
  CONSTRAINT fk_fc_id FOREIGN KEY (fc_id)
      REFERENCES tb_fc (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_school_id FOREIGN KEY (school_id)
      REFERENCES tb_school (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT "UQ_VISIT_DETAILS" UNIQUE (day, month, year, other_visit, school_id, fc_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tb_visit_details
  OWNER TO postgres;

-- Index: fki_fc_id

-- DROP INDEX fki_fc_id;

CREATE INDEX fki_fc_id
  ON tb_visit_details
  USING btree
  (fc_id);

-- Index: fki_school_id

-- DROP INDEX fki_school_id;

CREATE INDEX fki_school_id
  ON tb_visit_details
  USING btree
  (school_id);


-- Index: fki_school_id
-- DROP INDEX fki_school_id;

CREATE INDEX fki_school_id
  ON tb_visit_details
  USING btree
  (school_id);


-- Table: tb_performance_feedback
-- DROP TABLE tb_performance_feedback;

CREATE TABLE tb_performance_feedback
(
  id serial NOT NULL,
  visit_id integer,
  parents_teachers smallint,
  parents_parents smallint,
  parents_community smallint,
  assumed_actual_parents smallint,
  sdmc_teachers smallint,
  sdmc_parents smallint,
  sdmc_community smallint,
  assumed_actual_sdmc smallint,
  community_teachers smallint,
  community_parents smallint,
  community_community smallint,
  assumed_actual_comm smallint,
  teachers_teachers smallint,
  teachers_parents smallint,
  teachers_community smallint,
  assumed_actual_teachers smallint,
  addl_comments_fs character varying(750),
  CONSTRAINT pk_tb_performance_feedback PRIMARY KEY (id),
  CONSTRAINT fk_visit_id FOREIGN KEY (visit_id)
      REFERENCES tb_visit_details (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tb_performance_feedback
  OWNER TO postgres;

-- Table: tb_requirements_feedback
-- DROP TABLE tb_requirements_feedback;

CREATE TABLE tb_requirements_feedback
(
  id serial NOT NULL,
  visit_id integer,
  teacher_tlmsufficient smallint,
  teacher_work_overload smallint,
  teacher_need_training smallint,
  teacher_relationship_hm smallint,
  teacher_requirement smallint,
  parents_good_school smallint,
  parents_teachers_regular smallint,
  parents_attention_to_children smallint,
  parents_food_served smallint,
  parent_requirement smallint,
  community_qtm_to_teach smallint,
  community_str smallint,
  community_govt_involved smallint,
  community_good_infra smallint,
  community_requirement smallint,
  teacher_addl_comments character varying(750),
  parents_addl_comments character varying(750),
  community_addl_comments character varying(750),
  CONSTRAINT pk_tb_requirements_feedback PRIMARY KEY (id),
  CONSTRAINT fk_tb_reqmts_visit_id FOREIGN KEY (visit_id)
      REFERENCES tb_visit_details (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tb_requirements_feedback
  OWNER TO postgres;

-- Table: tb_weight_determination

-- DROP TABLE tb_weight_determination;

CREATE TABLE tb_weight_determination
(
  id integer NOT NULL,
  question character varying(150),
  total_yes_teachers integer,
  total_yes_parents integer,
  total_yes_community integer,
  agreement_percent_teacher numeric(5,2),
  agreement_percent_parents numeric(5,2),
  agreement_percent_community numeric(5,2),
  normalized_agreement_percent_t numeric(5,2),
  normalized_agreement_percent_p numeric(5,2),
  normalized_agreement_percent_c numeric(5,2),
  final_weights integer,
  CONSTRAINT "PK_TB_weight_determination" PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tb_weight_determination
  OWNER TO postgres;
-- Populate the weight determination criteria questions
insert into  tb_weight_determination(id,question) values (1, 'Are the Parents involved in the progress of the school?');
insert into  tb_weight_determination(id,question) values (2, 'Are the SDMC Members involved io the progress of the school?');
insert into  tb_weight_determination(id,question) values (3, 'Are the community members involved in the progress of the school?');
insert into  tb_weight_determination(id,question) values (4, 'Are the teacher involved in the progress of the school? ');
