def es_primo(numero):
	if numero <= 1:
		return False
	if numero == 2:
		return True
	if numero % 2 == 0:
		return False

	divisor = 3
	while divisor * divisor <= numero:
		if numero % divisor == 0:
			return False
		divisor += 2

	return True


if __name__ == "__main__":
	T=int(input())
	data = []
	for i in range(T):
		data.append(int(input()))
	for i in range(T):
		if es_primo(data[i]):
			print("Prime")
		else:
			print("Not prime")