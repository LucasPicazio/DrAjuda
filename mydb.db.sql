BEGIN TRANSACTION;
DROP TABLE IF EXISTS `usuario`;
CREATE TABLE IF NOT EXISTS `usuario` (
	`id`	INTEGER NOT NULL,
	`email`	VARCHAR ( 50 ) NOT NULL UNIQUE,
	`tipo_id`	VARCHAR ( 50 ) NOT NULL,
	`senha`	VARCHAR ( 15 ) NOT NULL,
	`nome`	VARCHAR ( 60 ) NOT NULL,
	`dt_nascimento`	DATE NOT NULL,
	PRIMARY KEY(`id`)
);
INSERT INTO `usuario` (id,email,tipo_id,senha,nome,dt_nascimento) VALUES (1,'usuario1@dkasd.com','0','123','Lucas Araujo','1998-02-05'),
 (2,'usuario2@dkasd.com','0','2222','Carlos Alberto','1985-11-05'),
 (3,'usuario3@dkasd.com','1','1212','Pedro Alvares','1472-11-05');
DROP TABLE IF EXISTS `medico`;
CREATE TABLE IF NOT EXISTS `medico` (
	`id`	INTEGER NOT NULL,
	`meduser_id`	INTEGER,
	`formacao`	VARCHAR ( 100 ),
	`anos_experiencia`	INTEGER,
	`bio`	VARCHAR ( 255 ),
	PRIMARY KEY(`id`),
	FOREIGN KEY(`meduser_id`) REFERENCES `usuario`(`id`)
);
INSERT INTO `medico` (id,meduser_id,formacao,anos_experiencia,bio) VALUES (1,1,'Universidade de São Paulo',11,'Eu so medico atualizado'),
 (2,2,'Universidade de Santos',11,'Eu so medico'),
 (3,3,'Universidade de Campinas',4,'Sou medico para caramba');
DROP TABLE IF EXISTS `lugar`;
CREATE TABLE IF NOT EXISTS `lugar` (
	`id_lugar`	INTEGER NOT NULL,
	`id`	INTEGER NOT NULL,
	`estado`	VARCHAR ( 2 ) NOT NULL,
	`cidade`	VARCHAR ( 100 ) NOT NULL,
	`logradouro`	VARCHAR ( 250 ),
	`bairro`	VARCHAR ( 250 ),
	`complemento`	VARCHAR ( 250 ),
	`CEP`	VARCHAR ( 8 ),
	FOREIGN KEY(`id`) REFERENCES `usuario`(`id`),
	PRIMARY KEY(`id_lugar`)
);
INSERT INTO `lugar` (id_lugar,id,estado,cidade,logradouro,bairro,complemento,CEP) VALUES (1,1,'SP','São Paulo','Rua 1821','Ipiranga','','04985060'),
 (2,2,'SP','São Paulo','Rua do Grito','Ipiranga','','04985060');
DROP TABLE IF EXISTS `horario`;
CREATE TABLE IF NOT EXISTS `horario` (
	`id`	INTEGER NOT NULL,
	`id_medico`	INTEGER NOT NULL,
	`inicio`	DATETIME NOT NULL,
	`fim`	DATETIME NOT NULL,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`id_medico`) REFERENCES `medico`(`id`)
);
INSERT INTO `horario` (id,id_medico,inicio,fim) VALUES (1,1,'2018-12-31 00:00:00.000000','2018-12-31 00:30:00.000000'),
 (2,1,'2012-12-31 00:00:00.000000','2020-12-31 00:30:00.000000');
DROP TABLE IF EXISTS `especialidade`;
CREATE TABLE IF NOT EXISTS `especialidade` (
	`id`	INTEGER NOT NULL,
	`especialidade`	VARCHAR ( 50 ) NOT NULL,
	PRIMARY KEY(`id`)
);
INSERT INTO `especialidade` (id,especialidade) VALUES (1,'Pediartia'),
 (2,'Oftamologia');
DROP TABLE IF EXISTS `espec_med`;
CREATE TABLE IF NOT EXISTS `espec_med` (
	`id_especialiade_medico`	INTEGER NOT NULL,
	`id_especialidade`	INTEGER,
	`id`	INTEGER,
	FOREIGN KEY(`id_especialidade`) REFERENCES `especialidade`(`id`),
	PRIMARY KEY(`id_especialiade_medico`),
	FOREIGN KEY(`id`) REFERENCES `usuario`(`id`)
);
INSERT INTO `espec_med` (id_especialiade_medico,id_especialidade,id) VALUES (1,1,1),
 (2,1,2);
DROP TABLE IF EXISTS `documento`;
CREATE TABLE IF NOT EXISTS `documento` (
	`id_documento`	INTEGER NOT NULL,
	`documento`	VARCHAR ( 50 ) NOT NULL,
	`tipo_doc`	VARCHAR ( 20 ),
	`id`	INTEGER,
	PRIMARY KEY(`id_documento`),
	FOREIGN KEY(`id`) REFERENCES `usuario`(`id`)
);
INSERT INTO `documento` (id_documento,documento,tipo_doc,id) VALUES (1,'58799657836','CPF',1),
 (2,'398518361','RG',2);
DROP TABLE IF EXISTS `agendamento`;
CREATE TABLE IF NOT EXISTS `agendamento` (
	`id_agendamento`	INTEGER NOT NULL,
	`id_medico`	INTEGER NOT NULL,
	`id_paciente`	INTEGER NOT NULL,
	`cadastro`	VARCHAR ( 20 ) NOT NULL,
	`inicio`	DATETIME NOT NULL,
	`fim`	DATETIME NOT NULL,
	`in_status`	INTEGER NOT NULL,
	`voucher`	VARCHAR ( 6 ),
	`valor`	FLOAT,
	FOREIGN KEY(`id_medico`) REFERENCES `usuario`(`id`),
	PRIMARY KEY(`id_agendamento`),
	FOREIGN KEY(`id_paciente`) REFERENCES `usuario`(`id`)
);
INSERT INTO `agendamento` (id_agendamento,id_medico,id_paciente,cadastro,inicio,fim,in_status,voucher,valor) VALUES (1,1,2,'hausddus','2018-02-28 00:00:00.000000','2018-02-27 00:00:00.000000',0,'dddd',100.0),
 (2,1,1,'abc','2018-02-27 00:00:00.000000','2018-02-27 00:00:00.000000',0,'abc',0.0),
 (3,1,2,'abcd','2018-02-28 00:00:00.000000','2018-02-27 00:00:00.000000',0,'dddd',100.0);
COMMIT;
