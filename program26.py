#necesitamos leer los datos de entrada son tres datos, separados por un espacio
"""
STDIN       Function
-----       --------
9 6 2015    day = 9, month = 6, year = 2015 (date returned)
6 6 2015    day = 6, month = 6, year = 2015 (date due)
"""
datos = list(map(int, input().split()))
dia_retorno = datos[0]
mes_retorno = datos[1]
ano_retorno = datos[2]
datos = list(map(int, input().split()))
dia_vencimiento = datos[0]
mes_vencimiento = datos[1]
ano_vencimiento = datos[2]
#print (dia_retorno, mes_retorno, ano_retorno, end=' ' + '\n')
#print (dia_vencimiento, mes_vencimiento, ano_vencimiento, end=' ')
#calculamos la multa, para esto necesitamos calcular la diferencia entre las fechas
#Comparación jerárquica: anos -> meses -> dias
if ano_retorno < ano_vencimiento:
	# El libro se devuelve en un ano anterior: sin multa
	print(0)
elif ano_retorno > ano_vencimiento:
	# El libro se devuelve en un ano posterior: multa máxima
	print(10000)
else:
	# Los anos son iguales, comparamos meses
	if mes_retorno < mes_vencimiento:
		# El libro se devuelve en un mes anterior: sin multa
		print(0)
	elif mes_retorno > mes_vencimiento:
		# El libro se devuelve en un mes posterior: multa por meses
		diferencia_meses = mes_retorno - mes_vencimiento
		print(500 * diferencia_meses)
	else:
		# anos y meses son iguales, comparamos dias
		if dia_retorno <= dia_vencimiento:
			# El libro se devuelve en el mismo dia o antes: sin multa
			print(0)
		else:
			# El libro se devuelve despues del dia de vencimiento: multa por dias
			diferecia_dias = dia_retorno - dia_vencimiento
			print(15 * diferecia_dias)
