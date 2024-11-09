def kalkulator():
    	def tambah (self):
		print ('1. Penjumlahan')
		a = input ('Masukkan nilai x = ')
		b = input ('Masukkan nilai y = ')
		c = a+b
		print ('x + y = ',c)
		print ('')
		tanya ()
	 
 
	def kurang () :
		print ('2. Pengurangan')
		a = input ('Masukkan nilai x = ')
		b = input ('Masukkan nilai y = ')
		c = a+b
		print ('x - y = ',c)
		print ('')
		tanya ()
	def kali () :
		print ('3. Perkalian')
		a = input ('Masukkan nilai x = ')
		b = input ('Masukkan nilai y = ')
		c = a+b
		print ('x * y = ',c)
		print ('')
		tanya ()
	def bagi () :
		print ('4. Pembagian')
		a = input ('Masukkan nilai x = ')
		b = input ('Masukkan nilai y = ')
		c = a+b
		print ('x / y = ',c)
		print ('')
		tanya ()

def tanya () :
	choose = input ('Apakah Anda ingin mengulang (Y/T)? ')
	if choose == 'Y' or choose == 'y':
	 	kalkulator()
	elif choose == 'T' or choose =='t':
		print ('Terima kasih')
	else :
		print ('Maaf,input yang Anda masukkan salah')
		print ('Silahkan masukkan Y atau T')
		tanya()


print ('Program Kalkulator Sederhana')
print ('1. Penjumlahan')
print ('2. Pengurangan')
print ('3. Perkalian')
print ('4. Pembagian')
print ('silahkan pilih 1-4')
print ('')
 
a=kalkulator()
pil = int(input ('Masukkan pilihan : '))
if pil == 1:
 	tambah()
elif pil == 2:
 	kurang ()
elif pil == 3:
 	kali ()
elif pil == 4:
 	bagi ()
else :
	 print ('Maaf, input yang Anda masukkan salah')
	 print ('coba ulangi lagi')
	 tanya ()