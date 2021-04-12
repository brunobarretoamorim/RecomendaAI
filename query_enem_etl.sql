create table enem.provas_enem_2019_etl
as
select NU_INSCRICAO,
       NU_ANO, 
       SG_UF_RESIDENCIA,
       NU_IDADE,
       TP_ST_CONCLUSAO,
       TP_ANO_CONCLUIU,
       TP_ESCOLA,
       TP_ENSINO,     
       CO_PROVA_CN,
       CO_PROVA_CH,
       CO_PROVA_LC,
       CO_PROVA_MT,
       NU_NOTA_CN,
       NU_NOTA_CH,
       NU_NOTA_LC,
       NU_NOTA_MT,
       TP_LINGUA,	
       NU_NOTA_COMP1,
       NU_NOTA_COMP2,
       NU_NOTA_COMP3,
       NU_NOTA_COMP4,
       NU_NOTA_COMP5,
       NU_NOTA_REDACAO
       from enem.ano_2019 a 
       where TP_PRESENCA_CH = '1'
       and TP_PRESENCA_CN = '1'
       and TP_PRESENCA_LC = '1'
       and TP_PRESENCA_MT = '1'
       and TX_RESPOSTAS_CH <> ''
       and TX_RESPOSTAS_CN <> ''
       and TX_RESPOSTAS_LC <> ''
       and TX_RESPOSTAS_MT  <> ''