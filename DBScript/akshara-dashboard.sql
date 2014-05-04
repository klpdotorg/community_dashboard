-- Table: tb_fc

-- DROP TABLE tb_fc;

CREATE TABLE tb_fc
(
  id integer NOT NULL,
  name character(120) NOT NULL,
  CONSTRAINT pk_tb_fc PRIMARY KEY (id)
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
  "ID" integer NOT NULL,
  district_name character(50),
  CONSTRAINT pk_tb_district PRIMARY KEY ("ID")
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
  id integer NOT NULL,
  block_name character(120),
  district_id integer,
  CONSTRAINT pk_tb_block PRIMARY KEY (id),
  CONSTRAINT fk_district_id FOREIGN KEY (district_id)
      REFERENCES tb_district ("ID") MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
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
  id integer NOT NULL,
  cluster_name character(150),
  block_id integer,
  CONSTRAINT pk_tb_cluster PRIMARY KEY (id),
  CONSTRAINT fk_block_id FOREIGN KEY (block_id)
      REFERENCES tb_block (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
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
  id integer NOT NULL,
  school_name character(500),
  cluster_id integer,
  klp_id numeric(15,0),
  CONSTRAINT pk_tb_school PRIMARY KEY (id),
  CONSTRAINT fk_cluster_id FOREIGN KEY (cluster_id)
      REFERENCES tb_cluster (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
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
  id numeric(15,0) NOT NULL,
  month smallint,
  day smallint,
  year integer,
  fc_id integer,
  other_visit character varying(500),
  school_id integer,
  CONSTRAINT pk_tb_visit_details PRIMARY KEY (id),
  CONSTRAINT fk_fc_id FOREIGN KEY (fc_id)
      REFERENCES tb_fc (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_school_id FOREIGN KEY (school_id)
      REFERENCES tb_school (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
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

-- Table: tb_performance_feedback

-- DROP TABLE tb_performance_feedback;

CREATE TABLE tb_performance_feedback
(
  id numeric(15,0) NOT NULL,
  visit_id numeric(15,0),
  parents_teachers smallint,
  parents_parents smallint,
  parents_community smallint,
  sdmc_teachers smallint,
  sdmc_parents smallint,
  sdmc_community smallint,
  community_teachers smallint,
  community_parents smallint,
  community_community smallint,
  teachers_teachers smallint,
  teachers_parents smallint,
  teachers_community smallint,
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
  id numeric(15,0) NOT NULL,
  visit_id numeric(15,0),
  teacher_tlmsufficient smallint,
  teacher_work_overload smallint,
  teacher_need_training smallint,
  teacher_relationship_hm smallint,
  parents_good_school smallint,
  parents_teachers_regular smallint,
  parents_attention_to_children smallint,
  parents_food_served smallint,
  community_qtm_to_teach smallint,
  community_str smallint,
  community_govt_involved smallint,
  community_good_infra smallint,
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
