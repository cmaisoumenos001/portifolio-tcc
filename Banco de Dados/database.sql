create database tcc
use tcc

create table usuario (
id_user int primary key identity(1,1),
nome varchar(75),
email varchar(50),
fone varchar(20),
senha varchar(20),
curso char(2),
serie int,
)


create table ligas(
id_ligas int primary key identity(1,1),
nome_da_liga varchar(30),
valor decimal(5,2),
criador_id int,
data_criacao datetime,
descricao varchar(500),
tipo varchar(15), --equipe, trio, dupla, solo
status varchar(20),

foreign key (criador_id) references usuario(id_user)
)

create table inscricoes(
id_inscricao int primary key identity(1,1),
id_user int,
id_liga int,
data_inscricao datetime,

foreign key (id_user) references usuario(id_user),
foreign key (id_liga) references ligas(id_ligas)
)

drop table inscricoes
drop table ligas
drop table usuario
select * from ligas