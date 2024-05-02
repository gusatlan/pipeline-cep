import pandas as pd
from sqlalchemy import create_engine


def get_connection(url='postgresql://airflow:airflow@postgres:5432/airflow'):
	db = create_engine(url)
	return db


def load_dataframe(filename, sep='@', columns_names: list=[], encoding:str='ISO-8859-1'):
	df = pd.read_csv(filename, delimiter=sep, header=None, encoding=encoding)
	df.columns = columns_names
	print(f'{filename} loaded into dataframe')
	return df


def write_to_db(df, table_name, conn):
	df.to_sql(table_name, conn, if_exists= 'replace', index=False)
	print(f'{table_name} persisted')


def ingest(filename: str, columns: list, tablename: str, conn=get_connection()):
	df = load_dataframe(filename=filename, columns_names=columns)
	write_to_db(df=df, table_name=tablename, conn=conn)


def ingest_all(root_path:str=''):
	maps = map_csv()
	for entry in maps:
		filename=f"{root_path}/{entry['filename']}"
		tablename= entry['tablename']
		columns = entry['columns']
		print(f'Filename: {filename}, Table: {tablename}, Columns: {columns}')

		ingest(filename=filename, columns=columns, tablename=tablename, conn=get_connection())
	print('Done')


def ingest_logradouro(root_path:str='', index_stage:int=0):
	maps = map_csv_logradouro()

	if index_stage == 0:
		maps = maps[:-3]
	elif index_stage == 1:
		maps = maps[-3:-2]
	elif index_stage == 2:
		maps = maps[-2:-1]
	elif index_stage == 3:
		maps = [maps[-1]]

	print(maps)

	for entry in maps:
		filename=f"{root_path}/{entry['filename']}"
		tablename= entry['tablename']
		columns = entry['columns']
		print(f'Filename: {filename}, Table: {tablename}, Columns: {columns}')

		ingest(filename=filename, columns=columns, tablename=tablename, conn=get_connection())
	print('Done')



def map_csv():
	maps = [
		{'filename': 'log_faixa_uf.txt', 'tablename': 'log_faixa_uf', 'columns': ['ufe_sg', 'ufe_cep_ini', 'ufe_cep_fim']},
		{'filename': 'log_localidade.txt', 'tablename': 'log_localidade','columns': ['loc_nu', 'ufe_sg', 'loc_no', 'cep', 'loc_in_sit', 'loc_in_tipo_loc', 'loc_nu_sub', 'loc_no_abrev', 'mun_nu']},
		{'filename': 'log_var_loc.txt', 'tablename': 'log_var_loc','columns': ['loc_nu', 'val_nu', 'val_tx']},
		{'filename': 'log_faixa_localidade.txt', 'tablename': 'log_faixa_localidade','columns': ['loc_nu', 'loc_cep_ini', 'loc_cep_fim', 'loc_tipo_faixa']},
		{'filename': 'log_bairro.txt', 'tablename': 'log_bairro','columns': ['bai_nu', 'ufe_sf', 'loc_nu', 'bai_no', 'bai_no_abrev']},
		{'filename': 'log_var_bai.txt', 'tablename': 'log_var_bai','columns': ['bai_nu', 'vdb_nu', 'vdb_tx']},
		{'filename': 'log_faixa_bairro.txt', 'tablename': 'log_faixa_bairro','columns': ['bai_nu', 'fcb_cep_ini', 'fcb_cep_fim']},
		{'filename': 'log_cpc.txt', 'tablename': 'log_cpc','columns': ['cpc_nu', 'ufe_sg', 'loc_nu', 'cpc_no', 'cpc_endereco', 'cep']},
		{'filename': 'log_faixa_cpc.txt', 'tablename': 'log_faixa_cpc','columns': ['cpc_nu', 'cpc_inicial', 'cpc_final']},
		{'filename': 'log_var_log.txt', 'tablename': 'log_var_log','columns': ['log_nu', 'vlo_nu', 'tlo_tx', 'vlo_tx']},
		{'filename': 'log_num_sec.txt', 'tablename': 'log_num_sec','columns': ['log_nu', 'sec_nu_ini', 'sec_nu_fim', 'sec_in_lado']},
		{'filename': 'log_grande_usuario.txt', 'tablename': 'log_grande_usuario','columns': ['gru_nu', 'ufe_sg', 'loc_nu', 'bai_nu', 'log_nu', 'gru_no', 'gru_endereco', 'cep', 'gru_no_abrev']},
		{'filename': 'log_unid_oper.txt', 'tablename': 'log_unid_oper','columns': ['uop_nu', 'ufe_sg', 'loc_nu', 'bai_nu', 'log_nu', 'uop_no', 'uop_endereco', 'cep', 'uop_in_cp', 'uop_no_abrev']},
		{'filename': 'log_faixa_uop.txt', 'tablename': 'log_faixa_uop','columns': ['uop_nu', 'fnc_inicial', 'fnc_final']},
		{'filename': 'ect_pais.txt', 'tablename': 'ect_pais','columns': ['pai_sg', 'pai_sg_alternativa', 'pai_no_portugues', 'pai_no_ingles', 'pai_no_frances', 'pai_abreviatura']}
    ]
	return maps


def map_csv_logradouro():
	columns = ['log_nu', 'ufe_sg', 'loc_nu', 'bai_nu_ini', 'bai_nu_fim', 'log_no', 'log_complemento', 'cep', 'tlo_tx', 'log_sta_tlo', 'log_no_abrev']
	filename = 'log_logradouro_xx.txt'
	tablename = 'log_logradouro'
	ufs = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'TO', 'MG', 'RJ', 'SP']
	ufs_lower = [x.lower() for x in ufs]
	maps = []
	for uf in ufs_lower:
		entry = {'filename': f"{filename.replace('xx', uf)}", 'tablename': tablename, 'columns': columns}
		maps.append(entry)
	return maps
	
